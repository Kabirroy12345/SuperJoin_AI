import streamlit as st
import requests
import pandas as pd
from typing import List, Dict, Any
import json

import sys
import os
import tempfile
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.pipeline import Pipeline

API_BASE_URL = "http://localhost:8000/api"

st.set_page_config(page_title="Fact Knowledge Layer", page_icon="🔍", layout="wide")

st.title("🔍 Fact Knowledge Layer")
st.markdown("Automated Fact Extraction, Evidence Grounding, and Cross-Document Reconciliation")

@st.cache_resource
def get_local_pipeline():
    db_path = str(PROJECT_ROOT / "knowledge.db")
    return Pipeline(db_path=db_path)

@st.cache_data(ttl=5)
def fetch_data(endpoint: str) -> Any:
    # 1. Try REST API
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=10.0)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass

    # 2. Seamless local pipeline fallback (standalone mode)
    try:
        p = get_local_pipeline()
        if endpoint == "/documents":
            docs = p.doc_store.get_all_documents()
            return [d.model_dump() for d in docs]
        elif endpoint.startswith("/facts"):
            facts = p.fact_store.get_facts()
            return [f.model_dump() for f in facts]
        elif endpoint.startswith("/relationships"):
            rels = p.rel_store.get_all()
            fact_map = {f.id: f for f in p.fact_store.get_facts()}
            enriched = []
            for r in rels:
                rd = r.model_dump()
                fa = fact_map.get(r.fact_a_id)
                fb = fact_map.get(r.fact_b_id)
                rd["fact_a"] = fa.model_dump() if fa else None
                rd["fact_b"] = fb.model_dump() if fb else None
                enriched.append(rd)
            return enriched
        elif endpoint.startswith("/cases/breakdown"):
            doc_id = None
            if "?doc_id=" in endpoint:
                doc_id = endpoint.split("?doc_id=")[1]
            return p.get_cases_breakdown(doc_id=doc_id)
        elif endpoint.startswith("/cases"):
            doc_id = None
            if "?doc_id=" in endpoint:
                doc_id = endpoint.split("?doc_id=")[1]
            cases = p.get_cases(doc_id=doc_id)
            return [c.model_dump() for c in cases]
        elif endpoint == "/export":
            return p.export_results()
    except Exception as e:
        return None

    return None

def _safe_float(val: Any, default: float = 0.0) -> float:
    try:
        if val is None:
            return default
        return float(val)
    except (ValueError, TypeError):
        return default

# Sidebar Navigation
page = st.sidebar.radio(
    "Navigation",
    ["📤 Upload Documents", "📄 Documents", "🔍 Facts Explorer", "🔗 Relationships", "✅ Four Required Cases", "📊 Export & Stats"]
)

st.sidebar.divider()
st.sidebar.subheader("System Maintenance")
if st.sidebar.button("🔄 Reset to Benchmark (Delhivery)", type="secondary", help="Restores the 3 benchmark Delhivery filings, 258 facts, and 47 relationships"):
    try:
        requests.post(f"{API_BASE_URL}/reset", timeout=5)
    except Exception:
        get_local_pipeline().reset_database()
    st.sidebar.success("Benchmark baseline restored successfully!")
    st.rerun()

if page == "📤 Upload Documents":
    st.header("Upload Documents")
    st.markdown("Upload PDF documents to parse, extract facts, ground evidence, and incrementally reconcile against existing knowledge.")

    uploaded_files = st.file_uploader("Choose PDF files", type=["pdf"], accept_multiple_files=True)

    if uploaded_files:
        if st.button("Process Documents", type="primary"):
            for file in uploaded_files:
                st.subheader(f"Processing: {file.name}")
                progress_bar = st.progress(0)
                status_text = st.empty()

                status_text.text("Uploading and running extraction pipeline...")
                progress_bar.progress(25)
                try:
                    # 1. Try via API
                    processed = False
                    try:
                        files = {"file": (file.name, file.getvalue(), "application/pdf")}
                        response = requests.post(f"{API_BASE_URL}/upload", files=files, timeout=600)
                        if response.status_code == 200:
                            result = response.json()
                            progress_bar.progress(100)
                            status_text.text("Processing complete!")
                            st.success(f"Successfully processed {file.name}")
                            with st.expander("Pipeline Output Details"):
                                st.json(result)
                            processed = True
                    except Exception:
                        pass

                    # 2. Local fallback if API is not running
                    if not processed:
                        temp_dir = tempfile.mkdtemp()
                        temp_path = os.path.join(temp_dir, file.name)
                        try:
                            with open(temp_path, "wb") as buffer:
                                buffer.write(file.getvalue())
                            local_res = get_local_pipeline().ingest_document(temp_path)
                            progress_bar.progress(100)
                            status_text.text("Processing complete (local pipeline)!")
                            st.success(f"Successfully processed {file.name}")
                            with st.expander("Pipeline Output Details"):
                                st.json(local_res)
                        finally:
                            if os.path.exists(temp_path):
                                os.remove(temp_path)
                            if os.path.exists(temp_dir):
                                os.rmdir(temp_dir)
                except Exception as e:
                    st.error(f"Error while processing {file.name}: {e}")

                st.divider()

elif page == "📄 Documents":
    st.header("Ingested Documents")

    docs = fetch_data("/documents")
    if docs is not None:
        if docs:
            df = pd.DataFrame(docs)
            st.dataframe(df, use_container_width=True)
            st.metric("Total Ingested Documents", len(docs))
        else:
            st.info("No documents uploaded yet. Go to 'Upload Documents' tab to get started.")
    else:
        st.warning("Could not reach backend API at http://localhost:8000. Is the API server running?")

elif page == "🔍 Facts Explorer":
    st.header("Extracted Facts Explorer")
    st.markdown("Browse and search extracted atomic facts, their source evidence, and contextual attributes.")

    facts = fetch_data("/facts")
    docs = fetch_data("/documents")

    if facts is not None and docs is not None:
        if not facts:
            st.info("No facts extracted yet.")
        else:
            doc_map = {d["id"]: d["filename"] for d in docs}
            doc_options = ["All Documents"] + list(doc_map.values())

            col1, col2 = st.columns(2)
            with col1:
                selected_doc = st.selectbox("Filter by Document", doc_options)
            with col2:
                search_query = st.text_input("Search Claims / Subjects / Keywords")

            filtered_facts = facts
            if selected_doc != "All Documents":
                doc_id_to_filter = next((k for k, v in doc_map.items() if v == selected_doc), None)
                filtered_facts = [f for f in filtered_facts if f.get("doc_id") == doc_id_to_filter]

            if search_query:
                q = search_query.lower()
                filtered_facts = [
                    f for f in filtered_facts
                    if q in f.get("claim", "").lower()
                    or q in f.get("subject", "").lower()
                    or q in f.get("object_value", "").lower()
                    or any(q in e.lower() for e in f.get("entities", []))
                ]

            st.write(f"Showing **{len(filtered_facts)}** facts")

            for fact in filtered_facts:
                claim_text = fact.get("claim", "No claim")
                with st.expander(f"**{claim_text}**"):
                    st.markdown(f"**Subject**: `{fact.get('subject')}` | **Predicate**: `{fact.get('predicate')}` | **Object/State**: `{fact.get('object_value')}`")

                    st.markdown("#### 📄 Grounded Source Evidence")
                    doc_name = fact.get("doc_filename") or doc_map.get(fact.get("doc_id"), "Unknown Document")
                    page_num = fact.get("page_number", "N/A")
                    st.caption(f"Source: **{doc_name}** — Page {page_num}")
                    quote = fact.get("source_quote", "")
                    if quote:
                        st.info(f"\"{quote}\"")

                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.markdown("#### Entities & Category")
                        st.write(f"**Category**: `{fact.get('category', 'general')}`")
                        entities = fact.get("entities", [])
                        entity_types = fact.get("entity_types", [])
                        if entities:
                            st.write("**Entities**:")
                            tags = [f"`{e}` ({t})" if i < len(entity_types) and (t := entity_types[i]) else f"`{e}`" for i, e in enumerate(entities)]
                            st.markdown(" ".join(tags))

                    with col_b:
                        st.markdown("#### Extraction Confidence")
                        conf = _safe_float(fact.get("confidence") or fact.get("confidence_score"), 0.85)
                        st.progress(min(max(conf, 0.0), 1.0))
                        st.write(f"Score: **{conf:.2f}** ({conf * 100:.1f}%)")

                    attrs = fact.get("attributes", {})
                    if attrs and isinstance(attrs, dict) and len(attrs) > 0:
                        st.markdown("#### Structured Attributes (Evolving Schema)")
                        attr_df = pd.DataFrame([{"Attribute": k, "Value": str(v)} for k, v in attrs.items()])
                        st.table(attr_df)
    else:
        st.warning("Backend API not reachable at http://localhost:8000. Start the server using: `python run.py --serve`")

elif page == "🔗 Relationships":
    st.header("Cross-Document Fact Relationships")
    st.markdown("Reconciliations discovered across different documents, classified by semantic comparison and contextual analysis.")

    relationships = fetch_data("/relationships")
    docs = fetch_data("/documents")

    if relationships is not None:
        if not relationships:
            st.info("No cross-document relationships discovered yet. Ensure at least two documents have been ingested.")
        else:
            rel_type = st.radio(
                "Filter by Relationship Type",
                ["All", "Corroboration", "Contradiction", "Contextual Reconciliation"],
                horizontal=True
            )

            filtered_rels = relationships
            if rel_type != "All":
                norm_type = rel_type.lower().replace(" ", "_")
                filtered_rels = [
                    r for r in filtered_rels
                    if r.get("relationship_type", "").lower() == norm_type or r.get("relationship_type", "").lower() == rel_type.lower()
                ]

            st.write(f"Showing **{len(filtered_rels)}** relationships")

            for rel in filtered_rels:
                fact_a = rel.get("fact_a")
                fact_b = rel.get("fact_b")

                rtype = rel.get("relationship_type", "unknown").lower()
                conf = _safe_float(rel.get("confidence") or rel.get("confidence_score"), 0.85)

                if "corroboration" in rtype:
                    st.success(f"✅ **CORROBORATION** (Confidence: {conf:.2f})")
                elif "contradiction" in rtype:
                    st.error(f"❌ **GENUINE CONTRADICTION** (Confidence: {conf:.2f})")
                elif "reconciliation" in rtype:
                    st.warning(f"🔄 **CONTEXTUAL RECONCILIATION** (Confidence: {conf:.2f})")
                else:
                    st.info(f"ℹ️ **{rtype.upper()}** (Confidence: {conf:.2f})")

                st.markdown(f"**System Reasoning & Evidence Analysis**:\n{rel.get('explanation', 'No explanation provided.')}")

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("#### Fact A")
                    if fact_a:
                        st.markdown(f"**Claim**: {fact_a.get('claim')}")
                        st.caption(f"📄 {fact_a.get('doc_filename', 'Unknown')} (Page {fact_a.get('page_number', 'N/A')})")
                        st.markdown(f"> *\"{fact_a.get('source_quote', '')}\"*")
                    else:
                        st.write(f"Fact ID: {rel.get('fact_a_id')}")

                with col2:
                    st.markdown("#### Fact B")
                    if fact_b:
                        st.markdown(f"**Claim**: {fact_b.get('claim')}")
                        st.caption(f"📄 {fact_b.get('doc_filename', 'Unknown')} (Page {fact_b.get('page_number', 'N/A')})")
                        st.markdown(f"> *\"{fact_b.get('source_quote', '')}\"*")
                    else:
                        st.write(f"Fact ID: {rel.get('fact_b_id')}")

                st.divider()
    else:
        st.warning("Backend API not reachable at http://localhost:8000.")

elif page == "✅ Four Required Cases":
    st.header("Four Required Analytical Cases")
    st.markdown("Demonstration of the four required scenarios specified in the Superjoin problem statement.")

    docs = fetch_data("/documents") or []
    doc_map = {d["id"]: d["filename"] for d in docs}
    doc_options = ["All Documents (Global)"] + list(doc_map.values())
    selected_doc_name = st.selectbox("Select Document Scope", doc_options)

    doc_filter_param = ""
    if selected_doc_name != "All Documents (Global)":
        doc_id_val = next((k for k, v in doc_map.items() if v == selected_doc_name), None)
        if doc_id_val:
            doc_filter_param = f"?doc_id={doc_id_val}"

    breakdown = fetch_data(f"/cases/breakdown{doc_filter_param}")

    if breakdown:
        featured = breakdown.get("featured_cases", [])
        corrobs = breakdown.get("corroborations", [])
        contras = breakdown.get("contradictions", [])
        recs = breakdown.get("reconciliations", [])
        limits = breakdown.get("limitations", [])

        # Display Top Metrics
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Corroborations", len(corrobs))
        m2.metric("Contradictions", len(contras))
        m3.metric("Reconciliations", len(recs))
        m4.metric("Limitations", len(limits))

        tab_spot, tab_corrob, tab_contra, tab_recon, tab_limit = st.tabs([
            "🌟 4 Spotlight Cases",
            f"All Corroborations ({len(corrobs)})",
            f"All Contradictions ({len(contras)})",
            f"All Reconciliations ({len(recs)})",
            f"Extraction Limitations ({len(limits)})"
        ])

        with tab_spot:
            if not featured:
                st.info("No cases identified for this document selection.")
            else:
                for case in featured:
                    c_num = case.get("case_number", "")
                    c_label = case.get("case_label", case.get("case_type", "Case"))
                    st.subheader(f"Case {c_num}: {c_label}")

                    if "Corroborat" in c_label:
                        st.success(f"**Analysis**: {case.get('explanation', '')}")
                    elif "Contradiction" in c_label:
                        st.error(f"**Analysis**: {case.get('explanation', '')}")
                    elif "Reconciliation" in c_label:
                        st.warning(f"**Analysis**: {case.get('explanation', '')}")
                    else:
                        st.info(f"**Analysis**: {case.get('explanation', '')}")

                    fact_a = case.get("fact_a")
                    fact_b = case.get("fact_b")

                    if fact_a and fact_b:
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("#### Evidence A")
                            st.markdown(f"**Claim**: {fact_a.get('claim')}")
                            st.caption(f"📄 {fact_a.get('doc_filename', 'Document')} (Page {fact_a.get('page_number')})")
                            st.markdown(f"> *\"{fact_a.get('source_quote', '')}\"*")
                        with col2:
                            st.markdown("#### Evidence B")
                            st.markdown(f"**Claim**: {fact_b.get('claim')}")
                            st.caption(f"📄 {fact_b.get('doc_filename', 'Document')} (Page {fact_b.get('page_number')})")
                            st.markdown(f"> *\"{fact_b.get('source_quote', '')}\"*")
                    elif fact_a:
                        st.markdown("#### Identified Challenge / Limitation")
                        st.markdown(f"**Claim**: {fact_a.get('claim')}")
                        st.caption(f"📄 {fact_a.get('doc_filename', 'Document')} (Page {fact_a.get('page_number')})")
                        st.markdown(f"> *\"{fact_a.get('source_quote', '')}\"*")

                    st.divider()

        with tab_corrob:
            if not corrobs:
                st.info("No corroborations found.")
            else:
                for r in corrobs:
                    fa = r.get("fact_a")
                    fb = r.get("fact_b")
                    st.markdown(f"**Signal Score**: {r.get('score')} | **Confidence**: {r.get('confidence'):.2f}")
                    st.info(f"**Reconciliation Reasoning**: {r.get('explanation')}")
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown(f"**Document A**: {fa.get('claim')}")
                        st.caption(f"📄 {fa.get('doc_filename')} (Pg {fa.get('page_number')})")
                        st.markdown(f"> *\"{fa.get('source_quote')}\"*")
                    with c2:
                        st.markdown(f"**Document B**: {fb.get('claim')}")
                        st.caption(f"📄 {fb.get('doc_filename')} (Pg {fb.get('page_number')})")
                        st.markdown(f"> *\"{fb.get('source_quote')}\"*")
                    st.divider()

        with tab_contra:
            if not contras:
                st.info("No contradictions found under this filter.")
            else:
                for r in contras:
                    fa = r.get("fact_a")
                    fb = r.get("fact_b")
                    st.error(f"**Contradiction Detected** (Score: {r.get('score')} | Confidence: {r.get('confidence'):.2f})")
                    st.markdown(f"**Conflict Reasoning**: {r.get('explanation')}")
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown(f"**Document A**: {fa.get('claim')}")
                        st.caption(f"📄 {fa.get('doc_filename')} (Pg {fa.get('page_number')})")
                        st.markdown(f"> *\"{fa.get('source_quote')}\"*")
                    with c2:
                        st.markdown(f"**Document B**: {fb.get('claim')}")
                        st.caption(f"📄 {fb.get('doc_filename')} (Pg {fb.get('page_number')})")
                        st.markdown(f"> *\"{fb.get('source_quote')}\"*")
                    st.divider()

        with tab_recon:
            if not recs:
                st.info("No contextual reconciliations found.")
            else:
                for r in recs:
                    fa = r.get("fact_a")
                    fb = r.get("fact_b")
                    st.warning(f"**Contextual Nuance** (Score: {r.get('score')} | Confidence: {r.get('confidence'):.2f})")
                    st.markdown(f"**Resolution Reasoning**: {r.get('explanation')}")
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown(f"**Document A**: {fa.get('claim')}")
                        st.caption(f"📄 {fa.get('doc_filename')} (Pg {fa.get('page_number')})")
                        st.markdown(f"> *\"{fa.get('source_quote')}\"*")
                    with c2:
                        st.markdown(f"**Document B**: {fb.get('claim')}")
                        st.caption(f"📄 {fb.get('doc_filename')} (Pg {fb.get('page_number')})")
                        st.markdown(f"> *\"{fb.get('source_quote')}\"*")
                    st.divider()

        with tab_limit:
            if not limits:
                st.info("No extraction limitations recorded.")
            else:
                for lim in limits:
                    f = lim.get("fact", {})
                    st.markdown(f"**Vulnerability in Layout / Token Stream** (Confidence: {lim.get('confidence'):.2f})")
                    st.markdown(f"> *\"{f.get('claim')}\"*")
                    st.caption(f"📄 {f.get('doc_filename')} (Pg {f.get('page_number')}) — Quote: \"{f.get('source_quote')}\"")
                    st.info(f"**Mitigation Analysis**: {lim.get('limitation_analysis')}")
                    st.divider()

    else:
        st.warning("Backend API not reachable at http://localhost:8000.")

elif page == "📊 Export & Stats":
    st.header("Export & System Statistics")
    st.markdown("Download full structured knowledge layer state as JSON.")

    export_data = fetch_data("/export")
    if export_data:
        summary = export_data.get("summary", {})
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Documents", summary.get("total_documents", 0))
        c2.metric("Total Facts", summary.get("total_facts", 0))
        c3.metric("Total Relationships", summary.get("total_relationships", 0))
        c4.metric("Corroborations", summary.get("corroborations", 0))

        c5, c6 = st.columns(2)
        c5.metric("Contradictions", summary.get("contradictions", 0))
        c6.metric("Contextual Reconciliations", summary.get("contextual_reconciliations", 0))

        json_str = json.dumps(export_data, indent=2)
        st.download_button(
            label="📥 Download Knowledge Graph JSON",
            data=json_str,
            file_name="fact_knowledge_layer_export.json",
            mime="application/json"
        )

        with st.expander("Preview Export JSON"):
            st.json(export_data)
    else:
        st.warning("Backend API not reachable at http://localhost:8000.")

import os
import shutil
import tempfile
from typing import List, Optional

from fastapi import FastAPI, UploadFile, File, Query, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from src.api.dashboard_html import get_dashboard_html

from src.pipeline import Pipeline

# Initialize the pipeline singleton
db_path = os.getenv("DB_PATH", "knowledge.db")
pipeline = Pipeline(db_path=db_path)

app = FastAPI(
    title="Superjoin Fact Knowledge Layer API",
    description="API for ingesting documents and extracting factual knowledge.",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/dashboard", response_class=HTMLResponse)
def get_dashboard():
    """Interactive Web Dashboard for viewing facts, cases, relationships, and uploading PDFs."""
    return HTMLResponse(content=get_dashboard_html())

@app.get("/")
def read_root(request: Request):
    """
    Root endpoint returning either the interactive Web Dashboard (for browsers)
    or JSON welcome message with available endpoints.
    """
    accept = request.headers.get("accept", "").lower()
    if "text/html" in accept and "application/json" not in accept:
        return HTMLResponse(content=get_dashboard_html())

    return {
        "message": "Welcome to the Superjoin Fact Knowledge Layer API",
        "dashboard": "http://localhost:8000/dashboard",
        "endpoints": [
            "GET /dashboard - Interactive Web Dashboard",
            "POST /api/upload - Upload one or more PDFs",
            "GET /api/documents - List all ingested documents",
            "GET /api/facts - List facts (optional ?doc_id=)",
            "GET /api/facts/{fact_id} - Get a specific fact",
            "GET /api/relationships - List relationships (optional ?type=)",
            "GET /api/cases - Get required analytical cases (optional ?doc_id=)",
            "GET /api/cases/breakdown - Get comprehensive 4-case categorized breakdown (optional ?doc_id=)",
            "POST /api/reset - Clear/reset all database records",
            "GET /api/export - Export full results"
        ]
    }

@app.post("/api/upload")
async def upload_documents(
    files: Optional[List[UploadFile]] = File(None),
    file: Optional[UploadFile] = File(None)
):
    """
    Upload one or more PDF documents.
    Each file is saved temporarily and ingested into the knowledge base.
    """
    upload_list: List[UploadFile] = []
    if files:
        upload_list.extend(files)
    if file:
        upload_list.append(file)

    if not upload_list:
        raise HTTPException(status_code=400, detail="No PDF files provided.")

    results = []
    for upload in upload_list:
        if not upload.filename.lower().endswith('.pdf'):
            results.append({
                "filename": upload.filename,
                "status": "error",
                "message": "Only PDF files are supported"
            })
            continue

        safe_name = os.path.basename(upload.filename)
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, safe_name)
        try:
            with open(temp_path, "wb") as buffer:
                shutil.copyfileobj(upload.file, buffer)

            # Ingest document incrementally
            ingest_result = pipeline.ingest_document(temp_path)
            results.append({
                "filename": safe_name,
                "status": "success",
                "result": ingest_result
            })
        except Exception as e:
            results.append({
                "filename": upload.filename,
                "status": "error",
                "message": str(e)
            })
        finally:
            upload.file.close()
            if os.path.exists(temp_path):
                os.remove(temp_path)
            if os.path.exists(temp_dir):
                os.rmdir(temp_dir)

    return JSONResponse(content={"results": results})

@app.get("/api/documents")
def get_documents():
    """
    Return a list of all ingested documents.
    """
    try:
        documents = pipeline.doc_store.get_all_documents()
        return [doc.model_dump() for doc in documents] if documents else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/facts")
def get_facts(doc_id: Optional[str] = Query(None, description="Filter facts by document ID")):
    """
    Return all extracted facts.
    """
    try:
        facts = pipeline.fact_store.get_facts(doc_id=doc_id)
        return [fact.model_dump() for fact in facts] if facts else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/facts/{fact_id}")
def get_fact(fact_id: str):
    """
    Return a specific fact by its ID.
    """
    try:
        fact = pipeline.fact_store.get_fact(fact_id)
        if fact:
            return fact.model_dump()
        raise HTTPException(status_code=404, detail="Fact not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/relationships")
def get_relationships(type: Optional[str] = Query(None, description="Filter relationships by type")):
    """
    Return all relationships, enriched with the underlying facts.
    """
    try:
        relationships = pipeline.rel_store.get_relationships(type=type.lower() if type else None)
        enriched_relationships = []
        if relationships:
            fact_map = {f.id: f for f in pipeline.fact_store.get_facts()}
            for rel in relationships:
                rel_dict = rel.model_dump()
                fact_a = fact_map.get(rel.fact_a_id)
                fact_b = fact_map.get(rel.fact_b_id)

                rel_dict["fact_a"] = fact_a.model_dump() if fact_a else None
                rel_dict["fact_b"] = fact_b.model_dump() if fact_b else None
                enriched_relationships.append(rel_dict)

        return enriched_relationships
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/cases")
def get_cases(doc_id: Optional[str] = Query(None, description="Filter cases by document ID or filename")):
    """
    Return the required analytical cases from the knowledge base.
    Optionally filtered by document.
    """
    try:
        cases = pipeline.get_cases(doc_id=doc_id)
        return [case.model_dump() for case in cases] if cases else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/cases/breakdown")
def get_cases_breakdown(doc_id: Optional[str] = Query(None, description="Filter cases breakdown by document ID or filename")):
    """
    Return comprehensive categorized breakdown of all discovered cases:
    - All Corroborations
    - All Contradictions
    - All Contextual Reconciliations
    - Identified Extraction Limitations
    - Featured Spotlight Cases
    Optionally filtered by document.
    """
    try:
        breakdown = pipeline.get_cases_breakdown(doc_id=doc_id)
        return breakdown
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/reset")
def reset_database(blank: bool = Query(False, description="If True, clears database completely; if False, resets to benchmark baseline")):
    """
    Resets the database. By default, restores the 3 benchmark Delhivery filings, facts,
    and relationships so the application always showcases verified ground truth.
    Set blank=true to wipe completely for external testing.
    """
    try:
        result = pipeline.reset_database(restore_benchmark=not blank)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/export")
def get_export():
    """
    Export the full knowledge base results.
    """
    try:
        export_data = pipeline.export_results()
        return export_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

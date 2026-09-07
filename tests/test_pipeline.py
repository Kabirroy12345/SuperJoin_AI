import os
import shutil
import tempfile
import pytest
from pathlib import Path

from src.schemas import (
    Document, Chunk, ChunkType, Fact, FactRelationship, RelationshipType
)
from src.ingestion.pdf_parser import PDFParser
from src.ingestion.chunker import Chunker
from src.ingestion.document_store import DocumentStore
from src.extraction.fact_store import FactStore
from src.reconciliation.embedder import FactEmbedder
from src.reconciliation.pairer import FactPairer
from src.reconciliation.reconciler import FactReconciler
from src.reconciliation.relationship_store import RelationshipStore
from src.llm.adapter import LLMAdapter
from src.pipeline import Pipeline


@pytest.fixture
def temp_db():
    temp_dir = tempfile.mkdtemp()
    db_path = os.path.join(temp_dir, "test_knowledge.db")
    yield db_path
    shutil.rmtree(temp_dir, ignore_errors=True)


def test_schemas():
    fact = Fact(
        claim="Delhivery reported revenue of 8142 crore in FY24",
        subject="Delhivery",
        predicate="annual revenue",
        object_value="8142 crore",
        doc_id="doc1",
        doc_filename="ar_2024.pdf",
        page_number=12,
        source_quote="Revenue from operations reached ₹8,142 crore in FY24.",
        entities=["Delhivery", "FY24"],
        entity_types=["Organization", "Period"],
        attributes={"value": 8142, "unit": "crore", "period": "FY24"},
        category="financial",
        confidence=0.95
    )
    assert fact.claim.startswith("Delhivery")
    assert fact.confidence == 0.95
    assert fact.attributes["value"] == 8142


def test_document_and_chunk_store(temp_db):
    doc_store = DocumentStore(db_path=temp_db)
    doc = Document(id="doc_123", filename="test.pdf", page_count=5)
    chunks = [
        Chunk(
            id="c1",
            doc_id="doc_123",
            doc_filename="test.pdf",
            page_number=1,
            text="First chunk of text about company revenue.",
            chunk_type=ChunkType.TEXT,
            token_estimate=10
        ),
        Chunk(
            id="c2",
            doc_id="doc_123",
            doc_filename="test.pdf",
            page_number=2,
            text="| Metric | FY24 |\n|---|---|\n| Revenue | 8142 |",
            chunk_type=ChunkType.TABLE,
            token_estimate=15
        )
    ]
    doc_store.add_document(doc, chunks)

    assert doc_store.document_exists("test.pdf") is True
    assert doc_store.document_exists("nonexistent.pdf") is False

    retrieved_doc = doc_store.get_document("doc_123")
    assert retrieved_doc is not None
    assert retrieved_doc.filename == "test.pdf"

    retrieved_chunks = doc_store.get_chunks("doc_123")
    assert len(retrieved_chunks) == 2
    assert retrieved_chunks[1].chunk_type == ChunkType.TABLE


def test_fact_store(temp_db):
    store = FactStore(db_path=temp_db)
    f1 = Fact(
        claim="Delhivery FY24 revenue was 8,142 Cr",
        subject="Delhivery",
        predicate="revenue",
        object_value="8,142 Cr",
        doc_id="doc_1",
        doc_filename="report1.pdf",
        page_number=4,
        source_quote="FY24 revenue was 8,142 Cr",
        entities=["Delhivery"],
        entity_types=["Organization"],
        attributes={"year": "FY24"},
        category="financial",
        confidence=0.98
    )
    store.add_facts([f1])

    assert store.count() == 1
    facts = store.get_facts(doc_id="doc_1")
    assert len(facts) == 1
    assert facts[0].claim == f1.claim
    assert facts[0].attributes["year"] == "FY24"


def test_embedder_and_pairer():
    embedder = FactEmbedder()
    pairer = FactPairer()

    f1 = Fact(
        id="f1",
        claim="Delhivery reported FY24 revenue of 8,142 crore",
        subject="Delhivery",
        predicate="revenue",
        object_value="8,142 crore",
        doc_id="doc_a",
        doc_filename="earnings.pdf",
        page_number=3,
        entities=["Delhivery"],
        attributes={"period": "FY24"}
    )
    f2 = Fact(
        id="f2",
        claim="Delhivery revenue from operations in FY24 stood at 8,142 crore",
        subject="Delhivery",
        predicate="revenue",
        object_value="8,142 crore",
        doc_id="doc_b",
        doc_filename="annual_report.pdf",
        page_number=22,
        entities=["Delhivery Limited"],
        attributes={"period": "FY24"}
    )
    f3 = Fact(
        id="f3",
        claim="The weather in Mumbai was warm during July",
        subject="Weather",
        predicate="condition",
        object_value="warm",
        doc_id="doc_c",
        doc_filename="weather.pdf",
        page_number=1,
        entities=["Mumbai"],
        attributes={}
    )

    embedded = embedder.embed([f1, f2, f3])
    assert f1.embedding is not None
    assert f2.embedding is not None

    candidates = pairer.find_candidates(new_facts=[f1], existing_facts=[f2, f3], min_cosine=0.60)
    assert len(candidates) >= 1
    matched_ids = [c[1].id for c in candidates]
    assert "f2" in matched_ids
    assert "f3" not in matched_ids


def test_reconciler_and_relationship_store(temp_db):
    llm = LLMAdapter()
    reconciler = FactReconciler(llm_adapter=llm)
    rel_store = RelationshipStore(db_path=temp_db)

    f1 = Fact(
        id="f1",
        claim="Delhivery reported revenue of 8,142 crore in FY24",
        subject="Delhivery",
        predicate="revenue",
        object_value="8,142 crore",
        doc_id="doc_a",
        doc_filename="doc_a.pdf",
        page_number=1,
        source_quote="Revenue was 8,142 crore in FY24."
    )
    f2 = Fact(
        id="f2",
        claim="Delhivery recorded revenue from operations of 8,142 crore in FY24",
        subject="Delhivery",
        predicate="revenue",
        object_value="8,142 crore",
        doc_id="doc_b",
        doc_filename="doc_b.pdf",
        page_number=5,
        source_quote="Revenue stood at 8,142 crore for the fiscal year 2024."
    )

    candidates = [(f1, f2, 0.95)]
    relationships = reconciler.reconcile(candidates)
    assert len(relationships) == 1
    assert relationships[0].relationship_type in [
        RelationshipType.CORROBORATION,
        RelationshipType.CONTEXTUAL_RECONCILIATION
    ]

    rel_store.add_relationships(relationships)
    stored = rel_store.get_all()
    assert len(stored) == 1


def test_pipeline_cases_and_export(temp_db):
    pipeline = Pipeline(db_path=temp_db)
    doc_a = Document(id="doc_a", filename="doc_a.pdf", page_count=2)
    doc_b = Document(id="doc_b", filename="doc_b.pdf", page_count=3)
    pipeline.doc_store.add_document(doc_a, [])
    pipeline.doc_store.add_document(doc_b, [])

    f1 = Fact(
        id="f1",
        claim="Delhivery revenue in FY24 was ₹8,142 crore",
        subject="Delhivery",
        predicate="revenue",
        object_value="8,142 crore",
        doc_id="doc_a",
        doc_filename="doc_a.pdf",
        page_number=1,
        source_quote="Revenue was ₹8,142 crore in FY24.",
        confidence=0.95
    )
    f2 = Fact(
        id="f2",
        claim="Delhivery revenue for FY24 was reported at ₹8,142 crore",
        subject="Delhivery",
        predicate="revenue",
        object_value="8,142 crore",
        doc_id="doc_b",
        doc_filename="doc_b.pdf",
        page_number=2,
        source_quote="FY24 revenue was reported at ₹8,142 crore.",
        confidence=0.96
    )
    pipeline.fact_store.add_facts([f1, f2])

    rel = FactRelationship(
        fact_a_id="f1",
        fact_b_id="f2",
        relationship_type=RelationshipType.CORROBORATION,
        explanation="Both documents report the identical FY24 revenue of 8,142 crore.",
        confidence=0.98
    )
    pipeline.rel_store.add_relationship(rel)

    cases = pipeline.get_cases()
    assert len(cases) >= 1
    assert any(c.case_label == "Corroborated Fact" for c in cases)

    export_data = pipeline.export_results()
    assert export_data["summary"]["total_documents"] == 2
    assert export_data["summary"]["total_facts"] == 2
    assert export_data["summary"]["total_relationships"] == 1

"""
End-to-end pipeline orchestrator for the Fact Knowledge Layer.

Coordinates: PDF parsing → chunking → fact extraction → embedding →
candidate pairing → reconciliation → storage.

Supports incremental ingestion: new documents are compared only against
existing facts, not reprocessed from scratch.
"""

import logging
import json
from pathlib import Path
from typing import Any

from src.schemas import (
    Document, Chunk, Fact, FactRelationship,
    ExtractionResult, ReconciliationResult, CaseExample,
    RelationshipType,
)
from src.ingestion.pdf_parser import PDFParser
from src.ingestion.chunker import Chunker
from src.ingestion.document_store import DocumentStore
from src.extraction.fact_extractor import FactExtractor
from src.extraction.fact_store import FactStore
from src.reconciliation.embedder import FactEmbedder
from src.reconciliation.pairer import FactPairer
from src.reconciliation.reconciler import FactReconciler
from src.reconciliation.relationship_store import RelationshipStore
from src.llm.adapter import LLMAdapter

logger = logging.getLogger(__name__)


class Pipeline:
    """
    End-to-end pipeline for the Fact Knowledge Layer.

    Usage:
        pipeline = Pipeline(db_path="knowledge.db")
        pipeline.ingest_document("path/to/document.pdf")
        cases = pipeline.get_cases()
    """

    def __init__(self, db_path: str = "knowledge.db"):
        self.db_path = db_path

        # Initialize components
        self.parser = PDFParser()
        self.chunker = Chunker()
        self.doc_store = DocumentStore(db_path=db_path)
        self.llm = LLMAdapter()
        self.extractor = FactExtractor(self.llm)
        self.fact_store = FactStore(db_path=db_path)
        self.embedder = FactEmbedder()
        self.pairer = FactPairer()
        self.reconciler = FactReconciler(self.llm)
        self.rel_store = RelationshipStore(db_path=db_path)

    def ingest_document(self, pdf_path: str) -> dict[str, Any]:
        """
        Ingest a single PDF document incrementally.

        1. Parse PDF → raw chunks
        2. Split into LLM-friendly chunks
        3. Extract facts via LLM
        4. Embed facts
        5. Find candidate pairs (new facts vs existing facts)
        6. Reconcile pairs via LLM
        7. Store everything

        Returns a summary dict with counts.
        """
        path = Path(pdf_path)
        filename = path.name

        # Check if already processed
        if self.doc_store.document_exists(filename):
            logger.info(f"Document '{filename}' already processed, skipping.")
            return {"status": "skipped", "reason": "already processed"}

        logger.info(f"=== Ingesting: {filename} ===")

        # Step 1: Parse PDF
        logger.info("Step 1/6: Parsing PDF...")
        document, raw_chunks = self.parser.parse(pdf_path)
        logger.info(f"  → {len(raw_chunks)} raw chunks from {document.page_count} pages")

        # Step 2: Chunk for LLM
        logger.info("Step 2/6: Chunking for LLM...")
        chunks = self.chunker.chunk(raw_chunks)
        logger.info(f"  → {len(chunks)} chunks after splitting")

        # Step 3: Store document & chunks
        self.doc_store.add_document(document, chunks)

        # Step 4: Extract facts
        logger.info("Step 3/6: Extracting facts via LLM...")
        new_facts = self.extractor.extract(chunks)
        logger.info(f"  → {len(new_facts)} facts extracted")

        if not new_facts:
            logger.warning("No facts extracted from document.")
            return {
                "status": "done",
                "document": filename,
                "chunks": len(chunks),
                "facts": 0,
                "relationships": 0,
            }

        # Step 5: Store facts
        self.fact_store.add_facts(new_facts)

        # Step 6: Embed new facts
        logger.info("Step 4/6: Embedding facts...")
        new_facts = self.embedder.embed(new_facts)

        # Step 7: Find candidate pairs (new vs existing)
        logger.info("Step 5/6: Finding candidate pairs...")
        existing_facts = self.fact_store.get_all(exclude_doc=document.id)

        new_relationships = []
        if existing_facts:
            # Embed existing facts if not already embedded
            existing_facts = self.embedder.embed(existing_facts)

            candidates = self.pairer.find_candidates(new_facts, existing_facts)
            logger.info(f"  → {len(candidates)} candidate pairs found")

            # Step 8: Reconcile
            if candidates:
                logger.info("Step 6/6: Reconciling pairs via LLM...")
                new_relationships = self.reconciler.reconcile(candidates)
                logger.info(f"  → {len(new_relationships)} relationships discovered")

                # Store relationships
                self.rel_store.add_relationships(new_relationships)
        else:
            logger.info("  → No existing facts to compare against (first document)")

        result = {
            "status": "done",
            "document": filename,
            "pages": document.page_count,
            "chunks": len(chunks),
            "facts": len(new_facts),
            "relationships": len(new_relationships),
        }
        logger.info(f"=== Done: {result} ===")
        return result

    def ingest_dataset(self, folder_path: str) -> list[dict[str, Any]]:
        """
        Process all PDFs in a folder sequentially.

        Each document is processed incrementally — only compared against
        previously processed documents, not recomputed from scratch.
        """
        folder = Path(folder_path)
        pdf_files = sorted(folder.glob("*.pdf"))

        if not pdf_files:
            logger.warning(f"No PDF files found in {folder_path}")
            return []

        logger.info(f"Found {len(pdf_files)} PDFs in {folder_path}")
        results = []
        for pdf_file in pdf_files:
            result = self.ingest_document(str(pdf_file))
            results.append(result)

        return results

    def get_cases(self) -> list[CaseExample]:
        """
        Return one example of each of the 4 required cases.

        Case 1: Corroborated fact
        Case 2: Genuine contradiction
        Case 3: Contextual reconciliation
        Case 4: Extraction failure / limitation
        """
        cases = []
        all_rels = self.rel_store.get_all()

        # Case 1: Corroboration
        corroborations = [r for r in all_rels
                          if r.relationship_type == RelationshipType.CORROBORATION]
        if corroborations:
            rel = corroborations[0]
            fact_a = self.fact_store.get_fact(rel.fact_a_id)
            fact_b = self.fact_store.get_fact(rel.fact_b_id)
            if fact_a and fact_b:
                cases.append(CaseExample(
                    case_number=1,
                    case_label="Corroborated Fact",
                    fact_a=fact_a,
                    fact_b=fact_b,
                    relationship=rel,
                    explanation=f"These two facts from different documents confirm each other. {rel.explanation}",
                ))

        # Case 2: Contradiction
        contradictions = [r for r in all_rels
                          if r.relationship_type == RelationshipType.CONTRADICTION]
        if contradictions:
            rel = contradictions[0]
            fact_a = self.fact_store.get_fact(rel.fact_a_id)
            fact_b = self.fact_store.get_fact(rel.fact_b_id)
            if fact_a and fact_b:
                cases.append(CaseExample(
                    case_number=2,
                    case_label="Genuine Contradiction",
                    fact_a=fact_a,
                    fact_b=fact_b,
                    relationship=rel,
                    explanation=f"These two facts genuinely conflict. {rel.explanation}",
                ))

        # Case 3: Contextual Reconciliation
        reconciliations = [r for r in all_rels
                           if r.relationship_type == RelationshipType.CONTEXTUAL_RECONCILIATION]
        if reconciliations:
            rel = reconciliations[0]
            fact_a = self.fact_store.get_fact(rel.fact_a_id)
            fact_b = self.fact_store.get_fact(rel.fact_b_id)
            if fact_a and fact_b:
                cases.append(CaseExample(
                    case_number=3,
                    case_label="Contextual Reconciliation",
                    fact_a=fact_a,
                    fact_b=fact_b,
                    relationship=rel,
                    explanation=f"These facts appear contradictory but are reconcilable. {rel.explanation}",
                ))

        # Case 4: Extraction failure — find a low-confidence fact
        all_facts = self.fact_store.get_facts()
        low_confidence = [f for f in all_facts if f.confidence < 0.5]
        if low_confidence:
            fact = low_confidence[0]
            cases.append(CaseExample(
                case_number=4,
                case_label="Extraction Failure / Limitation",
                fact_a=fact,
                explanation=(
                    f"This fact was extracted with low confidence ({fact.confidence:.2f}). "
                    f"The source text may be ambiguous, from a complex table, or partially "
                    f"extracted. Improvements could include better table parsing, OCR for "
                    f"scanned content, or multi-pass extraction with verification."
                ),
            ))
        elif all_facts:
            # If no low-confidence facts, pick the one with lowest confidence
            fact = min(all_facts, key=lambda f: f.confidence)
            cases.append(CaseExample(
                case_number=4,
                case_label="Extraction Failure / Limitation",
                fact_a=fact,
                explanation=(
                    f"This fact had the lowest extraction confidence ({fact.confidence:.2f}). "
                    f"While above the failure threshold, it demonstrates areas where "
                    f"extraction could be improved: complex tables, charts rendered as "
                    f"images, or ambiguous statements that need multi-document context."
                ),
            ))

        return cases

    def export_results(self) -> dict[str, Any]:
        """Export all facts and relationships as a JSON-serializable dict."""
        facts = self.fact_store.get_facts()
        rels = self.rel_store.get_all()
        docs = self.doc_store.get_all_documents()
        cases = self.get_cases()

        return {
            "documents": [d.model_dump() for d in docs],
            "facts": [f.model_dump() for f in facts],
            "relationships": [r.model_dump() for r in rels],
            "cases": [c.model_dump() for c in cases],
            "summary": {
                "total_documents": len(docs),
                "total_facts": len(facts),
                "total_relationships": len(rels),
                "corroborations": sum(1 for r in rels if r.relationship_type == RelationshipType.CORROBORATION),
                "contradictions": sum(1 for r in rels if r.relationship_type == RelationshipType.CONTRADICTION),
                "contextual_reconciliations": sum(1 for r in rels if r.relationship_type == RelationshipType.CONTEXTUAL_RECONCILIATION),
            },
        }

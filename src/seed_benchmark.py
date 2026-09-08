import json
import os
import sqlite3
import shutil
from pathlib import Path
from src.schemas import Document, Chunk, Fact, FactRelationship, RelationshipType
from src.pipeline import Pipeline
from src.ingestion.pdf_parser import PDFParser
from src.ingestion.chunker import Chunker

def seed_benchmark(db_path: str = "knowledge.db"):
    """Restores the 3 benchmark Delhivery documents, facts, and relationships."""
    pipeline = Pipeline(db_path=db_path)
    parser = PDFParser()
    chunker = Chunker()

    results_file = Path("results.json")
    if not results_file.exists():
        print("Error: results.json not found!")
        return False

    with open(results_file, encoding="utf-8") as f:
        data = json.load(f)

    # 1. Clean existing records in target db
    with sqlite3.connect(db_path) as conn:
        conn.execute("DELETE FROM fact_relationships")
        conn.execute("DELETE FROM facts")
        conn.execute("DELETE FROM chunks")
        conn.execute("DELETE FROM documents")
        conn.commit()

    # 2. Re-ingest documents and chunks
    delhivery_dir = Path("delhivery")
    for d_dict in data.get("documents", []):
        pdf_path = delhivery_dir / d_dict["filename"]
        if pdf_path.exists():
            parsed_doc, raw_chunks = parser.parse(str(pdf_path))
            chunks = chunker.chunk(raw_chunks)
            parsed_doc.id = d_dict["id"]
            for c in chunks:
                c.doc_id = d_dict["id"]
                c.doc_filename = d_dict["filename"]
            pipeline.doc_store.add_document(parsed_doc, chunks)
            print(f"Ingested doc & {len(chunks)} chunks for {d_dict['filename']}")
        else:
            doc = Document(**d_dict)
            pipeline.doc_store.add_document(doc, [])

    # 3. Restore facts
    facts = [Fact(**f) for f in data.get("facts", [])]
    pipeline.fact_store.add_facts(facts)
    print(f"Restored {len(facts)} facts.")

    # 4. Restore relationships
    rels = []
    for r in data.get("relationships", []):
        r_obj = FactRelationship(
            id=r["id"],
            fact_a_id=r["fact_a_id"],
            fact_b_id=r["fact_b_id"],
            relationship_type=RelationshipType(r["relationship_type"]),
            explanation=r["explanation"],
            confidence=r["confidence"]
        )
        rels.append(r_obj)
    pipeline.rel_store.add_relationships(rels)
    print(f"Restored {len(rels)} relationships.")

    # 5. Snapshot to benchmark_backup.db for instant future resets
    shutil.copy(db_path, "benchmark_backup.db")
    print("Created benchmark_backup.db snapshot for instant restores.")
    return True

if __name__ == "__main__":
    seed_benchmark()

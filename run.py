#!/usr/bin/env python3
"""
CLI entry point for the Fact Knowledge Layer.

Usage:
    # Process all PDFs in a dataset folder
    python run.py --dataset data/starter/delhivery/

    # Process a single PDF
    python run.py --pdf path/to/document.pdf

    # Export all results as JSON
    python run.py --export results.json

    # Show the 4 required cases
    python run.py --cases

    # Start the API server
    python run.py --serve
"""

import argparse
import json
import logging
import sys
from pathlib import Path


def setup_logging(verbose: bool = False) -> None:
    """Configure logging for the application."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )
    # Quiet down noisy libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("sentence_transformers").setLevel(logging.WARNING)


if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fact Knowledge Layer — extract, compare, and reconcile facts from PDFs",
    )
    parser.add_argument(
        "--dataset", type=str,
        help="Path to a folder of PDFs to process (e.g., delhivery/ or india-macroeconomy/)",
    )
    parser.add_argument(
        "--pdf", type=str,
        help="Path to a single PDF to process",
    )
    parser.add_argument(
        "--export", type=str, nargs="?", const="results.json",
        help="Export all results as JSON (default: results.json)",
    )
    parser.add_argument(
        "--cases", action="store_true",
        help="Show the 4 required cases (corroboration, contradiction, reconciliation, failure)",
    )
    parser.add_argument(
        "--serve", action="store_true",
        help="Start the FastAPI server",
    )
    parser.add_argument(
        "--db", type=str, default="knowledge.db",
        help="Path to SQLite database (default: knowledge.db)",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help="Enable verbose logging",
    )

    args = parser.parse_args()
    setup_logging(args.verbose)

    # If no action specified, show help
    if not any([args.dataset, args.pdf, args.export, args.cases, args.serve]):
        parser.print_help()
        sys.exit(1)

    from src.pipeline import Pipeline
    pipeline = Pipeline(db_path=args.db)

    # --- Process dataset ---
    if args.dataset:
        dataset_path = Path(args.dataset)
        if not dataset_path.exists():
            print(f"Error: Dataset folder '{args.dataset}' not found.")
            sys.exit(1)
        results = pipeline.ingest_dataset(str(dataset_path))
        print(f"\n{'='*60}")
        print("INGESTION COMPLETE")
        print(f"{'='*60}")
        for r in results:
            print(f"  {r.get('document', 'unknown'):50s} → {r.get('facts', 0)} facts, {r.get('relationships', 0)} relationships")
        total_facts = sum(r.get("facts", 0) for r in results)
        total_rels = sum(r.get("relationships", 0) for r in results)
        print(f"\n  Total: {total_facts} facts, {total_rels} relationships across {len(results)} documents")

    # --- Process single PDF ---
    if args.pdf:
        pdf_path = Path(args.pdf)
        if not pdf_path.exists():
            print(f"Error: PDF file '{args.pdf}' not found.")
            sys.exit(1)
        result = pipeline.ingest_document(str(pdf_path))
        print(f"\nResult: {json.dumps(result, indent=2)}")

    # --- Show cases ---
    if args.cases:
        cases = pipeline.get_cases()
        if not cases:
            print("\nNo cases found. Process some PDFs first with --dataset or --pdf.")
        else:
            print(f"\n{'='*60}")
            print("THE FOUR REQUIRED CASES")
            print(f"{'='*60}")
            for case in cases:
                print(f"\n{'-'*60}")
                print(f"CASE {case.case_number}: {case.case_label}")
                print(f"{'-'*60}")
                print(f"\n  Fact A:")
                print(f"    Claim:    {case.fact_a.claim}")
                print(f"    Source:   {case.fact_a.doc_filename}, page {case.fact_a.page_number}")
                print(f"    Quote:    \"{case.fact_a.source_quote[:150]}...\"" if len(case.fact_a.source_quote) > 150 else f"    Quote:    \"{case.fact_a.source_quote}\"")

                if case.fact_b:
                    print(f"\n  Fact B:")
                    print(f"    Claim:    {case.fact_b.claim}")
                    print(f"    Source:   {case.fact_b.doc_filename}, page {case.fact_b.page_number}")
                    print(f"    Quote:    \"{case.fact_b.source_quote[:150]}...\"" if len(case.fact_b.source_quote) > 150 else f"    Quote:    \"{case.fact_b.source_quote}\"")

                if case.relationship:
                    print(f"\n  Relationship: {case.relationship.relationship_type.value}")
                    print(f"  Confidence:   {case.relationship.confidence:.2f}")

                print(f"\n  Explanation: {case.explanation}")

    # --- Export results ---
    if args.export:
        results = pipeline.export_results()
        output_path = Path(args.export)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)
        print(f"\nResults exported to {output_path}")
        print(f"  Documents:     {results['summary']['total_documents']}")
        print(f"  Facts:         {results['summary']['total_facts']}")
        print(f"  Relationships: {results['summary']['total_relationships']}")
        print(f"    Corroborations:   {results['summary']['corroborations']}")
        print(f"    Contradictions:   {results['summary']['contradictions']}")
        print(f"    Reconciliations:  {results['summary']['contextual_reconciliations']}")

    # --- Start API server ---
    if args.serve:
        import uvicorn
        print("\nStarting Fact Knowledge Layer API server...")
        uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()

import json
import uuid
import logging
from typing import List, Tuple

from src.schemas import Fact, FactRelationship, RelationshipType
from src.llm.adapter import LLMAdapter

logger = logging.getLogger(__name__)

class FactReconciler:
    """Reconciles candidate fact pairs using an LLM to determine their relationship."""
    
    def __init__(self, llm_adapter: LLMAdapter):
        self.llm = llm_adapter

    def reconcile(self, candidates: List[Tuple[Fact, Fact, float]], batch_size: int = 4) -> List[FactRelationship]:
        """Evaluates candidate pairs using batched LLM classification.
        
        Args:
            candidates: List of tuples containing two Fact instances and their similarity score.
            batch_size: Number of pairs to evaluate per LLM prompt (default 4).
            
        Returns:
            A list of valid FactRelationships (filtering out UNRELATED pairs).
        """
        relationships = []
        if not candidates:
            return relationships

        for i in range(0, len(candidates), batch_size):
            batch = candidates[i:i + batch_size]
            pair_map = {f"p-{idx}": (fa, fb, sim) for idx, (fa, fb, sim) in enumerate(batch)}

            prompt_lines = [
                "You are an expert financial and corporate data auditor.",
                "Determine the relationship between pairs of extracted facts across different filings.\n",
                "CLASSIFICATION CATEGORIES:",
                "1. CORROBORATION: Both documents confirm the exact same metric, event, or claim across filings.",
                "2. CONTRADICTION: Both documents present mutually exclusive or conflicting metrics/claims without reconciliation.",
                "3. CONTEXTUAL_RECONCILIATION: Discrepancies are reconciled by differing time periods (e.g. 2021 vs 2024), definitions, or reporting scopes.",
                "4. UNRELATED: Discuss different metrics, topics, or entities.\n"
            ]

            for pid, (fa, fb, sim) in pair_map.items():
                prompt_lines.append(f"--- PAIR ID: {pid} ---")
                prompt_lines.append(f"Fact A [{fa.doc_filename}, Page {fa.page_number}]:")
                prompt_lines.append(f"  Claim: {fa.claim}")
                prompt_lines.append(f"  Source Quote: \"{fa.source_quote[:160]}\"")
                prompt_lines.append(f"Fact B [{fb.doc_filename}, Page {fb.page_number}]:")
                prompt_lines.append(f"  Claim: {fb.claim}")
                prompt_lines.append(f"  Source Quote: \"{fb.source_quote[:160]}\"\n")

            prompt_lines.append(
                "Respond with a JSON array where each object has:\n"
                "- \"pair_id\": (e.g. \"p-0\")\n"
                "- \"relationship_type\": (\"CORROBORATION\", \"CONTRADICTION\", \"CONTEXTUAL_RECONCILIATION\", or \"UNRELATED\")\n"
                "- \"explanation\": (2-3 clear sentences citing specific values, dates, or context from both sources)\n"
                "- \"confidence\": (Float between 0.0 and 1.0)\n\n"
                "Output ONLY a valid JSON array and no other text."
            )
            prompt = "\n".join(prompt_lines)

            try:
                results = self.llm.call_json(prompt)
                if not isinstance(results, list):
                    continue

                for res in results:
                    pid = res.get("pair_id")
                    if pid not in pair_map:
                        continue

                    fa, fb, sim = pair_map[pid]
                    rel_type_str = res.get("relationship_type", "").lower().strip()
                    norm_type = rel_type_str.replace(" ", "_").replace("-", "_")

                    if "unrelated" in norm_type:
                        continue
                    elif "corroborat" in norm_type:
                        rel_type = RelationshipType.CORROBORATION
                    elif "contradict" in norm_type:
                        rel_type = RelationshipType.CONTRADICTION
                    elif "reconcil" in norm_type or "context" in norm_type:
                        rel_type = RelationshipType.CONTEXTUAL_RECONCILIATION
                    else:
                        try:
                            rel_type = RelationshipType(norm_type)
                        except ValueError:
                            continue

                    explanation = res.get("explanation", "").strip()
                    raw_conf = res.get("confidence", 0.85)
                    try:
                        confidence = float(raw_conf)
                    except (ValueError, TypeError):
                        confidence = 0.85

                    rel = FactRelationship(
                        id=str(uuid.uuid4()),
                        fact_a_id=str(fa.id),
                        fact_b_id=str(fb.id),
                        relationship_type=rel_type,
                        explanation=explanation,
                        confidence=confidence
                    )
                    relationships.append(rel)

            except Exception as e:
                logger.error(f"Batch reconciliation error for batch starting at {i}: {e}")
                continue

        return relationships

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

    def reconcile(self, candidates: List[Tuple[Fact, Fact, float]]) -> List[FactRelationship]:
        """Evaluates candidate pairs and creates relationships.
        
        Args:
            candidates: List of tuples containing two Fact instances and their similarity score.
            
        Returns:
            A list of valid FactRelationships (filtering out UNRELATED pairs).
        """
        relationships = []
        
        for fact_a, fact_b, sim in candidates:
            prompt = self._build_prompt(fact_a, fact_b)
            
            try:
                # Request JSON format from the LLM Adapter
                response_text = self.llm.call(prompt)
                
                # Basic cleanup in case LLM adapter doesn't strip markdown code blocks
                response_text = response_text.strip()
                if response_text.startswith("```json"):
                    response_text = response_text[7:-3].strip()
                elif response_text.startswith("```"):
                    response_text = response_text[3:-3].strip()
                    
                result = json.loads(response_text)
                
                rel_type_str = result.get("relationship_type", "").upper()
                
                # Filter out UNRELATED pairs (don't store them)
                if rel_type_str == "UNRELATED":
                    continue
                    
                try:
                    rel_type = RelationshipType(rel_type_str.lower())
                except ValueError:
                    logger.warning(f"Invalid relationship type returned by LLM: {rel_type_str}")
                    continue
                    
                explanation = result.get("explanation", "")
                confidence = float(result.get("confidence", 0.0))
                
                rel = FactRelationship(
                    id=str(uuid.uuid4()),
                    fact_a_id=str(fact_a.id),
                    fact_b_id=str(fact_b.id),
                    relationship_type=rel_type,
                    explanation=explanation,
                    confidence=confidence
                )
                relationships.append(rel)
                
            except Exception as e:
                logger.error(f"Error reconciling facts {fact_a.id} and {fact_b.id}: {e}")
                
        return relationships

    def _build_prompt(self, fact_a: Fact, fact_b: Fact) -> str:
        """Builds a domain-agnostic prompt to evaluate the relationship between two facts."""
        return f"""You are an expert data analyst. Your task is to determine the relationship between two extracted facts from different documents.

Fact A:
- Document: {fact_a.doc_filename} (Page {fact_a.page_number})
- Claim: {fact_a.claim}
- Source Quote: "{fact_a.source_quote}"

Fact B:
- Document: {fact_b.doc_filename} (Page {fact_b.page_number})
- Claim: {fact_b.claim}
- Source Quote: "{fact_b.source_quote}"

Classify the relationship between Fact A and Fact B into exactly one of these categories:
1. CORROBORATION: They support or confirm each other.
2. CONTRADICTION: They conflict or present mutually exclusive information.
3. CONTEXTUAL_RECONCILIATION: They appear to conflict or be different, but can be reconciled (e.g., different dates, different reporting metrics, different scopes).
4. UNRELATED: They are completely unrelated or describing different entities/topics.

Respond with a JSON object containing:
- "relationship_type": (One of: "CORROBORATION", "CONTRADICTION", "CONTEXTUAL_RECONCILIATION", "UNRELATED")
- "explanation": (A 2-3 sentence explanation citing specific values, dates, or context from both sources)
- "confidence": (A float between 0.0 and 1.0 indicating your confidence)
"""

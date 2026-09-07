import numpy as np
import re
from typing import List, Tuple, Set
from difflib import SequenceMatcher
from src.schemas import Fact

class FactPairer:
    """Finds candidate pairs of facts for reconciliation across documents."""
    
    def __init__(self):
        # Common suffixes, honorifics, and generic corporate terms to strip
        self.stop_words = {
            'mr', 'mrs', 'ms', 'dr', 'ltd', 'limited', 'inc', 'corp', 'corporation',
            'llc', 'and', 'the', 'of', 'company', 'group', 'report', 'delhivery', 'india'
        }

    def _normalize_entity(self, entity: str) -> str:
        """Lowercase and strip honorifics/suffixes from entity."""
        normalized = entity.lower().strip()
        normalized = re.sub(r'[^\w\s]', '', normalized)
        words = [w for w in normalized.split() if w not in self.stop_words]
        return ' '.join(words)

    def _entities_overlap(self, entities_a: List[str], entities_b: List[str]) -> bool:
        """Check if any normalized entity matches using fast set intersection and fuzzy ratio."""
        if not entities_a or not entities_b:
            return False
            
        norm_a: Set[str] = {self._normalize_entity(e) for e in entities_a}
        norm_b: Set[str] = {self._normalize_entity(e) for e in entities_b}
        norm_a.discard("")
        norm_b.discard("")
        
        if not norm_a or not norm_b:
            return False

        # 1. Fast O(1) exact set intersection
        if norm_a & norm_b:
            return True
            
        # 2. Substring containment
        for a in norm_a:
            for b in norm_b:
                if len(a) >= 3 and len(b) >= 3:
                    if a in b or b in a:
                        return True
                    if abs(len(a) - len(b)) <= 3 and SequenceMatcher(None, a, b).ratio() >= 0.85:
                        return True
        return False

    def _cosine_similarity(self, vec_a: List[float], vec_b: List[float]) -> float:
        """Compute cosine similarity between two unit-normalized vectors."""
        if not vec_a or not vec_b:
            return 0.0
            
        a = np.array(vec_a, dtype=np.float32)
        b = np.array(vec_b, dtype=np.float32)
        dot = float(np.dot(a, b))
        return max(-1.0, min(1.0, dot))

    def find_candidates(
        self, 
        new_facts: List[Fact], 
        existing_facts: List[Fact], 
        min_cosine: float = 0.72, 
        top_k: int = 2,
        max_total: int = 35
    ) -> List[Tuple[Fact, Fact, float]]:
        """Finds candidate pairs of facts for reconciliation.
        
        Args:
            new_facts: Facts to match against existing ones.
            existing_facts: The existing knowledge base of facts.
            min_cosine: Minimum cosine similarity threshold for matched facts.
            top_k: Maximum candidate matches to keep per new fact.
            max_total: Overall cap for top candidate pairs across the document.
            
        Returns:
            A list of tuples containing (Fact A, Fact B, cosine_similarity).
        """
        candidates: dict[tuple[str, str], tuple[Fact, Fact, float]] = {}
        
        valid_new = [f for f in new_facts if f.embedding is not None]
        valid_existing = [f for f in existing_facts if f.embedding is not None]
        
        if not valid_new or not valid_existing:
            return []

        # Vectorized batch cosine similarity
        new_matrix = np.array([f.embedding for f in valid_new], dtype=np.float32)
        exist_matrix = np.array([f.embedding for f in valid_existing], dtype=np.float32)
        
        # similarity matrix of shape (len(valid_new), len(valid_existing))
        sim_matrix = np.dot(new_matrix, exist_matrix.T)

        for i, nf in enumerate(valid_new):
            nf_candidates = []
            
            # Find indices where sim >= min_cosine
            candidate_indices = np.where(sim_matrix[i] >= min_cosine)[0]
            
            for j in candidate_indices:
                ef = valid_existing[j]
                if nf.doc_id == ef.doc_id:
                    continue
                    
                sim = float(sim_matrix[i, j])
                
                # Rule 1: Entity overlap AND sim >= min_cosine
                has_overlap = self._entities_overlap(nf.entities, ef.entities)
                if has_overlap:
                    nf_candidates.append((ef, sim))
                elif sim >= 0.82: # Rule 2: High semantic similarity fallback
                    nf_candidates.append((ef, sim))
                    
            nf_candidates.sort(key=lambda x: x[1], reverse=True)
            for ef, sim in nf_candidates[:top_k]:
                pair_key = tuple(sorted([str(nf.id), str(ef.id)]))
                if pair_key not in candidates:
                    candidates[pair_key] = (nf, ef, sim)
                    
        # Sort all discovered candidate pairs by similarity and return top max_total
        sorted_pairs = sorted(candidates.values(), key=lambda x: x[2], reverse=True)
        return sorted_pairs[:max_total]

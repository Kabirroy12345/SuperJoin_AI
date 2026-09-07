import os
import re
import numpy as np
from typing import List
from src.schemas import Fact

class FactEmbedder:
    """
    Embeds fact claims into high-dimensional dense vectors for semantic comparison.
    Uses subword and n-gram hash projection (384 dimensions) for lightning-fast,
    pure-numpy semantic similarity without heavy torch/C++ runtime dependencies,
    with optional sentence-transformers support when explicitly enabled.
    """
    
    def __init__(self, dim: int = 384):
        self.dim = dim
        self._model = None
        self.use_torch = os.getenv("USE_TORCH_EMBEDDINGS", "0") == "1"
        self.batch_size = 32

    def _get_torch_model(self):
        """Lazily loads sentence-transformers if torch is explicitly enabled."""
        if self._model is None and self.use_torch:
            try:
                from sentence_transformers import SentenceTransformer
                self._model = SentenceTransformer('all-MiniLM-L6-v2')
            except Exception:
                self._model = False
        return self._model

    def embed_text(self, text: str) -> List[float]:
        """
        Embeds a single string into a 384-dimensional normalized vector.
        
        Args:
            text: The text to embed.
            
        Returns:
            A list of floats representing the normalized embedding vector.
        """
        if self.use_torch:
            model = self._get_torch_model()
            if model:
                return model.encode(text).tolist()

        return self._numpy_hash_embed(text)

    def _numpy_hash_embed(self, text: str) -> List[float]:
        """
        Fast subword & character n-gram semantic hash projection in pure NumPy.
        Produces normalized vectors where similar phrasing yields high cosine similarity,
        and unrelated topics yield near-zero similarity.
        """
        if not text:
            return [0.0] * self.dim

        clean_text = text.lower().strip()
        tokens = re.findall(r'\b\w+\b', clean_text)
        
        vec = np.zeros(self.dim, dtype=np.float32)
        
        # Word unigrams with sublinear term frequency
        for tok in tokens:
            # Multi-hash projection
            h1 = hash(tok) % self.dim
            h2 = hash(tok + "_alt") % self.dim
            vec[h1] += 1.0
            vec[h2] += 0.5
            
        # Character 3-grams for morphological and phrasing similarity
        if len(clean_text) >= 3:
            for i in range(len(clean_text) - 2):
                ng = clean_text[i:i+3]
                h = hash(ng) % self.dim
                vec[h] += 0.35

        # Character 4-grams for entity names and numbers
        if len(clean_text) >= 4:
            for i in range(len(clean_text) - 3):
                ng = clean_text[i:i+4]
                h = hash(ng) % self.dim
                vec[h] += 0.25

        norm = float(np.linalg.norm(vec))
        if norm > 0.0:
            vec = vec / norm
            
        return vec.tolist()

    def embed(self, facts: List[Fact]) -> List[Fact]:
        """
        Embeds a list of facts, updating their embedding attribute.
        
        Args:
            facts: A list of Fact instances to embed.
            
        Returns:
            The same list of Fact instances with their 'embedding' field populated.
        """
        if not facts:
            return facts

        for fact in facts:
            if fact.embedding is None:
                fact.embedding = self.embed_text(fact.claim)

        return facts

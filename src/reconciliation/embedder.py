import os
import re
import json
import logging
import urllib.request
import numpy as np
from typing import List, Dict, Optional
from dotenv import load_dotenv
from src.schemas import Fact

load_dotenv()
logger = logging.getLogger(__name__)

class FactEmbedder:
    """
    Embeds fact claims into high-dimensional dense vectors for semantic comparison.
    Prioritizes Google's neural embedding API (models/gemini-embedding-001, 3072-dim)
    when GOOGLE_API_KEY is available, with an automatic, pure-NumPy subword/n-gram
    hash projection fallback (384-dim) requiring zero external C++/runtime dependencies.
    """

    def __init__(self, dim: int = 3072):
        self.dim = dim
        self.api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        self.use_torch = os.getenv("USE_TORCH_EMBEDDINGS", "0") == "1"
        self._torch_model = None
        self._cache: Dict[str, List[float]] = {}
        self.batch_size = 16

    def _get_torch_model(self):
        """Lazily loads sentence-transformers if torch is explicitly enabled."""
        if self._torch_model is None and self.use_torch:
            try:
                from sentence_transformers import SentenceTransformer
                self._torch_model = SentenceTransformer('all-MiniLM-L6-v2')
            except Exception:
                self._torch_model = False
        return self._torch_model

    def embed_text(self, text: str) -> List[float]:
        """
        Embeds a single string into a normalized dense vector.
        """
        if not text:
            return [0.0] * self.dim

        if text in self._cache:
            return self._cache[text]

        # 1. Google Gemini Neural Embeddings (if API key available)
        if self.api_key:
            emb = self._call_gemini_embed(text)
            if emb:
                self._cache[text] = emb
                return emb

        # 2. PyTorch / sentence-transformers (if explicitly enabled)
        if self.use_torch:
            model = self._get_torch_model()
            if model:
                emb = model.encode(text).tolist()
                self._cache[text] = emb
                return emb

        # 3. Pure-NumPy subword & character n-gram projection fallback
        emb = self._numpy_hash_embed(text)
        self._cache[text] = emb
        return emb

    def _call_gemini_embed(self, text: str) -> Optional[List[float]]:
        """Call Gemini REST embedding endpoint."""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-001:embedContent?key={self.api_key}"
        payload = {
            "model": "models/gemini-embedding-001",
            "content": {"parts": [{"text": text[:2000]}]}
        }
        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=4) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                values = result.get("embedding", {}).get("values")
                if values:
                    # L2 normalize
                    arr = np.array(values, dtype=np.float32)
                    norm = float(np.linalg.norm(arr))
                    if norm > 0:
                        arr = arr / norm
                    return arr.tolist()
        except Exception as e:
            logger.debug(f"Gemini single embed failed: {e}")
        return None

    def _call_gemini_batch_embed(self, texts: List[str]) -> Optional[List[List[float]]]:
        """Call Gemini batch embedding endpoint for high-throughput batching."""
        if not self.api_key or not texts:
            return None

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-001:batchEmbedContents?key={self.api_key}"
        requests_payload = [
            {"model": "models/gemini-embedding-001", "content": {"parts": [{"text": t[:2000]}]}}
            for t in texts
        ]
        payload = {"requests": requests_payload}

        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=12) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                embeddings_data = result.get("embeddings", [])
                out = []
                for item in embeddings_data:
                    values = item.get("values")
                    if values:
                        arr = np.array(values, dtype=np.float32)
                        norm = float(np.linalg.norm(arr))
                        if norm > 0:
                            arr = arr / norm
                        out.append(arr.tolist())
                    else:
                        out.append(self._numpy_hash_embed(texts[len(out)]))
                return out
        except Exception as e:
            logger.warning(f"Gemini batch embed failed: {e}. Falling back to per-item/offline.")
            return None

    def _numpy_hash_embed(self, text: str, dim: Optional[int] = None) -> List[float]:
        """
        Fast subword & character n-gram semantic hash projection in pure NumPy.
        Produces normalized vectors where similar phrasing yields high cosine similarity,
        and unrelated topics yield near-zero similarity.
        """
        target_dim = dim or self.dim
        if not text:
            return [0.0] * target_dim

        clean_text = text.lower().strip()
        tokens = re.findall(r'\b\w+\b', clean_text)
        vec = np.zeros(target_dim, dtype=np.float32)

        for tok in tokens:
            h1 = hash(tok) % target_dim
            h2 = hash(tok + "_alt") % target_dim
            vec[h1] += 1.0
            vec[h2] += 0.5

        if len(clean_text) >= 3:
            for i in range(len(clean_text) - 2):
                ng = clean_text[i:i+3]
                h = hash(ng) % target_dim
                vec[h] += 0.35

        if len(clean_text) >= 4:
            for i in range(len(clean_text) - 3):
                ng = clean_text[i:i+4]
                h = hash(ng) % target_dim
                vec[h] += 0.25

        norm = float(np.linalg.norm(vec))
        if norm > 0.0:
            vec = vec / norm
        return vec.tolist()

    def embed(self, facts: List[Fact]) -> List[Fact]:
        """
        Embeds a list of facts, populating their embedding field.
        Uses batching for high efficiency.
        """
        if not facts:
            return facts

        uncached_facts = [f for f in facts if f.claim not in self._cache]

        # Batch embed uncached facts if using Gemini
        if self.api_key and uncached_facts:
            for i in range(0, len(uncached_facts), self.batch_size):
                batch = uncached_facts[i:i + self.batch_size]
                texts = [f.claim for f in batch]
                batch_embs = self._call_gemini_batch_embed(texts)
                if batch_embs and len(batch_embs) == len(batch):
                    for f, emb in zip(batch, batch_embs):
                        self._cache[f.claim] = emb
                else:
                    # On rate limit (429) or batch failure, immediately fall back to high-speed numpy projection
                    for f in batch:
                        self._cache[f.claim] = self._numpy_hash_embed(f.claim)

        for fact in facts:
            if fact.embedding is None:
                fact.embedding = self.embed_text(fact.claim)

        return facts

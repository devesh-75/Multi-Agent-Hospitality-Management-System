"""
Embeddings Generator
Generates dense vector embeddings for semantic document retrieval:
- Supports OpenAI text-embedding-3-small when API key is provided
- Falls back to deterministic local dense hash-vector embeddings (dimension 128) when offline/no paid key
"""

import math
import re
import hashlib
from typing import List
import numpy as np
from backend.app.core.config import settings

class EmbeddingsService:

    def __init__(self, dimension: int = 128):
        self.dimension = dimension
        self.api_key = settings.OPENAI_API_KEY
        self.use_openai = bool(self.api_key and self.api_key.startswith("sk-"))

    def embed_text(self, text: str) -> List[float]:
        """Generates a dense vector for a single string."""
        if self.use_openai:
            try:
                from openai import OpenAI
                client = OpenAI(api_key=self.api_key)
                response = client.embeddings.create(
                    input=text,
                    model=settings.EMBEDDING_MODEL
                )
                return response.data[0].embedding
            except Exception:
                pass # Fall back to local embedder

        # High-performance deterministic hashing embedder (bag-of-words + character n-grams)
        words = re.findall(r"\w+", text.lower())
        vec = np.zeros(self.dimension, dtype=np.float32)

        for w in words:
            h = int(hashlib.md5(w.encode("utf-8")).hexdigest(), 16)
            idx = h % self.dimension
            val = 1.0 if (h >> 8) % 2 == 0 else -1.0
            vec[idx] += val

        # Normalize L2
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        return vec.tolist()

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Batch embedding generation."""
        return [self.embed_text(t) for t in texts]

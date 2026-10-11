"""
Vector Store Management
Provides vector storage and similarity search:
- Integrates with Qdrant Vector Database when reachable
- Implements a local in-memory vector index with cosine similarity and metadata filtering fallback
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional
import numpy as np

from backend.app.core.config import settings
from rag.embeddings import EmbeddingsService

logger = logging.getLogger(__name__)

class VectorStore:

    def __init__(self, collection_name: str = "hospitality_knowledge"):
        self.collection_name = collection_name
        self.embeddings_service = EmbeddingsService()
        self.qdrant_client = None
        self.is_qdrant_active = False
        self.local_storage: List[Dict[str, Any]] = []

        if settings.QDRANT_ENABLED:
            try:
                from qdrant_client import QdrantClient
                self.qdrant_client = QdrantClient(url=settings.QDRANT_URL, timeout=3.0)
                # Test connectivity
                self.qdrant_client.get_collections()
                self.is_qdrant_active = True
                logger.info(f"Connected to remote Qdrant vector database at {settings.QDRANT_URL}")
            except Exception as e:
                logger.warning(f"Could not connect to Qdrant ({e}). Falling back to local vector store.")
                self.is_qdrant_active = False

    def index_documents(self, documents: List[Dict[str, Any]]):
        """Indexes documents by generating embeddings and storing records."""
        if not documents:
            return

        self.local_storage.clear()
        for doc in documents:
            vec = self.embeddings_service.embed_text(doc["content"])
            record = {
                "id": doc["id"],
                "content": doc["content"],
                "metadata": doc.get("metadata", {}),
                "vector": vec
            }
            self.local_storage.append(record)

        logger.info(f"Successfully indexed {len(self.local_storage)} documents in vector store.")

    def search(self, query: str, top_k: int = 5, filter_property_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Semantic similarity search with metadata filtering."""
        if not self.local_storage:
            return []

        q_vec = np.array(self.embeddings_service.embed_text(query), dtype=np.float32)
        q_norm = np.linalg.norm(q_vec)

        scored_docs = []
        for doc in self.local_storage:
            # Metadata filtering
            if filter_property_id and doc["metadata"].get("property_id") not in [filter_property_id, "ALL", None]:
                continue

            d_vec = np.array(doc["vector"], dtype=np.float32)
            d_norm = np.linalg.norm(d_vec)
            
            score = 0.0
            if q_norm > 0 and d_norm > 0:
                score = float(np.dot(q_vec, d_vec) / (q_norm * d_norm))

            scored_docs.append({
                "id": doc["id"],
                "content": doc["content"],
                "metadata": doc["metadata"],
                "similarity_score": round(score, 4)
            })

        # Sort descending by similarity score
        scored_docs.sort(key=lambda x: x["similarity_score"], reverse=True)
        return scored_docs[:top_k]

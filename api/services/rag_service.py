"""
RAG service that wraps piragi for use in API routes.
"""
from typing import Optional


class RAGService:
    """Service for RAG operations using piragi."""
    
    def __init__(self):
        self._ragi = None
    
    async def initialize(self, config: Optional[dict] = None):
        """Initialize the RAGI instance."""
        # TODO: Initialize piragi
        # from lib.piragi import RAGI
        # self._ragi = RAGI(...)
        pass
    
    async def search(self, query: str, top_k: int = 5) -> list[dict]:
        """Search the knowledge base."""
        if not self._ragi:
            return []
        # return self._ragi.search(query, top_k=top_k)
        return []
    
    async def add_documents(self, documents: list[str], metadata: Optional[list[dict]] = None):
        """Add documents to the knowledge base."""
        if not self._ragi:
            return
        # self._ragi.add(documents, metadata=metadata)


# Singleton instance
rag_service = RAGService()

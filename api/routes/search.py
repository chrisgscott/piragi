from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


class SearchResult(BaseModel):
    content: str
    score: float
    metadata: dict


class SearchResponse(BaseModel):
    results: list[SearchResult]
    query: str


@router.post("/", response_model=SearchResponse)
async def search(request: SearchRequest):
    """
    Search the knowledge base using piragi RAG.
    """
    # TODO: Implement with piragi
    # from lib.piragi import RAGI
    # ragi = RAGI(...)
    # results = ragi.search(request.query, top_k=request.top_k)
    
    return SearchResponse(
        query=request.query,
        results=[]  # Placeholder
    )

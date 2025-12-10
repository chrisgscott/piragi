#!/usr/bin/env python3
"""Test AsyncRagi with FastAPI endpoints."""

import asyncio
import os
from pathlib import Path
from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.piragi import AsyncRagi

# Initialize FastAPI app
app = FastAPI(title="AsyncRagi Test API")

# Global AsyncRagi instance
kb = None


class QueryRequest(BaseModel):
    query: str
    top_k: int = 5


class AddRequest(BaseModel):
    sources: List[str]


class AnswerResponse(BaseModel):
    answer: str
    citations: List[dict]


@app.on_event("startup")
async def startup():
    """Initialize AsyncRagi on startup."""
    global kb
    
    # Create a test directory with some sample content
    test_dir = Path("./test_docs")
    test_dir.mkdir(exist_ok=True)
    
    # Add a sample document if it doesn't exist
    sample_file = test_dir / "sample.txt"
    if not sample_file.exists():
        sample_file.write_text("""
        AsyncRagi Test Document
        
        This is a test document for the AsyncRagi FastAPI integration.
        
        Key features:
        - Async support for web frameworks
        - Non-blocking operations
        - Progress tracking with async iterators
        - Knowledge graph capabilities
        
        Usage examples:
        1. Use with FastAPI for high-performance web APIs
        2. Integrate with aiohttp for async web servers
        3. Works with Starlette applications
        
        The async wrapper uses asyncio.to_thread() to run synchronous
        operations in a thread pool, making it non-blocking.
        """)
    
    # Initialize AsyncRagi with local GPT-OSS
    kb = AsyncRagi(
        sources=str(test_dir),
        config={
            "llm": {
                "model": "gpt-oss",  # Use local GPT-OSS
                "base_url": "http://localhost:11434/v1"  # Ollama endpoint
            },
            "embedding": {"model": "all-MiniLM-L6-v2"}
        }
    )
    await kb.add(str(test_dir))
    print("AsyncRagi initialized and documents loaded!")


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "healthy", "message": "AsyncRagi FastAPI test server"}


@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QueryRequest):
    """Ask a question and get an answer with citations."""
    if not kb:
        raise HTTPException(status_code=500, detail="Knowledge base not initialized")
    
    try:
        answer = await kb.ask(request.query, top_k=request.top_k)
        return AnswerResponse(
            answer=answer.text,
            citations=[{"text": c.chunk, "source": c.source, "score": c.score} for c in answer.citations]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/add")
async def add_documents(request: AddRequest):
    """Add documents to the knowledge base."""
    if not kb:
        raise HTTPException(status_code=500, detail="Knowledge base not initialized")
    
    try:
        await kb.add(request.sources)
        return {"status": "success", "message": f"Added {len(request.sources)} sources"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/add-with-progress")
async def add_documents_with_progress(request: AddRequest):
    """Add documents with progress tracking."""
    if not kb:
        raise HTTPException(status_code=500, detail="Knowledge base not initialized")
    
    async def stream_progress():
        try:
            async for msg in kb.add(request.sources, progress=True):
                yield f"data: {msg}\n\n"
            yield "data: DONE\n\n"
        except Exception as e:
            yield f"data: ERROR: {e}\n\n"
    
    from fastapi.responses import StreamingResponse
    return StreamingResponse(
        stream_progress(),
        media_type="text/plain",
        headers={"Cache-Control": "no-cache"}
    )


@app.get("/count")
async def get_document_count():
    """Get the number of chunks in the knowledge base."""
    if not kb:
        raise HTTPException(status_code=500, detail="Knowledge base not initialized")
    
    count = await kb.count()
    return {"count": count}


@app.get("/retrieve")
async def retrieve_documents(query: str, top_k: int = 5):
    """Retrieve relevant documents without LLM generation."""
    if not kb:
        raise HTTPException(status_code=500, detail="Knowledge base not initialized")
    
    try:
        citations = await kb.retrieve(query, top_k=top_k)
        return {
            "citations": [
                {"text": c.chunk, "source": c.source, "score": c.score}
                for c in citations
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    print("Starting AsyncRagi FastAPI test server...")
    print("Available endpoints:")
    print("  GET  /           - Health check")
    print("  POST /ask        - Ask questions")
    print("  POST /add        - Add documents")
    print("  POST /add-with-progress - Add with progress streaming")
    print("  GET  /count      - Document count")
    print("  GET  /retrieve   - Retrieve documents")
    print("\nTest with:")
    print('  curl -X POST "http://localhost:8000/ask" -H "Content-Type: application/json" -d \'{"query": "What is AsyncRagi?"}\'')
    
    uvicorn.run(app, host="0.0.0.0", port=8000)

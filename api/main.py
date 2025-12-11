from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import health, search, agents

app = FastAPI(
    title="Piragi RAG API",
    description="API for RAG-powered search and AI agents",
    version="0.1.0",
)

# CORS configuration for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, tags=["health"])
app.include_router(search.router, prefix="/api/search", tags=["search"])
app.include_router(agents.router, prefix="/api/agents", tags=["agents"])


@app.get("/")
async def root():
    return {"message": "Piragi RAG API", "docs": "/docs"}

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.session import init_db
from app.routers import (
    health,
    chat,
    conversations,
    documents,
    workspace,
    search,
    audio,
    uploads
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize database tables and extensions
    print("[Startup] Initializing database tables and extensions...")
    await init_db()
    print("[Startup] Database ready.")
    yield
    print("[Shutdown] Cleaning up resources...")


app = FastAPI(
    title="Multimodal AI Chatbot MVP API",
    description="Full-stack Multimodal AI Companion with RAG, Vision, Audio, Web Search, and Document Editing.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Routers
app.include_router(health.router)
app.include_router(chat.router)
app.include_router(conversations.router)
app.include_router(documents.router)
app.include_router(workspace.router)
app.include_router(search.router)
app.include_router(audio.router)
app.include_router(uploads.router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to Multimodal AI Chatbot MVP API",
        "docs_url": "/docs",
        "health_url": "/api/health"
    }

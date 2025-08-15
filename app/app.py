"""FastAPI web application for RAG system."""
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Dict, Any

from src.config import PERSIST_DIR, TOP_K
from src.store import get_client, get_or_create_collection
from src.rag import retrieve_and_answer

app = FastAPI(title="Local RAG System", version="1.0.0")

# Mount static files and templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Initialize vector store
client = get_client(PERSIST_DIR)
collection = get_or_create_collection(client)

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str
    sources: List[Dict[str, Any]]

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the main chat interface."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """Answer a question using the RAG system."""
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    try:
        answer, sources = retrieve_and_answer(request.question, collection, TOP_K)
        return AnswerResponse(answer=answer, sources=sources)
    except Exception as e:
        # Log the full error for debugging
        import traceback
        print(f"Error in /ask endpoint: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@app.get("/favicon.ico")
async def favicon():
    """Serve favicon to avoid 404 errors."""
    from fastapi.responses import FileResponse
    return FileResponse("app/static/favicon.ico")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

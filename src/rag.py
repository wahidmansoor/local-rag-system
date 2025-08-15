"""High-level RAG orchestration."""
import os
import uuid
import time
from pathlib import Path
from typing import List, Tuple, Dict, Any
import pypdf

from src.chunking import split_into_chunks
from src.embeddings import embed_texts
from src.store import add_texts
from src.llm import chat
from src.prompt import build_system_prompt, build_user_prompt, render_messages
from src.config import MAX_CHARS, OVERLAP

def ingest_path(
    file_path: str,
    collection,
    max_chars: int = MAX_CHARS,
    overlap: int = OVERLAP
) -> int:
    """
    Ingest a single file (PDF, TXT, MD) into the vector store.
    
    Args:
        file_path: Path to the file to ingest
        collection: ChromaDB collection
        max_chars: Maximum characters per chunk
        overlap: Overlap between chunks
    
    Returns:
        Number of chunks added
    """
    path = Path(file_path)
    
    # Read file content based on extension
    if path.suffix.lower() == '.pdf':
        text = _read_pdf(file_path)
    elif path.suffix.lower() in ['.txt', '.md']:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        print(f"Skipping unsupported file type: {file_path}")
        return 0
    
    if not text.strip():
        print(f"No text content found in: {file_path}")
        return 0
    
    # Split into chunks
    chunks = split_into_chunks(text, max_chars, overlap)
    
    if not chunks:
        print(f"No chunks generated from: {file_path}")
        return 0
    
    # Generate embeddings with retry
    print(f"Generating embeddings for {len(chunks)} chunks from {path.name}")
    embeddings = _embed_with_retry(chunks, max_retries=3)
    
    if not embeddings:
        print(f"Failed to generate embeddings for: {file_path}")
        return 0
    
    # Generate stable IDs based on content
    ids = []
    metadatas = []
    
    for i, chunk in enumerate(chunks):
        # Create stable ID based on file and chunk content hash
        chunk_hash = str(hash(chunk))[-8:]
        chunk_id = f"{path.stem}_{i:03d}_{chunk_hash}"
        ids.append(chunk_id)
        metadatas.append({
            "source": path.name,
            "chunk": i + 1,
            "total_chunks": len(chunks),
            "file_path": str(path)
        })
    
    # Add to vector store
    try:
        add_texts(collection, ids, chunks, metadatas, embeddings)
        return len(chunks)
    except Exception as e:
        print(f"Failed to add chunks to store: {e}")
        return 0

def retrieve_and_answer(
    question: str,
    collection,
    k: int = 5
) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Retrieve relevant chunks and generate an answer.
    
    Args:
        question: User's question
        collection: ChromaDB collection
        k: Number of chunks to retrieve
    
    Returns:
        Tuple of (answer, sources)
    """
    from src.store import query
    
    # Retrieve relevant chunks
    contexts = query(collection, question, k)
    
    if not contexts:
        return "No relevant information found in the knowledge base.", []
    
    # Build prompts
    system_prompt = build_system_prompt()
    user_prompt = build_user_prompt(question, contexts)
    messages = render_messages(system_prompt, user_prompt)
    
    # Generate answer
    answer = chat(messages)
    
    # Prepare sources for return
    sources = []
    for i, (text, metadata) in enumerate(contexts, 1):
        sources.append({
            "source": metadata.get('source', 'Unknown'),
            "chunk": metadata.get('chunk', i),
            "text": text[:200] + "..." if len(text) > 200 else text
        })
    
    return answer, sources

def _embed_with_retry(chunks: List[str], max_retries: int = 3) -> List[List[float]]:
    """Generate embeddings with retry logic."""
    for attempt in range(max_retries):
        try:
            return embed_texts(chunks)
        except Exception as e:
            print(f"Embedding attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                print(f"Failed to generate embeddings after {max_retries} attempts")
                return []

def _read_pdf(file_path: str) -> str:
    """Read text content from a PDF file."""
    try:
        with open(file_path, 'rb') as file:
            reader = pypdf.PdfReader(file)
            text_parts = []
            
            for page in reader.pages:
                text_parts.append(page.extract_text())
            
            return "\n".join(text_parts)
    except Exception as e:
        print(f"Error reading PDF {file_path}: {e}")
        return ""

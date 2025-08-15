"""ChromaDB vector store operations."""
import chromadb
from typing import List, Tuple, Dict, Any
from src.config import PERSIST_DIR
from src.embeddings import embed_texts

def get_client(persist_dir: str = None) -> chromadb.PersistentClient:
    """Get ChromaDB persistent client."""
    if persist_dir is None:
        persist_dir = PERSIST_DIR
    
    return chromadb.PersistentClient(path=persist_dir)

def get_or_create_collection(client: chromadb.PersistentClient, name: str = "rag_docs"):
    """Get or create a collection in ChromaDB."""
    return client.get_or_create_collection(name=name)

def add_texts(
    collection,
    ids: List[str],
    documents: List[str],
    metadatas: List[Dict[str, Any]],
    embeddings: List[List[float]]
):
    """Add texts with embeddings to the collection with validation."""
    # Validate inputs
    if not all(len(arr) == len(ids) for arr in [documents, metadatas, embeddings]):
        raise ValueError("All input arrays must have the same length")
    
    if not ids:
        raise ValueError("No documents to add")
    
    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings
    )

def query(collection, query_text: str, k: int = 5) -> List[Tuple[str, Dict[str, Any]]]:
    """
    Query the collection for similar documents.
    
    Args:
        collection: ChromaDB collection
        query_text: Query string
        k: Number of results to return
    
    Returns:
        List of (document_text, metadata) tuples
    """
    if not query_text.strip():
        return []
    
    # Limit k to reasonable range
    k = max(1, min(20, k))
    
    try:
        # Generate embedding for query
        query_embedding = embed_texts([query_text])[0]
        
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )
        
        # Extract documents and metadatas
        documents = results['documents'][0] if results['documents'] else []
        metadatas = results['metadatas'][0] if results['metadatas'] else []
        
        return list(zip(documents, metadatas))
    
    except Exception as e:
        print(f"Query error: {e}")
        return []

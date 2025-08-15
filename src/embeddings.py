"""Embedding generation using Ollama."""
import requests
from typing import List
from src.config import OLLAMA_URL, EMBED_MODEL

def embed_texts(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for a list of texts using Ollama.
    
    Args:
        texts: List of text strings to embed
    
    Returns:
        List of embedding vectors
    """
    if not texts:
        return []
    
    url = f"{OLLAMA_URL}/api/embeddings"
    embeddings = []
    
    try:
        # Process each text individually for compatibility
        for text in texts:
            response = requests.post(
                url,
                json={
                    "model": EMBED_MODEL,
                    "prompt": text
                },
                timeout=120
            )
            response.raise_for_status()
            
            data = response.json()
            
            # Handle both 'embedding' and 'embeddings' response formats
            if 'embedding' in data and data['embedding']:
                embeddings.append(data['embedding'])
            elif 'embeddings' in data and data['embeddings']:
                embeddings.append(data['embeddings'])
            else:
                raise ValueError(f"No embedding returned for text: {text[:50]}...")
        
        return embeddings
            
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to generate embeddings: {e}")
    except (KeyError, ValueError) as e:
        raise RuntimeError(f"Invalid embedding response: {e}")

"""Text chunking utilities with sentence-aware splitting."""
import nltk
from typing import List

# Try to download punkt tokenizer data if not available
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    try:
        print("Downloading NLTK punkt tokenizer data...")
        nltk.download('punkt', quiet=True)
    except Exception as e:
        print(f"Warning: Could not download NLTK data: {e}")

def split_into_chunks(text: str, max_chars: int = 1100, overlap: int = 200) -> List[str]:
    """
    Split text into chunks with sentence awareness and overlap.
    
    Args:
        text: Input text to chunk
        max_chars: Maximum characters per chunk
        overlap: Number of characters to overlap between chunks
    
    Returns:
        List of text chunks
    """
    if not text.strip():
        return []
    
    chunks = []
    
    try:
        # Try sentence-aware splitting
        sentences = nltk.sent_tokenize(text)
        
        current_chunk = ""
        
        for sentence in sentences:
            # If adding this sentence would exceed max_chars, save current chunk
            if len(current_chunk) + len(sentence) > max_chars and current_chunk:
                chunks.append(current_chunk.strip())
                
                # Start new chunk with overlap from previous chunk
                if overlap > 0:
                    current_chunk = current_chunk[-overlap:] + " " + sentence
                else:
                    current_chunk = sentence
            else:
                # Add sentence to current chunk
                if current_chunk:
                    current_chunk += " " + sentence
                else:
                    current_chunk = sentence
        
        # Add final chunk if it exists
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
            
    except LookupError:
        # Fallback to raw character slicing if NLTK data not available
        print("Warning: NLTK punkt tokenizer not available, using fallback slicing")
        chunks = _fallback_chunk(text, max_chars, overlap)
    
    return chunks

def _fallback_chunk(text: str, max_chars: int, overlap: int) -> List[str]:
    """Fallback chunking using raw character slicing."""
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + max_chars
        chunk = text[start:end]
        
        if chunk.strip():
            chunks.append(chunk.strip())
        
        # Move start position with overlap consideration
        start = end - overlap if end < len(text) else len(text)
        
        if start >= len(text):
            break
    
    return chunks

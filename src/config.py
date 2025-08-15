"""Configuration management for RAG system."""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Ollama configuration
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")

# Model configuration
EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text")
CHAT_MODEL = os.getenv("CHAT_MODEL", "qwen2.5")

# Storage configuration
PERSIST_DIR = os.getenv("PERSIST_DIR", "vectorstore")

# Retrieval configuration with security validation
_top_k = int(os.getenv("TOP_K", "5"))
TOP_K = max(1, min(10, _top_k))  # Limit TOP_K to 1-10 range

# Chunking configuration
MAX_CHARS = int(os.getenv("MAX_CHARS", "1100"))
OVERLAP = int(os.getenv("OVERLAP", "200"))

def get_safe_config_summary() -> dict:
    """Get configuration summary without sensitive values."""
    return {
        "embed_model": EMBED_MODEL,
        "chat_model": CHAT_MODEL,
        "top_k": TOP_K,
        "max_chars": MAX_CHARS,
        "overlap": OVERLAP,
        "persist_dir": PERSIST_DIR
    }

"""Integration tests for the full RAG system."""
import pytest
import tempfile
import os
from pathlib import Path

def test_system_health():
    """Test that all modules can be imported successfully."""
    try:
        from src import config, chunking, embeddings, store, llm, prompt, rag
        print("✅ All modules imported successfully")
        assert True
    except ImportError as e:
        pytest.fail(f"Module import failed: {e}")

def test_config_loading():
    """Test that configuration loads without errors."""
    from src.config import get_safe_config_summary
    
    config_summary = get_safe_config_summary()
    assert isinstance(config_summary, dict)
    assert "embed_model" in config_summary
    assert "chat_model" in config_summary

def test_chunking_basic():
    """Test basic chunking functionality."""
    from src.chunking import split_into_chunks
    
    text = "This is a test sentence. This is another test sentence."
    chunks = split_into_chunks(text, max_chars=30, overlap=5)
    assert len(chunks) >= 1
    assert all(isinstance(chunk, str) for chunk in chunks)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
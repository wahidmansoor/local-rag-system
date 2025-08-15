"""Tests for the RAG system integration."""
import pytest
import tempfile
import os
from pathlib import Path

from src.config import PERSIST_DIR
from src.store import get_client, get_or_create_collection
from src.rag import ingest_path, retrieve_and_answer
from src.chunking import split_into_chunks


class TestRAGIntegration:
    
    def test_chunking_integration(self):
        """Test that chunking works with various text types."""
        # Test short text
        short_text = "This is a short text."
        chunks = split_into_chunks(short_text, max_chars=50, overlap=10)
        assert len(chunks) == 1
        assert chunks[0] == short_text
        
        # Test long text with sentences
        long_text = "First sentence. Second sentence. Third sentence. Fourth sentence."
        chunks = split_into_chunks(long_text, max_chars=30, overlap=5)
        assert len(chunks) >= 2
        assert all(len(chunk) <= 35 for chunk in chunks)  # Allow some flexibility
    
    def test_empty_inputs(self):
        """Test handling of empty inputs."""
        assert split_into_chunks("") == []
        assert split_into_chunks("   ") == []
        assert split_into_chunks("\n\n") == []
    
    def test_sample_document_ingestion(self):
        """Test ingesting a sample text document."""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("This is a test document. It contains multiple sentences. Each sentence provides some information.")
            temp_file = f.name
        
        try:
            # Use temporary directory for testing
            with tempfile.TemporaryDirectory() as temp_dir:
                client = get_client(temp_dir)
                collection = get_or_create_collection(client, "test_collection")
                
                # Test ingestion
                chunks_added = ingest_path(temp_file, collection)
                assert chunks_added > 0
                
        finally:
            # Clean up
            os.unlink(temp_file)
    
    def test_markdown_file_support(self):
        """Test that markdown files are supported."""
        markdown_content = """# Test Document
        
        This is a **test** markdown document.
        
        ## Section 1
        
        Some content here.
        
        ## Section 2
        
        More content here.
        """
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(markdown_content)
            temp_file = f.name
        
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                client = get_client(temp_dir)
                collection = get_or_create_collection(client, "test_md")
                
                chunks_added = ingest_path(temp_file, collection)
                assert chunks_added > 0
                
        finally:
            os.unlink(temp_file)


if __name__ == '__main__':
    pytest.main([__file__])

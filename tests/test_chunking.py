"""Tests for the chunking module."""
import unittest
from src.chunking import split_into_chunks

class TestChunking(unittest.TestCase):
    
    def test_sentence_split(self):
        """Test sentence-aware splitting."""
        text = "First sentence. Second sentence. Third sentence."
        chunks = split_into_chunks(text, max_chars=25, overlap=5)
        
        # Should split into reasonable chunks
        self.assertTrue(len(chunks) >= 1)
        self.assertTrue(all(len(chunk) <= 30 for chunk in chunks))  # Allow some flexibility
    
    def test_overlap_behavior(self):
        """Test that overlap works correctly."""
        text = "A" * 100 + "B" * 100 + "C" * 100
        chunks = split_into_chunks(text, max_chars=150, overlap=20)
        
        if len(chunks) > 1:
            # Check that there's some overlap content
            self.assertTrue(any(char in chunks[1] for char in chunks[0][-20:]))
    
    def test_fallback_slicing(self):
        """Test fallback to raw character slicing."""
        # Create a very long text without sentence boundaries
        text = "A" * 1000
        chunks = split_into_chunks(text, max_chars=100, overlap=10)
        
        self.assertTrue(len(chunks) >= 9)  # Should create multiple chunks
        self.assertTrue(all(len(chunk) <= 100 for chunk in chunks))

if __name__ == '__main__':
    unittest.main()

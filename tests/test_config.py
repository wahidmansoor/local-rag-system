"""Tests for configuration module."""
import unittest
import os
from unittest.mock import patch

class TestConfig(unittest.TestCase):
    
    def test_default_values(self):
        """Test that default configuration values are set correctly."""
        from src import config
        
        # Test defaults when no environment variables are set
        self.assertEqual(config.OLLAMA_URL, "http://127.0.0.1:11434")
        self.assertEqual(config.EMBED_MODEL, "nomic-embed-text")
        self.assertEqual(config.CHAT_MODEL, "qwen2.5")
        self.assertEqual(config.PERSIST_DIR, "vectorstore")
        self.assertTrue(1 <= config.TOP_K <= 10)
        self.assertEqual(config.MAX_CHARS, 1100)
        self.assertEqual(config.OVERLAP, 200)
    
    @patch.dict(os.environ, {'TOP_K': '15'})
    def test_top_k_security_limit(self):
        """Test that TOP_K is limited to safe range."""
        # Need to reload config to pick up environment changes
        import importlib
        from src import config
        importlib.reload(config)
        
        # Should be clamped to maximum of 10
        self.assertEqual(config.TOP_K, 10)
    
    @patch.dict(os.environ, {'TOP_K': '0'})
    def test_top_k_minimum_limit(self):
        """Test that TOP_K has minimum of 1."""
        import importlib
        from src import config
        importlib.reload(config)
        
        # Should be clamped to minimum of 1
        self.assertEqual(config.TOP_K, 1)
    
    def test_safe_config_summary(self):
        """Test that config summary doesn't expose sensitive values."""
        from src.config import get_safe_config_summary
        
        summary = get_safe_config_summary()
        
        # Should contain expected keys
        expected_keys = {"embed_model", "chat_model", "top_k", "max_chars", "overlap", "persist_dir"}
        self.assertEqual(set(summary.keys()), expected_keys)
        
        # Should not contain URL or other sensitive info
        self.assertNotIn("ollama_url", summary)
        self.assertNotIn("url", summary)


if __name__ == '__main__':
    unittest.main()

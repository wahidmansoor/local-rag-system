"""LLM interaction using Ollama chat API."""
import requests
from typing import List, Dict
from src.config import OLLAMA_URL, CHAT_MODEL

def chat(messages: List[Dict[str, str]]) -> str:
    """
    Send chat messages to Ollama and get response.
    
    Args:
        messages: List of message dictionaries with 'role' and 'content'
    
    Returns:
        Response text from the model
    """
    import json
    
    url = f"{OLLAMA_URL}/api/chat"
    
    try:
        # Use streaming mode since non-streaming appears to hang
        response = requests.post(
            url,
            json={
                "model": CHAT_MODEL,
                "messages": messages,
                "stream": True
            },
            timeout=60,
            stream=True
        )
        response.raise_for_status()
        
        # Collect the streaming response
        content_parts = []
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode())
                    if isinstance(data, dict) and 'message' in data:
                        if 'content' in data['message']:
                            content_parts.append(data['message']['content'])
                        if data.get('done', False):
                            break
                except json.JSONDecodeError:
                    # Skip lines that aren't valid JSON
                    continue
        
        return ''.join(content_parts)
            
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to get chat response: {e}")
    except Exception as e:
        raise RuntimeError(f"Error processing chat response: {e}")

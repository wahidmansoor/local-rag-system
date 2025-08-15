"""Prompt building utilities."""
from typing import List, Tuple, Dict

def build_system_prompt() -> str:
    """Build system prompt with safety and grounding instructions."""
    return """You are a helpful assistant that answers questions based only on the provided context. 
Always cite your sources using the numbered references provided in the context. 
If you cannot answer the question based on the given context, say so clearly.
Do not make up information that is not present in the context."""

def build_user_prompt(question: str, contexts: List[Tuple[str, Dict]]) -> str:
    """
    Build user prompt with question and numbered context citations.
    
    Args:
        question: User's question
        contexts: List of (text, metadata) tuples from retrieval
    
    Returns:
        Formatted prompt string
    """
    prompt_parts = [f"Question: {question}", "", "Context:"]
    
    for i, (text, metadata) in enumerate(contexts, 1):
        source = metadata.get('source', 'Unknown')
        chunk_num = metadata.get('chunk', 'N/A')
        
        prompt_parts.append(f"[{i}] From: {source} (chunk {chunk_num})")
        prompt_parts.append(f"    {text}")
        prompt_parts.append("")
    
    return "\n".join(prompt_parts)

def render_messages(system: str, user: str) -> List[Dict[str, str]]:
    """Render system and user prompts into message format."""
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user}
    ]

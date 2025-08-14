"""  
Author: Akshay NS
Contains: Provider for llm clients

"""

from langchain_ollama import ChatOllama
from typing import Dict


_llm_cache: Dict[str, ChatOllama] = {}

def get_llm(model_name: str, temperature: float = 0.1, max_tokens: int = 1000) -> ChatOllama:
    """returns a cached LLM instance if available, otherwise creates a new one.

    Args:
        model_name (str): _description_
        temperature (float, optional): _description_. Defaults to 0.1.
        max_tokens (int, optional): _description_. Defaults to 1000.

    Returns:
        ChatOllama: Configured LLM instance.
    """
    
    if model_name not in _llm_cache:
        llm =ChatOllama(
            model=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            base_url="http://localhost:11434",  # Explicit Ollama server URL
        )
        _llm_cache[model_name] = llm
        
    return _llm_cache[model_name]
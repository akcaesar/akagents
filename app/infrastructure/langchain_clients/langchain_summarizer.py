"""  
Author: Akshay NS
Contains: Summarization with langchain

"""
import sys, os

from langchain_ollama import ChatOllama

# Add project root to Python path when running directly
if __name__ == "__main__" or __name__ == "__mp_main__":
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
    sys.path.insert(0, project_root)

from app.domain.services.summarization_service import SummarizationService
from app.infrastructure.llm.factory import get_llm


def setup_llm(model_name: str) -> ChatOllama:
    llm = get_llm(model_name)
    return llm

class LangchainSummarizer(SummarizationService):
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.llm = setup_llm(model_name)

    def summarize(self, text: str|None) -> str:
        messages = [
            ("system", "You are a helpful assistant that summarizes text."),
            ("human", f"Summarize the following text: {text}")
            
        ]
        ai_msg = self.llm.invoke(messages)
        return ai_msg.content if ai_msg else "Error in summarization"

        
        
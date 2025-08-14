"""
Author: Akshay NS
Contains: API Interface for summarization.

"""

from fastapi import APIRouter
from app.application.use_cases.run_summarization import RunSummarization
from app.infrastructure.ollama_clients.ollama_summarizer import OllamaSummarizer
from app.infrastructure.langchain_clients.langchain_summarizer import LangchainSummarizer


router = APIRouter()

@router.post("/summarize")
def summarize_text(text: str):
    try:
        summarizer1 = OllamaSummarizer(model_name="gemma3:1b")
        summarizer2 = LangchainSummarizer(model_name="llama3-groq-tool-use:latest")
        use_case1 = RunSummarization(summarizer1)
        use_case2 = RunSummarization(summarizer2)
        summary1 = use_case1.execute(text)
        summary2 = use_case2.execute(text)
        return {"Ollama summary": summary1, "LangChain summary": summary2}
    except Exception as e:
        return {"error": str(e)}
    
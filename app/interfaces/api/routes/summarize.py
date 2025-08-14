"""
Author: Akshay NS
Contains: API Interface for summarization.

"""

from fastapi import APIRouter
from app.application.use_cases.run_summarization import RunSummarization
from app.infrastructure.ollama_clients.ollama_summarizer import OllamaSummarizer


router = APIRouter()

@router.post("/summarize")
def summarize_text(text: str):
    try:
        summarizer = OllamaSummarizer(model_name="gemma3:1b")
        use_case = RunSummarization(summarizer)
        summary = use_case.execute(text)
        return {"summary": summary}
    except Exception as e:
        return {"error": str(e)}
    
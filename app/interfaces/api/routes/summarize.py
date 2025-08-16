"""
Author: Akshay NS
Contains: API Interface for summarization.

"""

from fastapi import APIRouter
from app.application.use_cases.run_summarization import RunSummarization
from app.infrastructure.ollama_clients.ollama_summarizer import OllamaSummarizer
from app.infrastructure.langchain_clients.langchain_summarizer import LangchainSummarizer


router = APIRouter()

from app.interfaces.metrics import (
    REQUESTS_TOTAL, RESPONSE_TIME, SUCCESS_TOTAL, 
    FAILURE_TOTAL, LENGTH_RATIO
)
import time

@router.post("/summarize")
def summarize_text(text: str):
    try:
        # Initialize models
        model1_name = "gemma3:1b"
        model2_name = "llama3-groq-tool-use:latest"
        summarizer1 = OllamaSummarizer(model_name=model1_name)
        summarizer2 = LangchainSummarizer(model_name=model2_name)
        use_case1 = RunSummarization(summarizer1)
        use_case2 = RunSummarization(summarizer2)
        
        # Track metrics for first model
        REQUESTS_TOTAL.labels(model_name=model1_name).inc()
        start_time = time.time()
        try:
            summary1 = use_case1.execute(text)
            SUCCESS_TOTAL.labels(model_name=model1_name).inc()
            LENGTH_RATIO.labels(model_name=model1_name).observe(len(summary1) / len(text))
        except Exception as e:
            FAILURE_TOTAL.labels(model_name=model1_name).inc()
            raise e
        finally:
            RESPONSE_TIME.labels(model_name=model1_name).observe(time.time() - start_time)
        
        # Track metrics for second model
        REQUESTS_TOTAL.labels(model_name=model2_name).inc()
        start_time = time.time()
        try:
            summary2 = use_case2.execute(text)
            SUCCESS_TOTAL.labels(model_name=model2_name).inc()
            LENGTH_RATIO.labels(model_name=model2_name).observe(len(summary2) / len(text))
        except Exception as e:
            FAILURE_TOTAL.labels(model_name=model2_name).inc()
            raise e
        finally:
            RESPONSE_TIME.labels(model_name=model2_name).observe(time.time() - start_time)
        
        return {"Ollama summary": summary1, "LangChain summary": summary2}
    except Exception as e:
        return {"error": str(e)}
    
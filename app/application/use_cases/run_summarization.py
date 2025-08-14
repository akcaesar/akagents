"""
Author: Akshay NS
Contains: SummarizationService class that handles the logic for summarizing text.    
    
"""

from app.domain.services.summarization_service import SummarizationService
from app.infrastructure.decorators.logging_summarizer import LoggingSummarizer

class RunSummarization:
    def __init__(self, summarizer: SummarizationService):
        self.summarizer = LoggingSummarizer(summarizer) if not isinstance(summarizer, LoggingSummarizer) else summarizer
        
    def execute(self, text:str) -> str:
        return self.summarizer.summarize(text)
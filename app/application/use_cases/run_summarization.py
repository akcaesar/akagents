"""
Author: Akshay NS
Contains: SummarizationService class that handles the logic for summarizing text.    
    
"""

from app.domain.services.summarization_service import SummarizationService

class RunSummarization:
    def __init__(self, summarizer: SummarizationService):
        self.summarizer = summarizer
        
    def execute(self, text:str) -> str:
        return self.summarizer.summarize(text)
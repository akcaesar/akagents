"""
Author: Akshay NS
Contains: abstract service for producing summaries.
        
"""

from abc import ABC, abstractmethod

class SummarizationService(ABC):
    @abstractmethod
    def summarize(self, text: str) -> str:
        pass
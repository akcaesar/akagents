"""
Author: Akshay NS
Contains: SummaryTask entity representating the act of summarizing some text.
    
"""

from dataclasses import dataclass

@dataclass
class SummaryTask:
    id : str
    content: str
    summary: str | None = None

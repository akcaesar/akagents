""" 
Author: Akshay NS
Contains: Email entity

"""

from dataclasses import dataclass
from datetime import datetime

@dataclass
class Email:
    id: int
    sender: str
    subject: str
    body: str
    sent_at: datetime
    category: str = None
    summarised_text: str = None
    summarised: bool = False
    categorized: bool = False
    
    def mark_as_summarised(self):
        self.summarised = True
        
    def mark_as_categorized(self):
        self.categorized = True    
    
    def get_category(self):
        return self.category
    
    
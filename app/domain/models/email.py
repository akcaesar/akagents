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
    
    def get_category(self):
        return self.category
    
    
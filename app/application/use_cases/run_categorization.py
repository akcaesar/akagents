"""  
Author: Akshay NS
Contains: Use case to run categorization on email bodies.

"""
from app.domain.models.email import Email
from typing import List

    
    

class RunCategorization:
    def __init__(self, categorizer):
        self.categorizer = categorizer
        
    
    def execute(self, emails: List[Email]):
        for email in emails:
            if not email.categorized:
                category = self.categorizer.categorize(email.summarised_text or email.body)
                email.category = category
                email.mark_as_categorized() 
        return emails
        
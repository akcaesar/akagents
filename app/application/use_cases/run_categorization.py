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
        # Re-categorize all emails (overwrite default "inbox" categories)
        if not emails:
            return emails
            
        # Batch categorize all emails
        email_bodies = [email.summarised_text or email.body for email in emails]
        categories = self.categorizer.categorize(email_bodies)
        
        # Assign categories back to emails
        for email, category in zip(emails, categories):
            email.category = category
            email.mark_as_categorized()
            
        return emails
        
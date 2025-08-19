"""
Author: Akshay NS
Contains: Fetch and store emails
 
"""

from app.domain.services.email_fetch_service import EmailFetchService, EmailStoreService
from app.domain.repositories.email_respository import EmailRepository
from app.domain.models.email import Email
from app.domain.models.user_credentials import UserCredentials

class FetchStoreUseCase:
    def __init__(self, user: UserCredentials,  store_location: EmailRepository) -> None:
        self.user = user
        self.store_location = store_location
        
        def execute(self, fetch_service: EmailFetchService) -> None:
            emails = fetch_service.fetch(self.user)
            EmailStoreService.store(emails, self.store_location)
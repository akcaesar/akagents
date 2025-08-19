from app.domain.models.user_credentials import UserCredentials
from app.domain.models.email import Email
from app.domain.services.email_fetch_service import EmailFetchService, EmailStoreService
from app.application.use_cases import fetch_store_emails
from app.domain.repositories.email_respository import EmailRepository
from typing import List



email_list = [Email(id=1, sender="test", subject="test", body="test", sent_at="test", category="test"),
              Email(id=2, sender="test", subject="test", body="test", sent_at="test", category="test"),
              ]

create_user = UserCredentials(email="test@123.com", password="12345", list_of_emails=email_list)

class FakeEmailFetchService(EmailFetchService):
    def fetch(self, user_credentials: UserCredentials) -> List[Email]:
        return user_credentials.list_of_emails

def test_store_emails():
    user = create_user
    assert user.email == "test@123.com"
    
    fetch_emails = FakeEmailFetchService().fetch(user)
    assert len(fetch_emails) == len(email_list)
    
class FakeEmailRepository(EmailRepository):
    def __init__(self, email_list: List[Email]) -> None:
        self.email_list = email_list
        
    def get_count(self) -> int:
        return len(self.email_list)
    
    def get_all_emails(self) -> List[Email]:
        return self.email_list
    
    def get_by_id(self, email_id: int) -> Email:
        return self.email_list[email_id]
    
class FakeStoreService(EmailStoreService):
    def store(self, emails: List[Email], email_repository: EmailRepository) -> List[Email]:
        return email_repository(emails)    
    
def test_email_repository():
    create_fake_store_service = FakeStoreService().store(email_list, FakeEmailRepository)
    assert create_fake_store_service.get_count() == len(email_list)
    
    
    
    
          
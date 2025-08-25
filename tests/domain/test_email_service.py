from app.domain.models.user_credentials import UserCredentials
from app.domain.models.email import Email
from app.domain.services.email_fetch_service import EmailFetchService, EmailStoreService
from app.application.use_cases import fetch_store_emails
from app.domain.repositories.email_respository import EmailRepository
from typing import List
from app.infrastructure.email_repositories.sqlite_email_repository import SQLiteEmailRepository
from app.infrastructure.email_fetchers.email_fetcher_imap import EmailFetcherIMAP
from app.infrastructure.email_content_cleaners.email_content_clean_bs4 import EmailContentCleanBS4


email_list = [Email(id=1, sender="test", subject="test", body="test", sent_at="test", category="test"),
              Email(id=2, sender="test", subject="test", body="test", sent_at="test", category="test"),
              Email(id=3, sender="bhendi", subject="testbyid", body="test", sent_at="test", category="test"),
              ]

create_user = UserCredentials(email="test@123.com", password="12345", list_of_emails=email_list)

class FakeEmailFetchService(EmailFetchService):
    def fetch(self, user_credentials: UserCredentials) -> List[Email]:
        return user_credentials.list_of_emails

# def test_fetch_emails():
#     user = create_user
#     assert user.email == "test@123.com"
    
#     fetch_emails = FakeEmailFetchService().fetch(user)
#     assert len(fetch_emails) == len(email_list)
    

# def test_store_emails():
#     user = create_user
#     email_repository = SQLiteEmailRepository() 
#     email_repository.store(user.list_of_emails)
#    # print(email_repository.get_all_emails())
#     assert email_repository.get_by_id(3).sender == "bhendi"
    
    # assert email_repository.get_count() == len(user.list_of_emails)   
    
# def test_email_imap_fetcher():
#     user = UserCredentials(email="work.akshay77@gmail.com", password='ezusbfydvjzgbjcj')
#     email_fetcher = EmailFetcherIMAP()
#     list_of_emails = email_fetcher.fetch(user, limit=10)
#     assert len(list_of_emails) == 10
    
#     repo = SQLiteEmailRepository()
#     repo.store(list_of_emails)
#     assert repo.get_count() >= 10
    
def test_email_body_cleaner():
    
    """ clean all the email body content"""
    repo = SQLiteEmailRepository()
    emails = repo.get_all_emails()
    email_count = repo.get_count()
    cleaner = EmailContentCleanBS4()
    for email in emails:
        cleaned_body = cleaner.clean(email.body)
        email.body = cleaned_body
        repo.session.commit()
    
    print(f'Cleaned {email_count} email bodies and updated in the database.')    
    
    
          
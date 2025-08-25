"""
Author: Akshay NS
Contains: API Interface for email processing.

"""

from fastapi import APIRouter
from app.application.use_cases.fetch_store_emails import FetchStoreUseCase
from app.infrastructure.email_fetchers.email_fetcher_imap import EmailFetcherIMAP
from app.infrastructure.email_repositories.sqlite_email_repository import SQLiteEmailRepository
from app.infrastructure.email_content_cleaners.email_content_clean_bs4 import EmailContentCleanBS4
from app.domain.models.user_credentials import UserCredentials
from app.application.use_cases.run_summarization import RunSummarization
from app.infrastructure.ollama_clients.ollama_summarizer import OllamaSummarizer
router = APIRouter()    

@router.post("/email/loginfetch")
def login_fetch_store(email: str, password: str):
    try:
        user = UserCredentials(email=email, password=password)
        email_repository = SQLiteEmailRepository()
        fetch_service = EmailFetcherIMAP()
        emails = fetch_service.fetch(user, limit=30)
        email_repository.store(emails)
        
        return {"message": f"{len(emails)}Emails fetched, cleaned, and stored successfully."}
    except Exception as e:
        return {"error": str(e)}
    
    
@router.get("/email/showall")
def show_all_emails():
    try:
        email_repository = SQLiteEmailRepository()
        emails = email_repository.get_all_emails()
        return {"emails": [email.__dict__ for email in emails]}
    except Exception as e:
        return {"error": str(e)}  
    
@router.get("/email/clean")
def clean_emails():
    try:
        email_repository = SQLiteEmailRepository()
        emails = email_repository.get_all_emails()
        cleaner = EmailContentCleanBS4()
        for email in emails:
            cleaned_body = cleaner.clean(email.body)
            email.body = cleaned_body
            email_repository.session.commit()
        return {"message": f"{len(emails)} Emails cleaned successfully."}
    except Exception as e:
        return {"error": str(e)}      
    
@router.get("/email/summarize")
def summarize_emails():
    try:
        email_repository = SQLiteEmailRepository()
        emails = email_repository.get_all_emails()
        summarizer = OllamaSummarizer(model_name="gemma3:1b")
        use_case = RunSummarization(summarizer)
        summaries = {}
        for email in emails:
            summary = use_case.execute(email.body)
            email.body = summary
            email_repository.session.commit()
        return {"summaries": summaries}
    except Exception as e:
        return {"error": str(e)}    
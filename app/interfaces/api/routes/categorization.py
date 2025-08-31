"""
Author: Akshay NS
Contains: routers for email categorization APIs.
"""

from fastapi import APIRouter, Depends
from app.application.use_cases.run_categorization import RunCategorization
from app.infrastructure.langchain_clients.langchain_categorizer import OllamaCategorizer
from app.infrastructure.email_repositories.sqlite_email_repository import SQLiteEmailRepository

router = APIRouter()

@router.post("/categorize")
def categorize():
    try:
        email_repository = SQLiteEmailRepository()
        emails = email_repository.get_all_emails(limit=10)
        categorizer = OllamaCategorizer(model_name="gemma3:1b")
        use_case = RunCategorization(categorizer)
        use_case.execute(emails)
        email_repository.bulk_update(emails)
        return {"message": f"{len(emails)} Emails categorized successfully."}
    except Exception as e:
        return {"error": str(e)}

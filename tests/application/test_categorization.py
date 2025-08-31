""" 
Author: Akshay NS

Contains: Ollama Categorizer implementation tests

"""

from app.infrastructure.langchain_clients.langchain_categorizer import OllamaCategorizer
from app.application.use_cases.run_categorization import RunCategorization
from app.domain.models.email import Email
import pytest

@pytest.fixture
def ollama_categorizer():
    return OllamaCategorizer(model_name="gemma3:1b")

@pytest.fixture
def run_categorization(ollama_categorizer):
    return RunCategorization(ollama_categorizer)

def test_categorize_email(run_categorization):
    email = Email(
        id=1,
        sender="test",
        subject="test",
        body="""
        Congratulations! We are pleased to inform you that you have been selected for an interview for the Software Engineer position at Tech Innovators Inc. Please reply to this email to schedule your interview.
        
        
            """,
        sent_at="test",
        category=None
    )
    print("Before categorization:", email.category)
    assert email.categorized is False
    response = run_categorization.execute([email])
    print("After categorization:", email.category)
    assert email.categorized is True
    
    
    
"""
Author: Akshay NS
Contains: Concrete implementation of CategorizationService using Ollama API
  
"""

from app.domain.services.categorization_service import CategorizationService
from app.infrastructure.llm.factory import get_llm
from typing import List, Literal
import requests
from pydantic import BaseModel, Field



#define a more descriptive json structure using pydantic

class Categories(BaseModel):
    """
    Represents the category assigned to an email based on its content.
    The LLM should analyze the email body and select the most appropriate category from the following options:
    - 'Rejection': The email communicates that the application was not successful.
    - 'Interview': The email invites the recipient to an interview or discusses interview scheduling.
    - 'Offer': The email extends a job offer or discusses offer details.
    - 'Application Confirmation': The email confirms receipt of the application or acknowledges submission.
    The LLM should use clues such as keywords, tone, and intent in the email body to determine the category.
    """
    category: Literal['Rejection', 'Interview', 'Offer', 'Application Confirmation', 'Job Advertisement', 'Other'] = Field(
        description=(
            "Category of the email. Choose one based on the content: "
            "'Rejection' for unsuccessful applications, "
            "'Interview' for interview invitations or scheduling, "
            "'Offer' for job offers, "
            "'Application Confirmation' for submission acknowledgments.Does not mean rejection or an offer, but just confirms that i successfuly applied at some company."
            "'Job Advertisement' for emails that advertise job openings."
            "'Other' for emails that do not fit into the above categories."
        )
    )



class OllamaCategorizer(CategorizationService):
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.llm = get_llm(model_name, format="json, schema=Categories")
        
    def categorize(self, email_body: str) -> List[str]:
        messages = [
            ("system", "You categorize job application related emails into one of the following categories: 'Rejection', 'Interview', 'Offer', 'Application Confirmation', 'Job Advertisement', 'Other'. Respond in JSON format with a single field 'category'."),
            ("human", f"Categorize the following email body: {email_body}"),
        ]
        ai_msg = self.llm.with_structured_output(schema=Categories).invoke(messages)
        return ai_msg.category
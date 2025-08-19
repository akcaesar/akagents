""" 
Author: Akshay NS
Contains: Email repository interface

"""

from abc import ABC, abstractmethod
from typing import List
from app.domain.models.email import Email

class EmailRepository(ABC):
    """ 
    Abtract class for an email repository
    
    """
    @abstractmethod
    def get_count(self) -> int:
        pass
    
    @abstractmethod
    def get_all_emails(self) -> List[Email]:
        pass
    
    @abstractmethod
    def get_by_id(self, email_id: int) -> Email:
        pass
    
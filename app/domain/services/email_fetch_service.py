""" 
Author: Akshay NS
Contains: email fetch and store service

"""


from abc import ABC, abstractmethod
from app.domain.repositories.email_respository import EmailRepository
from app.domain.models.email import Email
from app.domain.models.user_credentials import UserCredentials
from typing import List



class EmailFetchService(ABC):
    @abstractmethod
    def fetch(self, user_credentials: UserCredentials) -> List[Email]:
        pass    
    
class EmailStoreService(ABC):
    """ 
    Stores emails in a given repository
    
    """
    @abstractmethod
    def store(self, emails: List[Email], email_repository: EmailRepository):
        pass
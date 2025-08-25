""" 

Author: Akshay NS
Contains: user credentials for email

"""

from dataclasses import dataclass
from app.domain.models.email import Email
from typing import List, Optional

@dataclass
class UserCredentials:
    email: str
    password: str
    
    list_of_emails: Optional[List[Email]] = None
"""  
Author: Akshay NS

Contains: abstract service for categorizing emails.

"""

from abc import ABC, abstractmethod
from typing import List


class CategorizationService(ABC):
    @abstractmethod
    def categorize(self, email_bodies: List[str]) -> List[str]:
        pass
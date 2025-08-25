"""
Author: Akshay NS
Contains: Email Content Cleaner Service

"""

from abc import ABC, abstractmethod


class EmailContentCleaner(ABC):
    @abstractmethod
    def clean(self, text: str) -> str:
        pass
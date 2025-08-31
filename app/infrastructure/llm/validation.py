"""
Author: Akshay NS

Contains: LLM validation utilities 
for example categoriation of emails using ollama 4 categories liker rejectio, interview, offer, others  
"""

from langchain_ollama import ChatOllama
from typing import List
from pydantic import BaseModel, ValidationError



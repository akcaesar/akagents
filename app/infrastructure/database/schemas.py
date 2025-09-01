"""
Author: Akshay NS
Contains: Pure database table schemas - separate from domain models
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class EmailTable(Base):
    """Database table schema for emails - pure infrastructure concern"""
    __tablename__ = 'emails'
    
    id = Column(Integer, primary_key=True)
    sender = Column(String)
    subject = Column(String)
    body = Column(String)
    sent_at = Column(DateTime)
    category = Column(String)
    summarised_text = Column(String)
    summarised = Column(Boolean, default=False)
    categorized = Column(Boolean, default=False)
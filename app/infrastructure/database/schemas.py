"""
Author: Akshay NS
Contains: Pure database table schemas - separate from domain models
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class EmailTable(Base):
    """Core email data - pure transactional data"""
    __tablename__ = 'emails'
    
    id = Column(Integer, primary_key=True)
    sender = Column(String, nullable=False)
    subject = Column(String)
    body = Column(Text)
    sent_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False)

class ProcessingTable(Base):
    """Processing results - analytical data separate from core email data"""
    __tablename__ = 'email_processing'
    
    id = Column(Integer, primary_key=True)
    email_id = Column(Integer, ForeignKey('emails.id'), nullable=False)
    processing_type = Column(String, nullable=False)  # 'summarization', 'categorization', etc.
    result_data = Column(Text)  # JSON or text result
    processed_at = Column(DateTime, nullable=False)
    processor_version = Column(String)  # Track which model/version was used

class CategoryTable(Base):
    """Normalized category lookup table"""
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)  # 'inbox', 'important', 'spam', etc.
    description = Column(String)
    created_at = Column(DateTime, nullable=False)

class EmailCategoryTable(Base):
    """Many-to-many relationship between emails and categories"""
    __tablename__ = 'email_categories'
    
    id = Column(Integer, primary_key=True)
    email_id = Column(Integer, ForeignKey('emails.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    confidence_score = Column(Float)  # How confident the categorization is
    assigned_at = Column(DateTime, nullable=False)
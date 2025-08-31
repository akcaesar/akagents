"""  
Author: Akshay NS
Contains: SQLiteEmailRepository using SQLAlchemy

"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.domain.repositories.email_respository import EmailRepository
from app.domain.models.email import Email
from typing import List
from datetime import datetime
from email.utils import parsedate_to_datetime

Base = declarative_base()

class EmailModel(Base):
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

class SQLiteEmailRepository(EmailRepository):
    def __init__(self, db_path: str = "sqlite:///emails.db"):
        self.engine = create_engine(db_path)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self._migrate_existing_data()
    
    def get_count(self) -> int:
        return self.session.query(EmailModel).count()
    
    def get_all_emails(self, limit: int = None) -> List[Email]:
        query = self.session.query(EmailModel)
        if limit is not None:
            query = query.limit(limit)
        email_models = query.all()
        return [
            Email(
                id=email_model.id,
                sender=email_model.sender,
                subject=email_model.subject,
                body=email_model.body,
                sent_at=email_model.sent_at,
                category=email_model.category,
                summarised_text=email_model.summarised_text,
                summarised=email_model.summarised,
                categorized=email_model.categorized
            )
            for email_model in email_models
        ]
    
    def get_by_id(self, email_id: int) -> Email:
        email_model = self.session.query(EmailModel).filter_by(id=email_id).first()
        if not email_model:
            raise ValueError(f"Email {email_id} not found")
        return Email(
            id=email_model.id,
            sender=email_model.sender,
            subject=email_model.subject,
            body=email_model.body,
            sent_at=email_model.sent_at,
            category=email_model.category,
            summarised_text=email_model.summarised_text,
            summarised=email_model.summarised,
            categorized=email_model.categorized
        )
    
    
    def update(self, email: Email):
        """Update an existing email record in the database."""
        email_model = self.session.query(EmailModel).filter_by(id=email.id).first()
        if not email_model:
            raise ValueError(f"Email {email.id} not found")

        # Update fields
        email_model.sender = email.sender
        email_model.subject = email.subject
        email_model.body = email.body
        
        # Parse sent_at if it's a string
        sent_at = email.sent_at
        if isinstance(sent_at, str):
            try:
                sent_at = parsedate_to_datetime(sent_at)
            except (ValueError, TypeError):
                sent_at = datetime.now()
        email_model.sent_at = sent_at
        
        email_model.category = email.category
        email_model.summarised_text = email.summarised_text
        email_model.summarised = email.summarised
        email_model.categorized = email.categorized

        self.session.commit()
    
    def bulk_update(self, emails: List[Email]):
        """Update multiple existing email records in the database."""
        # Get all email models in one query
        email_ids = [email.id for email in emails]
        email_models = self.session.query(EmailModel).filter(EmailModel.id.in_(email_ids)).all()
        
        # Create a mapping for quick lookup
        email_model_map = {model.id: model for model in email_models}
        
        for email in emails:
            email_model = email_model_map.get(email.id)
            if email_model:
                # Update fields
                email_model.sender = email.sender
                email_model.subject = email.subject
                email_model.body = email.body
                
                # Parse sent_at if it's a string
                sent_at = email.sent_at
                if isinstance(sent_at, str):
                    try:
                        sent_at = parsedate_to_datetime(sent_at)
                    except (ValueError, TypeError):
                        sent_at = datetime.now()
                email_model.sent_at = sent_at
                
                email_model.category = email.category
                email_model.summarised_text = email.summarised_text
                email_model.summarised = email.summarised
                email_model.categorized = email.categorized
        
        # Single commit for all updates
        self.session.commit()
    
    def store(self, emails: List[Email]):
        for email in emails:
            # Parse sent_at if it's a string
            sent_at = email.sent_at
            if isinstance(sent_at, str):
                try:
                    sent_at = parsedate_to_datetime(sent_at)
                except (ValueError, TypeError):
                    # Fallback to current datetime if parsing fails
                    sent_at = datetime.now()
            
            email_model = EmailModel(
                sender=email.sender,
                subject=email.subject,
                body=email.body,
                sent_at=sent_at,
                category=email.category,
                summarised_text=email.summarised_text,
                summarised=email.summarised,
                categorized=email.categorized
            )
            self.session.add(email_model)
        self.session.commit()
        
    def delete_all_emails(self):
        self.session.query(EmailModel).delete()
        self.session.commit()
    
    def _migrate_existing_data(self):
        """Migrate existing data to handle schema changes"""
        try:
            # Check if migration is needed by trying to access new columns
            emails = self.session.query(EmailModel).first()
            if emails:
                # Test if new columns exist by accessing them
                _ = emails.summarised
                _ = emails.categorized
                _ = emails.summarised_text
        except Exception:
            # Migration needed - recreate table with new schema
            # Note: This is a simple migration that will drop existing data
            # For production, you'd want to preserve data with proper migration
            Base.metadata.drop_all(self.engine)
            Base.metadata.create_all(self.engine)
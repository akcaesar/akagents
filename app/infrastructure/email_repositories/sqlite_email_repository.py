"""  
Author: Akshay NS
Contains: SQLiteEmailRepository using SQLAlchemy

"""

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.domain.repositories.email_respository import EmailRepository
from app.domain.models.email import Email
from typing import List

Base = declarative_base()

class EmailModel(Base):
    __tablename__ = 'emails'
    
    id = Column(Integer, primary_key=True)
    sender = Column(String)
    subject = Column(String)
    body = Column(String)
    sent_at = Column(String)
    category = Column(String)

class SQLiteEmailRepository(EmailRepository):
    def __init__(self, db_path: str = "sqlite:///emails.db"):
        self.engine = create_engine(db_path)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def get_count(self) -> int:
        return self.session.query(EmailModel).count()
    
    def get_all_emails(self) -> List[Email]:
        email_models = self.session.query(EmailModel).all()
        return email_models
    
    def get_by_id(self, email_id: int) -> Email:
        email_model = self.session.query(EmailModel).filter_by(id=email_id).first()
        if not email_model:
            raise ValueError(f"Email {email_id} not found")
        return Email(email_model.id, email_model.sender, email_model.subject, email_model.body, email_model.sent_at, email_model.category)
    
    
    def update(self, email: Email):
        """Update an existing email record in the database."""
        email_model = self.session.query(EmailModel).filter_by(id=email.id).first()
        if not email_model:
            raise ValueError(f"Email {email.id} not found")

        # Update fields
        email_model.sender = email.sender
        email_model.subject = email.subject
        email_model.body = email.body
        email_model.sent_at = email.sent_at
        email_model.category = email.category

        self.session.commit()
    def store(self, emails: List[Email]):
        for email in emails:
            email_model = EmailModel(
                sender=email.sender,
                subject=email.subject,
                body=email.body,
                sent_at=email.sent_at,
                category=email.category
            )
            self.session.add(email_model)
        self.session.commit()
        
    def delete_all_emails(self):
        self.session.query(EmailModel).delete()
        self.session.commit()
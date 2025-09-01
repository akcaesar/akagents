"""  
Author: Akshay NS
Contains: SQLiteEmailRepository using SQLAlchemy

"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.domain.repositories.email_respository import EmailRepository
from app.domain.models.email import Email
from app.infrastructure.database.schemas import Base, EmailTable
from app.infrastructure.database.mappers import EmailMapper
from typing import List

class SQLiteEmailRepository(EmailRepository):
    def __init__(self, db_path: str = "sqlite:///emails.db"):
        self.engine = create_engine(db_path)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self._migrate_existing_data()
    
    def get_count(self) -> int:
        return self.session.query(EmailTable).count()
    
    def get_all_emails(self, limit: int = None) -> List[Email]:
        query = self.session.query(EmailTable)
        if limit is not None:
            query = query.limit(limit)
        email_tables = query.all()
        return [
            EmailMapper.to_domain(email_table)
            for email_table in email_tables
        ]
    
    def get_by_id(self, email_id: int) -> Email:
        email_table = self.session.query(EmailTable).filter_by(id=email_id).first()
        if not email_table:
            raise ValueError(f"Email {email_id} not found")
        return EmailMapper.to_domain(email_table)
    
    
    def update(self, email: Email):
        """Update an existing email record in the database."""
        email_table = self.session.query(EmailTable).filter_by(id=email.id).first()
        if not email_table:
            raise ValueError(f"Email {email.id} not found")

        # Convert domain model to schema and update fields
        updated_table = EmailMapper.to_schema(email)
        
        # Update all fields from the converted schema
        email_table.sender = updated_table.sender
        email_table.subject = updated_table.subject
        email_table.body = updated_table.body
        email_table.sent_at = updated_table.sent_at
        email_table.category = updated_table.category
        email_table.summarised_text = updated_table.summarised_text
        email_table.summarised = updated_table.summarised
        email_table.categorized = updated_table.categorized

        self.session.commit()
    
    def bulk_update(self, emails: List[Email]):
        """Update multiple existing email records in the database."""
        # Get all email tables in one query
        email_ids = [email.id for email in emails]
        email_tables = self.session.query(EmailTable).filter(EmailTable.id.in_(email_ids)).all()
        
        # Create a mapping for quick lookup
        email_table_map = {table.id: table for table in email_tables}
        
        for email in emails:
            email_table = email_table_map.get(email.id)
            if email_table:
                # Convert domain to schema and update fields
                updated_schema = EmailMapper.to_schema(email)
                
                email_table.sender = updated_schema.sender
                email_table.subject = updated_schema.subject
                email_table.body = updated_schema.body
                email_table.sent_at = updated_schema.sent_at
                email_table.category = updated_schema.category
                email_table.summarised_text = updated_schema.summarised_text
                email_table.summarised = updated_schema.summarised
                email_table.categorized = updated_schema.categorized
        
        # Single commit for all updates
        self.session.commit()
    
    def store(self, emails: List[Email]):
        for email in emails:
            # Convert domain model to schema
            email_table = EmailMapper.to_schema(email)
            self.session.add(email_table)
        self.session.commit()
        
    def delete_all_emails(self):
        self.session.query(EmailTable).delete()
        self.session.commit()
    
    def _migrate_existing_data(self):
        """Migrate existing data to handle schema changes"""
        try:
            # Check if migration is needed by trying to access new columns
            emails = self.session.query(EmailTable).first()
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
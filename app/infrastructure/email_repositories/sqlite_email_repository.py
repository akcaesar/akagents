"""  
Author: Akshay NS
Contains: SQLiteEmailRepository using SQLAlchemy

"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.domain.repositories.email_respository import EmailRepository
from app.domain.models.email import Email
from app.infrastructure.database.schemas import (
    Base, EmailTable, ProcessingTable, CategoryTable, EmailCategoryTable
)
from app.infrastructure.database.mappers import EmailMapper, ProcessingMapper, CategoryMapper
from typing import List
from datetime import datetime

class SQLiteEmailRepository(EmailRepository):
    def __init__(self, db_path: str = "sqlite:///emails.db"):
        self.engine = create_engine(db_path)
        self._migrate_to_normalized_schema()
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def _migrate_to_normalized_schema(self):
        """Migrate from old schema to new normalized schema"""
        # Simple migration: drop and recreate if old schema detected
        try:
            # Test if old schema exists by checking for old columns
            with self.engine.connect() as conn:
                result = conn.execute("PRAGMA table_info(emails)")
                columns = [row[1] for row in result.fetchall()]
                
                # If old schema detected (has summarised_text but no created_at)
                if 'summarised_text' in columns and 'created_at' not in columns:
                    print("🔄 Migrating to normalized schema (old data will be lost)...")
                    Base.metadata.drop_all(self.engine)
                    
        except Exception:
            # Table doesn't exist yet, no migration needed
            pass
    
    def get_count(self) -> int:
        return self.session.query(EmailTable).count()
    
    def get_all_emails(self, limit: int = None) -> List[Email]:
        # Get email tables
        query = self.session.query(EmailTable)
        if limit is not None:
            query = query.limit(limit)
        email_tables = query.all()
        
        emails = []
        for email_table in email_tables:
            # Get processing results for this email
            processing_results = self.session.query(ProcessingTable).filter_by(email_id=email_table.id).all()
            
            # Get categories for this email
            categories_query = (
                self.session.query(CategoryTable.name)
                .join(EmailCategoryTable, CategoryTable.id == EmailCategoryTable.category_id)
                .filter(EmailCategoryTable.email_id == email_table.id)
            )
            categories = [cat.name for cat in categories_query.all()]
            
            # Convert to domain model
            email = EmailMapper.to_domain(email_table, processing_results, categories)
            emails.append(email)
            
        return emails
    
    def get_by_id(self, email_id: int) -> Email:
        email_table = self.session.query(EmailTable).filter_by(id=email_id).first()
        if not email_table:
            raise ValueError(f"Email {email_id} not found")
            
        # Get processing results for this email
        processing_results = self.session.query(ProcessingTable).filter_by(email_id=email_id).all()
        
        # Get categories for this email
        categories_query = (
            self.session.query(CategoryTable.name)
            .join(EmailCategoryTable, CategoryTable.id == EmailCategoryTable.category_id)
            .filter(EmailCategoryTable.email_id == email_id)
        )
        categories = [cat.name for cat in categories_query.all()]
        
        return EmailMapper.to_domain(email_table, processing_results, categories)
    
    
    def update(self, email: Email):
        """Update an existing email record in the database."""
        email_table = self.session.query(EmailTable).filter_by(id=email.id).first()
        if not email_table:
            raise ValueError(f"Email {email.id} not found")

        # Update core email fields
        updated_core = EmailMapper.to_core_schema(email)
        email_table.sender = updated_core.sender
        email_table.subject = updated_core.subject
        email_table.body = updated_core.body
        email_table.sent_at = updated_core.sent_at

        # Update processing data - clear old and add new
        self.session.query(ProcessingTable).filter_by(email_id=email.id).delete()
        processing_data = EmailMapper.extract_processing_data(email)
        for proc_data in processing_data:
            processing_record = ProcessingMapper.to_schema(
                email_id=email.id,
                processing_type=proc_data['type'],
                result_data=proc_data['data'],
                processor_version=proc_data['version']
            )
            self.session.add(processing_record)

        # Update category relationships - clear old and add new
        self.session.query(EmailCategoryTable).filter_by(email_id=email.id).delete()
        if email.category:
            category = self._get_or_create_category(email.category)
            email_category = CategoryMapper.to_email_category_schema(
                email_id=email.id,
                category_id=category.id
            )
            self.session.add(email_category)

        self.session.commit()
    
    def bulk_update(self, emails: List[Email]):
        """Update multiple existing email records in the database."""
        email_ids = [email.id for email in emails]
        
        # Get all email tables in one query
        email_tables = self.session.query(EmailTable).filter(EmailTable.id.in_(email_ids)).all()
        email_table_map = {table.id: table for table in email_tables}
        
        # Clear old processing and category data for all emails
        self.session.query(ProcessingTable).filter(ProcessingTable.email_id.in_(email_ids)).delete()
        self.session.query(EmailCategoryTable).filter(EmailCategoryTable.email_id.in_(email_ids)).delete()
        
        for email in emails:
            email_table = email_table_map.get(email.id)
            if email_table:
                # Update core email fields
                updated_core = EmailMapper.to_core_schema(email)
                email_table.sender = updated_core.sender
                email_table.subject = updated_core.subject
                email_table.body = updated_core.body
                email_table.sent_at = updated_core.sent_at
                
                # Add new processing data
                processing_data = EmailMapper.extract_processing_data(email)
                for proc_data in processing_data:
                    processing_record = ProcessingMapper.to_schema(
                        email_id=email.id,
                        processing_type=proc_data['type'],
                        result_data=proc_data['data'],
                        processor_version=proc_data['version']
                    )
                    self.session.add(processing_record)
                
                # Add new category relationships
                if email.category:
                    category = self._get_or_create_category(email.category)
                    email_category = CategoryMapper.to_email_category_schema(
                        email_id=email.id,
                        category_id=category.id
                    )
                    self.session.add(email_category)
        
        # Single commit for all updates
        self.session.commit()
    
    def store(self, emails: List[Email]):
        for email in emails:
            # Store core email data
            email_table = EmailMapper.to_core_schema(email)
            self.session.add(email_table)
            self.session.flush()  # Get the ID
            
            # Store processing data separately
            processing_data = EmailMapper.extract_processing_data(email)
            for proc_data in processing_data:
                processing_record = ProcessingMapper.to_schema(
                    email_id=email_table.id,
                    processing_type=proc_data['type'],
                    result_data=proc_data['data'],
                    processor_version=proc_data['version']
                )
                self.session.add(processing_record)
            
            # Store category relationships
            if email.category:
                category = self._get_or_create_category(email.category)
                email_category = CategoryMapper.to_email_category_schema(
                    email_id=email_table.id,
                    category_id=category.id
                )
                self.session.add(email_category)
                
        self.session.commit()
    
    def _get_or_create_category(self, category_name: str) -> CategoryTable:
        """Get existing category or create new one"""
        category = self.session.query(CategoryTable).filter_by(name=category_name).first()
        if not category:
            category = CategoryMapper.to_schema(category_name)
            self.session.add(category)
            self.session.flush()  # Get the ID
        return category
        
    def delete_all_emails(self):
        # Delete in proper order due to foreign key constraints
        self.session.query(EmailCategoryTable).delete()
        self.session.query(ProcessingTable).delete()
        self.session.query(EmailTable).delete()
        # Keep categories as they can be reused
        self.session.commit()

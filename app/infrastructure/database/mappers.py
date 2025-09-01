"""
Author: Akshay NS
Contains: Mappers to convert between domain models and database schemas
"""

from datetime import datetime
from email.utils import parsedate_to_datetime
from app.domain.models.email import Email
from app.infrastructure.database.schemas import EmailTable

class EmailMapper:
    """Handles conversion between Email domain model and EmailTable schema"""
    
    @staticmethod
    def to_domain(email_table: EmailTable) -> Email:
        """Convert database table record to domain model"""
        return Email(
            id=email_table.id,
            sender=email_table.sender,
            subject=email_table.subject,
            body=email_table.body,
            sent_at=email_table.sent_at,
            category=email_table.category,
            summarised_text=email_table.summarised_text,
            summarised=email_table.summarised,
            categorized=email_table.categorized
        )
    
    @staticmethod
    def to_schema(email: Email) -> EmailTable:
        """Convert domain model to database table record"""
        # Handle date parsing if needed
        sent_at = email.sent_at
        if isinstance(sent_at, str):
            try:
                sent_at = parsedate_to_datetime(sent_at)
            except (ValueError, TypeError):
                sent_at = datetime.now()
        
        return EmailTable(
            id=email.id,
            sender=email.sender,
            subject=email.subject,
            body=email.body,
            sent_at=sent_at,
            category=email.category,
            summarised_text=email.summarised_text,
            summarised=email.summarised,
            categorized=email.categorized
        )
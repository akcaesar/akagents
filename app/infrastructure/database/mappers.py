"""
Author: Akshay NS
Contains: Mappers to convert between domain models and database schemas
"""

import json
from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import List, Dict, Any
from app.domain.models.email import Email
from app.infrastructure.database.schemas import (
    EmailTable, ProcessingTable, CategoryTable, EmailCategoryTable
)

class ProcessingMapper:
    """Handles conversion for processing results"""
    
    @staticmethod
    def to_schema(email_id: int, processing_type: str, result_data: Any, processor_version: str = None) -> ProcessingTable:
        """Convert processing result to database schema"""
        # Convert result_data to JSON string if it's a dict/list
        if isinstance(result_data, (dict, list)):
            result_str = json.dumps(result_data)
        else:
            result_str = str(result_data) if result_data is not None else None
            
        return ProcessingTable(
            email_id=email_id,
            processing_type=processing_type,
            result_data=result_str,
            processed_at=datetime.now(),
            processor_version=processor_version
        )
    
    @staticmethod
    def from_schema(processing_table: ProcessingTable) -> Dict[str, Any]:
        """Convert database record to processing result dict"""
        # Try to parse JSON, fall back to string
        try:
            result_data = json.loads(processing_table.result_data) if processing_table.result_data else None
        except (json.JSONDecodeError, TypeError):
            result_data = processing_table.result_data
            
        return {
            'processing_type': processing_table.processing_type,
            'result_data': result_data,
            'processed_at': processing_table.processed_at,
            'processor_version': processing_table.processor_version
        }

class CategoryMapper:
    """Handles conversion for categories"""
    
    @staticmethod
    def to_schema(name: str, description: str = None) -> CategoryTable:
        """Convert category info to database schema"""
        return CategoryTable(
            name=name,
            description=description,
            created_at=datetime.now()
        )
    
    @staticmethod
    def to_email_category_schema(email_id: int, category_id: int, confidence_score: float = None) -> EmailCategoryTable:
        """Convert email-category relationship to database schema"""
        return EmailCategoryTable(
            email_id=email_id,
            category_id=category_id,
            confidence_score=confidence_score,
            assigned_at=datetime.now()
        )

class EmailMapper:
    """Handles conversion between Email domain model and normalized database schemas"""
    
    @staticmethod
    def to_domain(email_table: EmailTable, processing_results: List[ProcessingTable] = None, 
                  categories: List[str] = None) -> Email:
        """Convert database records to domain model"""
        
        # Extract processing results
        summarised_text = None
        summarised = False
        categorized = False
        category = None
        
        if processing_results:
            for proc in processing_results:
                if proc.processing_type == 'summarization':
                    summarised_text = proc.result_data
                    summarised = True
                elif proc.processing_type == 'categorization':
                    categorized = True
        
        # Use first category as primary category for backward compatibility
        if categories:
            category = categories[0]
            categorized = True  # If email has categories, it's been categorized
        
        return Email(
            id=email_table.id,
            sender=email_table.sender,
            subject=email_table.subject,
            body=email_table.body,
            sent_at=email_table.sent_at,
            category=category,
            summarised_text=summarised_text,
            summarised=summarised,
            categorized=categorized
        )
    
    @staticmethod
    def to_core_schema(email: Email) -> EmailTable:
        """Convert domain model to core email table record (no processing data)"""
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
            created_at=datetime.now()
        )
    
    @staticmethod
    def extract_processing_data(email: Email) -> List[Dict[str, Any]]:
        """Extract processing data from domain model for separate storage"""
        processing_data = []
        
        if email.summarised_text:
            processing_data.append({
                'type': 'summarization',
                'data': email.summarised_text,
                'version': 'current'
            })
        
        if email.categorized and email.category:
            processing_data.append({
                'type': 'categorization', 
                'data': email.category,
                'version': 'current'
            })
            
        return processing_data
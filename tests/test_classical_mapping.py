"""
Test classical mapping implementation - domain models separate from database schemas
"""

import pytest
from datetime import datetime
from app.infrastructure.email_repositories.sqlite_email_repository import SQLiteEmailRepository
from app.domain.models.email import Email

def test_classical_mapping_basic():
    """Test that classical mapping works - domain stays pure, ORM in infrastructure"""
    
    # Test repository initialization
    repo = SQLiteEmailRepository()
    
    # Test creating a sample email (pure domain object)
    email = Email(
        id=None,
        sender='test@example.com',
        subject='Test Classical Mapping',
        body='Testing that domain model stays pure while ORM handles persistence',
        sent_at=datetime.now(),
        category='inbox'
    )
    
    # Test storing email (should use mapper internally)
    repo.store([email])
    
    # Test retrieving emails (should use mapper to convert back to domain)
    retrieved_emails = repo.get_all_emails()
    
    assert len(retrieved_emails) > 0
    retrieved = retrieved_emails[-1]  # Get last added
    
    # Verify domain object properties
    assert retrieved.sender == 'test@example.com'
    assert retrieved.subject == 'Test Classical Mapping'
    assert retrieved.category == 'inbox'
    assert isinstance(retrieved, Email)  # Pure domain object
    
    print("✅ Classical mapping test passed!")
    print(f"✅ Domain object type: {type(retrieved)}")
    print(f"✅ Retrieved email: {retrieved.sender} - {retrieved.subject}")

def test_update_with_classical_mapping():
    """Test update operations work with classical mapping"""
    
    repo = SQLiteEmailRepository()
    
    # Create and store initial email
    email = Email(
        id=None,
        sender='update@test.com',
        subject='Original Subject',
        body='Original body',
        sent_at=datetime.now(),
        category='inbox'
    )
    
    repo.store([email])
    emails = repo.get_all_emails()
    stored_email = emails[-1]
    
    # Update the domain object
    stored_email.subject = 'Updated Subject'
    stored_email.category = 'important'
    stored_email.mark_as_categorized()
    
    # Update in database
    repo.update(stored_email)
    
    # Retrieve and verify
    updated_email = repo.get_by_id(stored_email.id)
    assert updated_email.subject == 'Updated Subject'
    assert updated_email.category == 'important'
    assert updated_email.categorized == True
    
    print("✅ Update with classical mapping test passed!")

if __name__ == "__main__":
    test_classical_mapping_basic()
    test_update_with_classical_mapping()
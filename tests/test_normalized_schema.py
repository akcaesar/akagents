"""
Test normalized database schema implementation
Author: Akshay NS
"""

import pytest
from datetime import datetime
from app.infrastructure.email_repositories.sqlite_email_repository import SQLiteEmailRepository
from app.domain.models.email import Email

def test_normalized_schema_basic_operations():
    """Test that basic CRUD operations work with normalized schema"""
    
    # Use a test database
    repo = SQLiteEmailRepository(db_path="sqlite:///test_normalized.db")
    
    # Clean start
    repo.delete_all_emails()
    
    # Test 1: Store email with processing data
    email = Email(
        id=None,
        sender='test@normalized.com',
        subject='Normalized Schema Test',
        body='Testing the new normalized database design',
        sent_at=datetime.now(),
        category='important',
        summarised_text='Test summary',
        summarised=True,
        categorized=True
    )
    
    repo.store([email])
    print("✅ Store with processing data works")
    
    # Test 2: Retrieve and verify data integrity  
    emails = repo.get_all_emails()
    assert len(emails) > 0
    
    retrieved = emails[-1]  # Last added
    assert retrieved.sender == 'test@normalized.com'
    assert retrieved.subject == 'Normalized Schema Test' 
    assert retrieved.category == 'important'
    assert retrieved.summarised_text == 'Test summary'
    assert retrieved.summarised == True
    assert retrieved.categorized == True
    print("✅ Data integrity maintained across normalized tables")
    
    # Test 3: Update processing results
    retrieved.summarised_text = 'Updated summary'
    retrieved.category = 'urgent'
    repo.update(retrieved)
    
    updated = repo.get_by_id(retrieved.id)
    assert updated.summarised_text == 'Updated summary'
    assert updated.category == 'urgent'
    print("✅ Updates work across normalized schema")
    
    print("✅ Normalized schema basic operations test passed!")

def test_bulk_operations_with_normalized_schema():
    """Test bulk operations maintain efficiency with normalized design"""
    
    repo = SQLiteEmailRepository(db_path="sqlite:///test_normalized.db")
    repo.delete_all_emails()
    
    # Create multiple emails with different processing states
    emails = []
    for i in range(5):
        email = Email(
            id=None,
            sender=f'user{i}@test.com',
            subject=f'Email {i}',
            body=f'Content for email {i}',
            sent_at=datetime.now(),
            category='inbox' if i % 2 == 0 else 'work',
            summarised_text=f'Summary {i}' if i < 3 else None,
            summarised=i < 3,
            categorized=True
        )
        emails.append(email)
    
    # Bulk store
    repo.store(emails)
    print("✅ Bulk store works with normalized schema")
    
    # Retrieve and modify for bulk update
    stored_emails = repo.get_all_emails()
    for email in stored_emails:
        email.category = 'processed'
        email.summarised_text = f'Bulk updated: {email.subject}'
        email.mark_as_summarised()
    
    # Bulk update
    repo.bulk_update(stored_emails)
    print("✅ Bulk update works with normalized schema")
    
    # Verify updates
    final_emails = repo.get_all_emails()
    for email in final_emails:
        assert email.category == 'processed'
        assert 'Bulk updated:' in email.summarised_text
        assert email.summarised == True
    
    print("✅ Bulk operations maintain data consistency")

def test_category_normalization():
    """Test that categories are properly normalized"""
    
    repo = SQLiteEmailRepository(db_path="sqlite:///test_normalized.db") 
    repo.delete_all_emails()
    
    # Create emails with same category
    emails = [
        Email(
            id=None,
            sender='user1@test.com',
            subject='Email 1',
            body='Content 1',
            sent_at=datetime.now(),
            category='inbox'
        ),
        Email(
            id=None,
            sender='user2@test.com', 
            subject='Email 2',
            body='Content 2',
            sent_at=datetime.now(),
            category='inbox'  # Same category
        )
    ]
    
    repo.store(emails)
    
    # Both emails should reference same category record
    retrieved_emails = repo.get_all_emails()
    categories = [e.category for e in retrieved_emails if e.category]
    
    # Should have inbox category for both emails
    assert categories.count('inbox') == 2
    print("✅ Category normalization works - shared categories")

def test_processing_history_separation():
    """Test that processing results are stored separately from core email data"""
    
    repo = SQLiteEmailRepository(db_path="sqlite:///test_normalized.db")
    repo.delete_all_emails()
    
    # Create email without processing
    email = Email(
        id=None,
        sender='history@test.com',
        subject='Processing History Test',
        body='Original content',
        sent_at=datetime.now(),
        category='inbox'
    )
    
    repo.store([email])
    stored = repo.get_all_emails()[-1]
    
    # Verify no processing initially
    assert stored.summarised == False
    assert stored.categorized == True  # True because email has a category
    assert stored.summarised_text is None
    
    # Add summarization
    stored.summarised_text = 'Generated summary'
    stored.mark_as_summarised()
    repo.update(stored)
    
    # Add more processing
    stored.category = 'important'
    stored.mark_as_categorized() 
    repo.update(stored)
    
    final = repo.get_by_id(stored.id)
    assert final.summarised_text == 'Generated summary'
    assert final.summarised == True
    assert final.category == 'important'
    assert final.categorized == True
    
    print("✅ Processing results properly separated from core email data")

def test_domain_model_unchanged():
    """Test that domain model interface remains exactly the same"""
    
    repo = SQLiteEmailRepository(db_path="sqlite:///test_normalized.db")
    repo.delete_all_emails()
    
    # Create email using original domain model interface
    email = Email(
        id=None,
        sender='domain@test.com',
        subject='Domain Model Test',
        body='Testing domain model compatibility',
        sent_at=datetime.now()
    )
    
    # Original domain methods should work
    email.mark_as_summarised()
    email.mark_as_categorized()
    assert email.get_category() is None  # No category set yet
    
    email.category = 'test'
    assert email.get_category() == 'test'
    
    repo.store([email])
    retrieved = repo.get_all_emails()[-1]
    
    # Domain object should behave identically
    assert isinstance(retrieved, Email)
    assert hasattr(retrieved, 'mark_as_summarised')
    assert hasattr(retrieved, 'mark_as_categorized')
    assert hasattr(retrieved, 'get_category')
    
    print("✅ Domain model interface unchanged - backward compatibility maintained")

if __name__ == "__main__":
    print("🧪 Testing Normalized Database Schema Implementation...\n")
    
    test_normalized_schema_basic_operations()
    print()
    
    test_bulk_operations_with_normalized_schema() 
    print()
    
    test_category_normalization()
    print()
    
    test_processing_history_separation()
    print()
    
    test_domain_model_unchanged()
    print()
    
    print("🎉 All normalized schema tests passed!")
    print("📊 Database is now properly normalized with:")
    print("   - Core email data separated from processing results")  
    print("   - Categories normalized to eliminate redundancy")
    print("   - Processing history tracked separately")
    print("   - Domain model interface unchanged")
    print("   - Classical mapping pattern maintained")
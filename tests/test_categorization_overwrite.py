"""
Test categorization overwrite functionality - ensures AI categories replace default "inbox"
"""

import pytest
from datetime import datetime
from app.infrastructure.email_repositories.sqlite_email_repository import SQLiteEmailRepository
from app.domain.models.email import Email

class MockCategorizer:
    """Mock categorizer for testing"""
    def categorize(self, email_bodies):
        # Return different categories for different email patterns
        categories = []
        for body in email_bodies:
            if 'rejected' in body.lower() or 'unsuccessful' in body.lower():
                categories.append('Rejection')
            elif 'interview' in body.lower():
                categories.append('Interview') 
            elif 'offer' in body.lower() or 'congratulations' in body.lower():
                categories.append('Offer')
            else:
                categories.append('Application Confirmation')
        return categories

def test_categorization_overwrites_default_inbox():
    """Test that AI categorization overwrites default 'inbox' categories"""
    
    from app.application.use_cases.run_categorization import RunCategorization
    
    repo = SQLiteEmailRepository(db_path="sqlite:///test_overwrite.db")
    repo.delete_all_emails()
    
    # Create emails with default "inbox" category (simulating IMAP fetch)
    emails = [
        Email(
            id=None, sender='hr@company.com', subject='Interview Invitation', 
            body='We would like to invite you for an interview next week',
            sent_at=datetime.now(), category='inbox', categorized=True
        ),
        Email(
            id=None, sender='jobs@corp.com', subject='Application Status',
            body='Unfortunately, we have decided to move forward with other candidates',
            sent_at=datetime.now(), category='inbox', categorized=True
        ),
        Email(
            id=None, sender='talent@startup.com', subject='Job Offer',
            body='Congratulations! We are pleased to offer you the position',
            sent_at=datetime.now(), category='inbox', categorized=True
        )
    ]
    
    # Store emails (all have default "inbox" category)
    repo.store(emails)
    stored_emails = repo.get_all_emails()
    
    # Verify all emails initially have "inbox" category
    assert all(email.category == 'inbox' for email in stored_emails)
    assert all(email.categorized == True for email in stored_emails)
    
    # Run AI categorization (should overwrite)
    categorizer = MockCategorizer()
    use_case = RunCategorization(categorizer)
    use_case.execute(stored_emails)
    
    # Update in database
    repo.bulk_update(stored_emails)
    
    # Retrieve and verify categories were overwritten
    final_emails = repo.get_all_emails()
    categories = [email.category for email in final_emails]
    
    # Should have AI categories, not "inbox"
    assert 'Interview' in categories
    assert 'Rejection' in categories  
    assert 'Offer' in categories
    assert 'inbox' not in categories  # Default should be overwritten
    
    print("✅ Categorization successfully overwrote default inbox categories")
    print(f"✅ Final categories: {categories}")

def test_batch_categorization_interface():
    """Test that categorizer properly handles batch input/output"""
    
    categorizer = MockCategorizer()
    
    # Test batch processing
    email_bodies = [
        "Thank you for your application. We will review it carefully.",
        "We regret to inform you that your application was unsuccessful.", 
        "Please join us for an interview on Monday at 2 PM.",
        "Congratulations on your new position with our company!"
    ]
    
    categories = categorizer.categorize(email_bodies)
    
    # Verify correct batch processing
    assert len(categories) == len(email_bodies)
    assert isinstance(categories, list)
    assert all(isinstance(cat, str) for cat in categories)
    
    # Verify categorization logic
    assert categories[0] == 'Application Confirmation'
    assert categories[1] == 'Rejection' 
    assert categories[2] == 'Interview'
    assert categories[3] == 'Offer'
    
    print("✅ Batch categorization interface working correctly")

if __name__ == "__main__":
    test_categorization_overwrite_default_inbox()
    test_batch_categorization_interface()
    print("\n🎉 All categorization overwrite tests passed!")
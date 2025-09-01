"""
Debug script to check what's happening with categories in the database
"""

import sqlite3
from app.infrastructure.email_repositories.sqlite_email_repository import SQLiteEmailRepository

def debug_database():
    print("🔍 Debugging category storage...")
    
    # Check database schema
    conn = sqlite3.connect('emails.db')
    cursor = conn.cursor()
    
    print("\n=== DATABASE TABLES ===")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print("Tables:", [t[0] for t in tables])
    
    if ('categories',) in tables:
        print("\n=== CATEGORIES TABLE ===")
        cursor.execute("SELECT * FROM categories")
        categories = cursor.fetchall()
        print("Categories:", categories)
        
        cursor.execute("PRAGMA table_info(categories)")
        schema = cursor.fetchall()
        print("Categories schema:", [(col[1], col[2]) for col in schema])
    
    if ('email_categories',) in tables:
        print("\n=== EMAIL_CATEGORIES TABLE ===")
        cursor.execute("SELECT * FROM email_categories")
        email_cats = cursor.fetchall()
        print("Email-Category links:", email_cats)
    
    if ('emails',) in tables:
        print("\n=== EMAILS TABLE SCHEMA ===")
        cursor.execute("PRAGMA table_info(emails)")
        schema = cursor.fetchall()
        print("Emails columns:", [(col[1], col[2]) for col in schema])
        
        print("\n=== SAMPLE EMAILS ===")
        cursor.execute("SELECT id, sender, subject FROM emails LIMIT 3")
        emails = cursor.fetchall()
        for email in emails:
            print(f"Email {email[0]}: {email[1][:30]}... - {email[2][:30]}...")
    
    conn.close()
    
    print("\n=== REPOSITORY TEST ===")
    repo = SQLiteEmailRepository()
    emails = repo.get_all_emails(limit=3)
    for email in emails:
        print(f"Email {email.id}: category='{email.category}', categorized={email.categorized}")

if __name__ == "__main__":
    debug_database()
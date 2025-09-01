import sqlite3
conn = sqlite3.connect('emails.db')
cursor = conn.cursor()

#check if new tables exist

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [row[0] for row in cursor.fetchall()]
print("Tables:", tables)

# 2. If categories table exists, check what's in it      
if 'categories' in tables:
      cursor.execute("SELECT * FROM categories")
      print("Categories:", cursor.fetchall())

      cursor.execute("SELECT * FROM email_categories LIMIT 5")
      print("Email-Category links:", cursor.fetchall())    
else:
      print("❌ Normalized tables don't exist - migration failed")

conn.close()
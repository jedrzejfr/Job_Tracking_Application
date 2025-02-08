import sqlite3
import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'jobs.db')

# Test the database connection
conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()

# Check if the `jobs` table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='jobs'")
table_exists = cursor.fetchone()

if table_exists:
    print("The `jobs` table exists!")
else:
    print("The `jobs` table does not exist.")

conn.close()
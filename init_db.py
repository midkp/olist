import sqlite3
import os

db_path = "olist.db"  # Adjust if needed

# Check if the database exists, otherwise create it
if not os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sellers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        );
    """)
    conn.commit()
    conn.close()

print("Database initialized successfully!")

import sqlite3
import os

db_path = os.path.join('instance', 'online_compiler.db')

if not os.path.exists(db_path):
    print("Database not found at", db_path)
    exit()

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Add is_playground if it doesn't exist
    try:
        cursor.execute('ALTER TABLE snippets ADD COLUMN is_playground BOOLEAN DEFAULT 0')
        print("Added is_playground to snippets")
    except sqlite3.OperationalError as e:
        print("is_playground already exists or error:", e)

    # Add language_id to snippets if it doesn't exist (it should, but just in case)
    try:
        cursor.execute('ALTER TABLE snippets ADD COLUMN language_id INTEGER REFERENCES languages(id)')
        print("Added language_id to snippets")
    except sqlite3.OperationalError as e:
        print("language_id already exists or error:", e)

    conn.commit()
    conn.close()
    print("Database patched successfully")
except Exception as e:
    print("Error patching database:", e)

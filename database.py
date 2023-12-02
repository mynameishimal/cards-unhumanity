import sqlite3

conn = sqlite3.connect('new_user_database.db')
cursor = conn.cursor()

# Drop the existing 'users' table if it already exists
cursor.execute('''DROP TABLE IF EXISTS users''')

# Create the 'users' table
cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password_hash TEXT NOT NULL
    )
''')

print("Table 'users' recreated.")

conn.commit()
conn.close()

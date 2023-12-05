import sqlite3

conn = sqlite3.connect('user_stats.db')
cursor = conn.cursor()

# Create a table to store user stats
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_stats (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        games_played INTEGER,
        average_score REAL,
        past_scores TEXT
    )
''')

conn.commit()
conn.close()
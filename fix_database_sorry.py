import sqlite3

# Connect to your database file
conn = sqlite3.connect('user_stats.db')
cursor = conn.cursor()

# Replace 'user_stats' with the actual table name
table_name = 'user_stats'

# Fetch table schema
cursor.execute(f"PRAGMA table_info({table_name})")
schema = cursor.fetchall()

# Display the schema
for column in schema:
    print(column)

# Close the connection
conn.close()

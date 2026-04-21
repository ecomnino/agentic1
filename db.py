import sqlite3

conn = sqlite3.connect("local_database.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM data")

rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()
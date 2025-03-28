import sqlite3

conn = sqlite3.connect('users.db')
c = conn.cursor()

c.execute('SELECT username, password FROM users')
users = c.fetchall()

for user in users:
    print(user)

conn.close()
import sqlite3

#connection = sqlite3.connect(":memory:")
connection = sqlite3.connect("first.db")

cursor = connection.cursor()
cursor.execute("DROP TABLE IF EXISTS users")
cursor.execute("CREATE TABLE users(userId INT)")

connection.commit()
connection.close()

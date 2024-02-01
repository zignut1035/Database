import sqlite3
connection : sqlite3.Connection = sqlite3.connect("first.db")
cursor : sqlite3.Cursor = connection.cursor()
cursor.execute("DROP TABLE IF EXISTS users")
cursor.execute('''
  CREATE TABLE users (
    userId INTEGER NOT NULL,
    age SMALLINT,
    name TEXT,
    PRIMARY KEY (userId)           
  )             
''')
connection.commit()
cursor.execute('''
    INSERT INTO users (age, name) VALUES
    (19, "Minna"),
    (58, "Matti")
''')
usersFound = cursor.execute("SELECT COUNT(*) FROM users").fetchone()[0]
if usersFound == 1:
    print("One User Found")
elif usersFound > 1:
    print("Multiple Users Found")
else:
    print("No User Found")

# Insert user with qmark style
user = 'Tony'
cursor.execute('INSERT INTO users (age, name) VALUES (?, ?)',(80, user,))

# Insert user with named style
newUser = {"age":60,"name":"Matt"}
cursor.execute("INSERT INTO users (age, name) VALUES (:age, :name)", newUser)

users = [
    (11, "Sanni"),
    (61, "Markku"),
    (88, "Ann")
]
cursor.executemany("INSERT INTO users (age, name) VALUES (?, ?)", users)
for row in cursor.execute("SELECT * FROM users"):
    print(row)

import re
def removeSpecialCharacters(text):
    return re.sub('[^A-Za-z0-9,]+',"", text)
tableName = "cars!!_"
columns = "carId INTEGER, NAME TEXT"
cursor.execute(f"DROP TABLE IF EXISTS {removeSpecialCharacters(tableName)}")
cursor.execute(f"CREATE TABLE {removeSpecialCharacters(tableName)} ({removeSpecialCharacters(columns)})")

connection.commit()
connection.close()
import sqlite3
import requests

user_num = 20
api_url = 'https://randomuser.me/api/?results=' + str(user_num)

response = requests.get(api_url)

print(f"API URL: {api_url}")
data = response.json()
connection: sqlite3.Connection = sqlite3.connect("users.db")
cursor: sqlite3.Cursor = connection.cursor()
cursor.execute("DROP TABLE IF EXISTS Users")
cursor.execute('''
    CREATE TABLE Users (
        userId INTEGER NOT NULL,
        firstname TEXT,
        lastname TEXT,               
        email TEXT,
        PRIMARY KEY (userId)           
    )             
''')

cursor.execute("DROP TABLE IF EXISTS UserAddresses")
cursor.execute('''
    CREATE TABLE UserAddresses (
        userAddressId INTEGER NOT NULL,
        street_number INTEGER,
        street_name TEXT,
        city TEXT,               
        country TEXT,
        postcode INTEGER,
        userId INTEGER,
        PRIMARY KEY (userAddressId),
        FOREIGN KEY (userId) REFERENCES Users(userId)                      
    )             
''')

cursor.execute("DROP TABLE IF EXISTS UserPictures")
cursor.execute('''
    CREATE TABLE UserPictures (
        userPictureId INTEGER NOT NULL,
        largeImg BLOB,
        mediumImg BLOB,               
        thumbnailImg BLOB,
        userId INTEGER,
        PRIMARY KEY (userPictureId),
        FOREIGN KEY (userId) REFERENCES Users(userId)           
    )             
''')

connection.commit()

if data and 'results' in data:
    random_users = data['results']

    if random_users:
        for userId, user in enumerate(random_users, start=1):
            firstname = user.get('name', {}).get('first', '')
            lastname = user.get('name', {}).get('last', '')
            email = user.get('email', '')

            cursor.execute('INSERT INTO Users (firstname, lastname, email) VALUES (?, ?, ?)',
                           (firstname, lastname, email))

            location = user.get('location', {})
            street = location.get('street', {})
            number = street.get('number', '')
            name = street.get('name', '')
            city = location.get('city', '')
            country = location.get('country', '')
            postcode = location.get('postcode', '')

            cursor.execute('INSERT INTO UserAddresses (street_number, street_name, city, country, postcode, userId) VALUES (?, ?, ?, ?, ?, ?)',
                           (number, name, city, country, postcode, userId))

            picture = user.get('picture', {})
            largeImg = picture.get('large', '')
            mediumImg = picture.get('medium', '')
            thumbnailImg = picture.get('thumbnail', '')

            cursor.execute('INSERT INTO UserPictures (largeImg, mediumImg, thumbnailImg, userId) VALUES (?, ?, ?, ?)',
                           (largeImg, mediumImg, thumbnailImg, userId))

        connection.commit()

cursor.close()
connection.close()

# Create a script that
# 1. Reads contents of the files users.csv, purchases.csv, and purchaseParts.csv
# 2. Creates a new database called purchases.db
# 3. Creates tables for each of the csv files called: users, purchases, and purchaseParts
# 4. Inserts the data for each of the tables
# 5. Finally, join data from all the 3 tables and print it all out. Order the data by "users.email" ascending.
#    Expected output should be like this:
#      (3, 'danny@boy.com', 1, 3, 1, 1, 'Poster')
#      (3, 'danny@boy.com', 2, 3, 2, 2, 'Nail Clipper')
#      (5, 'f51wt@mymail.com', 4, 5, 5, 4, 'Monitor')
#      (5, 'f51wt@mymail.com', 4, 5, 6, 4, 'Keyboard')
#      (2, 'my@mail.com', 3, 2, 3, 3, 'Laptop')
#      (2, 'my@mail.com', 3, 2, 4, 3, 'Monitor')

import sqlite3  # For communicating with sqlite databases

database = "purchases.db"
filenames = ["users.csv", "purchases.csv", "purchaseParts.csv"]

connection = sqlite3.connect(database)  # Initialize connection to database, we could also use the parameter :memory:
cursor = connection.cursor()  # Fetch cursor from connection

def dropAndCreateTable(cursor, tableName, field, foreign_keys=None):
    cursor.execute(f'DROP TABLE IF EXISTS {tableName}')
    create_table_query = f'CREATE TABLE {tableName} ({field}'
    if foreign_keys:
        create_table_query += f', {foreign_keys}'
    create_table_query += ')'
    cursor.execute(create_table_query)

def insertData(cursor, tableName, data_values):
    placeholders = ",".join(["?" for _ in range(len(data_values))])
    cursor.execute(f'INSERT INTO {tableName} VALUES ({placeholders})', data_values)
    
# Loop through all the files
for filename in filenames:
    file = open(filename, "r")  # Open a file
    lines = file.readlines()  # Lines of the file are now stored here
    print("File: " + filename)
    index = 0  # Create an index variable so we can determine if it is a header or actual data for the table
    # Loop through lines inside the files
    
    for line in lines:
        tableName = filename.replace(".csv", "")
        print("Table name: " + tableName)
        print("line: " + line)
        data_values = line.strip().split(',')
        if index == 0:
            header_fields = [field.replace(' ', '_') for field in data_values]
            dropAndCreateTable(cursor, tableName, ",".join(header_fields))
        else:
            insertData(cursor, tableName, data_values)
        if index < len(lines) - 1:
            print("index: " + str(index))
        index += 1

connection.commit()


# If index is 0, this is a header for the table. In this case, we need to split the columns by comma
# and drop + create the table using the function dropAndCreateTable(...)

# If index is 1, this is data for a table. Use function insertData(...) to insert the data into the
# corresponding table

# Part 2: We just need to create a JOIN statement to get all the results and then loop them and
# print out the results
cursor.execute('''SELECT * FROM users
               JOIN purchases ON users.userId = purchases.userId
               JOIN purchaseParts ON purchaseParts.purchaseId = purchases.purchaseId
               ORDER BY users.email ASC''')
result = cursor.fetchall()
formatted_result = []
for ans in result:
    formatted_row = tuple(int(value.strip('"')) if value.isdigit() else value.strip('"') for value in ans)
    formatted_result.append(formatted_row)
for Ans in formatted_result:
    print(Ans)
connection.commit()
connection.close()

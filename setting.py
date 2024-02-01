import sqlite3
connection : sqlite3.Connection = sqlite3.connect("setting.db")
cursor : sqlite3.Cursor = connection.cursor()
cursor.execute("DROP TABLE IF EXISTS setting")
cursor.execute('''
  CREATE TABLE setting (
    settingId INTEGER NOT NULL,
    urlKey TEXT NOT NULL,
    urlValue TEXT,
    PRIMARY KEY (settingId)           
  )             
''')
connection.commit()
valid_commands = ['store setting', 'view all settings', 'view setting', 'delete setting', 'exit']
while True:
    command = input('What do you want to do?: ').strip().lower()
    if command in valid_commands:
        if command == 'store setting':
            key = input('What is the key?: ')
            value = input('What is the value?: ')
            cursor.execute('INSERT INTO setting (urlKey, urlValue) VALUES (?, ?)',(key,value))
            print("The key and value has been stored")
            connection.commit()
            cursor.execute('UPDATE setting SET urlValue=? WHERE urlKey=?',(value,key))
            print('The value has been updated')
            connection.commit()
        elif command == 'view all settings':
            cursor.execute('SELECT * FROM setting')
            result = cursor.fetchall()
            print('The setting is showing')
            for ans in result:
                print(ans)
            connection.commit()
        elif command == 'view setting':
            view = input('Which key do you want to view?: ')
            cursor.execute('SELECT urlValue FROM setting WHERE urlKey=?',(view,))
            result = cursor.fetchone()
            if result is not None:
                print(f'key {view} is {result[0]}')
            else:
                print('This key does not exist')
            connection.commit()
        elif command == 'delete setting':
            delete = input('What key do you want to delete?: ')
            cursor.execute("DELETE FROM setting WHERE urlKey=?",(delete,))
            connection.commit()
            if cursor.rowcount > 0:
                print('The key has been deleted')
            else:
                print('This key does not exist')
            
        elif command == 'exit':
            connection.commit()
            print('Quit the application')
            break
    else:
        print('Please type in English')
cursor.close()
connection.close()

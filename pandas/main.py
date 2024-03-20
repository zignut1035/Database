import pandas as pd
from sqlite3 import connect

df = pd.read_csv('pandas/testusers.csv', encoding="UTF-8")

engine = connect(":memory:")
df.to_sql('users', engine)

print(df)
print("ALL COLUMNS:")
columns = ""
for column in df: columns += f",{column}"
print(columns)

def getFirstRow() -> pd.DataFrame:
    sql = "SELECT * FROM users LIMIT 1"
    df = pd.read_sql_query(sql, engine)
    return df
print(getFirstRow())

def getAllNames() -> pd.DataFrame:
    sql = "SELECT Name FROM users"
    df = pd.read_sql_query(sql, engine)
    return df
print("All names:")
print(getAllNames())

def getSpecificUser(name : str) -> pd.DataFrame:
    sql = f'''
            SELECT Name AS NAME, Title AS TITLE
            FROM users WHERE Name = '{name}'
            '''
    df = pd.read_sql_query(sql, engine)
    return df
print("Specific user:")
print(getSpecificUser("Jane Smith"))
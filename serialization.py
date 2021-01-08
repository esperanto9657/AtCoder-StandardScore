import pandas as pd
import sqlite3

db_name = "AtCoder.db"
table_name = "users"

def save_data(df):
    with sqlite3.connect(db_name) as connection:
        df.to_sql(table_name, connection, if_exists = "replace", index = False)
        connection.commit()

def load_data():
    query = "select * from users"
    with sqlite3.connect(db_name) as connection:
        df = pd.read_sql_query(query, connection)
    return df
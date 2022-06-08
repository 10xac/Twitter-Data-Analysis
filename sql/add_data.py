import os
from config import config
import pandas as pd
import mysql.connector as mysql
from mysql.connector import Error
from configparser import ConfigParser

config = ConfigParser()
file = 'config.ini'
config.read(file)

config['aws']['host']
config['aws.server.com']['user']
config['aws.server.com']['passwd']

def DBConnect(host_name, user_name, user_passwd, dbName=None):
    try :
        conn = mysql.connect(host=host_name, user=user_name, password=user_passwd,
                         database=dbName, buffered=True)
        cur = conn.cursor()
        print('Database Connection Succesfully Completed')
    except Error as err: 
        print(f'Error "{err}"')
    return conn, cur

def emojiDB(dbName: str) -> None:
    conn, cur = DBConnect(config['aws']['host'], config['aws.server.com']['user'], config['aws.server.com']['passwd'], dbName)
    try:
        dbQuery = f"ALTER DATABASE {dbName} CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;"
        cur.execute(dbQuery)
        conn.commit()
        print('Alter Completed')
    except Error as err:
        print(f'Error "{err}" ecounted')

def createDB(dbName: str) -> None:
    try:
        conn, cur = DBConnect(config['aws']['host'], config['aws.server.com']['user'], config['aws.server.com']['passwd'])
        cur.execute(f"CREATE DATABASE IF NOT EXISTS {dbName};")
        conn.commit()
        cur.close()
        print('Database Created Successfully')
    except Error as err:
        print(f'Error "{err}" ecounted')
    

def createTables(dbName: str) -> None:
    conn, cur = DBConnect(config['aws']['host'], config['aws.server.com']['user'], config['aws.server.com']['passwd'], dbName)
    sqlFile = 'schema.sql'
    fd = open(sqlFile, 'r')
    readSqlFile = fd.read()
    fd.close()

    sqlCommands = readSqlFile.split(';')

    for command in sqlCommands:
        try:
            res = cur.execute(command)
        except Exception as ex:
            print("Command skipped: ", command)
            print(ex)
    conn.commit()
    cur.close()

    return

def preprocess_df(df: pd.DataFrame) -> pd.DataFrame:
    # cols_2_drop = ['original_text']
    try:
        # df = df.drop(columns=cols_2_drop, axis=1)
        df = df.fillna(0)
    except KeyError as e:
        print("Error:", e)

    return df


def insert_to_tweet_table(dbName: str, df: pd.DataFrame, table_name: str) -> None:
    conn, cur = DBConnect(config['aws']['host'], config['aws.server.com']['user'], config['aws.server.com']['passwd'],dbName)

    df = preprocess_df(df)

    for _, row in df.iterrows():
        sqlQuery = f"""INSERT INTO {table_name} (statuses_count, created_at, source, original_text, clean_tweet, polarity, subjectivity, lang,
                    favorite_count, retweet_count, screen_name, followers_count, friends_count, sensitivity,
                    hashtags, user_mentions, place)
             VALUES(%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        data = (row[0], row[1], row[2], row[3], (row[4]), (row[5]), row[6], row[7], row[8], row[9], row[10], row[11], 
                (row[12]), (row[13]), (row[14]), (row[15]), (row[16]))

        try:
            # Execute the SQL command
            cur.execute(sqlQuery, data)
            # Commit your changes in the database
            conn.commit()
            print("Data Inserted Successfully")
        except Exception as e:
            conn.rollback()
            print("Error: ", e)
    return

def db_execute_fetch(*args, many=False, tablename='', rdf=True, **kwargs) -> pd.DataFrame:
    connection, cursor1 = DBConnect(config['aws']['host'], config['aws.server.com']['user'], config['aws.server.com']['passwd'],**kwargs)
    if many:
        cursor1.executemany(*args)
    else:
        cursor1.execute(*args)

    # get column names
    field_names = [i[0] for i in cursor1.description]

    # get column values
    res = cursor1.fetchall()

    # get row count and show info
    nrow = cursor1.rowcount
    if tablename:
        print(f"{nrow} recrods fetched from {tablename} table")

    cursor1.close()
    connection.close()

    # return result
    if rdf:
        return pd.DataFrame(res, columns=field_names)
    else:
        return res


if __name__ == "__main__":
    createDB(dbName='tweets')
    emojiDB(dbName='tweets')
    createTables(dbName='tweets')
    
    df = pd.read_csv('../data/clean_economic_data.csv')
    try: 
        insert_to_tweet_table(dbName='tweets', df=df, table_name='TweetInformation')
    except Exception as err: 
        print(f'Variable "{err}"')
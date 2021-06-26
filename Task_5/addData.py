import os
import pandas as pd
import mysql.connector as mysql
from mysql.connector import Error


def ConnectDatabase(dbName=None):
    conn = mysql.connect(host='192.168.1.1', user='root', password='rootroot',
                         database=dbName, buffered=True)
    cur = conn.cursor()
    return conn, cur


def Alterdatabse(dbName: str) -> None:
    conn, cur = ConnectDatabase(dbName)
    dbQuery = f"ALTER DATABASE {dbName} CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;"
    cur.execute(dbQuery)
    conn.commit()


def createdatabase(dbName: str) -> None:
    conn, cur = ConnectDatabase()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {dbName};")
    conn.commit()
    cur.close()


def createTables(dbName: str) -> None:
    conn, cur = ConnectDatabase(dbName)
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
    df['possibly_sensitive'] = df['possibly_sensitive'].fillna(0)
    df['place'] = df['place'].fillna(" ")

    df['hashtags'] = df['hashtags'].fillna(" ")
    df['user_mentions'] = df['user_mentions'].fillna(" ")

    df['retweet_count'] = df['retweet_count'].fillna(0)
   
    return df


def insert_to_tweet_table(dbName: str, df: pd.DataFrame, table_name: str) -> None:
    conn, cur = ConnectDatabase(dbName)

    df = preprocess_df(df)

    for _, row in df.iterrows():
        sqlQuery = f"""INSERT INTO {table_name} (created_at, source, original_text, polarity, subjectivity, lang,
                    favorite_count, retweet_count, original_author, followers_count, friends_count, possibly_sensitive,
                    hashtags, user_mentions, place, clean_text)
             VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        data = (row[0], row[1], row[2], row[3], (row[4]), (row[5]), row[6], row[7], row[8], row[9], row[10], row[11],
                row[12], row[13], row[14], row[15])

        try:
            cur.execute(sqlQuery, data)
            conn.commit()
            print("Data Inserted Successfully")
        except Exception as e:
            conn.rollback()
            print("Error: ", e)
    return


def db_execute_fetch(*args, many=False, tablename='', rdf=True, **kwargs) -> pd.DataFrame:
    connection, cursor1 = ConnectDatabase(**kwargs)
    if many:
        cursor1.executemany(*args)
    else:
        cursor1.execute(*args)

    field_names = [i[0] for i in cursor1.description]
    res = cursor1.fetchall()
    nrow = cursor1.rowcount
    if tablename:
        print(f"{nrow} recrods fetched from {tablename} table")
    cursor1.close()
    connection.close()
    if rdf:
        return pd.DataFrame(res, columns=field_names)
    else:
        return res
if __name__ == "__main__":
    createdatabase(dbName='tweets')
    Alterdatabse(dbName='tweets')
    createTables(dbName='tweets')

    df = pd.read_csv('../cleaned_tweet_data.csv')
    df.info()

    insert_to_tweet_table(dbName='tweets', df=df,
                          table_name='TweetInformation')
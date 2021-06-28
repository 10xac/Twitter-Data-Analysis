import pandas as pd
import psycopg2
from psycopg2 import Error
from decouple import config

postgres_user, postgres_pass = config('postgres_user'), config('postgres_pass')
# print(postgres_user, postgres_pass)

def DBConnect(dbName=None):
    """

    Parameters
    ----------
    dbName :
        Default value = None)

    Returns
    -------

    """
    try:
        conn = psycopg2.connect(host='localhost',
                                user=postgres_user,
                                password=postgres_pass,
                                database=dbName,
                                port="5432")

        cur = conn.cursor()
        conn.autocommit = True
        print('Connection Established')

    except (Exception, Error) as error:
        print(error)
        conn, cur = None, None

    return conn, cur

#
# def emojiDB(dbName: str) -> None:
#     conn, cur = DBConnect(dbName)
#     dbQuery = f"ALTER DATABASE {dbName} CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;"
#     cur.execute(dbQuery)
#     conn.commit()

def createDB(dbName: str) -> None:
    """

    Parameters
    ----------
    dbName :
        str:
    dbName :
        str:
    dbName:str :


    Returns
    -------

    """
    try:
        postgres_db = config('postgres_user')
        # print(postgres_db)
        conn, cur = DBConnect(postgres_db)
        sql = f"CREATE DATABASE {dbName};"
        cur.execute(sql)
        # conn.commit()
        cur.close()

    except (Exception, Error) as e:
        print(e)

def createTables(dbName: str) -> None:
    """

    Parameters
    ----------
    dbName :
        str:
    dbName :
        str:
    dbName:str :


    Returns
    -------

    """
    conn, cur = DBConnect(dbName)
    sqlFile = 'table_schema.sql'
    fd = open(sqlFile, 'r')
    readSqlFile = fd.read()
    fd.close()

    sqlCommands = readSqlFile.split(';')

    for command in sqlCommands:
        try:
            res = cur.execute(command)
            response = "Table created sucessfuly"
        except Exception as ex:
            print("Command skipped: ", command)
            response = "Table Not Created"
            print(ex)
    conn.commit()
    cur.close()

    return print(response)

def preprocess_df(df: pd.DataFrame) -> pd.DataFrame:
    """

    Parameters
    ----------
    df :
        pd.DataFrame:
    df :
        pd.DataFrame:
    df:pd.DataFrame :


    Returns
    -------

    """
    cols_2_drop = ['Unnamed: 0', 'timestamp']
    try:
        df = df.drop(columns=cols_2_drop, axis=1)
        df = df.fillna(0)
    except KeyError as e:
        print("Error:", e)

    return df


def insert_to_tweet_table(dbName: str, df: pd.DataFrame, table_name: str) -> None:
    """

    Parameters
    ----------
    dbName :
        str:
    df :
        pd.DataFrame:
    table_name :
        str:
    dbName :
        str:
    df :
        pd.DataFrame:
    table_name :
        str:
    dbName:str :

    df:pd.DataFrame :

    table_name:str :


    Returns
    -------

    """
    conn, cur = DBConnect(dbName)

    df = preprocess_df(df)

    for _, row in df.iterrows():
        sqlQuery = f"""INSERT INTO {table_name} (created_at, source, clean_text, language, favorite_count,retweet_count, 
                                                polarity, subjectivity, original_author, followers_count,  
                                                friends_count,sensitivity,hashtags, user_mentions, place)
             VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        data = (row[0], row[1], row[2], row[3], (row[5]), (row[6]), row[7], row[8], row[9], row[10], row[11], row[12],
                row[13], row[14], row[15])

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
    """

    Parameters
    ----------
    *args :

    many :
         (Default value = False)
    tablename :
         (Default value = '')
    rdf :
         (Default value = True)
    **kwargs :


    Returns
    -------

    """
    connection, cursor1 = DBConnect(**kwargs)
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
    # emojiDB(dbName='tweets')
    createTables(dbName='tweets')

    df = pd.read_csv('processed_tweet_data.csv')
    print(df.head())

    insert_to_tweet_table(dbName='tweets', df=df, table_name='TweetInformation')
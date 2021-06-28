from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import pandas as pd
import yaml
import logging
logger = logging.getLogger('ftpuploader')
app = Flask(__name__)



# def DBConnect():
    #configure DB
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
# print('Connected to DB')

mysql = MySQL(app)


    # return mysql

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        userDetails = request.form
        name = userDetails['name']
        email = userDetails['email']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name, email) VALUES(%s, %s)", (name, email)) 
        mysql.connection.commit()
        cur.close()
        return '<h1>Successfully added to db!</h1>'
        # return redirect('/tweets')
    return render_template('index.html')


@app.route('/add-data', methods=['GET', 'POST'])
def indexRoute():
    if request.method == 'POST':
        df = pd.read_csv('processed_tweet_data.csv')
        df = df.fillna(0)
        cur = mysql.connection.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS `TweetssLastsss` (`id` INT NOT NULL AUTO_INCREMENT, `created_at` TEXT NOT NULL, `source` VARCHAR(200) NOT NULL, `polarity` FLOAT DEFAULT NULL,   `subjectivity` FLOAT DEFAULT NULL, `lang` TEXT DEFAULT NULL,  `favorite_count`INT DEFAULT NULL,  `retweet_count` INT DEFAULT NULL,   `original_author` TEXT DEFAULT NULL,`followers_count` INT DEFAULT NULL,`friends_count` INT DEFAULT NULL, `possibly_sensitive` text DEFAULT NULL, `hashtags` TEXT DEFAULT NULL,`user_mentions` TEXT DEFAULT NULL,`location` TEXT DEFAULT NULL, `clean_text` TEXT DEFAULT NULL, PRIMARY KEY (`id`))")

        # cur.execute("INSERT INTO TweetInformation(name, email) VALUES(%s, %s)", (name, email)) 
        mysql.connection.commit()
        for _, row in df.iterrows():
            insert_stmt = (
            "INSERT INTO TweetssLastsss (created_at, source, polarity, subjectivity, lang, favorite_count, retweet_count, original_author, followers_count, friends_count, possibly_sensitive, hashtags,  user_mentions, location, clean_text) "
            "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            )

            data = (row[1], row[2], row[3], (row[4]), (row[5]), row[6], row[7], row[8], row[9], row[10], row[11],
                    row[12], row[13], row[14], row[15])
    
            try:
                cur.execute(insert_stmt, data)
                mysql.connection.commit()
                # print('DATA INSERTED')
            except Exception as e:
             logger.error('Failed to upload to ftp: '+ str(e))
    return '<h1>Successfully Inserted into DB!</h1>'
        # return redirect('/tweets')
    # return render_template('index.html')
    # insert_to_tweet_table(dbName='tweets', df=df, table_name='TweetInformation')

@app.route('/tweets')
def tweets():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM TweetInformation");
    if resultValue > 0:
        tweetDetails = cur.fetchall()
        return render_template('tweets.html', tweetDetails)


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
    # cols_2_drop = ['Unnamed: 0', 'timestamp', 'sentiment', 'possibly_sensitive', 'original_text']
    try:
        # df = df.drop(columns=cols_2_drop, axis=1)
        df = df.fillna(0)
    except KeyError as e:
        print("Error other here:", e)

    return df


@app.route('/insert', methods=['GET', 'POST'])
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
    # DBConnect()
    # print(mysql.connection)

    # cur = mysql.connection.cursor()
    # conn = mysql.connection.commit()
    db = yaml.load(open('db.yaml'))
    app.config['MYSQL_HOST'] = db['mysql_host']
    app.config['MYSQL_USER'] = db['mysql_user']
    app.config['MYSQL_PASSWORD'] = db['mysql_password']
    app.config['MYSQL_DB'] = db['mysql_db']

    mysql = MySQL(app)
    cur = mysql.connection.cursor()

    df = preprocess_df(df)

    for _, row in df.iterrows():
        sqlQuery = f"""INSERT INTO {table_name} (created_at, source, polarity, subjectivity, original_text, lang, favorite_count, retweet_count, original_author, followers_count, friends_count, possibly_sensitive, hashtags,  user_mentions, location)
             VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        data = (row[0], row[1], row[2], row[3], (row[4]), (row[5]), row[6], row[7], row[8], row[9], row[10], row[11],
                row[12], row[13], row[14])

        try:
            # Execute the SQL command
            cur.execute(sqlQuery, data)
            # Commit your changes in the database
            mysql.connection.commit()
            cur.close()
            print("Data Inserted Successfully")
            return '<h1>Data Inserted Successfully!</h1>'
        except Exception as e:
            # mysql.connection.rollback()
            print("Error Here: ", e)
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

if __name__ == '__main__':
    app.run(debug=True)


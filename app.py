from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import pandas as pd
import yaml

app = Flask(__name__)



def DBConnect():
    #configure DB
    db = yaml.load(open('db.yaml'))
    app.config['MYSQL_HOST'] = db['mysql_host']
    app.config['MYSQL_USER'] = db['mysql_user']
    app.config['MYSQL_PASSWORD'] = db['mysql_password']
    app.config['MYSQL_DB'] = db['mysql_db']
    
mysql = MySQL(app) 

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        userDetails = request.form
        name = userDetails['name']
        email = userDetails['email']
        cur = mysql.connection.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS `TweetInformation` (`id` INT NOT NULL AUTO_INCREMENT, `created_at` TEXT NOT NULL, `source` VARCHAR(200) NOT NULL,  `clean_text` TEXT DEFAULT NULL, `polarity` FLOAT DEFAULT NULL,   `subjectivity` FLOAT DEFAULT NULL,   `language` TEXT DEFAULT NULL,  `favorite_count` INT DEFAULT NULL,  `retweet_count` INT DEFAULT NULL,   `original_author` TEXT DEFAULT NULL,   `screen_count` INT NOT NULL,`followers_count` INT DEFAULT NULL,`friends_count` INT DEFAULT NULL,`hashtags` TEXT DEFAULT NULL,`user_mentions` TEXT DEFAULT NULL,`place` TEXT DEFAULT NULL,`place_coordinate` VARCHAR(100) DEFAULT NULL,PRIMARY KEY (`id`))")
        cur.execute("INSERT INTO TweetInformation(name, email) VALUES(%s, %s)", (name, email)) 
        mysql.connection.commit()
        cur.close()
        return redirect('/tweets')
    return render_template('index.html')

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
    cols_2_drop = ['Unnamed: 0', 'timestamp', 'sentiment', 'possibly_sensitive', 'original_text']
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
        sqlQuery = f"""INSERT INTO {table_name} (created_at, source, clean_text, polarity, subjectivity, language,
                    favorite_count, retweet_count, original_author, screen_count, followers_count, friends_count,
                    hashtags, user_mentions, place, place_coordinate)
             VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        data = (row[0], row[1], row[2], row[3], (row[4]), (row[5]), row[6], row[7], row[8], row[9], row[10], row[11],
                row[12], row[13], row[14], row[15])

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


if __name__ == '__main__':
    app.run(debug=True)
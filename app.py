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

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         userDetails = request.form
#         name = userDetails['name']
#         email = userDetails['email']
#         cur = mysql.connection.cursor()
#         cur.execute("INSERT INTO users(name, email) VALUES(%s, %s)", (name, email)) 
#         mysql.connection.commit()
#         cur.close()
#         return '<h1>Successfully added to db!</h1>'
#         # return redirect('/tweets')
#     return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        df = pd.read_csv('processed_tweet_data.csv')
        df = df.fillna(0)
        # print(df.columns)
        # userDetails = request.form
        # name = userDetails['name']
        # email = userDetails['email']
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
            # cur.execute(insert_stmt, data)
            # mysql.connection.commit()
            # print('DATA INSERTED')


            #  created_at source  polarity subjectivity original_text lang favorite_count retweet_count original_author followers_count friends_count possibly_sensitive hashtags user_mentions location
    
            try:
                cur.execute(insert_stmt, data)
                mysql.connection.commit()
                print('DATA INSERTED')
            #     # Execute the SQL command
            #     cur.execute(insert_stmt, data, multi=True)
            #     # Commit your changes in the database
            #     mysql.connection.commit()
            #     cur.close()
            #     print("Data Inserted Successfully")
            #     return '<h1>Data Inserted Successfully!</h1>'
            except Exception as e:
            #     # mysql.connection.rollback()
                # print("Error Here: ", e)
                logger.error('Failed to upload to ftp: '+ str(e))
            # cur.execute()
            # cur.close()
        return '<h1>Successfully Inserted into DB!</h1>'
        # return redirect('/tweets')
    # return render_template('index.html')
    insert_to_tweet_table(dbName='tweets', df=df, table_name='TweetInformation')

@app.route('/tweets')
def tweets():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM TweetInformation");
    if resultValue > 0:
        tweetDetails = cur.fetchall()
        return render_template('tweets.html', tweetDetails)



if __name__ == '__main__':
    # db = yaml.load(open('db.yaml'))
    # app.config['MYSQL_HOST'] = db['mysql_host']
    # app.config['MYSQL_USER'] = db['mysql_user']
    # app.config['MYSQL_PASSWORD'] = db['mysql_password']
    # app.config['MYSQL_DB'] = db['mysql_db']
    # mysql = MySQL(app)
    # df = pd.read_csv('processed_tweet_data.csv')
    # print(df.head())
    # insert_to_tweet_table(dbName='tweets', df=df, table_name='TweetInformation')
    # for _, row in df.iterrows():
    #     print(row[0])
    #     break
    app.run(debug=True)
    # DBConnect()   
    # mysql = MySQL(app) 


    # CREATE TABLE TweetInformation(created_at varchar(40), source varchar(50), polarity float(15), subjectivity float(15), original_text varchar(400), lang varchar(10), favorite_count float(15), retweet_count float(15), original_author varchar(20), followers_count int(15), friends_count int(15), possibly_sensitive varchar(20), hashtags varchar(50), user_mentions varchar(50), location varchar(30));


    # Name: 1025, dtype: object
# created_at                               Fri Jun 18 19:13:38 +0000 2021
# source                <a href="http://twitter.com/download/iphone" r...
# polarity                                                      -0.522222
# subjectivity                                                          1
# original_text                                                       NaN
# lang                                                                 en
# favorite_count                                                      NaN
# retweet_count                                                       NaN
# original_author                                         Alaskacryptogi1
# followers_count                                                    6705
# friends_count                                                      7330
# possibly_sensitive                                                  NaN
# hashtags                                                            NaN
# user_mentions                                                       NaN
# location       


#  created_at source  polarity subjectivity original_text lang favorite_count retweet_count original_author followers_count friends_count possibly_sensitive hashtags user_mentions location
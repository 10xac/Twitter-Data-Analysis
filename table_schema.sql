CREATE TABLE TweetInformation
(
    id SERIAL PRIMARY KEY,
    created_at TEXT NOT NULL,
    source VARCHAR(200) NOT NULL,
    clean_text TEXT DEFAULT NULL,
    polarity FLOAT DEFAULT NULL,
    subjectivity FLOAT DEFAULT NULL,
    language TEXT DEFAULT NULL,
    favorite_count INT DEFAULT NULL,
    retweet_count INT DEFAULT NULL,
    original_author TEXT DEFAULT NULL,
    followers_count INT DEFAULT NULL,
    friends_count INT DEFAULT NULL,
    hashtags TEXT DEFAULT NULL,
    sensitivity TEXT DEFAULT NULL,
    user_mentions TEXT DEFAULT NULL,
    place TEXT DEFAULT NULL
)
-- ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_unicode_ci;
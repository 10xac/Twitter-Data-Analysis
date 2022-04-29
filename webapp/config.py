import os


class DBConfig:
    USER = os.environ.get('root')
    PWORD = os.environ.get('root')
    HOST = os.environ.get('localhost')

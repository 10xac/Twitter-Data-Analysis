import os

class DBConfig:
    USER = os.environ.get('root')
    PWORD = os.environ.get('root')
    HOST = os.environ.get('localhost')

if __name__:'__main__':
    print(type(os.environ.get('root')))

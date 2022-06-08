# from configparser import ConfigParser


# with open ('config.ini', 'w') as file: 
#     config.write(file)

from configparser import ConfigParser
config = ConfigParser()
# config['DEFAULT'] = {'ServerAliveInterval': '45',
#                      'Compression': 'yes',
#                      'CompressionLevel': '9'}
# config['aws'] = {}
# config['aws']['host'] = 'database-1.co54fdfg9rmy.us-east-1.rds.amazonaws.com'
# config['aws.server.com'] = {}
# topsecret = config['aws.server.com']
# topsecret['user'] = 'admin'     # mutates the parser
# topsecret['passwd'] = 'admin123'  # same here
# config['DEFAULT']['ForwardX11'] = 'yes'
# with open('sql/config.ini', 'w') as configfile:
#   config.write(configfile)

file = 'config.ini'
# config = ConfigParser()
config.read(file)
print(config.sections())
print(config['aws']['host'])



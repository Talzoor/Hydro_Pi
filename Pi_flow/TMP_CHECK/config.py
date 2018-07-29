class Configuration(object):
    DATABASE = {
        'name': 'Readings',
        'engine': 'peewee.MySQLDatabase',
        'user': 'root',
        'passwd': 'root'
    }
    DEBUG = True
    SECRET_KEY = 'tz'

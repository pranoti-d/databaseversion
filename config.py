import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    MYSQL_HOST = 't'
    MYSQL_USER = ''
    MYSQL_PASSWORD = 'xxxxxxx'
    MYSQL_DB = ''
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = False
  

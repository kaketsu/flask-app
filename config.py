import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'YNWL'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://huajie:123456@localhost:3306/argus'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
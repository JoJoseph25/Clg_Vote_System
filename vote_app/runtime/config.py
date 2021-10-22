import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = '~t\x86\xc9\x1ew\x8bOcX\x85O\xb6\xa2\x11kL\xd1\xce\x7f\x14<y\x9e'
    JWT_SECRET_KEY = 'dasasdasdasd'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=3)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=15)
    REDDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    DEBUG = False
    HTTP_AUTHORIZATION = ""


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'vote_sys.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    PROPAGATE_EXCEPTIONS=True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'vote_sys.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS=True


config_by_name = dict(
    dev = DevelopmentConfig,
    prod = ProductionConfig
)
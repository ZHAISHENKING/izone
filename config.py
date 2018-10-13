import os, datetime
from local_settings import *


class Config(object):
    DEBUG = False
    TESTING = False

    SID = 1234567
    SAFE_KEY = "abc"
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    SECRET_KEY = 'abchghghhnnbkd'
    REMEMBER_COOKIE_DURATION = datetime.timedelta(hours=3)
    BABEL_DEFAULT_LOCALE = 'zh_CN'
    DB_USER = 'root'
    DB_PASSWORD = SQLPWD
    DB_HOST = 'localhost'
    DB_DB = 'izone'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql://' + DB_USER + ':' + DB_PASSWORD + '@' + DB_HOST + '/' + DB_DB

    # Flask-Security config
    SECURITY_URL_PREFIX = "/api/admin/"
    SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
    SECURITY_PASSWORD_SALT = "ATGUOHAELKiubahiughaerGOJAEGj"

    # Flask-Security URLs
    SECURITY_LOGIN_URL = "/api/login/"
    SECURITY_LOGOUT_URL = "/api/logout/"
    SECURITY_REGISTER_URL = "/api/reg/"

    SECURITY_POST_LOGIN_VIEW = "/api/admin/"
    SECURITY_POST_LOGOUT_VIEW = "/api/admin/"
    SECURITY_POST_REGISTER_VIEW = "/api/admin/"

    # Flask-Security features
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False

    # redis
    CACHE_TYPE = "redis"
    CACHE_REDIS_HOST = "127.0.0.1"
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = ""
    CACHE_REDIS_PASSWORD = ""

    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    DEBUG = True


class PrdConfig(Config):
    # DEBUG = False
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
    DEBUG = True

    WTF_CSRF_ENABLED = False


config = {
    'dev': DevConfig,
    'prd': PrdConfig,
    'testing': TestingConfig,
    'default': DevConfig,
}

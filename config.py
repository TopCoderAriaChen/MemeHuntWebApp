from datetime import timedelta
import os

class BaseConfig:
  SECRET_KEY = "your secret key"
  SQLALCHEMY_TRACK_MODIFICATIONS = False

  PERMANENT_SESSION_LIFETIME = timedelta(days=7)

  UPLOAD_IMAGE_PATH = os.path.join(os.path.dirname(__file__),"/static/images")

  PER_PAGE_COUNT = 10


class DevelopmentConfig(BaseConfig):

  SQLALCHEMY_DATABASE_URI0 = "mysql+pymysql://root:ttys024@127.0.0.1:3306/pythonbbs_final?charset=utf8mb4"

  SQLALCHEMY_DATABASE_URI = "sqlite:////Users/cnt68/Desktop/CITS5505-Group-Project/db.sqlite"

  MAIL_SERVER = "smtp.163.com"
  MAIL_USE_SSL = True
  MAIL_PORT = 465
  MAIL_USERNAME = "hynever@163.com"
  MAIL_PASSWORD = "1111111111111"
  MAIL_DEFAULT_SENDER = "hynever@163.com"

  # redis
  CACHE_TYPE = "RedisCache"
  CACHE_REDIS_HOST = "127.0.0.1"
  CACHE_REDIS_PORT = 6379

  # Celery
  # redis://:password@hostname:port/db_number
  CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
  CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"

  AVATARS_SAVE_PATH = os.path.join(BaseConfig.UPLOAD_IMAGE_PATH,"avatars")



class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI0 = "mysql+pymysql://[user]:[pass]@[IP]:[port]/pythonbbs?charset=utf8mb4"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    CELERY_BROKER_URL = 'memory://'
    CELERY_RESULT_BACKEND = 'rpc://'
    CACHE_TYPE = 'null'  # Disable caching for tests
    SERVER_NAME = 'localhost.localdomain'  # Set a valid SERVER_NAME
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"



class ProductionConfig(BaseConfig):
  SQLALCHEMY_DATABASE_URI0 = "mysql+pymysql://bbs:Bbs#hwygl123@127.0.0.1:3306/pythonbbs?charset=utf8mb4"

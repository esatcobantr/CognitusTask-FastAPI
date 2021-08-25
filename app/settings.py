import os
from dotenv import load_dotenv

load_dotenv()


class Settings(object):
    REDIS_URL = os.getenv("redis_url")
    DATABASE_HOST = os.getenv("db_host")
    DATABASE_PORT = os.getenv("db_port")
    DATABASE_USER = os.getenv("db_user")
    DATABASE_PASSWORD = os.getenv("db_password")
    DATABASE_NAME = os.getenv("db_name")
    SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}:{}/{}".format(
        DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT, DATABASE_NAME
    )

settings = Settings()



from dotenv import load_dotenv
from utils.config import CF as conf
from utils.path import ENV_PATH

load_dotenv(ENV_PATH)


class Config:
    DB_USER = conf.db.DB_USER
    DB_PASSWORD = conf.db.DB_PASSWORD
    DB_NAME = conf.db.DB_NAME
    DB_HOST = conf.db.DB_HOST
    DB_PORT = conf.db.DB_PORT
    DB_CONFIG = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
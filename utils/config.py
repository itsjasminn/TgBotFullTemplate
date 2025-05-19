from os import getenv
from pathlib import Path

from dotenv import load_dotenv

from utils.path import ENV_PATH

load_dotenv(ENV_PATH)



class DBConfig:
    DB_USER = getenv("DB_USER")
    DB_PASSWORD = getenv("DB_PASSWORD")
    DB_NAME = getenv("DB_NAME")
    DB_HOST = getenv("DB_HOST")
    DB_PORT = getenv("DB_PORT")


class WebConfig:
    ADMIN_USERNAME = getenv("ADMIN_USERNAME")
    ADMIN_PASSWORD = getenv("ADMIN_PASSWORD")


class PaymentConfig:
    PAY_APP = getenv("PAY_APP")
    PAY_TOKEN = getenv("PAY_TOKEN")

class BotConfig:
    TOKEN = getenv("TOKEN")


class CF:
    db = DBConfig()
    web = WebConfig()
    pay = PaymentConfig()
    bot = BotConfig()

import pymongo
import os

from datetime import timedelta
from environs import Env

env = Env()
env.read_env()

class Config:
    DB_USERNAME = env("DB_USERNAME")
    DB_PASSWORD = env("DB_PASS")
    DB_CLUSTER_NAME = env("DB_CLUSTER_NAME")
    DB_URI = env("DB_URI")

    DB_CONNECTION_URI = "mongodb+srv://" + DB_USERNAME + ":" + DB_PASSWORD + "@" + DB_URI
    DB_CONNECTION_STRING = pymongo.MongoClient("mongodb+srv://" + DB_USERNAME + ":" + DB_PASSWORD + "@" + DB_URI)
    DB_CLUSTER = DB_CONNECTION_STRING[DB_CLUSTER_NAME]

    COLLECTION_NAMES = {
        "logins": "logins",
        "user_stats": "user_stats",
        "user_schedule": "user_schedule"
    }

    SECRET_KEY = b"uP0tGp(.d:J:Uo}<AoeK|6r`XJ-*S0"
    DEBUG = False

    ACCESS_TOKEN_EXPIRY = timedelta(minutes=15)
    REFRESH_TOKEN_EXPIRY = timedelta(weeks=2)


class DevelopmentConfig:
    DEBUG = True


class TestingConfig:
    DEBUG = True


class ProductionConfig:
    DEBUG = False


by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    production=ProductionConfig
)
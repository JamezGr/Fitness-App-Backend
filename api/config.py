import pymongo
import os


class Config:
    DB_USERNAME = 'admin'
    DB_PASSWORD = '7VCbdWPGfZsXQ95s'
    DB_CLUSTER_NAME = 'fitness_app'
    DB_URI = 'fitness-app.bi9i8.mongodb.net/test?retryWrites=true&w=majority'

    DB_CONNECTION_STRING = pymongo.MongoClient("mongodb+srv://" + DB_USERNAME + ":" + DB_PASSWORD + "@" + DB_URI)
    DB_CLUSTER = DB_CONNECTION_STRING[DB_CLUSTER_NAME]

    COLLECTION_NAMES = {
        "logins": "logins"
    }

    SECRET_KEY = b"uP0tGp(.d:J:Uo}<AoeK|6r`XJ-*S0"
    DEBUG = False


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

key = Config.SECRET_KEY

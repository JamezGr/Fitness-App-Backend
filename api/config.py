import pymongo
import os

from datetime import timedelta
from environs import Env

env = Env()
env.read_env()

class Config:
    DB_USERNAME = env("DB_USERNAME")
    DB_PASSWORD = env("DB_PASS")
    DB_NAME = env("DB_NAME")
    DB_URI = env("DB_URI")

    REDIS_URL = env("REDISTOGO_URL")
    DB_CONNECTION_STRING = "mongodb+srv://" + DB_USERNAME + ":" + DB_PASSWORD + "@" + DB_URI

    SECRET_KEY = b"uP0tGp(.d:J:Uo}<AoeK|6r`XJ-*S0"
    DEBUG = False

    ACCESS_TOKEN_EXPIRY = timedelta(minutes=15)
    REFRESH_TOKEN_EXPIRY = timedelta(weeks=2)

    ENDPOINT_PREFIX = "/api"
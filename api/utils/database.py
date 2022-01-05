from flask_pymongo import PyMongo
from pymongo import MongoClient

from api.config import Config

client = MongoClient(Config.DB_CONNECTION_STRING)
db = client[Config.MAIN_DB_NAME]
file_db = client[Config.FILE_DB_NAME]
mongo = PyMongo()
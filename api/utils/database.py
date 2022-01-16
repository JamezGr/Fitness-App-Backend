import os
import sys
from flask_pymongo import PyMongo
from pymongo import MongoClient
from api.config import Config

import mongomock

def get_db_client():
    # check if unit tests are running
    if hasattr(sys, '_TEST_MODE'):
        return mongomock.MongoClient() 

    return MongoClient(Config.DB_CONNECTION_STRING)

client = get_db_client()
db = client[Config.MAIN_DB_NAME]
file_db = client[Config.FILE_DB_NAME]
mongo = PyMongo()
import base64
import os
import json
import re
import jsonschema


from flask import jsonify, url_for
from jsonschema import validate
from api.models.user import UserProfile
from api.utils import *
from api.config import Config, DevelopmentConfig, TestingConfig, ProductionConfig
from bson.json_util import dumps, loads
from bson.objectid import ObjectId

from datetime import datetime
import time
import calendar

salt = os.urandom(32)


class ManageForm(object):
    def __init__(self, user):
        self.user = user
    
    def delete_user(self): 
        db_cluster_collection = Config.DB_CLUSTER[Config.COLLECTION_NAMES["logins"]]
        user_to_delete = {"user": self.user}

        db_cluster_collection.delete_one(user_to_delete)

    def get_user_id(self): 
        db_cluster_collection = Config.DB_CLUSTER[Config.COLLECTION_NAMES["logins"]]
        user_to_find = db_cluster_collection.find_one({"user": self.user})

        try:
            user_id = user_to_find.get('_id')
            return str(user_id)

        except:
            return None

class UserProfileForm(object):
    def __init__(self, user, stats = None):
        self.user = user
        self.stats = stats

    def get_profile(self):
        db_cluster_collection = Config.DB_CLUSTER[Config.COLLECTION_NAMES["user_stats"]]

        user_id = ManageForm(self.user).get_user_id()        
        user_stats = db_cluster_collection.find_one({"user_id": user_id})

        return json.loads(dumps(user_stats))


    def update_profile(self):
        db_cluster_collection = Config.DB_CLUSTER[Config.COLLECTION_NAMES["user_stats"]]
        user_stats = self.get_profile()
        user_id = ManageForm(self.user).get_user_id()
        
        self.stats["user_id"] = user_id

        print(self.user)
        print(self.stats)
        
        if user_id is None:
            return None

        if user_stats is None:
            # db_cluster_collection.insert_one(self.stats)
            db_cluster_collection.insert_one(self.stats)

        else: 
            # db_cluster_collection.find_one_and_replace({'user_id': ObjectId(user_id)}, {'$set': self.stats})
            db_cluster_collection.replace_one({"user_id": user_id}, self.stats)

        return self.stats

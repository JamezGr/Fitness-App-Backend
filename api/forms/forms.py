import base64
import os
import json
import re
import jsonschema


from flask import jsonify, url_for
from jsonschema import validate
from api.models.user import UserProfile
from api.utils import *
from api.utils.database import db
from bson.json_util import dumps, loads
from bson.objectid import ObjectId

from datetime import datetime
import time
import calendar

salt = os.urandom(32)


class ManageForm(object):
    def __init__(self, user):
        self.user = user
        self.collection = db.logins
    
    def delete_user(self): 
        self.collection.delete_one({"user": self.user})

    def get_user_id(self): 
        user_to_find = self.collection.find_one({"user": self.user})

        try:
            user_id = user_to_find.get('_id')
            return str(user_id)

        except:
            return None

class UserProfileForm(object):
    def __init__(self, user, stats = None):
        self.user = user
        self.stats = stats
        self.collection = db.user_stats

    def get_profile(self):
        user_id = ManageForm(self.user).get_user_id()        
        user_stats = self.collection.find_one({"user_id": user_id})

        return json.loads(dumps(user_stats))


    def update_profile(self):
        user_stats = self.get_profile()
        user_id = ManageForm(self.user).get_user_id()
        
        self.stats["user_id"] = user_id

        if user_id is None:
            return None

        if user_stats is None:
            self.collection.insert_one(self.stats)

        else: 
            self.collection.replace_one({"user_id": user_id}, self.stats)

        return self.stats

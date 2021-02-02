import json

from api.config import Config, DevelopmentConfig, TestingConfig, ProductionConfig
from api.utils import user_auth

from bson.json_util import dumps, loads

class LoginForm(object):
    def __init__(self, form_data):
        self.user = form_data.user
        self.password = form_data.password


    def check_username_exists(self):
        db_cluster_collection = Config.DB_CLUSTER[Config.COLLECTION_NAMES["logins"]]
        users_found = db_cluster_collection.find({"user": {"$regex": '^' + self.user + '$'}})

        if users_found.count() > 0:
            return True
        else:
            return False


    def check_user_credentials(self):
        db_cluster_collection = Config.DB_CLUSTER[Config.COLLECTION_NAMES["logins"]]
        password = self.password

        try:
            users_found = db_cluster_collection.find({"user": {"$regex": '^' + self.user + '$'}})
            user_details = json.loads(dumps(users_found))[0]

            return user_auth.verify_password(user_details["password"], password)

        except IndexError:
            return False
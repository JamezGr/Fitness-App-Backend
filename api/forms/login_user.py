import json

from api.utils import user_auth
from api.utils.database import db

from bson.json_util import dumps, loads

class LoginForm(object):
    def __init__(self, form_data):
        self.user = form_data.user
        self.password = form_data.password
        self.collection = db.logins


    def check_username_exists(self):
        users_found = self.collection.find({"user": {"$regex": '^' + self.user + '$'}})

        if users_found.count() > 0:
            return True
        else:
            return False


    def check_user_credentials(self):
        try:
            users_found = self.collection.find({"user": {"$regex": '^' + self.user + '$'}})
            user_details = json.loads(dumps(users_found))[0]

            return user_auth.verify_password(user_details["password"], self.password)

        except IndexError:
            return False
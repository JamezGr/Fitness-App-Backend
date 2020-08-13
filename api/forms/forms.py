import base64
import os
from api.utils import *
import json
import re

from api.config import Config, DevelopmentConfig, TestingConfig, ProductionConfig
from bson.json_util import dumps, loads


salt = os.urandom(32)


class RegisterForm(object):

    USER_SETTINGS = {
        "MIN_LENGTH": 3,
        "MAX_LENGTH": 30,
        "ILLEGAL_CHARACTERS": list('&=()<>+,')
    }

    PASSWORD_SETTINGS = {
        "MIN_LENGTH": 8,
        "MAX_LENGTH": 32,

        # password must contain at least 3 character types
        "MUST_CONTAIN": {
            "UPPER_CASE_LETTERS": list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
            "LOWER_CASE_LETTERS": list("abcdefghijklmnopqrstuvwxyz"),
            "NUMBERS": list("0123456789"),
            "SYMBOLS": list("~!@#$%^&*_-+=`|\(){}[]:;'<>,.?/")}
    }

    def __init__(self, form_data):
        self.email = form_data.email
        self.user = form_data.user
        self.password = form_data.password
        self.confirm_password = form_data.confirm_password
    
    def validate(self):
        user_settings = RegisterForm.USER_SETTINGS
        password_settings = RegisterForm.PASSWORD_SETTINGS
        password_character_types = password_settings["MUST_CONTAIN"]

        password_character_types = sum([
            any(character_type in self.password for character_type in password_character_types["UPPER_CASE_LETTERS"]),
            any(character_type in self.password for character_type in password_character_types["LOWER_CASE_LETTERS"]),
            any(character_type in self.password for character_type in password_character_types["NUMBERS"]),
            any(character_type in self.password for character_type in password_character_types["SYMBOLS"])
        ])

        # check username satisfies min and max length rules
        if len(self.user) < user_settings["MIN_LENGTH"] or len(self.user) > user_settings["MAX_LENGTH"]:
            return False

        # check for illegal characters in username
        if any(illegal_character in self.user for illegal_character in user_settings["ILLEGAL_CHARACTERS"]):
            return False

        # check password satisfies min and max length rules
        if len(self.password) < password_settings["MIN_LENGTH"] or len(self.user) > password_settings["MAX_LENGTH"]:
            return False

        # check password satisfies minimum number of character types
        if password_character_types < 3:
            return False

        # check if password and confirm password values match
        if self.password != self.confirm_password:
            return False

        return True

    def check_email_valid(self):
        email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if(re.search(email_regex, self.email)):  
            return True
        
        else:
            return False

    def check_username_valid(self):
        user_settings = RegisterForm.USER_SETTINGS

        # check username satisfies min and max length rules
        if len(self.user) < user_settings["MIN_LENGTH"]:
            print("Username does not satisfy Min length rule")
            return False

        if len(self.user) > user_settings["MAX_LENGTH"]:
            print("Username does not satisfy Max length rule")
            return False

        # check for illegal characters in username
        if any(illegal_character in self.user for illegal_character in user_settings["ILLEGAL_CHARACTERS"]):
            print("Illegal Character(s) found in Username")
            return False

        # check for spaces in User
        if " " in self.user:
            return False

        return True

    def check_password_valid(self):
        password_settings = RegisterForm.PASSWORD_SETTINGS
        password_character_types = password_settings["MUST_CONTAIN"]

        password_character_types = sum([
            any(character_type in self.password for character_type in password_character_types["UPPER_CASE_LETTERS"]),
            any(character_type in self.password for character_type in password_character_types["LOWER_CASE_LETTERS"]),
            any(character_type in self.password for character_type in password_character_types["NUMBERS"]),
            any(character_type in self.password for character_type in password_character_types["SYMBOLS"])
        ])

        # check password satisfies min and max length rules
        if len(self.password) < password_settings["MIN_LENGTH"]:
            print("Password does not satisfy min length rules")
            return False

        if len(self.password) > password_settings["MAX_LENGTH"]:
            print("Password does not satisfy max length rules")
            return False

        # check password satisfies minimum number of character types
        if password_character_types < 3:
            print("Password does not minimum number of Character Types")
            return False

        # check if password and confirm password values match
        if self.password != self.confirm_password:
            print("Password and Confirmed Password Values do not match")
            return False
        
        return True

    def check_username_exists(self):
        db_cluster_collection = Config.DB_CLUSTER[Config.COLLECTION_NAMES["logins"]]
        emails_found = db_cluster_collection.find({"email": {"$regex": '^' + self.email + '$'}})
        users_found = db_cluster_collection.find({"user": {"$regex": '^' + self.user + '$'}})

        print(emails_found.count(), users_found.count())

        if emails_found.count() > 0 or users_found.count() > 0:
            return True

        else:
            return False

    def create_username(self):
        db_cluster_collection = Config.DB_CLUSTER[Config.COLLECTION_NAMES["logins"]]

        password = self.password
        hashed_password = hash_password(password)

        db_cluster_collection.insert_one({"email": self.email, "user": self.user, "password": hashed_password})


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

            return verify_password(user_details["password"], password)

        except IndexError:
            return False


class ManageForm(object):
    def __init__(self, form_data):
        self.email = form_data.email
        self.user = form_data.user
    
    def delete_user(self): 
        db_cluster_collection = Config.DB_CLUSTER[Config.COLLECTION_NAMES["logins"]]
        user_to_delete = {"email": self.email, "user": self.user}

        db_cluster_collection.delete_one(user_to_delete)


class UserStatsForm(object):
    def __init__(self, form_data):
        self.user = form_data.user

    def get_stats(self):
        db_cluster_collection = Config.DB_CLUSTER[Config.COLLECTION_NAMES["user_stats"]]
        users_found = db_cluster_collection.find({"user": {"$regex": '^' + self.user + '$'}})

        if users_found.count() == 0:
            return None

        else:
            user_details = json.loads(dumps(users_found))[0]
            return user_details
    
    # def update_stats(self):
    #     db_cluster_collection = Config.DB_CLUSTER[Config.COLLECTION_NAMES["user_stats"]]
    #     users_found = db_cluster_collection.find_one_and_update({"user": {"$regex": '^' + self.user + '$'}})

    def create_stats(self):
        try:
            db_cluster_collection = Config.DB_CLUSTER[Config.COLLECTION_NAMES["user_stats"]]
            db_cluster_collection.insert_one({
                "user": self.user,
                "gender": None,
                "date_of_birth": None,
                "height": None,
                "weight": None,
                "avatar": None
            })

            return True
        except:
            return False


    # def create_stats(self): 

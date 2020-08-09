import model
import forms

from response import ErrorMessage, SuccessMessage
from flask import Flask, abort, request, jsonify
from config import Config

URI_CLUSTER = Config.DB_CONNECTION_STRING
DB_CLUSTER = URI_CLUSTER[Config.DB_CLUSTER_NAME]

# cluster = pymongo.MongoClient("mongodb+srv://admin:7VCbdWPGfZsXQ95s@fitness-app.bi9i8.mongodb.net/test?retryWrites=true&w=majority")
# DB_USER = "admin"
# DB_PASSWORD = "7VCbdWPGfZsXQ95s"

# DB_CLUSTER = cluster["fitness_app"]
# DB_CLUSTER_COLLECTION = DB_CLUSTER["logins"]

# collection.insert_one({"id": 0, "user_name": "test"})

app = Flask(__name__)


@app.route("/")
def hello():
    return "test"


@app.route("/api/users", methods=['POST'])
def create_user():
    data = request.json

    email = request.json.get("email")
    username = request.json.get("username")
    password = request.json.get("password")
    confirm_password = request.json.get("confirm_password")

    user = model.User(email, username, password, confirm_password)
    new_user = forms.RegisterForm(user)

    if new_user.check_user_exists() is True:
        # abort(404, description="Username/Email already exists")
        return jsonify(ErrorMessage.REGISTER["USERNAME_EXISTS"]), 409

    if new_user.validate() is False:
        # abort(404, description="Invalid Username Requested")
        return jsonify(ErrorMessage.REGISTER["INVALID_CREDENTIALS"]), 401

    if None in (email, username, password, confirm_password):
        # abort(404, description="Resource not found")
        return jsonify(ErrorMessage.REGISTER["INVALID_REQUEST"]), 400

    new_user.create_user()

    return jsonify(SuccessMessage(user).create_user()), 201


@app.route("/api/login", methods=['POST'])
def login():
    data = request.json

    username = request.json.get("username")
    password = request.json.get("password")

    user = model.User(email=None, user=username, password=password, confirm_password=None)
    login_user = forms.LoginForm(user)

    if login_user.check_user_credentials() is False:
        # abort(404, description="Invalid Username or Password Entered")
        return jsonify(ErrorMessage.LOGIN["INVALID_CREDENTIALS"]), 401

    return jsonify(SuccessMessage(user).set_login()), 200


if __name__ == "__main__":
    app.run()



from api.config import Config

from api.response import *
from api.models.user import User
from api.forms.forms import *

from flask import Flask, abort, request, jsonify

URI_CLUSTER = Config.DB_CONNECTION_STRING
DB_CLUSTER = URI_CLUSTER[Config.DB_CLUSTER_NAME]


app = Flask(__name__)


@app.route("/")
def hello_world():
    return "test"


@app.route("/api/users", methods=['POST'])
def create_user():
    data = request.json

    email = request.json.get("email")
    username = request.json.get("username")
    password = request.json.get("password")
    confirm_password = request.json.get("confirm_password")

    user = User(email, username, password, confirm_password)
    new_user = RegisterForm(user)

    if new_user.check_email_valid() is False:
        return jsonify({"errors": [ErrorMessage.REGISTER["INVALID_EMAIL"]]}), 401

    if None or "" in (email, username, password, confirm_password):
        return jsonify({"errors": [ErrorMessage.REGISTER["INVALID_REQUEST"]]}), 400

    if new_user.check_user_exists() is True:
        return jsonify({"errors": [ErrorMessage.REGISTER["USERNAME_EXISTS"]]}), 409

    if new_user.validate() is False:
        return jsonify({"errors": [ErrorMessage.REGISTER["INVALID_CREDENTIALS"]]}), 401

    new_user.create_user()

    return jsonify(SuccessMessage(user).create_user()), 201


@app.route("/api/login", methods=['POST'])
def login():
    data = request.json

    username = request.json.get("username")
    password = request.json.get("password")

    user = User(email=None, user=username, password=password, confirm_password=None)
    login_user = LoginForm(user)

    if login_user.check_user_credentials() is False:
        return jsonify(ErrorMessage.LOGIN["INVALID_CREDENTIALS"]), 401

    return jsonify(SuccessMessage(user).set_login()), 200


if __name__ == "__main__":
    app.run()



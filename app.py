from api.config import Config

from api.response import *
from api.models.user import User
from api.forms.forms import *
from api.utils import *

from flask import Flask, abort, request, jsonify

URI_CLUSTER = Config.DB_CONNECTION_STRING
DB_CLUSTER = URI_CLUSTER[Config.DB_CLUSTER_NAME]


app = Flask(__name__)


@app.route("/")
def hello_world():
    return "test"


@app.route("/api/users", methods=['POST'])
def create_username():
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

    if new_user.check_username_exists() is True:
        return jsonify({"errors": [ErrorMessage.REGISTER["USERNAME_EXISTS"]]}), 409

    if new_user.validate() is False:
        return jsonify({"errors": [ErrorMessage.REGISTER["INVALID_CREDENTIALS"]]}), 401

    new_user.create_username()

    return jsonify(SuccessMessage(user).create_username()), 201


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

# @app.route("/api/users/<user>/stats", methods=['PUT'])

@app.route("/api/users/<user>/stats", methods=['POST'])
def create_user_stats(user):

    username = request.json.get("username")
    user_to_check = User(email=None, user=username, password=None, confirm_password=None)

    if UserStatsForm(user_to_check).get_stats() is not None:
        return jsonify({"errors": [ErrorMessage.USERS_STATS["STATS_ALREADY_EXIST"]]}), 409

    if UserStatsForm(user_to_check).create_stats() is False: 
        return jsonify({"errors": [ErrorMessage.USERS_STATS]}), 0

    else:
        return jsonify(SuccessMessage(user_to_check).create_user_stats()), 201


@app.route("/api/users/<user>/stats", methods=['GET'])
def get_user_stats(user):

    user_to_check = User(email=None, user=user, password=None, confirm_password=None)

    if decode_auth_token(request.headers["Authorization"]) != user:
        return jsonify({"errors": [ErrorMessage.FORBIDDEN]}), 403

    if UserStatsForm(user_to_check).get_stats() is None:
        return jsonify({"errors": [ErrorMessage.USERS_STATS["NO_STATS_AVAILABLE"]]}), 422

    else:
        return UserStatsForm(user).get_stats()

# @app.route("/api/users/<user>/stats", methods=['PUT'])

if __name__ == "__main__":
    app.run()



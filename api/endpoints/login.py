from api.response import ErrorMessage
from api.models.user import User
from api.forms.login_user import LoginForm
from api.config import Config

from flask import Blueprint
from flask_jwt_extended import jwt_required
from flask import jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token

blueprint = Blueprint(name="login_endpoint", import_name=__name__)

@blueprint.route('login', methods=['POST'])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    user = User(email=None, user=username, password=password, confirm_password=None)
    login_user = LoginForm(user)

    if login_user.check_user_credentials() is False:
        return jsonify(ErrorMessage.LOGIN["INVALID_CREDENTIALS"]), 401

    return jsonify({
        "status": "201",
        "data": {
            "username": username,
            "access_token": create_access_token(identity=username, expires_delta=Config.ACCESS_TOKEN_EXPIRY),
            "refresh_token": create_refresh_token(identity=username, expires_delta=Config.REFRESH_TOKEN_EXPIRY)
        },
        "message": "Successfully Logged In"
    }), 200
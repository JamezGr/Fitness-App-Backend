from api.response import ErrorMessage
from api.models.user import User
from api.forms.register_user import RegisterForm
from api.response import *

from flask import Blueprint
from flask import jsonify, request

blueprint = Blueprint(name="register_user_endpoint", import_name=__name__)

@blueprint.route("/api/users", methods=['POST'])
def create_username():
    body_data = request.json

    email = body_data.get("email")
    username = body_data.get("username")
    password = body_data.get("password")
    confirm_password = body_data.get("confirm_password")

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

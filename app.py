from api.config import Config

from api.response import *
from api.models.user import User, UserProfile
from api.forms.forms import *
from api.forms.register_user import RegisterForm
from api.forms.login_user import LoginForm
from api.forms.schedule_activities import ScheduleActivities
from api.forms.map_route import MapRoute
from api.utils import *
from api.utils import files
from api.utils import response

from api.endpoints import default

from flask import Flask, abort, request, jsonify, after_this_request, make_response, redirect
from flask_cors import CORS, cross_origin

from webargs import fields
from webargs.flaskparser import use_args

from bson.json_util import dumps
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, verify_jwt_refresh_token_in_request
)

from jsonschema import validate
from flask_pymongo import PyMongo
from bson.binary import Binary

URI_CLUSTER = Config.DB_CONNECTION_STRING
DB_CLUSTER = URI_CLUSTER[Config.DB_CLUSTER_NAME]

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = Config.SECRET_KEY
app.config['CORS_HEADERS'] = 'Content-Type'

jwt = JWTManager(app)
mongo = PyMongo(app=app, uri=Config.DB_CONNECTION_URI)

CORS(app, resources={
    r"/*": {
        "origins": "*"
    }
})

current_date_time_obj = date_time.get_current_datetime()
current_date_time_str = date_time.convert_datetime_obj_to_str(current_date_time_obj)

app.register_blueprint(default.blueprint, url_prefix="/")


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

    return jsonify({
        "status": "201",
        "data": {
            "username": username,
            "access_token": create_access_token(identity=username, expires_delta=Config.ACCESS_TOKEN_EXPIRY),
            "refresh_token": create_refresh_token(identity=username, expires_delta=Config.REFRESH_TOKEN_EXPIRY)
        },
        "message": "Successfully Logged In"
    }), 200


@app.route("/api/users/<user>/profile", methods=['GET'])
@jwt_required
def get_user_profile(user):

    user_to_check = User(email=None, user=user, password=None, confirm_password=None)

    if UserProfileForm(user).get_profile() is None:
        return jsonify({"errors": [ErrorMessage.USER_PROFILE["NO_PROFILE_AVAILABLE"]]}), 422

    else:
        return UserProfileForm(user).get_profile()

@app.route("/uploads/<path:filename>")
def get_upload(filename):
    return mongo.send_file(filename)

@app.route("/api/users/<user>/profile", methods=['POST'])
@jwt_required
def update_user_profile(user):    
    user_to_check = User(email=None, user=user, password=None, confirm_password=None)
    updated_profile = {}

    # TODO: Find Better Way to Convert Form Data to JSON 
    if "avatar" in request.files:
        avatar_image = request.files["avatar"]
        updated_profile["avatar"] = avatar_image.filename;

    form_data = request.form

    for key in form_data.keys():
        updated_value = form_data[key]
        is_numeric = updated_value.isnumeric()

        if is_numeric:
            updated_profile[key] = int(updated_value)

        else:
            updated_profile[key] = str(updated_value)

    try:
        validate(instance=updated_profile, schema=UserProfile.updatable_fields, format_checker=jsonschema.FormatChecker())

    except jsonschema.ValidationError as error:
        return jsonify({"errors": error.message}), 400
    
    user_profile = UserProfileForm(user, updated_profile).update_profile()

    if user_profile is not None:
        mongo.save_file(avatar_image.filename, avatar_image)
        return jsonify(SuccessMessage(user_to_check).update_profile()), 201

    else:
        return jsonify({"errors": [ErrorMessage.USER_PROFILE["INVALID_USER"]]}), 400


# Generate New Access Token once Expired
@app.route("/api/refresh", methods=['POST'])
@jwt_refresh_token_required
def refresh():
    verify_token = verify_jwt_refresh_token_in_request()
    current_user = get_jwt_identity()
    ret = {
        'access_token': create_access_token(identity=current_user)
    }
    return jsonify(ret), 200


# Get Current User Logged In
@app.route("/api/users", methods=['GET'])
@jwt_required
def protected():
    username = get_jwt_identity()
    return jsonify(logged_in_as=username), 200


@app.route("/api/schedule", methods=['POST'])
@jwt_required
def update_user_schedule():
    schedule_data = request.json

    scheduled_activity = ScheduleActivities(schedule_data)
    update_schedule_data = scheduled_activity.update_schedule_data()

    if update_schedule_data["success"]:
        return jsonify(SuccessMessage.SCHEDULE["UPDATED"]), 201
    
    else:
        error_message = ErrorMessage.SCHEDULE["INVALID"]
        error_message["errors"] = update_schedule_data[0]["errors"]

        return jsonify(error_message), 400


@app.route("/api/schedule", methods=['GET'])
@jwt_required
@use_args({
    "user_id": fields.Str(required=True),
    "activity_id": fields.Str(missing=""),
    "start_date": fields.Str(missing=current_date_time_str),
    "end_date": fields.Str(missing=current_date_time_str),
    "returnDetails": fields.Bool(missing=True),
    "returnIdsOnly": fields.Bool(missing=False),
    "returnSummary": fields.Bool(missing=False)
    })
def get_scheduled_activities(args):
    request_params = args
    schedule_data = {
        "request_params": request_params 
    }

    schedule_activities = ScheduleActivities(schedule_data)
    fetched_schedule_data = schedule_activities.get_scheduled_data()

    return fetched_schedule_data


@app.route("/api/schedule", methods=['DELETE'])
@jwt_required
def delete_activity():
    schedule_data = {
        "request_params": request.json 
    }
    schedule_activities = ScheduleActivities(schedule_data)
    deleted_activity = schedule_activities.delete_scheduled_data()

    if deleted_activity is True:
        return jsonify(SuccessMessage.SCHEDULE["DELETED"]), 202

    else:
        return jsonify(ErrorMessage.SCHEDULE["DELETE_ERROR"]), 405

@app.route("/api/routes", methods=['POST'])
def add_route():
    if "file" not in request.files:
        return jsonify(ErrorMessage.INVALID_REQUEST), 401

    file = request.files['file']

    request_body = {
        "file": file,
        "user_id": request.form["user_id"]
    }

    route = MapRoute(request_body)

    if route.is_gpx_file() is False:
        data_response = response.set_error(["File type is not gpx"])

    saved_file = mongo.save_file(file.filename, file)

    ## return object id of saved file
    data_response = response.set_ok({"id": str(saved_file)})

    return jsonify(data_response), data_response["status"]

# No cacheing at all for API endpoints.
@app.after_request
def add_header(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    
    return response

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify(ErrorMessage.METHOD_NOT_ALLOWED), 405

@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
    error_message = ErrorMessage.EXPIRED_TOKEN

    return jsonify(error_message), 401
    
if __name__ == "__main__":
    app.run(debug=True)

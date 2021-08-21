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
from api.utils.database import mongo
from api.endpoints import default, login, user

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
app.config['MONGO_URI'] = Config.DB_CONNECTION_URI

jwt = JWTManager(app)
mongo.init_app(app)

CORS(app, resources={
    r"/*": {
        "origins": "*"
    }
})

current_date_time_obj = date_time.get_current_datetime()
current_date_time_str = date_time.convert_datetime_obj_to_str(current_date_time_obj)

app.register_blueprint(default.blueprint, url_prefix="/")
app.register_blueprint(login.blueprint, url_prefix=Config.ENDPOINT_PREFIX)
app.register_blueprint(user.blueprint, url_prefix=Config.ENDPOINT_PREFIX)

@app.route("/uploads/<path:filename>")
def get_upload(filename):
    return mongo.send_file(filename)

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

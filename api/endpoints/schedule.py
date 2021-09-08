from api.models.schedule import ActivitySchema
from api.utils import date_time, query, response
from api.response import ErrorMessage, SuccessMessage
from api.forms.schedule_activities import ScheduleActivities

from flask import Blueprint
from flask import jsonify, request
from flask_jwt_extended import jwt_required
from flask_expects_json import expects_json

from webargs import fields, validate
from webargs.flaskparser import use_args

blueprint = Blueprint(name="schedule_endpoint", import_name=__name__)

@blueprint.route("schedule", methods=['POST'])
@expects_json(ActivitySchema.request_body)
# @jwt_required
def create_user_schedule():
    request_body = request.json

    if query.object_id_is_valid(request_body["user_id"]) is False:
        error = response.set_error(["Invalid user_id provided."])
        return jsonify(error), error["status"]
    
    request_date_str = request_body["date"]
    current_date_str = date_time.get_current_datetime_as_string()

    if date_time.validate_date_format(request_date_str) is False:
        error = response.set_error(["Date provided is not in format YYYY-MM-DD."])
        return jsonify(error), error["status"]

    if date_time.is_before_date(current_date_str, request_date_str) is True:
        error = response.set_error(["Date provided is in the future."])
        return jsonify(error), error["status"]

    request_response = ScheduleActivities(request_body).create()

    return jsonify(request_response), request_response["status"]
    # schedule_data = request.json

    # scheduled_activity = ScheduleActivities(schedule_data)
    # update_schedule_data = scheduled_activity.update_schedule_data()

    # if update_schedule_data["success"]:
    #     return jsonify(SuccessMessage.SCHEDULE["UPDATED"]), 201
    
    # else:
    #     error_message = ErrorMessage.SCHEDULE["INVALID"]
    #     error_message["errors"] = update_schedule_data[0]["errors"]

    #     return jsonify(error_message), 400


@blueprint.route("schedule", methods=['GET'])
# @jwt_required
@use_args({
    "user_id": fields.Str(
        required=True,
        validate=lambda id: query.object_id_is_valid(id)
    ),
    "activity_id": fields.Str(missing=None),
    "start_date": fields.Str(
        missing=date_time.get_current_datetime_as_string(),
        validate=lambda date: date_time.validate_date_format(date)
    ),
    "end_date": fields.Str(
        missing=date_time.get_current_datetime_as_string(),
        validate=lambda date: date_time.validate_date_format(date)
    ),
    "returnDetails": fields.Bool(missing=True),
    "returnIdsOnly": fields.Bool(missing=False),
    "returnSummary": fields.Bool(missing=False)
    })
def get_activities(request_params):
    # request_params = args
    # schedule_data = {
    #     "request_params": request_params 
    # }

    # schedule_activities = ScheduleActivities(request_params)
    # fetched_schedule_data = schedule_activities.get()

    # return fetched_schedule_data

    activities = ScheduleActivities(request_params)
    request_response = activities.get()

    return jsonify(request_response), request_response["status"]


@blueprint.route("schedule", methods=['DELETE'])
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
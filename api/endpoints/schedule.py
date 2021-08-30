from api.utils import date_time
from api.response import ErrorMessage, SuccessMessage
from api.forms.schedule_activities import ScheduleActivities

from flask import Blueprint
from flask import jsonify, request
from flask_jwt_extended import jwt_required

from webargs import fields
from webargs.flaskparser import use_args

blueprint = Blueprint(name="schedule_endpoint", import_name=__name__)

@blueprint.route("schedule", methods=['POST'])
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


@blueprint.route("schedule", methods=['GET'])
@jwt_required
@use_args({
    "user_id": fields.Str(required=True),
    "activity_id": fields.Str(missing=""),
    "start_date": fields.Str(missing=date_time.get_current_datetime_as_string()),
    "end_date": fields.Str(missing=date_time.get_current_datetime_as_string()),
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
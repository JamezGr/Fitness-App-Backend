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
@expects_json(ActivitySchema.insert_params)
@jwt_required
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


@blueprint.route("schedule", methods=['PUT'])
@expects_json(ActivitySchema.update_params)
def update_user_schedule():
    request_body = request.json

    is_user_id_valid = query.object_id_is_valid(request_body["user_id"])
    is_activity_ids_valid = all(query.object_id_is_valid(item["id"]) for item in request_body["items"])

    if is_user_id_valid is False:
        request_response = response.set_error(["Invalid user_id passed."])
        return jsonify(request_response), request_response["status"]

    if is_activity_ids_valid is False:
        request_response = response.set_error(["Invalid activity_id passed."])
        return jsonify(request_response), request_response["status"]

    request_response = ScheduleActivities(request_body).update() 

    return jsonify(request_response), request_response["status"]


@blueprint.route("schedule", methods=['GET'])
@jwt_required
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
    "returnSummary": fields.Bool(missing=False),
    "returnComments": fields.Bool(missing=True),
    })
def get_activities(request_params):
    activities = ScheduleActivities(request_params)
    request_response = activities.get()

    return jsonify(request_response), request_response["status"]


@blueprint.route("schedule", methods=['DELETE'])
@jwt_required
@use_args({
    "user_id": fields.Str(
        required=True,
        validate=lambda id: query.object_id_is_valid(id)
    ),
    "activity_id": fields.Str(
        required=False,
        missing=None,
        validate=lambda id: query.object_id_is_valid(id)
    ),
    # schedule items as object ids
    "items": fields.List(
        fields.String(),
        required=False,
        missing=None,
        validate=lambda items: all(query.object_id_is_valid(item) for item in items)
    )
})
def delete_activity(request_params):
    if request_params["activity_id"] is None and request_params["items"] is None:
        request_response = ErrorMessage.SCHEDULE["INVALID"]
        return jsonify(request_response), request_response["status"]

    request_response = ScheduleActivities(request_params).delete()

    return jsonify(request_response), request_response["status"]
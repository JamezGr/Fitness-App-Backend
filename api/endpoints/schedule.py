import os
from werkzeug.exceptions import BadRequestKeyError
from api.models.schedule import ActivitySchema
from api.utils import date_time, query, response
from api.response import ErrorMessage, SuccessMessage
from api.forms.schedule_activities import ScheduleActivities
from api.utils.response import response_error, response_ok

from flask import Blueprint
from flask import jsonify, request
from flask_jwt_extended import jwt_required
from flask_expects_json import expects_json

from webargs import fields
from webargs.flaskparser import use_args

from api.utils.files import limit_content_length

blueprint = Blueprint(name="schedule_endpoint", import_name=__name__)

@blueprint.route("schedule/attachments", methods=['POST'])
@limit_content_length(ActivitySchema.max_attachment_size)
@jwt_required
def upload_attachment():
    if "file" not in request.files:
        return response_error(message="Expected 'file' to be provided")

    if "activity_id" not in request.form:
        return response_error(message="Expected 'activity_id' to be provided")

    file = request.files["file"]

    params = {
        "file": file,
        "activity_id": request.form["activity_id"],
        "user_id": request.form["user_id"],
    }

    activity = ScheduleActivities(params)
    activity_found = activity.get_activity_by_id()

    if activity_found is None:
        return response_error(message="No activity found for provided activity_id")

    if file.content_type not in ActivitySchema.allowed_attachment_files_by_type[activity_found["name"]]:
        return response_error(message="Invalid File Type Provided.")

    attachments_count = activity.get_attachments_count()

    if attachments_count >= ActivitySchema.max_attachments:
        return response_error(message="No attachments uploaded. Maximum number of attachments uploaded have been reached.", status=304)

    activity.upload_attachment()
    return response_ok(message="ok");


@blueprint.route("schedule/<activity_id>/attachments", methods=['GET'])
@jwt_required
def get_attachments_list_by_activity_id(activity_id):
    print("getting list of attachments for activity id")
    print(activity_id)
    attachments = ScheduleActivities({"activity_id": activity_id}).get_all_attachments_by_activity_id()
    return response_ok(data=attachments)


@blueprint.route("schedule/attachments/<attachment_filename>", methods=['GET'])
@jwt_required
def get_attachment_by_filename(attachment_filename):
    print("getting attachment by filename")

    return ScheduleActivities({"attachment_filename": attachment_filename}).get_attachment_by_filename()


@blueprint.route("schedule/attachments", methods=['DELETE'])
@jwt_required
@use_args({
    "attachment_id": fields.Str(required=True),
    "activity_id": fields.Str(required=True),
    "user_id": fields.Str(required=True)
})
def delete_multiple_attachments(request_params):
    attachment = ScheduleActivities(request_params).delete_activity_attachment()

    if attachment.deleted_count > 0:
        return response_ok(message="ok")

    else:
        return response_error(message="No attachment was deleted", status=304)


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
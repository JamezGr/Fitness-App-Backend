import unittest
import pytest

from api.forms.register_user import RegisterForm
from api.forms.schedule_activities import ScheduleActivities
from api.models.user import User
from api.utils.query import object_id_is_valid
from test.helpers.schedule import test_valid_schedule_data, test_valid_request_params, test_invalid_schedule_data

""" Should Create Activity in Schedule with Valid Request Body """
def test_create_activity():
    updated_activity_data = ScheduleActivities(test_valid_schedule_data).update_schedule_data()
    
    activity_found = ScheduleActivities(test_valid_request_params).get_scheduled_data()
    activity_id = updated_activity_data["data"]["id"]

    updated_params = {
        "request_params": {
            "activity_id": str(activity_id)
        }
    }

    ScheduleActivities(updated_params).delete_scheduled_data()
    assert activity_found["data"][0]["activities"] == test_valid_schedule_data["activities"]

""" Should not create activity with invalid Request Body """
def test_create_activity_with_invalid_request_body():
    created_activity = ScheduleActivities(test_invalid_schedule_data).update_schedule_data()

    assert created_activity["status"] == 400

""" Should Fetch Data by Activity Id """
def test_fetch_data_by_activity_id():
    activity_data = ScheduleActivities(test_valid_schedule_data).update_schedule_data()
    activity_id_to_find = str(activity_data["data"]["id"])

    test_params = test_valid_request_params
    test_params["request_params"]["activity_id"] = activity_id_to_find

    activity_data_to_find = ScheduleActivities(test_params).get_scheduled_data()

    ScheduleActivities(test_params).delete_scheduled_data()
    assert activity_id_to_find == activity_data_to_find["data"]["_id"]["$oid"]

""" Should Delete Scheduled Data Created """
def test_delete_activity():
    updated_activity_data = ScheduleActivities(test_valid_schedule_data).update_schedule_data()
    
    activity_id = updated_activity_data["data"]["id"]

    updated_params = {
        "request_params": {
            "activity_id": str(activity_id)
        }
    }

    ScheduleActivities(updated_params).delete_scheduled_data()
    activity_found = ScheduleActivities(test_valid_request_params).get_scheduled_data()

    assert len(activity_found["data"]) == 0
    assert activity_found["status"] == 200

""" Should Fetch Data by Activity Id """
def test_get_activity_by_id():
    updated_activity_data = ScheduleActivities(test_valid_schedule_data).update_schedule_data()
    
    activity_found = ScheduleActivities(test_valid_request_params).get_scheduled_data()
    activity_id = updated_activity_data["data"]["id"]

    updated_params = test_valid_request_params
    updated_params["request_params"]["activity_id"] = str(activity_id)
    updated_params["request_params"]["user_id"] = test_valid_schedule_data["user_id"]

    activity_to_find = ScheduleActivities(updated_params).get_scheduled_data()
    ScheduleActivities(updated_params).delete_scheduled_data()

    assert activity_to_find["data"]["_id"]["$oid"] == str(activity_id)

""" Should not Fetch Data with Invalid Activity Id Type """
def test_check_invalid_activity_id_type():
    test_params = test_valid_request_params
    test_params["request_params"]["activity_id"] = "None"
    test_params["request_params"]["user_id"] = test_valid_schedule_data["user_id"]

    activity_to_find = ScheduleActivities(test_params).get_scheduled_data()

    assert activity_to_find["data"] == []

""" Should not allow request where End Date is before Start Date """
def test_check_invalid_date_range():
    test_params = test_valid_request_params
    test_params["request_params"]["end_date"] = "2021-02-01"

    response = ScheduleActivities(test_params).get_scheduled_data()

    assert response["status"] == 400

""" Should return Activity Ids only if returnIdsOnly set to true """
def test_return_ids_only():
    activity_data = ScheduleActivities(test_valid_schedule_data).update_schedule_data()
    activity_id_to_find = str(activity_data["data"]["id"])

    test_params = test_valid_request_params
    test_params["request_params"]["activity_id"] = activity_id_to_find
    test_params["request_params"]["returnIdsOnly"] = True
    test_params["request_params"]["returnSummaryOnly"] = False

    activity_data_to_find = ScheduleActivities(test_params).get_scheduled_data()

    ScheduleActivities(test_params).delete_scheduled_data()
    id_list_valid = all(object_id_is_valid(id) for id in activity_data_to_find["data"])

    assert id_list_valid == True

""" Should return Summary of Activities if returnSummary set to true """
def test_return_summary():
    activity_data = ScheduleActivities(test_valid_schedule_data).update_schedule_data()
    activity_id_to_find = str(activity_data["data"]["id"])

    test_params = test_valid_request_params
    test_params["request_params"]["activity_id"] = activity_id_to_find
    test_params["request_params"]["returnIdsOnly"] = False
    test_params["request_params"]["returnDetails"] = False
    test_params["request_params"]["returnSummary"] = True

    activity_data_to_find = ScheduleActivities(test_params).get_scheduled_data()
    response_data = activity_data_to_find["data"]

    ScheduleActivities(test_params).delete_scheduled_data()
    summary_is_valid = "details" not in response_data["activities"]
    assert summary_is_valid == True

""" Should return Details of Activities if returnDetails set to true """
def test_return_details():
    activity_data = ScheduleActivities(test_valid_schedule_data).update_schedule_data()
    activity_id_to_find = str(activity_data["data"]["id"])

    test_params = test_valid_request_params
    test_params["request_params"]["activity_id"] = activity_id_to_find
    test_params["request_params"]["returnIdsOnly"] = False
    test_params["request_params"]["returnDetails"] = True
    test_params["request_params"]["returnSummary"] = False

    activity_data_to_find = ScheduleActivities(test_params).get_scheduled_data()
    response_data = activity_data_to_find["data"]

    ScheduleActivities(test_params).delete_scheduled_data()
    details_exists = all("details" in data for data in response_data["activities"])

    assert details_exists == True
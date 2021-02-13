from api.models.schedule import Schedule
from api.models.url_params import UrlParams
from api.config import Config, DevelopmentConfig, TestingConfig, ProductionConfig
from api.utils import date_time, query, schedule, response
from bson.json_util import dumps, loads
from bson.objectid import ObjectId

import jsonschema
import datetime
import json

class ScheduleActivities(object):
    def __init__(self, activity_data):
        self.activity_data = activity_data
        self.request_params = activity_data.get("request_params", None)

        self.errors = []
        self.db_cluster_collection = Config.DB_CLUSTER[Config.COLLECTION_NAMES["user_schedule"]]

    def validate_schedule_format(self, schedule_data):
        try:
            jsonschema.validate(instance=schedule_data, schema=Schedule.data, format_checker=jsonschema.FormatChecker())
            return True
        
        except jsonschema.ValidationError as error:
            self.errors.append(error.message)
            return False


    def validate_activity_format(self, activity_data): 
        try: 
            activity_schema = Schedule.activities["data"]
            jsonschema.validate(instance=activity_data, schema=activity_schema, format_checker=jsonschema.FormatChecker())

            return True

        except jsonschema.ValidationError as error:
            self.errors.append(error.message)
            return False


    def validate_activity_details(self, activity_details, activity_name):
        try:
            for detail in activity_details:
                activity_schema = Schedule.activities["details"][activity_name]
                jsonschema.validate(instance=detail, schema=activity_schema, format_checker=jsonschema.FormatChecker())

                return True

        except jsonschema.ValidationError as error:
            self.errors.append(error.message)
            return False


    def validate_request_params(self):
        try: 
            jsonschema.validate(instance=self.request_params, schema=UrlParams.schedule, format_checker=jsonschema.FormatChecker())

        except jsonschema.ValidationError as error:
            self.errors.append(error.message)
            return False


    def validate_request_dates(self):
        try:
            request_params = self.activity_data["request_params"]
            start_date = request_params["start_date"]
            end_date = request_params["end_date"]
            activity_id = request_params["activity_id"]

            start_date_obj = date_time.convert_datetime_str_to_obj(start_date)
            end_date_obj = date_time.convert_datetime_str_to_obj(end_date)

            ## no date needed if only activity id is specified 
            if start_date_obj is None and end_date_obj is None and activity_id is not None:
                return True

            if start_date_obj is None and start_date is not None:
                self.errors.append("Invalid start_date {date}".format(date=start_date))

            if end_date_obj is None and end_date is not None:
                self.errors.append("Invalid end_date {date}".format(date=end_date))

            if start_date > end_date:
                self.errors.append("start_date {start} is after end_date {end}".format(start=start_date, end=end_date))

        except:
            return False 


    def set_request_dates(self, request_dates):
        start_date = request_dates["start_date"]
        end_date = request_dates["end_date"]

        start_date_obj = date_time.convert_datetime_str_to_obj(start_date)
        end_date_obj = date_time.convert_datetime_str_to_obj(end_date)


        if start_date_obj is None and end_date_obj is None:
            return request_dates

        if start_date_obj and end_date_obj is None:
            current_date_obj = date_time.get_current_datetime()
            current_date_str = date_time.convert_datetime_obj_to_str(current_date_obj)

            end_date = current_date_str
        
        if start_date_obj is None and end_date_obj:

            start_of_month_date_obj = date_time.get_first_day_of_selected_month(end_date_obj)
            updated_start_date_str = date_time.convert_datetime_obj_to_str(start_of_month_date_obj)

            start_date = updated_start_date_str

        return {
            "start_date": start_date,
            "end_date": end_date
        }


    def update_scheduled_data(self):
        schedule_activities = self.activity_data["activities"]
        schedule_valid = self.validate_schedule_format(self.activity_data)

        for activity in schedule_activities:
            activity_details = activity["details"]
            activity_name = activity["name"]
            
            activity_format_valid = self.validate_activity_format(activity)
            activity_details_valid = self.validate_activity_details(activity_details, activity_name)


        if len(self.errors):
            return response.set_response_error(self.errors)

        else:
            date = date_time.convert_datetime_str_to_obj(self.activity_data["date"])

            self.db_cluster_collection.find_one_and_replace(
                {"date": date},
                self.activity_data,
                projection=None,
                upsert=True
            )

            return response.set_response_ok()


    def get_surpressed_fields(self):
        surpressed_fields = {}
        surpressed_fields["user_id"] = 0

        if self.request_params["returnIdsOnly"] is True:
            surpressed_fields["_id"] = 1
            surpressed_fields["activities"] = 0
            return surpressed_fields

        if self.request_params["returnSummary"] is True:
            surpressed_fields["activities.details"] = 0
            return surpressed_fields

        return surpressed_fields


    def get_scheduled_data(self):
        request_dates = self.set_request_dates({
            "start_date": self.request_params["start_date"],
            "end_date": self.request_params["end_date"]
        })

        activity_id = self.request_params["activity_id"]

        self.request_params["start_date"] = request_dates["start_date"]
        self.request_params["end_date"] = request_dates["end_date"]

        valid_request_dates = self.validate_request_dates()
        valid_request_params = self.validate_request_params()

        if len(activity_id) and query.object_id_is_valid(activity_id) is False:
            self.errors.append("Invalid Activity ID type {activity_id}".format(activity_id=activity_id))

        if len(self.errors):
            return response.set_response_error(self.errors)

        else:
            surpressed_fields = self.get_surpressed_fields()

            if len(activity_id):
                schedule_data = self.db_cluster_collection.find_one(
                    {
                        "_id": ObjectId(activity_id),
                        "user_id": self.request_params["user_id"]
                    }, surpressed_fields
                )
            
            else:
                schedule_data = self.db_cluster_collection.find({"$and": [
                    {"date": {
                        "$gte": date_time.convert_datetime_str_to_obj(self.request_params["start_date"]),
                        "$lte": date_time.convert_datetime_str_to_obj(self.request_params["end_date"])
                    }, 
                    "user_id": self.request_params["user_id"]},
                ]}, surpressed_fields)

            data = json.loads(dumps(schedule_data))

            return response.set_response_ok(data)

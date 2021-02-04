from api.models.schedule import Schedule
from api.models.url_params import UrlParams
from api.config import Config, DevelopmentConfig, TestingConfig, ProductionConfig
from api.utils import date_time
from bson.json_util import dumps, loads

import jsonschema
import datetime
import json

class ScheduleActivities(object):
    def __init__(self, activity_data):
        self.activity_data = activity_data
        self.request_params = activity_data["request_params"] if activity_data["request_params"] else None

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
            schedule_activities = self.activity_data["request_params"]
            start_date = schedule_activities["start_date"]
            end_date = schedule_activities["end_date"]

            start_date_obj = date_time.convert_datetime_str_to_obj(start_date)
            end_date_obj = date_time.convert_datetime_str_to_obj(end_date)


            if start_date_obj is None and start_date is not None:
                self.errors.append("invalid start_date")

            if end_date_obj is None and end_date is not None:
                self.errors.append("invalid end_date")

            if start_date > end_date:
                self.errors.append("start date is after end date")

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
            return {
                "success": False,
                "errors": self.errors
            }

        else:
            date = date_time.convert_datetime_str_to_obj(self.activity_data["date"])

            self.db_cluster_collection.find_one_and_replace(
                {"date": date},
                self.activity_data,
                projection=None,
                upsert=True
            )

            return {
                "success": True,
                "errors": self.errors
            }


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
        errors = self.errors

        request_dates = self.set_request_dates({
            "start_date": self.request_params["start_date"],
            "end_date": self.request_params["end_date"]
        })

        self.request_params["start_date"] = request_dates["start_date"]
        self.request_params["end_date"] = request_dates["end_date"]

        valid_request_dates = self.validate_request_dates()
        valid_request_params = self.validate_request_params()

        if len(errors):
            return {
                "success": False,
                "errors": errors
            }

        else:
            surpressed_fields = self.get_surpressed_fields()

            schedule_data = self.db_cluster_collection.find({"$and": [
                {"date": {
                    "$gte": date_time.convert_datetime_str_to_obj(self.request_params["start_date"]),
                    "$lt": date_time.convert_datetime_str_to_obj(self.request_params["end_date"])
                }},
                {"user_id": self.request_params["user_id"]}
            ]}, surpressed_fields)

            data = json.loads(dumps(schedule_data))

            return {
                "success": True,
                "data": data,
                "errors": errors,
            }

from flask.globals import request
from api.utils.json_encoder import JsonEncoder
# from api.models.schedule import Schedule
from api.models.url_params import UrlParams
from api.config import Config, DevelopmentConfig, TestingConfig, ProductionConfig
from api.utils import date_time, query, response
from bson.json_util import dumps, loads
from bson.objectid import ObjectId

from pymongo.collection import ReturnDocument

import jsonschema
import datetime
import json

class ScheduleActivities(object):
    def __init__(self, request_data):
        # self.activity_data = activity_data
        # self.errors = []
        # self.request_params = activity_data.get("request_params", None)
        self.user_id = request_data.get("user_id", None)
        self.activity_id = request_data.get("activity_id", None)
        self.date = request_data.get("date", None)
        self.start_date = request_data.get("start_date", None)
        self.end_date = request_data.get("end_date", None)
        self.activities = request_data.get("activities", None)

        self.return_details = request_data.get("returnDetails", None)
        self.return_ids = request_data.get("returnIdsOnly", None)
        self.return_summary = request_data.get("returnSummary", None)

        self.collection = Config.DB_CLUSTER[Config.COLLECTION_NAMES["user_schedule"]]

    # def is_valid_format(self):
    #     try:
    #         jsonschema.validate(instance=self.activity_data, schema=Schedule.data, format_checker=jsonschema.FormatChecker())
    #         return True
        
    #     except jsonschema.ValidationError as error:
    #         self.errors.append(error.message)
    #         return False


    # def is_valid_activity_format(self):
    #     try:
    #         activities = self.activity_data["activities"]
    #         for activity in activities:
    #             activity_details = activity["details"]
    #             activity_name = activity["name"]
                
    #             for detail in activity_details:
    #                 activity_schema = Schedule.activities["details"][activity_name]
    #                 jsonschema.validate(instance=detail, schema=activity_schema, format_checker=jsonschema.FormatChecker())

    #                 return True

    #     except jsonschema.ValidationError as error:
    #         self.errors.append(error.message)
    #         return False


    # def is_valid_request_params(self):
    #     try:
    #         jsonschema.validate(instance=self.request_params, schema=UrlParams.schedule, format_checker=jsonschema.FormatChecker())
    #         return True
        
    #     except jsonschema.ValidationError as error:
    #         self.errors.append(error.message)
    #         return False


    # def is_valid_request_date_range(self):
    #     try:
    #         request_params = self.activity_data["request_params"]
    #         start_date = request_params["start_date"]
    #         end_date = request_params["end_date"]

    #         start_date_obj = date_time.convert_datetime_str_to_obj(start_date)
    #         end_date_obj = date_time.convert_datetime_str_to_obj(end_date)

    #         if start_date_obj is None and start_date is not None:
    #             self.errors.append("Invalid start_date {date}".format(date=start_date))

    #         if end_date_obj is None and end_date is not None:
    #             self.errors.append("Invalid end_date {date}".format(date=end_date))

    #         if start_date > end_date:
    #             self.errors.append("start_date {start} is after end_date {end}".format(start=start_date, end=end_date))

    #         if len(self.errors):
    #             return False

    #         return True

    #     except:
    #         return False 


    def get_surpressed_fields(self):
        surpressed_fields = {
            "user_id": 0,
        }

        if self.return_ids is True:
            surpressed_fields["_id"] = 1
            surpressed_fields["activities"] = 0
            surpressed_fields["date"] = 0
            surpressed_fields["name"] = 0
            surpressed_fields["details"] = 0
            surpressed_fields["last_updated"] = 0
            return surpressed_fields

        if self.return_details is True:
            return surpressed_fields

        if self.return_details is False:
            surpressed_fields["details"] = 0


        if self.return_summary is True:
            surpressed_fields["details"] = 0
            surpressed_fields["last_updated"] = 0
            return surpressed_fields

        return surpressed_fields


    # def get_scheduled_data_by_id(self):
    #     activity_id = self.request_params["activity_id"]
    #     user_id = self.request_params["user_id"]

    #     schedule_data = self.collection.find_one(
    #         {
    #             "_id": ObjectId(activity_id),
    #             "user_id": user_id
    #         }, self.get_surpressed_fields()
    #     )

    #     data = json.loads(dumps(schedule_data))
    #     return data


    # def get_scheduled_data_by_date_range(self):
    #     if self.is_valid_request_date_range() is False:
    #         return response.set_error(self.errors)

    #     start_date = date_time.convert_datetime_str_to_obj(self.request_params["start_date"])
    #     end_date = date_time.convert_datetime_str_to_obj(self.request_params["end_date"])

    #     schedule_data = self.collection.find({"$and": [
    #         {"date": {
    #             "$gte": start_date,
    #             "$lte": end_date
    #         }, 
    #         "user_id": self.request_params["user_id"]},
    #     ]}, self.get_surpressed_fields())

    #     data = json.loads(dumps(schedule_data))
    #     return data


    def get_by_id(self):
        activity_found = self.collection.find_one({
                "_id": ObjectId(self.activity_id),
                "user_id": ObjectId(self.user_id)
            }, self.get_surpressed_fields())

        data = json.loads(json.dumps(activity_found, indent=4, cls=JsonEncoder))
        return data


    def get_by_date_range(self):
        activities_found = self.collection.find({"$and": [
            {"date": {
                "$gte": date_time.convert_datetime_str_to_obj(self.start_date),
                "$lte":  date_time.convert_datetime_str_to_obj(self.end_date)
            }, 
            "user_id": ObjectId(self.user_id)},
        ]}, self.get_surpressed_fields())

        data = json.loads(json.dumps(list(activities_found), indent=4, cls=JsonEncoder))
        return data


    def create(self):
        documents = [dict(item, **{
            "user_id": ObjectId(self.user_id),
            "last_updated": date_time.get_current_datetime(),
            "date": date_time.convert_datetime_str_to_obj(self.date)
        }) for item in self.activities]

        self.collection.insert(documents)
        return response.set_ok({"message": "Successfully Created."})


    def get(self):
        if self.start_date != self.end_date:
            if date_time.is_before_date(self.start_date, self.end_date) is False:
                return response.set_error(["start_date is after end_date"])

        if self.activity_id is not None:
            data = self.get_by_id()

        else:
            data = self.get_by_date_range()

        return response.set_ok(data)


    def update_schedule_data(self):
        if self.is_valid_format() is False:
            return response.set_error(self.errors)

        if self.is_valid_activity_format() is False:
            return response.set_error(self.errors)
        
        date_obj = date_time.convert_datetime_str_to_obj(self.activity_data["date"])

        updated_data_params = { 
            "date": date_time.convert_datetime_str_to_obj(self.activity_data["date"]),
            "user_id": self.activity_data["user_id"]
        }

        data_to_update = dict(self.activity_data, **updated_data_params)

        updated_data = self.collection.find_one_and_update(
            updated_data_params,
            {"$set": data_to_update },
            upsert=True,
            return_document=ReturnDocument.AFTER
        )

        data = {
            "id": updated_data["_id"]
        }

        return response.set_ok(data)


    def delete_scheduled_data(self):
        if "activity_id" not in self.request_params:
            return False
        
        if query.object_id_is_valid(self.request_params["activity_id"]) is False:
            return False
        
        self.collection.delete_one({'_id': ObjectId(self.request_params["activity_id"])})
        return True
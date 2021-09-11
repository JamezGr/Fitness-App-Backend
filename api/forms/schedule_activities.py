from api.response import ErrorMessage, SuccessMessage
from flask.globals import request
from flask.json import jsonify
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

        # activities as object ids
        self.items = request_data.get("items", None)

        self.return_details = request_data.get("returnDetails", None)
        self.return_ids = request_data.get("returnIdsOnly", None)
        self.return_summary = request_data.get("returnSummary", None)

        self.collection = Config.DB_CLUSTER[Config.COLLECTION_NAMES["user_schedule"]]

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
            "created_at": date_time.get_current_datetime(),
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


    def delete(self):
        if self.activity_id is not None:
            return self.delete_by_id()
        
        if self.items is not None:
            return self.delete_many()


    def delete_many(self):
        try:
            items = [ObjectId(item) for item in self.items]

            deleted_items = self.collection.delete_many({
                "_id": { "$in": items},
                "user_id": ObjectId(self.user_id)
            })

            if deleted_items.deleted_count > 0:
                return SuccessMessage.SCHEDULE["BULK_DELETE"]
            else:
                return SuccessMessage.SCHEDULE["EMPTY_DELETE"]

        except:
            return ErrorMessage.SCHEDULE["DELETE_ERROR"]


    def delete_by_id(self):
        try: 
            deleted_resource = self.collection.delete_one({
                "_id": ObjectId(self.activity_id),
                "user_id": ObjectId(self.user_id)
            })

            if deleted_resource.deleted_count > 0:
                return SuccessMessage.SCHEDULE["SINGLE_DELETED"]
            else:
                return SuccessMessage.SCHEDULE["EMPTY_DELETE"]

        except:
            return ErrorMessage.SCHEDULE["DELETE_ERROR"]

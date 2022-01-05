from api.models.schedule import ActivitySchema
from api.response import ErrorMessage, SuccessMessage
from api.utils import cache
from api.utils.files import save_file
from api.utils.json_encoder import JsonEncoder
from api.utils.database import db, file_db
from api.utils import date_time, response
from api.utils.database import mongo
from bson.objectid import ObjectId

import json

class ScheduleActivities(object):
    def __init__(self, request_data):
        self.user_id = request_data.get("user_id", None)
        self.activity_id = request_data.get("activity_id", None)
        self.date = request_data.get("date", None)
        self.start_date = request_data.get("start_date", None)
        self.end_date = request_data.get("end_date", None)

        self.items = request_data.get("items", None)
        self.return_details = request_data.get("returnDetails", None)
        self.return_ids = request_data.get("returnIdsOnly", None)
        self.return_summary = request_data.get("returnSummary", None)
        self.return_comments = request_data.get("returnComments", None)

        self.file = request_data.get("file", None)
        self.collection = db.user_schedule

        self.attachments_count_key_suffix = "attachments_count"


    def get_attachments_count_cache_key(self):
        return self.activity_id + "_" + self.attachments_count_key_suffix


    def update_attachments_count_cached_value(self, count):
        cache.set_value(self.get_attachments_count_cache_key(), value=count)


    def get_attachments_count_cached_value(self):
        cached_value = cache.get_value(self.get_attachments_count_cache_key())

        if cached_value is not None:
            return int(cached_value)

        return cached_value


    def upload_attachment(self):
        activity = self.get_activity_by_id()
        file = self.file

        if activity is None:
            print("No activity found for provided activity_id")
            return response.set_ok({ "message": "No activity found for provided activity_id" })


        if file.content_type not in ActivitySchema.allowed_attachment_files_by_type[activity["name"]]:
            print("File type provided not allowed.")
            return response.set_error({ "message": "Invalid File Type Provided." }, status=400)

        metadata = {
            "activity_id": self.activity_id,
            "user_id": self.user_id,
        }

        attachments_count = self.get_attachments_count()

        if attachments_count >= ActivitySchema.max_attachments:
            self.update_attachments_count_cached_value(attachments_count)
            return response.set_ok({ "message": "No attachments uploaded. Maximum number of attachments uploaded have been reached." })

        save_file(file, metadata=metadata)
        self.update_attachments_count_cached_value(attachments_count + 1)

        return response.set_ok({ "message": "ok" })


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
            surpressed_fields["comments"] = 0
            return surpressed_fields

        if self.return_comments is False:
            surpressed_fields["comments"] = 0

        if self.return_details is True:
            return surpressed_fields

        if self.return_details is False:
            surpressed_fields["details"] = 0

        if self.return_summary is True:
            surpressed_fields["details"] = 0
            surpressed_fields["last_updated"] = 0
            return surpressed_fields

        return surpressed_fields


    # get number of attachments by user id and activity id
    def get_attachments_count(self):
        print("fetching cache", self.get_attachments_count_cached_value())
        if self.get_attachments_count_cached_value() is not None:
            attachments_count = self.get_attachments_count_cached_value()

        else:
            attachments_count = file_db.fs.files.count({
                "kwargs.user_id": self.user_id,
                "kwargs.activity_id": self.activity_id
            })

        return int(attachments_count)


    def get_activity_by_id(self):
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
        }) for item in self.items]

        created_items = self.collection.insert_many(documents)
        item_ids = [str(id) for id in created_items.inserted_ids]
        return response.set_ok(item_ids)


    def update(self):
        update_count = 0

        for item in self.items:
            updated_item = self.collection.find_one_and_update({
                "_id": ObjectId(item["id"]),
                "user_id": ObjectId(self.user_id),
                "name": item["name"]
            },
            {
                "$set": {
                    "details": item["details"],
                    "comments": item["comments"]
                }
            })

            if updated_item:
                update_count += 1

        if update_count == 0:
            message = "No items were updated."

        else:
            message = "Successfully Updated"

        return response.set_ok({"message": message})


    def get(self):
        if self.start_date != self.end_date:
            if date_time.is_before_date(self.start_date, self.end_date) is False:
                return response.set_error(["start_date is after end_date"])

        if self.activity_id is not None:
            data = self.get_activity_by_id()

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

from api.models.schedule import Schedule
from api.config import Config, DevelopmentConfig, TestingConfig, ProductionConfig
from api.utils import date_time
import jsonschema
import datetime

class ScheduleActivities(object):
    def __init__(self, activity_data):
        self.activity_data = activity_data
        self.errors = []
        self.db_cluster_collection = Config.DB_CLUSTER[Config.COLLECTION_NAMES["user_schedule"]]

    def validate_schedule_format(self, schedule_data):
        try:
            jsonschema.validate(instance=schedule_data, schema=Schedule.data, format_checker=jsonschema.FormatChecker())
            return True
        
        except jsonschema.ValidationError as error:
            print("line 17", error.message)
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
            self.activity_data["date"] = date_time.convert_datetime_string_to_datetime_object(self.activity_data["date"])

            self.db_cluster_collection.find_one_and_replace(
                {"date": self.activity_data["date"]},
                self.activity_data,
                projection=None,
                upsert=True
            )

            return {
                "success": True,
                "errors": self.errors
            }

    def get_scheduled_data():
        print("fetched")

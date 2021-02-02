from api.models.schedule import Schedule
import jsonschema

class ScheduleActivities(object):
    def __init__(self, activity_data):
        self.activity_data = activity_data
        self.errors = []


    def validate_schedule_format(self, schedule_data):
        try:
            jsonschema.validate(instance=schedule_data, schema=Schedule.data, format_checker=jsonschema.FormatChecker())
            return True
        
        except jsonschema.ValidationError as error:
            # print(error.message)
            self.errors.append(error.message)
            return False


    def validate_activity_format(self, activity_data): 
        try: 
            activity_schema = Schedule.activities["data"]
            jsonschema.validate(instance=activity_data, schema=activity_schema, format_checker=jsonschema.FormatChecker())

            return True

        except jsonschema.ValidationError as error:
            # print(error.message)
            self.errors.append(error.message)
            return False


    def validate_activity_details(self, activity_details, activity_name):
        try:
            activity_schema = Schedule.activities["details"][activity_name]
            jsonschema.validate(instance=activity_details, schema=activity_schema, format_checker=jsonschema.FormatChecker())

            return True

        except jsonschema.ValidationError as error:
            # print(error.message)
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
            return False

        else:
            return True

    def get_scheduled_data():
        print("fetched")

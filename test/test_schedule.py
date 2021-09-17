from api.forms.schedule_activities import ScheduleActivities
from test.data.schedule import post_request_body, get_request_params

import unittest

class TestSchedule(unittest.TestCase):
    def create_activities(self):
        return ScheduleActivities(post_request_body).create()


    def delete_activities(self, items):
        delete_params = {
            "items": items,
            "user_id": post_request_body["user_id"]
        }

        return ScheduleActivities(delete_params).delete_many()


    def test_create_activities(self):
        inserted_activities = self.create_activities()
        self.delete_activities(inserted_activities["data"])

        self.assertEqual(len(inserted_activities["data"]), len(post_request_body["items"]))


    def test_get_activity_by_id(self):
        inserted_activities = self.create_activities()

        activity_id = inserted_activities["data"][0]

        get_params = {
            "user_id": post_request_body["user_id"],
            "activity_id": activity_id
        }

        activities_found = ScheduleActivities(get_params).get()
        self.delete_activities(inserted_activities["data"])

        self.assertEqual(activities_found["status"], 200)


    def test_get_activity_by_date_range(self):
        inserted_activities = self.create_activities()
        date_to_find = post_request_body["date"]

        get_params = {
            "user_id": post_request_body["user_id"],
            "start_date": date_to_find,
            "end_date": date_to_find,
        }

        activities_found = ScheduleActivities(get_params).get()
        self.delete_activities(inserted_activities["data"])

        self.assertEqual(activities_found["status"], 200)
        self.assertEqual(len(activities_found["data"]), len(post_request_body["items"]))

    
    def test_delete_activity_by_id(self):
        inserted_activities = self.create_activities()
        activity_id = inserted_activities["data"][0]

        delete_params = {
            "user_id": post_request_body["user_id"],
            "activity_id": activity_id,
            **get_request_params
        }

        ScheduleActivities(delete_params).delete_by_id()
        activities_found = ScheduleActivities(delete_params).get()

        self.assertEqual(activities_found["data"], {})


    def test_delete_many_activities(self):
        inserted_activity_1 = self.create_activities()
        inserted_activity_2 = self.create_activities()

        activity_id_1 = inserted_activity_1["data"][0]
        activity_id_2 = inserted_activity_2["data"][0]

        self.delete_activities([activity_id_1, activity_id_2])

        params_1 = {
            "user_id": post_request_body["user_id"],
            "activity_id": activity_id_1
        }

        params_2 = {
            **params_1,
            "activity_id": activity_id_2
        }

        activity_found_1 = ScheduleActivities(params_1).get()
        activity_found_2 = ScheduleActivities(params_2).get()

        self.assertEqual(activity_found_1["data"], {})
        self.assertEqual(activity_found_2["data"], {})


    # def test_update_activities(self):

if __name__ == '__main__':
    unittest.main()
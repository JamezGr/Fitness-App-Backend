import random_object_id

post_request_body = {
    "user_id": random_object_id.generate(),
    "date": "2021-09-09",
    "items": [{
        "name": "lifting",
        "details": [{
            "intensity": "very_light",
            "exercise": "test",
            "weight": 100,
            "reps": 1,
            "sets": 1
        }],
        "comments": "unit tests❗❗"
    }]
}

get_request_params = {
    "returnDetails": True,
    "returnIdsOnly": False,
    "returnSummary": False,
    "returnComments": False,
}
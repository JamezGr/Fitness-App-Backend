test_valid_schedule_data = {
	"activities": [
		{
		"details": [
			{
			"INTENSITY": "MODERATE",
			"STROKE": "Breaststroke",
			"DISTANCE": 1,
			"TIME": "00:10:00"
			}
		],
		"name": "SWIMMING",
		"start_time": "09:30",
		"end_time": "10:00"
		}
	],
	"user_id": "5fa81914efcc8c0d997195de",
	"date": str("2021-02-04")
}

test_valid_request_params = {
    "request_params" : {
        "start_date": "2021-02-04",
        "end_date": "2021-02-04",
        "user_id": "5fa81914efcc8c0d997195de",
        "returnDetails": True,
        "returnIdsOnly": False,
        "returnSummary": False
    }
}

test_invalid_schedule_data = {
	"activities": [
		{
		"details": [
			{
			"INTENSITY": "MODERATE",
			"STROKE": "Breaststroke",
			"DISTANCE": 1,
			"TIME": "00:10:00"
			}
		],
		"name": "SWIMMING",
		"start_time": "09:30",
		"end_time": "10:00"
		}
	],
	"user_id": "TEST",
	"date": "TEST"
}
class UrlParams:
    schedule = {
        "type": "object",
        "properties": {
            "user_id": {
                "type": "string"
            },
            "start_date": {
                "type": "string",
                "format": "date"
            },
            "end_date": {
                "type": "string",
                "format": "date"
            },
            "returnDetails": {
                "type": "boolean"
            },
            "returnIdsOnly": {
                "type": "boolean"
            },
            "returnSummary": {
                "type": "boolean"
            }
        },
        "required": [
            "user_id", 
            "start_date", 
            "end_date", 
            "returnDetails", 
            "returnIdsOnly", 
            "returnSummary"
        ]
    }
class Schedule:
    data = {
        "type": "object",
        "properties": {
            "activities": {
                "type": "array"
            },
            "user_id": {
                "type": "string"
            },
            "date": {
                "type": "string",
                "format": "date"
            }
        },
        "required": ["activities", "user_id", "date"]
    }


    activities = {
        "data": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "details": {
                    "type": "array"
                },
                "start_time": {
                    "type": "string",
                    "pattern": "^([01]?[0-9]|2[0-3]):[0-5][0-9]$"
                },
                "end_time": {
                    "type": "string",
                    "pattern": "^([01]?[0-9]|2[0-3]):[0-5][0-9]$"
                },
                "name": {
                    "type": "string"
                }
            },
            "required": ["details", "start_time", "end_time", "name"]
        },
        "details": {
            "LIFTING": {
                "type": "object",
                "properties": {
                    "INTENSITY": {
                        "type": "string"
                    },
                    "EXERCISE": {
                        "type": "string"
                    },
                    "WEIGHT": {
                        "type": "number",
                        "minimum": 2.5
                    },
                    "SETS": {
                        "type": "number",
                        "minimum": 1
                    },
                    "REPS": {
                        "type": "number",
                        "minimum": 1
                    }
                },
                "required": ["INTENSITY", "EXERCISE", "WEIGHT", "SETS", "REPS"]
            },
            "RUNNING": {
                "type": "object",
                "properties": {
                    "INTENSITY": {
                        "type": "string"
                    },
                    "DISTANCE": {
                        "type": "number",
                        "minimum": 0.1
                    },
                    "TIME": {
                        "type": "string",
                        "format": "time"
                    }
                },
                "required": ["INTENSITY", "DISTANCE", "TIME"]
            },
            "CYCLING": {
                "type": "object",
                "properties": {
                    "INTENSITY": {
                        "type": "string"
                    },
                    "DISTANCE": {
                        "type": "number",
                        "minimum": 0.1
                    },
                    "TIME": {
                        "type": "string",
                        "format": "time"
                    }
                },
                "required": ["INTENSITY", "DISTANCE", "TIME"]
            },
            "SWIMMING": {
                "type": "object",
                "properties": {
                    "INTENSITY": {
                        "type": "string"
                    },
                    "STROKE": {
                        "type": "string"
                    },
                    "DISTANCE": {
                        "type": "number",
                        "minimum": 0.1
                    },
                    "TIME": {
                        "type": "string",
                        "format": "time"
                    }
                },
                "required": ["INTENSITY", "STROKE", "DISTANCE", "TIME"]
            }
        }
    }
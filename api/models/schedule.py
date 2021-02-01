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
                "type": "number"
            }
        },
        "required": ["activities", "user_id", "date"]
    }


    activities = {
        "data": {
            "type": "object",
            "properties": {
                "details": {
                    "type": "object"
                },
                "start_time": {
                    "type": "number"
                },
                "end_time": {
                    "type": "number"
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
                    "GOAL_TIME": {
                        "type": "string"
                    }
                },
                "required": ["INTENSITY", "DISTANCE", "GOAL_TIME"]
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
                    "GOAL_TIME": {
                        "type": "string"
                    }
                },
                "required": ["INTENSITY", "DISTANCE", "GOAL_TIME"]
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
                    "GOAL_TIME": {
                        "type": "string"
                    }
                },
                "required": ["INTENSITY", "STROKE", "DISTANCE", "GOAL_TIME"]
            }
        }
    }
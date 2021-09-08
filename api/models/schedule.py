class ActivitySchema:
    intensity_types = ["very_light", "light", "moderate", "hard", "maximum"]

    default_activity_schema = {
        "intensity": {
            "type": "string",
            "enum": intensity_types,
            "description": "Intensity of given exercise."
        }
    }

    # for activities involving distance and time metrics
    distance_time_schema = {
        "distance": {
            "type": "number",
            "minimum": 0.025
        },
        "time": {
            "type": "integer",
            "minimum": 1
        }
    }

    default_required_activity_fields = ["name", "details"]

    by_type = {
        "lifting": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "name": {
                    "type": "string",
                    "const": "lifting"
                },
                "details": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            **default_activity_schema,
                            "exercise": {
                                "type": "string"
                            },
                            "weight": {
                                "description": "Weight of exercise performed in kilograms",
                                "type": "number",
                                "minimum": 2.5
                            },
                            "sets": {
                                "description": "Number of Sets performed for given exercise",
                                "type": "integer",
                                "minimum": 1
                            },
                            "reps": {
                                "description": "Number of Reps performed for given exercise",
                                "type": "integer",
                                "minimum": 1
                            }
                        },
                        "required": ["intensity", "exercise", "weight", "sets", "reps"]
                    }
                },
            },
            "required": default_required_activity_fields
        },
        "running": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "name": {
                    "type": "string",
                    "const": "running"
                },
                "details": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            **default_activity_schema,
                            **distance_time_schema
                        },
                        "required": ["intensity", "distance", "time"]
                    }
                },
            },
            "required": default_required_activity_fields
        },
        "walking": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "name": {
                    "type": "string",
                    "const": "walking"
                },
                "details": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            **default_activity_schema,
                            **distance_time_schema
                        },
                        "required": ["intensity", "distance", "time"]
                    }
                },
            },
            "required": default_required_activity_fields
        },
        "cycling": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "name": {
                    "type": "string",
                    "const": "cycling"
                },
                "details": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            **default_activity_schema,
                            **distance_time_schema
                        },
                        "required": ["intensity", "distance", "time"]
                    }
                },
            },
            "required": default_required_activity_fields
        },
        "swimming": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "name": {
                    "type": "string",
                    "const": "swimming"
                },
                "details": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            **default_activity_schema,
                            **distance_time_schema,
                            "stroke": {
                                "type": "string",
                                "minLength": 3,
                            }
                        },
                        "required": ["intensity", "distance", "time", "stroke"]
                    }
                },
            },
            "required": default_required_activity_fields
        },
    }

    request_body = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "user_id": {
                "type": "string"
            },
            "activities": {
                "type": "array",
                "minItems": 1,
                "items": {
                    "oneOf": [
                        by_type["lifting"],
                        by_type["running"],
                        by_type["walking"],
                        by_type["cycling"],
                        by_type["swimming"]
                    ]
                }
            },
            "date": {
                "type": "string",
                "format": "date"
            }
        }
    }
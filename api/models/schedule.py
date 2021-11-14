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

    default_required_activity_fields = ["name", "details", "comments"]

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
                "comments": {
                    "type": "string",
                    "maxLength": 500
                }
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
                "comments": {
                    "type": "string",
                    "maxLength": 500
                }
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
                    },
                    "comments": {
                        "type": "string",
                        "maxLength": 500
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
                "comments": {
                    "type": "string",
                    "maxLength": 500
                }
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
                "comments": {
                    "type": "string",
                    "maxLength": 500
                }
            },
            "required": default_required_activity_fields
        },
    }

    insert_params = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "user_id": {
                "type": "string"
            },
            "items": {
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
            },
        },
        "required": ["user_id", "items", "date"]
    }

    update_additional_params = {
        "activity_id": {
            "type": "string"
        },
        "comments": {
            "type": "string",
            "maxLength": 500
        }
    }

    update_required_fields = default_required_activity_fields + ["activity_id"]

    update_params = {
        "type": "object",
        "properties": {
            "user_id": {
                "type": "string"
            },
            "items": {
                "type": "array",
                "minItems": 1,
                "items": {
                    "anyOf": [
                        {
                            **by_type["lifting"],
                            "properties": {
                                **by_type["lifting"]["properties"],
                                **update_additional_params
                            },
                            "required": update_required_fields
                        },
                        {
                            **by_type["running"],
                            "properties": {
                                **by_type["running"]["properties"],
                                **update_additional_params
                            },
                            "required": update_required_fields
                        },
                        {
                            **by_type["walking"],
                            "properties": {
                                **by_type["walking"]["properties"],
                                **update_additional_params
                            },
                            "required": update_required_fields
                        },
                        {
                            **by_type["cycling"],
                            "properties": {
                                **by_type["cycling"]["properties"],
                                **update_additional_params
                            },
                            "required": update_required_fields
                        },
                        {
                            **by_type["swimming"],
                            "properties": {
                                **by_type["swimming"]["properties"],
                                **update_additional_params
                            },
                            "required": update_required_fields
                        }
                    ]
                }
            },
        },
        "required": ["user_id", "items"]
    }
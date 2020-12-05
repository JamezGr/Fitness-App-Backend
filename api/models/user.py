class User(object):
    def __init__(self, email=None, user=None, password=None, confirm_password=None):
        self.email = email
        self.user = user
        self.password = password
        self.confirm_password = confirm_password


class UserProfile:
    updatable_fields = {
        "type": "object",
        "properties": {
            "birthday": {
                "type": "string",
                "format": "date"
            },
            "gender": {
                "type": "string",
                "enum": ["MALE", "FEMALE", "OTHER"]
            },
            "unit_measurement": {
                "type": "string",
                "enum": ["METRIC", "IMPERIAL"]
            },
            "height": { 
                "type": "number" 
            },
            "current_weight": { 
                "type": "number" 
            },
            "goal_weight": { 
                "type": "number" 
            }
        }
    }
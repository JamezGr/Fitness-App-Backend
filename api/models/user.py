class User(object):
    def __init__(self, email=None, user=None, password=None, confirm_password=None):
        self.email = email
        self.user = user
        self.password = password
        self.confirm_password = confirm_password


class UserStats:
    updatable_fields = {
        "type": "object",
        "properties": {
            "gender": { "type": "string",
                        "pattern": "[FM]" },
            "height": { "type": "number" },
            "weight": { "type": "number" },
            "avatar": { "type": "string" }
        }
    }
from api.utils import encode_auth_token


class SuccessMessage(object):
    def __init__(self, form_data):
        self.email = form_data.email
        self.username = form_data.user

    def set_login(self):
        return {
                "status": "200",
                "data": {
                    "username": self.username,
                    "auth_token": encode_auth_token(self.username).decode('utf-8')
                },
                "message": "Successfully Logged In"
        }

    def create_username(self):
        return {
            "status": "201",
            "data": {
                "email": self.email,
                "username": self.username,
            },
            "message": "Successfully Registered"
        }

    def update_profile(self):
        return {
            "status": "201",
            "data": {
                "username": self.username,
            },
            "message": "Successfully Updated User Profile."
        }


class ErrorMessage:
    LOGIN = {
        "INVALID_USERNAME": {
            "status": "404",
            "source": {"pointer": "/api/login"},
            "title": "Invalid Username",
            "detail": "Username does not exist."
        },
        "INVALID_CREDENTIALS": {
            "status": "401",
            "source": {"pointer": "/api/login"},
            "title": "Invalid Credentials Sent",
            "detail": "Invalid Username or Password Entered."
        },
        "INVALID_REQUEST": {
            "status": "400",
            "source": {"pointer": "/api/login"},
            "title": "Invalid Request",
            "detail": "The request could not be satisfied."
        }
    }

    REGISTER = {
        "INVALID_EMAIL": {
            "status": "422",
            "source": {"pointer": "/api/users"},
            "title": "Invalid Email Sent",
            "detail": "Email Requested does not exist or has an Invalid Format"
        },
        "USERNAME_EXISTS": {
            "status": "409",
            "source": {"pointer": "/api/users"},
            "title": "Username and/or Email already exists",
            "detail": "Username and/or Email Entered already Exists."
        },
        "INVALID_CREDENTIALS": {
            "status": "422",
            "source": {"pointer": "/api/users"},
            "title": "Invalid Credentials Sent",
            "detail": "Username Requested did not meet all of the criteria. (Min. 3 Characters, Max. 30 Characters, " +
                      "Does not Include '&=()<>+,' Characters)"
        },
        "INVALID_REQUEST": {
            "status": "400",
            "source": {"pointer": "/api/users"},
            "title": "Invalid Request",
            "detail": "The request could not be satisfied."
        }
    }

    USER_PROFILE = {
        "INVALID_USER": {
            "status": "400",
            "source": {"pointer": "/api/users/<user>/profile"},
            "title": "Invalid User.",
            "detail": "Unable to create Profile for User that does not exist."
        },
        "NO_PROFILE_AVAILABLE": { 
            "status": "422",
            "source": {"pointer": "/api/users/<user>/profile"},
            "title": "No Profile Available.",
            "detail": "No Profile Available for Requested Username."
        },
        "PROFILE_ALREADY_EXISTS": {
            "status": "409",
            "source": {"pointer": "/api/users/<user>/profile"},
            "title": "Profile already Exists.",
            "detail": "Profile already Exists for Requested User."
        }
    }

    FORBIDDEN = {
        "status": "403",
        "title": "Forbidden",
        "detail": "Not Authorized to access this resource/api."
    }

    UNKNOWN_ERROR = {
        "status": "0",
        "title": "HttpErrorResponse",
        "detail": "Unknown Error Occured."
    }

    INVALID_REQUEST = {
        "status": "401",
        "title": "Invalid Request",
        "detail": "The request could not be satisfied."
    }
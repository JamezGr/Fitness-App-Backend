from typing import Union
from flask.json import jsonify

def set_ok(data = None):
    success_reponse = {
        "success": True,
        "status": 200,
        "data": {}
    }

    if data is not None:
        success_reponse["data"] = data

    return success_reponse

def set_error(errors, status = 400):
    return {
        "success": False,
        "errors": errors,
        "status": status
    }


def response_ok(message=None, status=200, data=None):
    response = {}

    if message is not None:
        response["message"] = message

    if data is not None:
        response["data"] = data

    return jsonify(response), status


def response_error(message=None, errors=None, status=400):
    response = {}

    if message is not None:
        response["message"] = message

    if errors is not None:
        response["errors"] = errors
    
    return jsonify(response), status
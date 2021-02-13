def set_response_ok(data):
    success_reponse = {
        "success": True
    }

    if data is not None:
        success_reponse["data"] = data

    return success_reponse

def set_response_error(errors):
    return {
        "success": False,
        "errors": errors
    }
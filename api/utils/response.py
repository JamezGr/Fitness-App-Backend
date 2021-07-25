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
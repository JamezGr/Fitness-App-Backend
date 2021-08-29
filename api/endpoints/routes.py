from api.utils import query
from api.forms.map_route import MapRoute
from api.utils import response

from flask import Blueprint
from flask import jsonify, request

from webargs import fields
from webargs.flaskparser import use_args

blueprint = Blueprint(name="routes_endpoint", import_name=__name__)

@blueprint.route("routes", methods=['POST'])
def add_route():
    file = request.files['file']

    if file.filename == '':
        return jsonify(response.set_error(["Required request part 'file' is not present"])), 401

    request_body = {
        "file": file,
    }

    upload_response = MapRoute(request_body).upload()

    ## return object id of saved file
    return jsonify(upload_response), upload_response["status"]


@blueprint.route("routes", methods=['GET'])
@use_args({
    "route_id": fields.Str(required=True),
    })
def get_route(args):
    request_params = args
    route_id = request_params["route_id"]

    if route_id is None or query.object_id_is_valid(route_id) is False:
        return jsonify(response.set_error(["route_id is invalid format."]))

    get_response = MapRoute(request_params).get()

    if get_response is None:
        return jsonify(response.set_ok({"message": "no route found"}))

    return get_response

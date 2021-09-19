from flask import Blueprint
from flask import jsonify
from flask_cors import cross_origin

from api.response import ErrorMessage

blueprint = Blueprint(name="default_endpoint", import_name=__name__)

@cross_origin
@blueprint.route('/', methods=['GET', 'POST'])
def default_response():
    return jsonify(ErrorMessage.INVALID_REQUEST), 401
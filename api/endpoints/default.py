from flask import Blueprint
from flask_jwt_extended import jwt_required
from flask import jsonify

from api.response import ErrorMessage

blueprint = Blueprint(name="default_endpoint", import_name=__name__)

@blueprint.route('/', methods=['GET', 'POST'])
def default_response():
    return jsonify(ErrorMessage.INVALID_REQUEST), 401
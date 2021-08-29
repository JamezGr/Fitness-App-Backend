from flask import Blueprint
from api.utils.database import mongo

blueprint = Blueprint(name="uploads_endpoint", import_name=__name__)

@blueprint.route('uploads/<path:filename>')
def get_upload(filename):
    return mongo.send_file(filename)
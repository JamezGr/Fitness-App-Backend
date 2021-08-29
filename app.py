from api.config import Config

from api.response import *
from api.forms.forms import *
from api.forms.map_route import MapRoute
from api.utils import *
from api.utils import response
from api.utils.database import mongo
from api.endpoints import (
    default,
    auth,
    user,
    uploads,
    schedule,
)

from flask import Flask, request, jsonify
from flask_cors import CORS

from flask_jwt_extended import JWTManager

URI_CLUSTER = Config.DB_CONNECTION_STRING
DB_CLUSTER = URI_CLUSTER[Config.DB_CLUSTER_NAME]

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = Config.SECRET_KEY
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['MONGO_URI'] = Config.DB_CONNECTION_URI

jwt = JWTManager(app)
mongo.init_app(app)

CORS(app, resources={
    r"/*": {
        "origins": "*"
    }
})

app.register_blueprint(default.blueprint, url_prefix="/")
app.register_blueprint(auth.blueprint, url_prefix=Config.ENDPOINT_PREFIX)
app.register_blueprint(user.blueprint, url_prefix=Config.ENDPOINT_PREFIX)
app.register_blueprint(uploads.blueprint, url_prefix="/")
app.register_blueprint(schedule.blueprint, url_prefix=Config.ENDPOINT_PREFIX)

@app.route("/api/routes", methods=['POST'])
def add_route():
    if "file" not in request.files:
        return jsonify(ErrorMessage.INVALID_REQUEST), 401

    file = request.files['file']

    request_body = {
        "file": file,
        "user_id": request.form["user_id"]
    }

    route = MapRoute(request_body)

    if route.is_gpx_file() is False:
        data_response = response.set_error(["File type is not gpx"])

    saved_file = mongo.save_file(file.filename, file)

    ## return object id of saved file
    data_response = response.set_ok({"id": str(saved_file)})

    return jsonify(data_response), data_response["status"]

# No cacheing at all for API endpoints.
@app.after_request
def add_header(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    
    return response

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify(ErrorMessage.METHOD_NOT_ALLOWED), 405

@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
    error_message = ErrorMessage.EXPIRED_TOKEN

    return jsonify(error_message), 401
    
if __name__ == "__main__":
    app.run(debug=True)

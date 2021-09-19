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
    routes,
    user,
    uploads,
    schedule,
)

from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS

from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = Config.SECRET_KEY
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['MONGO_URI'] = Config.DB_CONNECTION_STRING

jwt = JWTManager(app)
mongo.init_app(app)

# cors = CORS()
# cors.init_app(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}})

CORS(app, supports_credentials=True)

# No cacheing at all for API endpoints.
@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    
    return response

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify(ErrorMessage.METHOD_NOT_ALLOWED), 405

@jwt.expired_token_loader
def my_expired_token_callback():
    error_message = ErrorMessage.EXPIRED_TOKEN

    return jsonify(error_message), 401


app.register_blueprint(default.blueprint, url_prefix="/")
app.register_blueprint(auth.blueprint, url_prefix=Config.ENDPOINT_PREFIX)
app.register_blueprint(user.blueprint, url_prefix=Config.ENDPOINT_PREFIX)
app.register_blueprint(uploads.blueprint, url_prefix="/")
app.register_blueprint(schedule.blueprint, url_prefix=Config.ENDPOINT_PREFIX)
app.register_blueprint(routes.blueprint, url_prefix=Config.ENDPOINT_PREFIX)
    
if __name__ == "__main__":
    app.run(debug=True)

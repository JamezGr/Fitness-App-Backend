import os
import uuid
from bson.objectid import ObjectId
from functools import wraps
from flask import request, abort
from werkzeug.utils import secure_filename

from gridfs import GridFS
from gridfs.errors import NoFile
from marshmallow.fields import String
from api.utils.database import mongo

## Extension Names for File Uploads 
class Extension:
    gpx = ".gpx"
    jpeg = ".jpeg"
    jpg = ".jpg"
    png = ".png"
    gif = ".gif"

def is_valid_extension(file_name, file_extension):
    current_file_extension = os.path.splitext(file_name)[1]
    
    return str(current_file_extension) == file_extension

def get_file_by_id(id):
    storage = GridFS(mongo.db, "fs")

    try:
        file = storage.get(file_id=ObjectId(id))
        return file.read()
    
    except NoFile:
        return None


def get_request_file_size(file):
    file.seek(0, os.SEEK_END)
    file_size = file.tell()

    return file_size

# upload file to grid fs
# returns oid of saved file
def save_file(file, metadata):
    # generate random file name
    filename = str(uuid.uuid4()) + "." + file.filename.split('.')[-1]

    saved_file = mongo.save_file(filename=filename, fileobj=file, kwargs=metadata)
    return saved_file


def delete_file(id):
    storage = GridFS(mongo.db, "fs")

    try:
        storage.delete(file_id=ObjectId(id))
        return True
    
    # not sure what to do here...
    except Exception as e:
        return False


def limit_content_length(max_length):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            cl = request.content_length
            if cl is not None and cl > max_length:
                abort(413)
            return f(*args, **kwargs)
        return wrapper
    return decorator
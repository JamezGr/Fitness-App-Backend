import os
from bson.objectid import ObjectId

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
    saved_file = mongo.save_file(file.filename, file, kwargs=metadata)
    return saved_file


def delete_file(id):
    storage = GridFS(mongo.db, "fs")

    try:
        storage.delete(file_id=ObjectId(id))
        return True
    
    # not sure what to do here...
    except Exception as e:
        return False

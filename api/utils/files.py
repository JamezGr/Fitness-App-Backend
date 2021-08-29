import os
from bson.objectid import ObjectId

from gridfs import GridFS
from gridfs.errors import NoFile
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

def delete_file(id):
    storage = GridFS(mongo.db, "fs")

    try:
        storage.delete(file_id=ObjectId(id))
        return True
    
    # not sure what to do here...
    except Exception as e:
        return False
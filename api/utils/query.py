import bson

def object_id_is_valid(id):
    return bson.objectid.ObjectId.is_valid(id)
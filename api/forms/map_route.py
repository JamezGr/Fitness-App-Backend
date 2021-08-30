from api.response import ErrorMessage, SuccessMessage
from api.utils import files
from api.utils.database import mongo
from api.utils import response

class MapRoute(object):
    def __init__(self, form_data):
        self.file = form_data.get("file", None)
        self.user_id = form_data.get("user_id", None)
        self.route_id = form_data.get("route_id", None)

    def is_gpx_file(self):
        return files.is_valid_extension(self.file.filename, files.Extension.gpx)

    def upload(self):
        if self.is_gpx_file() is False:
            return ErrorMessage.MAP_ROUTE["INVALID_FILE_TYPE"]

        uploaded_file = mongo.save_file(self.file.filename, self.file)

        return response.set_ok({"id": str(uploaded_file)})
    
    def get(self):
        file = files.get_file_by_id(self.route_id)    

        return file
    
    def delete(self):
        deleted_file = files.delete_file(self.route_id)

        if deleted_file is True:
            return SuccessMessage.MAP_ROUTE["DELETED"]
        
        else:
            return response.set_error(["no file found with provided route_id"])
            

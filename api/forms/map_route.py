from api.utils import files
from api.utils.database import mongo
from api.utils import response, query

from gridfs import GridFS

class MapRoute(object):
    def __init__(self, form_data):
        self.file = form_data.get("file", None)
        self.user_id = form_data.get("user_id", None)
        self.route_id = form_data.get("route_id", None)

    def is_gpx_file(self):
        return files.is_valid_extension(self.file.filename, files.Extension.gpx)

    def upload(self):
        if self.is_gpx_file() is False:
            return response.set_error(["Required request part 'file' is not present"])

        uploaded_file = mongo.save_file(self.file.filename, self.file)
        # return id of uploaded file
        return response.set_ok({"id": str(uploaded_file)})
    
    def get(self):
        file = files.get_file_by_id(self.route_id)            

        return file
        
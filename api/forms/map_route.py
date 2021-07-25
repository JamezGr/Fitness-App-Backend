from api.utils import files, query, response
# from app import mongo

class MapRoute(object):
    def __init__(self, form_data):
        self.file = form_data["file"]
        self.user_id = form_data["user_id"]

    def is_gpx_file(self):
        return files.is_valid_extension(self.file.filename, files.Extension.gpx)
        
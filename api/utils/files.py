import os

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
import json
import datetime

# source: https://stackoverflow.com/questions/67596481/how-to-remove-all-the-oid-and-date-in-a-json-file
class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return int(obj.strftime("%s"))
        if hasattr(obj, '__str__'):  # This will handle ObjectIds
            return str(obj)

        return super(JsonEncoder, self).default(obj)
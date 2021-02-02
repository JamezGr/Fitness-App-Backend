import datetime

## convert YYYY-MM-DD to date time object
def convert_datetime_string_to_datetime_object(datetime_str):
    try:
        return datetime.datetime.strptime(datetime_str, "%Y-%m-%d")

    except:
        return None

def get_current_datetime():
    return datetime.datetime.now()
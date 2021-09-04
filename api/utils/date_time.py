import datetime

## convert YYYY-MM-DD to date time object
def convert_datetime_str_to_obj(datetime_str):
    try:
        return datetime.datetime.strptime(datetime_str, "%Y-%m-%d")

    except:
        return None

def get_current_datetime():
    return datetime.datetime.now()

def get_current_datetime_as_string():
    curent_datetime = get_current_datetime()
    current_datetime_str = convert_datetime_obj_to_str(curent_datetime)

    return current_datetime_str

def get_first_day_of_selected_month(datetime_obj):
    try:
        return datetime_obj.replace(day=1)

    except:
        return None

def convert_datetime_obj_to_str(datetime_obj):
    try:
        return datetime_obj.strftime("%Y-%m-%d")

    except:
        return None

def validate_datetime(datetime_obj):
    if isinstance(datetime_obj, datetime.datetime):
        return True

    else:
        return False

# check if date in format YYYY-MM-DD
def validate_date_format(date_string):
    try:
        datetime.datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def is_before_date(start_date, end_date):
    if validate_date_format(start_date) is False or validate_date_format(end_date) is False:
        return False

    start_date_obj = convert_datetime_str_to_obj(start_date)
    end_date_obj = convert_datetime_str_to_obj(end_date)

    return start_date_obj.date() < end_date_obj.date()
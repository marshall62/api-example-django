import datetime


def time_format(dt_str):
    ''' Convert a time string as it comes out of the Appointment table from YYYY-mm-ddTHH:MM:SS to a simple HH:MM on 12hr clock'''
    dt = datetime.datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S")
    hr = dt.hour % 12 if dt.hour > 12 else dt.hour
    if hr == 0:
        hr = 12
    m = "0" + str(dt.minute) if dt.minute < 10 else str(dt.minute)
    return "{}:{}".format(hr,m)

def timestamp_api_format (dt):
    '''Convert a date to a timestamp in the format the API wants it yyyy-mm-ddThh:mm:ss'''
    return dt.strftime("%Y-%m-%dT%H:%M:%S")


def apidt_to_ts (dt_str):
    ymd, t = dt_str.split('T')
    y,m,d = ymd.split('-')
    h,min,s = t.split(':')
    dt = datetime.datetime(int(y), int(m), int(d),int(h),int(min),int(s))
    return dt
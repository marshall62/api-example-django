import datetime


def time_format(dt_str):
    ''' Convert a time string as it comes out of the Appointment table from YYYY-mm-ddTHH:MM:SS to a simple HH:MM on 12hr clock'''
    dt = datetime.datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S")
    hr = dt.hour % 12 if dt.hour > 12 else dt.hour
    m = "0" + str(dt.minute) if dt.minute < 10 else str(dt.minute)
    return "{}:{}".format(hr,m)
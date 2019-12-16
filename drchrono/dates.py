import datetime


def time_format(dt_str):
    ''' Convert a time string as it comes out of the Appointment table from YYYY-mm-ddTHH:MM:SS to a simple HH:MM on 12hr clock'''
    dt = datetime.datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S")
    hr = dt.hour % 12 if dt.hour > 12 else dt.hour
    ampm = "AM" if dt.hour < 12  else "PM"
    if hr == 0:
        hr = 12
    m = "0" + str(dt.minute) if dt.minute < 10 else str(dt.minute)

    return "{}:{} {}".format(hr,m, ampm)

def timestamp_api_format (dt):
    '''Convert a date to a timestamp in the format the API wants it yyyy-mm-ddThh:mm:ss'''
    return dt.strftime("%Y-%m-%dT%H:%M:%S")

def time_diff (d1_str, d2_str):
    '''
    Times given in yyyy-mm-ddTHH:MM:SS
    :param d1_str:
    :param d2_str:
    :return: (minutes, seconds)
    '''
    d = apidt_to_ts(d1_str) - apidt_to_ts(d2_str)
    datetime.timedelta(0, 8, 562000)
    return divmod(d.days * 86400 + d.seconds, 60)

def min2minSec (min):
    return hrminsec(min // 60, min % 60)

def hrminsec (min, sec):
    s = ""
    if min > 60:
        s += str(min // 60) + ":"
    min = min % 60
    if min >= 0 and min < 10:
        s += "0{}:".format(min)
    else: s += str(min) + ":"
    if sec >= 0 and sec < 10:
        s += "0"+str(sec)
    else: s += str(sec)
    return s



def apidt_to_ts (dt_str):
    ymd, t = dt_str.split('T')
    y,m,d = ymd.split('-')
    h,min,s = t.split(':')
    dt = datetime.datetime(int(y), int(m), int(d),int(h),int(min),int(s))

    return dt
from string import capwords
from datetime import datetime

ABSOLUTE_ZERO = -273.15


def to_celsius(temp_kelvin, round_num=0):
    if round_num == -1:
        return temp_kelvin + ABSOLUTE_ZERO
    else:
        return int(round(temp_kelvin + ABSOLUTE_ZERO, round_num))


def prep_location_str(loc):
    return capwords(loc.strip())


def format_time(time):
    return datetime.fromtimestamp(time).strftime('%d/%m %H:%S')

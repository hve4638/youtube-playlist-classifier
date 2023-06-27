import re
from datetime import timedelta

re_duration_format = re.compile("PT([0-9]|H|S|M)+")
re_duration_h = re.compile(".*?([0-9]+)H.*?")
re_duration_m = re.compile(".*?([0-9]+)M.*?")
re_duration_s = re.compile(".*?([0-9]+)S.*?")

def youtube_duration(duration:str):
    hours = 0
    minutes = 0;
    seconds = 0;
    if re_duration_format.match(duration) is None:
        pass
    else:
        if m := re_duration_h.match(duration):
            hours = int(m.group(1))
        if m := re_duration_m.match(duration):
            minutes = int(m.group(1))
        if m := re_duration_s.match(duration):
            seconds = int(m.group(1))
    
    return hours, minutes, seconds



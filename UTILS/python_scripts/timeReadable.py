import datetime
import time

intervals = (
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
    )

def display_time(seconds, granularity=4):
    result = []

    iter = 0
    for name, count in intervals:
        value = seconds // count
        seconds -= value * count
        if value == 1:
            name = name.rstrip('s')
        result.append("{} {}".format(str(value).zfill(2), name))
        iter = iter + 1
    return ' '.join(result[:granularity])

timeSeconds = 86400
print("{} seconds is {}".format(timeSeconds, display_time(timeSeconds, 3)))

nextDate = datetime.datetime.fromtimestamp(timeSeconds + time.time()).strftime("%d-%m-%Y %H:%M:%S")
print("now + {} seconds is [{}]".format(timeSeconds, nextDate))

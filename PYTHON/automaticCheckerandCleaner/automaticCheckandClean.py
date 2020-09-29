import sys
import subprocess
import time

# display time with XX days XX hours XX minutes XX seconds format from
# seconds in int
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

# intervals for time check
intervals = (
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
    )

# fetch sys arguments
procWait    = int(sys.argv[1])
timeType    = sys.argv[2]

# handle time types
timeMult = 0
timeTypeString = None
if timeType == "-ss" :
    timeMult = 1
    timeTypeString = "seconds"
if timeType == "-mm" :
    timeMult = 60
    timeTypeString = "minutes"
if timeType == "-hh" :
    timeMult = 3600
    timeTypeString = "hours"
if timeType == "-dd" :
    timeMult = 86400
    timeTypeString = "days"

# exit if error
if timeMult == 0 :
    print("Incorrect argument format.")
    exit()

while True :
    # measure time in
    tIn = time.time()

    # clean fromStreamer folder
    cleanFromStreamer = subprocess.Popen([sys.executable, "jsonCleaner.py", "fromStreamer"])
    cleanFromStreamer.communicate()

    # check tweets
    tweetChecker = subprocess.Popen([sys.executable, "tweetChecker.py"])
    tweetChecker.communicate()

    # cautious wait
    time.sleep(1)

    # clean fromChecker folder
    cleanFromStreamer = subprocess.Popen([sys.executable, "jsonCleaner.py", "fromChecker"])
    cleanFromStreamer.communicate()

    #
    tOut = time.time()

    # diff to process
    diff = tOut - tIn

    # wait until next start
    timeToWait_temp = procWait * timeMult - diff
    if(timeToWait_temp < 0) :
        timeToWait = 1 * timeMult
    else:
        timeToWait = timeToWait_temp

    # log
    diffReadable = display_time(diff)
    nextCheckDate = datetime.fromtimestamp(timeToWait + time.time()).strftime("%d-%m-%Y %H:%M:%S")
    print("Check lasted {}\tRestarting on [{}]".format(diffReadable, nextCheckDate))

    # sleep
    time.sleep(timeToWait)

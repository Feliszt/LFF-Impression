import sys
import subprocess
import time

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
    tellTime.communicate()

    # clean fromChecker folder
    cleanFromStreamer = subprocess.Popen([sys.executable, "jsonCleaner.py", "fromChecker"])
    tellTime.communicate()

    # check tweets
    tellTime = subprocess.Popen([sys.executable, "tweetChecker.py"])
    tellTime.communicate()

    #
    tOut = time.time()

    # diff to process
    diff = tOut - tIn
    print("diff = {}".format(diff))

    # wait until next start
    timeToWait_temp = procWait * timeMult - diff
    if(timeToWait_temp < 0) :
        timeToWait = 1 * timeMult
    else:
        timeToWait = timeToWait_temp
    time.sleep(timeToWait)




#

#
#      --- Plannify a python script ---
#      Specify a script name, run time and wait time in between runs
#

import time
import datetime
import os
import signal
import subprocess
import sys

# edit python command depending on OS
pythonCmd = "python"
if sys.platform == "linux" or platform == "linux2":
    pythonCmd = "python3"

# fetch sys arguments
procName    = sys.argv[1]
procLength  = int(sys.argv[2])
procWait    = int(sys.argv[3])
timeType    = sys.argv[4]

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

# exit if error
if timeMult == 0 :
    print("Incorrect argument format.")
    exit()

while True :

    # start process
    timeNow = datetime.datetime.fromtimestamp(time.time()).strftime("%d-%m-%Y %H:%M:%S")
    print("[STREAMPLANNER @ {}]\tStart process for {} {}.".format(timeNow, procLength, timeTypeString))
    process = subprocess.Popen([pythonCmd, procName + '.py'])

    # run process for specified time
    time.sleep(procLength * timeMult)

    # kill process
    timeNow = datetime.datetime.fromtimestamp(time.time()).strftime("%d-%m-%Y %H:%M:%S")
    print("[STREAMPLANNER @ {}]\tKill process and wait {} {}.".format(timeNow, procWait, timeTypeString))
    process.kill()

    # wait until next start
    time.sleep(procWait * timeMult)

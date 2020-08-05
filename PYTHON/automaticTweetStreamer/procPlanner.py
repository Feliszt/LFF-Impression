#
#      --- Plannify a python script ---
#      Specify a script name, run time and wait time in between runs
#

import time
import os
import signal
import subprocess
import sys

# fetch sys arguments
procName    = sys.argv[1]
procLength  = int(sys.argv[2])
procWait    = int(sys.argv[3])

while True :

    # start process
    print("[STREAMPLANNER]\tStart process for " + str(procLength) + " minutes.")
    process = subprocess.Popen(['python', procName + '.py'])

    # run process for specified time
    time.sleep(procLength * 60)

    # kill process
    print("[STREAMPLANNER]\tKill process and wait " + str(procWait) + " minutes.\n")
    process.kill()

    # wait until next start
    time.sleep(procWait * 60)

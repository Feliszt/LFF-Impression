#
#      This script performs the streaming and storing of tweets.
#

import json
import random
import time
import datetime

# edit python command depending on OS
pythonCmd = "python"
if sys.platform == "linux" or sys.platform == "linux2":
    pythonCmd = "python3"

# get config file
config = "../../DATA/config.json"
with open(config, 'r') as f_config :
    config = json.load(f_config)

# main loop
while True :
    # start process
    timeNow = datetime.datetime.fromtimestamp(time.time()).strftime("%d-%m-%Y %H:%M:%S")
    print("[STREAMPLANNER @ {}]\tStart process for {} seconds.".format(timeNow, config["tweetStreamerDuration"]))
    process = subprocess.Popen([pythonCmd, "tweetStreamer" + '.py'])

    # run process for specified time
    time.sleep(config["tweetStreamerDuration"])

    # kill process
    timeNow = datetime.datetime.fromtimestamp(time.time()).strftime("%d-%m-%Y %H:%M:%S")
    procWait = int(random.uniform(config["tweetStreamerWaitMin"], config["tweetStreamerWaitMax"]))
    print("[STREAMPLANNER @ {}]\tKill process and wait {} seconds.".format(timeNow, procWait))
    process.kill()

    # wait until next start
    time.sleep(procWait)

#
#   - script to populate a fake logFile to make a long video of tweets
#

import os
import random
import json

# set target number of tweets
numTweets = 4000

# set folders and files
tweetsFolder = "../../DATA/fromChecker/"
resultLogFile = "../../DATA/events/videoPDF/videoPDF_tweetsLog.txt"

# get files
tweetsFiles = [f for f in os.listdir(tweetsFolder) if os.path.isfile(os.path.join(tweetsFolder, f))]

#
n = 0
with open(resultLogFile, 'a') as f_out:
    while(n <= numTweets):
        # open random file
        random_file = random.choice(tweetsFiles)
        n = n + 1

        with open(tweetsFolder + random_file, 'r') as f_in :
            tweetsData = json.load(f_in)["tweets"]

            # get a single random tweet
            random_tweet  = random.choice(tweetsData)

            # string to append
            str_toappend = "{} {}\n".format(random_file, random_tweet["id"])

            # write to file
            f_out.write(str_toappend)

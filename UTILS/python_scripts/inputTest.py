#
#   - script to make log file
#

import os
import random
import json

# set target number of tweets
numTweets = 500
eventName = "OE2020"

# set folders and files
tweetsFolder = "../../DATA/fromChecker/"
resultLogFile = "../../DATA/events/videoPDF/{}_tweetsLog.txt".format(eventName)

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

            # show tweet
            print(random_tweet["text"])

            print("oui (o)? non (n)?")

            #
            goodValidation = False
            pickTweet = False
            while(not goodValidation) :
                validation = input()
                if(validation != "o" and validation != "n") :
                    continue
                else:
                    goodValidation = True
                    if(validation == "o") :
                        pickTweet = True

            if(pickTweet) :
                print("TWEET PICKED")
            else:
                print("TWEET DISCARDED")


            # string to append
            str_toappend = "{} {}\n".format(random_file, random_tweet["id"])

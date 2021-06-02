#
#   -- Search for specific words in tweets
#

from os import listdir
from os.path import isfile, join
import json

# set words list
wordsList = ['bite']

# specify folder
folder = "../../DATA/fromChecker/"

# get files
onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]

# loop through files
for file in onlyfiles :

    # get file name
    fileName = file.split('.')[0]

    # save all lines in a dict
    with open(folder + file, "r", encoding="utf8") as dataFile:
        # load json that is in file
        tweets = json.load(dataFile)["tweets"]

        # loop through all tweets
        tweetNum = 0
        for tweet in tweets :
            # incr
            tweetNum = tweetNum + 1

            #
            #if any(word in tweet['text'] for word in wordsList) :
            #    print("[{}] - {} - [{}]".format(fileName, tweet['id'], tweet['text'].replace('\n', ' ')))

            if tweet['has_image'] :
                print("[{}] - {} - [{}]".format(fileName, tweet['id'], tweet['text'].replace('\n', ' ')))

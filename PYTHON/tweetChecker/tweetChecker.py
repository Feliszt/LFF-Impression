#
#   -- This script goes through all the tweets that have been saved
#   -- and check how many likes and favorites it received.
#   -- Saves the result if the tweet hasn't been liked nor favorited.
#

import tweepy
from os import listdir
from os.path import isfile, join
from keys import *
import json
import time
import datetime

# function that process a tweet to check if it follows the rules
# for .rar installation
def processTweet(_tweet) :
    # get extended tweet
    try :
        tweet_status = _api.get_status(_id, tweet_mode="extended")
    except tweepy.TweepError as e:
        return -1, None

    # get today's date
    dateToday = datetime.datetime.now().strftime("%d/%m/%Y")

    # append stuff to tweet
    _tweet['checked_at']     = dateToday
    _tweet['retweet_count']  = tweet_status.retweet_count
    _tweet['favorite_count'] = tweet_status.favorite_count

    if(_tweet['retweet_count'] > 0 or _tweet['favorite_count'] > 0) :
        return -2, None

    if(_tweet["possibly_sensitive"] == True) :
        return -3, None

    return 1, _tweet

# authentification and creation of api object
auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# set folders
folderToProcess = "../_TWEETS_AND_DATA/fromStreamer/"
folderToSave = "../_TWEETS_AND_DATA/fromChecker/toclean/"

# exclude list
excludeList = ["07-08-2020"]

# get files
onlyfiles = [f for f in listdir(folderToProcess) if isfile(join(folderToProcess, f))]

# loop through files
for file in onlyfiles :
    # get file name only
    fileToPrint = file.split('.')[0]

    # ignore if in exclude list
    if fileToPrint in excludeList :
        print("[{}] in exclude list.".format(fileToPrint))
        continue

    # print info
    print("Processing [{}].".format(fileToPrint))

    #
    with open(folderToProcess + file) as dataFile:
        # get data
        data = json.load(dataFile)["tweets"]

        #
        tweetTotal = len(data)

        # loop through all tweets
        tweetNum = 0
        for tweet in data :
            # we start by waiting to not overflow the API
            time.sleep(1.01)

            # incr
            tweetNum = tweetNum + 1

            # process tweet
            res, tweet_checked = processTweet(tweet)

            # set success state
            successState = ""
            if(res == -1) :
                successState = "Can't access tweet."
            if(res == -2) :
                successState = "Tweet has like or favorite."
            if(res == -3) :
                successState = "Tweet is offensive."
            if(res == 1) :
                # write to file
                with open(folderToSave + fileToPrint + '_checked.json', 'a') as outfile:
                    json.dump(tweet_checked, outfile)
                    outfile.write('\n')
                #
                successState = "Save completed."

            # print info
            print("{} / {} of {}\t[{}] => {}".format(tweetNum, tweetTotal, fileToPrint, tweet["id"], successState))

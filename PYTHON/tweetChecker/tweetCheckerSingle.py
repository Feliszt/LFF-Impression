import tweepy
from keys import *
import json
import time
import datetime

# authentification and creation of api object
auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# file with tweet
folder = "D:/PERSO/_CREA/rar/_DEV/PYTHON/automaticTweetStreamer/json/cleaned/"
file = "07-08-2020.json"
fileToPrint = file.split(".")[0]

#
with open(folder + file) as dataFile:
    # get data
    data = json.load(dataFile)["tweets"]

    #
    tweetTotal = len(data)

    # loop through all tweets
    tweetNum = 0
    for tweet in data :
        # print text
        print("Tweet #{} / {}\tid : {} [{}]".format(tweetNum, tweetTotal, tweet["id"], tweet["text"]))

        # leave after 1 tweet
        #if tweetNum == 1:
        #    break

        tweetNum = tweetNum + 1

        # get extended tweet
        try :
            tweet_status = api.get_status(tweet["id"], tweet_mode="extended")
        except tweepy.TweepError as e:
             print("TWEET INACCESSIBLE")
             time.sleep(1.01)
             print()
             continue

        # get today's date
        dateToday = datetime.datetime.now().strftime("%d/%m/%Y")

        # append stuff to tweet
        tweet['checked_at']     = dateToday
        tweet['retweet_count']  = tweet_status.retweet_count
        tweet['favorite_count'] = tweet_status.favorite_count

        if(tweet['retweet_count'] > 0 or tweet['favorite_count'] > 0) :
            print("LIKE OU RETWEET")
            time.sleep(1.01)
            print()
            continue

        # write to file
        with open('json/' + fileToPrint + '_checked.json', 'a') as outfile:
            json.dump(tweet, outfile)
            outfile.write('\n')

        time.sleep(1.01)
        print()

import tweepy
from keys import *
import json
import time
import datetime
import sys
import random
import threading

def analyze_tweet(status, verbose) :

    # get time of creation
    createdAt = status.created_at
    createdAtTimestamp = datetime.datetime.timestamp(createdAt) + 7200  # correct for timezone
    createdAt = datetime.fromtimestamp(createdAtTimestamp)

    # get current time
    now = datetime.datetime.now()
    nowTimestamp = datetime.datetime.timestamp(now)

    # get diff
    diffTime = int(nowTimestamp - createdAtTimestamp)

    # init json
    jsonData = {}

    # check if retweet
    try:
        status.retweeted_status
        if(verbose) :
            print("RETWEET")
        return -1, diffTime
    except AttributeError:  # Not a Retweet
        if(verbose) :
            print("NOT A RETWEET")

    # check if reply
    if(status.in_reply_to_status_id is not None) :
        if(verbose) :
            print("REPLY")
        return -2, diffTime
    if(verbose) :
        print ("NOT A REPLY")

    # check if quoted
    if(status.is_quote_status) :
        if(verbose) :
            print("QUOTE")
        return -3, diffTime
    if(verbose) :
        print ("NOT A QUOTE")

    # create json
    #post stuff
    jsonData['created_at']          = str(createdAt)
    jsonData['id']                  = status.id
    jsonData['id_str']              = status.id_str
    jsonData['text']                = status.text
    jsonData['retweet_count']       = status.retweet_count
    jsonData['favorite_count']      = status.favorite_count

    # user stuff
    jsonData['user_id']             = status.user.id
    jsonData['user_id_str']         = status.user.id_str
    jsonData['user_name']           = status.user.name
    jsonData['user_screen_name']    = status.user.screen_name
    jsonData['user_followers']      = status.user.followers_count

    # image stuff
    # check if tweet has media
    jsonData['has_image']   = False
    has_media = False
    try:
        medias = status.extended_entities['media']
        has_media = True

        # loop through media
        num_media = 0
        for el in medias:
            # check if photo
            if(el['type'] == 'photo') :
                num_media += 1

                # if has at least one image
                if(num_media == 1) :
                    if(verbose) :
                        print("HAS IMAGE")
                    jsonData['has_image']   = True
                    jsonData['images']      = []

                # append image
                jsonData['images'].append({
                    'link'  : el['media_url'] + "?format=jpg&name=large",
                    'w'     : el['sizes']['large']['w'],
                    'h'     : el['sizes']['large']['h']
                })

    except AttributeError:  # Not a Retweet
        if(verbose) :
            print("HAS NO IMAGE")

    # check if has url
    if(len(status.entities['urls']) > 0) :
        return -4, diffTime

    # check if has mention
    if(len(status.entities['user_mentions']) > 0) :
        return -5, diffTime

    # check if has media but no photo
    if(has_media and not jsonData['has_image']) :
        return -6, diffTime

    return jsonData, diffTime

#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def __init__(self):
        super(MyStreamListener, self).__init__()

        # get date
        dateTime = datetime.datetime.now().strftime("%d-%m-%Y")

        # get hour
        h = int(datetime.datetime.now().strftime("%H"))
        hMapped = 0
        if(h >= 0 and h < 6):
            hMapped = 1
        if(h >= 6 and h < 12):
            hMapped = 2
        if(h >= 12 and h < 18):
            hMapped = 3
        if(h >= 18 and h < 24):
            hMapped = 4

        #self.jsonName = dateTime + "_" + str(hMapped)
        self.jsonName = dateTime
        self.verbose = False
        self.numTweets = 0

    # called when a tweet is received
    def on_status(self, status):
        # perform classification
        if(threading.active_count()) <= 5:
            t = threading.Thread(target=self.processTweet, args=(status,))
            t.start()

    def processTweet(self, _status) :
        #print(status.text)
        #with open('tweet.json', 'w') as outfile:
        #    json.dump(status._json, outfile)

        # analyze tweet
        res, diffTime = analyze_tweet(_status, False)

        # save to file
        if(isinstance(res, dict)) :
            self.numTweets = self.numTweets + 1
            print("[TWEETSTREAMER]\tSaving tweet [{}]\tthreads : {}\tDiffTime = {}".format(self.numTweets, threading.active_count(), diffTime))
            with open(folderToSave + self.jsonName + '.json', 'a') as outfile:
                json.dump(res, outfile)
                outfile.write('\n')
        else :
            if self.verbose :
                if res == -1 :
                    print("[TWEETSTREAMER]\tTweet is a retweet... not saving.")
                if res == -2 :
                    print("[TWEETSTREAMER]\tTweet is a reply... not saving.")
                if res == -3 :
                    print("[TWEETSTREAMER]\tTweet is a quote... not saving.")
                if res == -4 :
                    print("\tTweet has a url... not saving.")
                if res == -5 :
                    print("[TWEETSTREAMER]\tTweet has a mention... not saving.")
                if res == -6 :
                    print("[TWEETSTREAMER]\tTweet has a media but not photo... not saving.")

# folder to save in
folderToSave = "../_TWEETS_AND_DATA/fromStreamer/toclean/"

# authentification and creation of api object
auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# create stream listener
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener, tweet_mode= 'extended')
# launch stream

#myStream.filter(languages=["fr"], track=["non"])
myStream.filter(languages=["fr"], track=["je", "le", "la", "les", "tu", "es", "suis", "a", "as", "es", "oui", "non", "y", "et"])

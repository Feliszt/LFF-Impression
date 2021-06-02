#
#   -- This script perform a check for one tweet
#   -- and check how many likes and favorites it received.
#

import tweepy
from keys import *
import json

# folder
folderData = "../../DATA/"
keyFile = folderData + "keys.json"

# get keys and tokens
with open(keyFile, 'r') as f_keys :
    data = json.load(f_keys)
    api_key = data["api_key"]
    api_secret_key = data["api_secret_key"]
    access_token = data["access_token"]
    access_token_secret = data["access_token_secret"]

# init api
auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# process tweet
tweet_id = "1374381282168172548"
tweet_status = api.get_status(tweet_id, tweet_mode="extended")
tweet_content = tweet_status._json

#
with open(folderData + "others/tweetAnalysis.json", 'w') as outfile:
    json.dump(tweet_status._json, outfile)

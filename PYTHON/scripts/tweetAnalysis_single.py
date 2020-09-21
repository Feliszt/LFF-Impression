#
#   -- This script perform a check for one tweet
#   -- and check how many likes and favorites it received.
#

import tweepy
from keys import *
import json

# authentification and creation of api object
auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# process tweet
tweet_id = "1308052070541529091"
tweet_status = api.get_status(tweet_id, tweet_mode="extended")
tweet_content = tweet_status._json

#
print(tweet_content["possibly_sensitive"])

#
with open('./tweetAnalysis.json', 'w') as outfile:
    json.dump(tweet_status._json, outfile)

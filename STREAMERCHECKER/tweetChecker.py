#
#   -- This script goes through all the tweets that have been saved
#   -- and check how many likes and favorites it received.
#   -- Saves the result if the tweet hasn't been liked nor favorited.
#

import os
import requests
import json
import time
import datetime

def create_url(_tweet_fields_array, _tweet_ids_array):
    tweet_fields = "tweet.fields={}".format(','.join(_tweet_fields_array))
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    ids = "ids={}".format(','.join(_tweet_ids_array))
    # You can adjust ids to include a single Tweets.
    # Or you can add to up to 100 comma-separated IDs
    url = "https://api.twitter.com/2/tweets?{}&{}".format(ids, tweet_fields)
    return url

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2TweetLookupPython"
    return r

def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def get_tweet_from_id(_data, _id):
    for el in _data :
        tweet = json.loads(el)
        if _id == str(tweet["id"]) :
            return tweet
    return None

# set folders
folderData = "../DATA/"
uncheckedTweetsFolder = folderData + "tweetsUnchecked/"
checkedTweetsFolder = folderData + "tweetsChecked/"
imageFolder = folderData + "images/"
keyFile = folderData + "keys.json"
configFile = folderData + "config.json"

# get config
with open(configFile, 'r') as f_config :
    config = json.load(f_config)

# get keys and tokens
with open(keyFile, 'r') as f_keys :
    data = json.load(f_keys)
    bearer_token = data["bearer_key"]

# get files
filesFromStreamer = [f for f in os.listdir(uncheckedTweetsFolder) if os.path.isfile(os.path.join(uncheckedTweetsFolder, f)) and f != ".gitkeep"]
filesFromChecker = [f for f in os.listdir(checkedTweetsFolder) if os.path.isfile(os.path.join(checkedTweetsFolder, f)) and f != ".gitkeep"]

# get today's date
today = datetime.datetime.now()
#today = today.strftime("%d-%m-%Y")

# filter out files that are less than 2 weeks old and files that have already been checked
filesToProcess = [f for f in filesFromStreamer if datetime.datetime.strptime(f.split('.')[0], "%d-%m-%Y") < today - datetime.timedelta(days=config["checkOffset"]) and f.split('.')[0] + "_checked.json" not in filesFromChecker]

# log
print("[tweetChecker] Processing {} files.".format(len(filesToProcess)))

# init some variables
numImageTotal = 0
numTweetTotal = 0

# loop through files
fileIter = 0
fileNum = len(filesToProcess)
for file in filesToProcess :
    # get file name only
    fileToPrint = file.split('.')[0]
    fileIter = fileIter + 1

    # process file
    tweetIdArray = []
    batch = 0
    with open(uncheckedTweetsFolder + file, 'r') as dataFile:
        # get data
        data = dataFile.readlines()
        tweetTotal = len(data)
        numTweetTotal = numTweetTotal + tweetTotal

        # print info
        print("Processing [{}] with {} tweets.".format(fileToPrint, tweetTotal))

        for tweetLine in data :
            tweet = json.loads(tweetLine)
            tweetIdArray.append(tweet["id"])

            if len(tweetIdArray) == 100 or tweetLine == data[-1] :
                # wait to not exceed API limitations
                time.sleep(10)
                batch = batch + 1
                print("Processing [{}]\tBatch #{}.".format(fileToPrint, batch))

                #print("pop request\t{}".format(len(tweetIdArray)))
                twitter_url = create_url(["public_metrics", "entities"], map(str, tweetIdArray))
                tweetIdArray = []
                json_response = connect_to_endpoint(twitter_url)

                if "data" not in json_response :
                    print("Error with json response.")
                    continue

                for res in json_response["data"] :
                    # discard urls
                    if "entities" in res and "urls" in res["entities"]:
                        print("{} has url. discard.".format(res["id"]))
                        continue

                    # discard tweets with retweets, replies, likes or quotes
                    if res["public_metrics"]["like_count"] != 0 or res["public_metrics"]["quote_count"] != 0 or res["public_metrics"]["reply_count"] != 0 or res["public_metrics"]["retweet_count"] != 0 :
                        print("{} has metrics. discard.".format(res["id"]))
                        continue

                    # fetch tweet in source file and store it in database
                    tweet_to_save = get_tweet_from_id(data, res["id"])

                    # discard errors
                    if tweet_to_save == None :
                        print("Couldn't get {}. discard.".format(res["id"]))
                        continue

                    # save tweet
                    print("Saving {}".format(res["id"]))
                    with open(checkedTweetsFolder + fileToPrint + '_checked.json', 'a') as outfile:
                        json.dump(tweet_to_save, outfile)
                        outfile.write('\n')

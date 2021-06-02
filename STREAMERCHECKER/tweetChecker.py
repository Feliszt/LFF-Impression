#
#   -- This script goes through all the tweets that have been saved
#   -- and check how many likes and favorites it received.
#   -- Saves the result if the tweet hasn't been liked nor favorited.
#

import tweepy
import os
import requests
import json
import time
import datetime

# function that process a tweet to check if it follows the rules
# for .rar installation
def processTweet(_tweet) :
    # get extended tweet
    try :
        tweet_status = api.get_status(_tweet["id"], tweet_mode="extended")
    except tweepy.TweepError as e:
        return -1, None

    # get content
    tweet_content = tweet_status._json

    # check if tweet has retweets or favorites
    if(tweet_content["retweet_count"] > 0 or tweet_content["favorite_count"] > 0) :
        return -2, None

    # check if tweet is sensitive according to Twitter API
    if("possibly_sensitive" in tweet_content and tweet_content["possibly_sensitive"]) :
        return -3, None

    # get today's date
    dateToday = datetime.datetime.now().strftime("%d/%m/%Y")

    # append stuff to tweet
    _tweet['checked_at']     = dateToday
    _tweet['retweet_count']  = tweet_content["retweet_count"]
    _tweet['favorite_count'] = tweet_content["favorite_count"]

    return 1, _tweet

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
    api_key = data["api_key"]
    api_secret_key = data["api_secret_key"]
    access_token = data["access_token"]
    access_token_secret = data["access_token_secret"]

# authentification and creation of api object
auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

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

    # print info
    print("Processing [{}]".format(fileToPrint))

    #
    with open(uncheckedTweetsFolder + file, 'r') as dataFile:
        # get data
        data = dataFile.readlines()

        #
        tweetTotal = len(data)
        numImageTotal = numImageTotal + tweetTotal

        # loop through all tweets
        tweetNum = 0
        for tweet_line in data :
            # we start by waiting to not overflow the API
            time.sleep(2)

            # incr
            tweet = json.loads(tweet_line)
            tweetNum = tweetNum + 1

            # print info
            baseDebug = "{} / {} of [{}] file {} / {}".format(tweetNum, tweetTotal, fileToPrint, fileIter, fileNum)
            print("{}\t[{}]".format(baseDebug, tweet["id"]))

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
                successState = "Tweet is fine."

            # show debug
            print("{}\t{}".format(baseDebug, successState))

            # go to next tweet if not fine
            if(res == -1 or res == -2 or res == - 3) :
                continue

            # we check for images, and download them
            if(tweet_checked["has_image"]) :
                # get number of images for this tweet
                numImage = len(tweet_checked["images"])
                numImageTotal = numImageTotal + numImage
                idImage = 1

                # show debug
                print("{}\tTweet has {} images.".format(baseDebug, numImage))

                # loop through all images
                for im in tweet["images"] :
                    baseDebugImage = "image {} / {}".format(idImage, numImage);
                    print("{}\t{}\tlink [{}]".format(baseDebug, baseDebugImage, im["link"]))

                    # download image
                    try :
                        imgData = requests.get(im["link"])
                        time.sleep(1)
                    except requests.exceptions.RequestException as e:
                        print("{}\t{}\t{}".format(baseDebug, baseDebugImage, e))
                        break

                    # get folder to save the image in and create it if it doesn't exist
                    imgSubFolder = imageFolder + fileToPrint
                    if not os.path.exists(imgSubFolder):
                        os.makedirs(imgSubFolder)

                    # save image
                    imgPath = "{}{}/{}_{}.jpg".format(imageFolder, fileToPrint, tweet["id"], idImage)
                    print("{}\t{}\tsaving at [{}]".format(baseDebug, baseDebugImage, imgPath))
                    with open(imgPath, 'wb') as imgFile :
                        imgFile.write(imgData.content)

                    # incr
                    idImage = idImage + 1


            # write to file
            with open(checkedTweetsFolder + fileToPrint + '_checked.json', 'a') as outfile:
                json.dump(tweet_checked, outfile)
                outfile.write('\n')

            # debug
            print("{}\tTweet saved.".format(baseDebug))

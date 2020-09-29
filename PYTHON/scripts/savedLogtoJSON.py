import json
import os

def searchTweet(_file, _id) :
    with open(_file, "r", encoding="utf8") as file :
        # get data
        data = json.load(file)["tweets"]

        # loop through tweets and return when found
        for tweet in data :
            if(tweet["id_str"] == _id) :
                return tweet

# set up file and folders
logFolder = "../../DATA/log/"
logFile = logFolder + "savedTweets.txt"
fromChecker = "../../DATA/fromChecker/"

# init tweet list
tweet_list = []

# read file
with open(logFile, "r", encoding="utf8") as f:
    # read lines
    lines = f.readlines()

    # loop through each line
    for line in lines:
        # clean line
        line = line.strip('\n')
        elements = line.split(' ')

        if(len(elements) != 2) :
            print("ERROR WITH LINE [{}]".format(line))
            continue

        # get info about tweet
        tweetFile = elements[0]
        tweetId = elements[1]

        # get tweet
        tweet = searchTweet(fromChecker + tweetFile, tweetId)

        # append tweet to list
        tweet_list.append(tweet)

# write result json
with open(logFolder + "savedTweets_json.json", "w") as f:
    tweets = {}
    tweets["tweets"] = tweet_list
    json.dump(tweets, f)

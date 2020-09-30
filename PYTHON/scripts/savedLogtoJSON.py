import json
import os
import datetime

# function that searches for tweet with id in its file
def searchTweet(_file, _id) :
    with open(_file, "r", encoding="utf8") as file :
        # get data
        data = json.load(file)["tweets"]

        # loop through tweets and return when found
        for tweet in data :
            if(tweet["id_str"] == _id) :
                return tweet

# map the inputs to the function blocks
months = { 1    : "janvier",
           2    : "février",
           3    : "mars",
           4    : "avril",
           5    : "mai",
           6    : "juin",
           7    : "juillet",
           8    : "août",
           9    : "septembre",
           10   : "octobre",
           11   : "novembre",
           12   : "décembre"
}

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

        # get time of creation
        tweetCreatedAt = tweet["created_at"]
        tweetCreatedAt_datetime = datetime.datetime.strptime(tweetCreatedAt, '%Y-%m-%d %H:%M:%S')

        # get date info
        tweetCreatedAt_day = tweetCreatedAt_datetime.strftime("%d")
        tweetCreatedAt_month = months[int(tweetCreatedAt_datetime.strftime("%m"))]
        tweetCreatedAt_year = tweetCreatedAt_datetime.strftime("%Y")

        # get hour info
        tweetCreatedAt_hour = tweetCreatedAt_datetime.strftime("%H")
        tweetCreatedAt_minute = tweetCreatedAt_datetime.strftime("%M")
        tweetCreatedAt_second = tweetCreatedAt_datetime.strftime("%S")

        # create readable data
        tweetCreatedAt_dateReadable = "{} {} {}".format(tweetCreatedAt_day, tweetCreatedAt_month, tweetCreatedAt_year)
        tweetCreatedAt_hourReadable = "{}h{}".format(tweetCreatedAt_hour, tweetCreatedAt_minute)

        # append to tweet
        tweet["created_at_date_readable"] = tweetCreatedAt_dateReadable
        tweet["created_at_hour_readable"] = tweetCreatedAt_hourReadable

        # append tweet to list
        tweet_list.append(tweet)

# write result json
with open(logFolder + "savedTweets_json.json", "w") as f:
    tweets = {}
    tweets["tweets"] = tweet_list
    json.dump(tweets, f)

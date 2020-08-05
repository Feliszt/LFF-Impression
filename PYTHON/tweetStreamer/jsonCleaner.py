#
#   -- This script cleans a badly appended json file
#

import json

tweet_list = []

numtweet = 0
with open("tweetStreamerDump.json", "r") as f:
    for line in f:
        numtweet += 1
        tweet_list.append(json.loads(line))

print(str(numtweet) + " tweets.")

with open("tweetStreamerDump_clean.json", "w") as f:
    tweets = {}
    tweets["tweets"] = tweet_list
    json.dump(tweets, f)

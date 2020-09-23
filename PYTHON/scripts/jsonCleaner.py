#
#   -- This script cleans a badly appended json file
#

from os import listdir
from os.path import isfile, join
import json

# specify folder
folder = "../../DATA/fromStreamer/toclean/"
folderPrevious = '/'.join(folder.split('/')[:-2]) + '/'

# get files
onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]

# loop through files
for file in onlyfiles :

    # get file name
    fileName = file.split('.')[0]

    # init tweet list
    tweet_list = []
    numtweet = 0

    # save all lines in a dict
    with open(folder + file, "r", encoding="utf8") as f:
        lines = f.readlines()
        for line in lines:
            numtweet += 1
            #print(line)
            tweet_list.append(json.loads(line))

    # display info
    print("Processing [{}] with {} tweets.".format(file, numtweet))

    # save file
    with open(folderPrevious + fileName + '.json', "w") as f:
        tweets = {}
        tweets["tweets"] = tweet_list
        json.dump(tweets, f)

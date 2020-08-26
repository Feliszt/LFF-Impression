#
#   -- This script cleans a badly appended json file
#
from os import listdir
from os.path import isfile, join
import json

# specify folder
folder = "D:/PERSO/_CREA/rar/_DEV/PYTHON/automaticTweetStreamer/json/toclean/"

# get files
onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]

# loop through files
for file in onlyfiles :

    # get file name
    fileName = file.split('.')[0]

    # check if file has already been processed
    if(isfile(folder + fileName + '_clean.json')) :
        print(fileName + " already processed.")
        continue

    # check if file has already been processed
    if("_clean" in file) :
        print(fileName + " is a clean file.")
        continue

    print("Processing [" + file + "]")

    # init tweet list
    tweet_list = []

    numtweet = 0
    with open(folder + file, "r", encoding="utf8") as f:
        lines = f.readlines()
        for line in lines:
            numtweet += 1
            #print(line)
            tweet_list.append(json.loads(line))

    print(str(numtweet) + " tweets.")


    with open(folder + fileName + '_clean.json', "w") as f:
        tweets = {}
        tweets["tweets"] = tweet_list
        json.dump(tweets, f)

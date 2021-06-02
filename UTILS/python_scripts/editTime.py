#
#   -- This script to edit error in timestamp save
#

from os import listdir
from os.path import isfile, join
import json
import datetime

# specify folder
folderToProcess = "../../DATA/fromChecker/"
folderToSave = folderToProcess + "temp/"

# get files
onlyfiles = [f for f in listdir(folderToProcess) if isfile(join(folderToProcess, f))]

# filter
fileToProcess = ["27-08-2020", "28-08-2020", "29-08-2020", "30-08-2020", "31-08-2020", "01-09-2020", "02-09-2020", "03-09-2020", "04-09-2020", "05-09-2020", "06-09-2020", "07-09-2020"]

# loop through files
for file in onlyfiles :
    # get file name
    fileName = file.split('.')[0].split('_')[0]


    if(fileName not in fileToProcess):
        continue

    # init tweet list
    tweet_list = []
    numtweet = 0

    # save all lines in a dict
    with open(folderToSave + file, "w", encoding="utf8") as file_out:
        with open(folderToProcess + file, "r", encoding="utf8") as file_in:
            #
            tweets = json.load(file_in)["tweets"]

            #
            tweets_modified = []

            for tweet in tweets :
                #
                timeCreated = tweet["created_at"]
                timeCreated_dtobject =  datetime.datetime.strptime(timeCreated, '%Y-%m-%d %H:%M:%S')
                timeCreated_timestamp = datetime.datetime.timestamp(timeCreated_dtobject)

                #
                timeCreated_timestamp_correct = timeCreated_timestamp + 7200
                timeCreated_dtobject_correct = datetime.datetime.fromtimestamp(timeCreated_timestamp_correct)
                tweet["created_at"] = str(timeCreated_dtobject_correct)

                #
                tweets_modified.append(tweet)

            #
            tweets = {}
            tweets["tweets"] = tweets_modified
            json.dump(tweets, file_out)

#
#   -- This script to edit error in timestamp save
#

from os import listdir
from os.path import isfile, join
import json
import datetime

# specify folder
folderToProcess = "../_TWEETS_AND_DATA/fromStreamer/toclean/"
folderToSave = folderToProcess + "temp/"

# get files
onlyfiles = [f for f in listdir(folderToProcess) if isfile(join(folderToProcess, f))]

# loop through files
for file in onlyfiles :
    # get file name
    fileName = file.split('.')[0]

    # init tweet list
    tweet_list = []
    numtweet = 0

    # save all lines in a dict
    with open(folderToSave + file, "w", encoding="utf8") as file_out:
        with open(folderToProcess + file, "r", encoding="utf8") as file_in:
            lines = file_in.readlines()
            for line in lines:
                numtweet += 1
                tweet = json.loads(line)

                #
                timeCreated = tweet["created_at"]
                timeCreated_dtobject =  datetime.datetime.strptime(timeCreated, '%Y-%m-%d %H:%M:%S')
                timeCreated_timestamp = datetime.datetime.timestamp(timeCreated_dtobject)

                #
                timeCreated_timestamp_correct = timeCreated_timestamp + 7200
                timeCreated_dtobject_correct = datetime.datetime.fromtimestamp(timeCreated_timestamp_correct)
                tweet["created_at"] = str(timeCreated_dtobject_correct)

                #
                json.dump(tweet, file_out)
                file_out.write('\n')
                #print("{}\t{}".format(timeCreated_dtobject, timeCreated_dtobject_correct))

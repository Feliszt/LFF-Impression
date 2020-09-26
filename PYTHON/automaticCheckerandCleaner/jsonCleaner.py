from os import listdir
from os.path import isfile, join
import json
import sys
import datetime

def createDict(file):
    # init tweet list
    tweet_list = []
    numtweet = 0

    # save all lines in a dict
    with open(file, "r", encoding="utf8") as f:
        lines = f.readlines()
        for line in lines:
            numtweet += 1
            tweet_list.append(json.loads(line))

    # log
    print("[{}] processed with {} tweets.".format(file, numtweet))

    return tweet_list, numtweet

# get args
if(len(sys.argv) != 2) :
    print("Arguments not right.")
    exit()

# get folders
folderToProcess = sys.argv[1]
folderToStore = "../../DATA/" + folderToProcess + "/"
folderToProcess = folderToStore + "toclean/"

# get all files from both folders
filesFromFolder = [f for f in listdir(folderToStore) if isfile(join(folderToStore, f))]
filesFromFolder_toclean = [f for f in listdir(folderToProcess) if isfile(join(folderToProcess, f))]

# get today's date
todayFile = datetime.datetime.now().strftime('%d-%m-%Y') + ".json"

# get files that are in toclean/ folder but not in store folder, also ignore file from today
filesToProcess = [f for f in filesFromFolder_toclean if f not in filesFromFolder and f != todayFile]

# log
print("[jsonCleaner - {}] Processing {} files.".format(folderToProcess, len(filesToProcess)))

# loop through all files and
for el in filesToProcess:

    # create dict from file
    fileToProcess = folderToProcess + el
    tweet_list, numtweet = createDict(fileToProcess)

    # save file
    fileToWrite = folderToStore + el
    with open(fileToWrite, "w") as f:
        tweets = {}
        tweets["tweets"] = tweet_list
        json.dump(tweets, f)

    print("[{}] file written.".format(fileToWrite))

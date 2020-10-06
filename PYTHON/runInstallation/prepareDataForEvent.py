import json
import os
import datetime
import sys
import random
import math

# return number of lines of file
def fileLen(_fileName):
    with open(_fileName) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


# function that searches for tweet with id in its file
def searchTweet(_file, _id) :
    with open(_file, "r", encoding="utf8") as file :
        # get data
        data = json.load(file)["tweets"]

        # loop through tweets and return when found
        for tweet in data :
            if(tweet["id_str"] == _id) :
                return tweet

# define base debug
baseDebug = "[prepareDataForEvent]\t"

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

# check for inputs
if(len(sys.argv) != 2) :
    print("{}Script needs exactly one argument that is the name of the event.".format(baseDebug))
    quit()

# set up file and folders
eventsFolder = "../../DATA/events/"
fromChecker = "../../DATA/fromChecker/"

# get event
eventName = sys.argv[1]
eventFolder = eventsFolder + eventName + "/"

# check if event exists
if(not os.path.isdir(eventFolder)) :
    print("{}Folder for event [{}] doesn't exist.".format(baseDebug, eventName))
    quit()

# debug
print("{}Working with event [{}]".format(baseDebug, eventName))

# set files
logFile         = eventFolder + eventName + "_tweetsLog.txt"
scheduleFile    = eventFolder + eventName + "_schedule.json"
tweetsFinalFile = eventFolder + eventName + "_tweetsFinal.json"
printLogFile    = eventFolder + eventName + "_printlog.txt"

# create and reset printLog file
with open(printLogFile, "w") as f:
    f.write("")

# check if file exists / logFile
if(not os.path.isfile(logFile)) :
    print("{}Log file for event [{}] doesn't exist.".format(baseDebug, eventName))
    quit()

# check if file exists / scheduleFile
if(not os.path.isfile(scheduleFile)) :
    print("{}Schedule file for event [{}] doesn't exist.".format(baseDebug, eventName))
    quit()

# load scheduleFile
scheduleData = []
with open(scheduleFile, 'r') as scheduleFile_f:
    scheduleData = json.load(scheduleFile_f)

# get min and max freq
printFreqMin = scheduleData["printFreqMin"]
printFreqMax = scheduleData["printFreqMax"]
meanFreq = (printFreqMin + printFreqMax) * 0.5

# debug
print("{}min freq = {}\tmax freq = {}\tmean freq = {}".format(baseDebug, printFreqMin, printFreqMax, meanFreq))

# compute number of pages for each date
numberPrintsTotalAvg = 0
numberPrintsTotalMax = 0
incr = 1
for el in scheduleData["sessions"] :
    #
    date = el["date"]
    timeStart = el["timeStart"]
    timeEnd = el["timeEnd"]

    # get minutes between the times
    datetime_start = datetime.datetime.strptime(date + " " + timeStart, '%d/%m/%Y %H:%M')
    datetime_end = datetime.datetime.strptime(date + " " + timeEnd, '%d/%m/%Y %H:%M')

    # get diff in minutes
    datetime_diff = datetime_end - datetime_start
    datetime_diff = datetime_diff.total_seconds() / 60

    # compute number of prints on average
    numberPrintsAvg = datetime_diff / meanFreq
    numberPrintsAvg = math.ceil(numberPrintsAvg)
    numberPrintsTotalAvg = numberPrintsTotalAvg + numberPrintsAvg

    # compute number of prints minimum
    numberPrintsMax = datetime_diff / printFreqMin
    numberPrintsMax = math.ceil(numberPrintsMax)
    numberPrintsTotalMax = numberPrintsTotalMax + numberPrintsMax

    # put number of prints in json data
    el["numberPrintsAvg"] = numberPrintsAvg
    el["numberPrintsMax"] = numberPrintsMax

    # debug
    print("{}date #{}\t\t{}\t{}\t=> {} minutes\t => {} prints on average. Maximum {} prints.".format(baseDebug, incr, datetime_start, datetime_end, datetime_diff, numberPrintsAvg, numberPrintsMax))

    #
    incr = incr + 1

# debug
print("{}{} prints total on average. Maximum {} prints total.".format(baseDebug, numberPrintsTotalAvg, numberPrintsTotalMax))

# get number of tweets for this event
numTweets = fileLen(logFile)

# check if we have at least more tweets than prints
if (numTweets < numberPrintsTotalMax) :
    print("{}Not enough tweets in log. Log has {} tweets and schedule requests {} tweets.".format(baseDebug, numTweets, numberPrintsTotalMax))
    quit()

# init tweet list
tweetList = []

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
        tweetList.append(tweet)

# shuffle list in order to maximize randomness
random.shuffle(tweetList)

# go over list again and this time adds increments
incrTot = 1
incrSess = 0
tweetListFinal = []
for el in scheduleData["sessions"] :
    # increment for each date
    incrSess = incrSess + 1

    # get time of printing
    tweetPrintedAt_datetime = datetime.datetime.strptime(el["date"], '%d/%m/%Y')

    # get date info // printed at
    tweetPrintedAt_day = tweetPrintedAt_datetime.strftime("%d")
    tweetPrintedAt_month = tweetPrintedAt_datetime.strftime("%m")
    tweetPrintedAt_monthReadable = months[int(tweetPrintedAt_month)]
    tweetPrintedAt_year = tweetPrintedAt_datetime.strftime("%Y")

    # create readable data and saving data
    tweetPrintedAt_dateSaving = "{}-{}-{}".format(tweetPrintedAt_day, tweetPrintedAt_month, tweetPrintedAt_year)
    tweetPrintedAt_dateReadable = "{} {} {}".format(tweetPrintedAt_day, tweetPrintedAt_monthReadable, tweetPrintedAt_year)

    # create folders
    sessionPDFFolder = eventFolder + "pdfs/" + tweetPrintedAt_dateSaving
    if(not os.path.isdir(sessionPDFFolder)):
        os.mkdir(sessionPDFFolder)

    #
    for i in range(1, el["numberPrintsMax"] + 1) :
        # get corresponding tweet
        tweet = tweetList[incrTot - 1]

        # get time of creation and printing
        tweetCreatedAt = tweet["created_at"]
        tweetCreatedAt_datetime = datetime.datetime.strptime(tweetCreatedAt, '%Y-%m-%d %H:%M:%S')

        # get date info // created at
        tweetCreatedAt_day = tweetCreatedAt_datetime.strftime("%d")
        tweetCreatedAt_month = tweetCreatedAt_datetime.strftime("%m")
        tweetCreatedAt_monthReadable = months[int(tweetCreatedAt_month)]
        tweetCreatedAt_year = tweetCreatedAt_datetime.strftime("%Y")

        # get hour info
        tweetCreatedAt_hour = tweetCreatedAt_datetime.strftime("%H")
        tweetCreatedAt_minute = tweetCreatedAt_datetime.strftime("%M")
        tweetCreatedAt_second = tweetCreatedAt_datetime.strftime("%S")

        # create readable data and saving data
        tweetCreatedAt_dateReadable = "{} {} {}".format(tweetCreatedAt_day, tweetCreatedAt_monthReadable, tweetCreatedAt_year)
        tweetCreatedAt_hourReadable = "{}h{}".format(tweetCreatedAt_hour, tweetCreatedAt_minute)

        # append to tweet
        tweet["created_at_date_readable"] = tweetCreatedAt_dateReadable
        tweet["printed_at_date_readable"] = tweetPrintedAt_dateReadable
        tweet["printed_at_date_saving"] = tweetPrintedAt_dateSaving
        tweet["created_at_hour_readable"] = tweetCreatedAt_hourReadable

        # set date index and tweet index
        tweet["sessionIndex"] = str(incrSess).zfill(2)
        tweet["printIndex"] = str(i)
        tweet["printIndexPadded"] = str(i).zfill(3)

        # append to final list
        tweetListFinal.append(tweet)

        #
        #print("{}day [{}]\ttweet [{}]\t=> tweet #{}\t{}".format(baseDebug, tweet["sessionIndex"], tweet["printIndex"], incrTot, tweetList[incrTot]["created_at"]))

        #
        incrTot = incrTot + 1


with open(tweetsFinalFile, "w") as f:
    tweets = {}
    tweets["tweets"] = tweetListFinal
    json.dump(tweets, f)

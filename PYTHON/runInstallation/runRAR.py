import os
import sys
import time
import datetime
import json
import random

# return number of lines of file
def fileLen(_fileName):
    i = -1
    with open(_fileName) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

# define base debug
baseDebug = "[runRAR]\t"

# check for inputs
if(len(sys.argv) != 2) :
    print("{}Script needs exactly one argument that is the name of the event.".format(baseDebug))
    quit()

# set up folder
eventsFolder = "../../DATA/events/"

# get event
eventName = sys.argv[1]
eventFolder = eventsFolder + eventName + "/"

# check if event exists
if(not os.path.isdir(eventFolder)) :
    print("{}Folder for event [{}] doesn't exist.".format(baseDebug, eventName))
    quit()

# set files
scheduleFile    = eventFolder + eventName + "_schedule.json"
eventPDFFolder  = eventFolder + "pdfs/"
printLogFile    = eventFolder + eventName + "_printlog.txt"

# check if event exists
if(not os.path.isdir(eventPDFFolder)) :
    print("{}Event [{}] doesn't have a PDF folder. Creating it.".format(baseDebug, eventName))
    os.mkdir(pdfFolder)
    quit()

# check if pdfs folder is empty
if len(os.listdir(eventPDFFolder)) == 0:
    print("{}PDF folder for event [{}] is empty. Run 'savedLogtoJSON.py' then 'JSONtoPDFs_script.jsx'.".format(baseDebug, eventName))
    quit()

# check if file exists / scheduleFile
if(not os.path.isfile(scheduleFile)) :
    print("{}Schedule file for event [{}] doesn't exist.".format(baseDebug, eventName))
    quit()

# debug
print("{}Working with event [{}]".format(baseDebug, eventName))

# load scheduleFile
scheduleData = []
with open(scheduleFile, 'r') as scheduleFile_f:
    scheduleData = json.load(scheduleFile_f)

# get min and max freq
printFreqMin = scheduleData["printFreqMin"]
printFreqMax = scheduleData["printFreqMax"]
meanFreq = (printFreqMin + printFreqMax) * 0.5

# debug
print("{}Event [{}] has settings : min freq = {}\tmax freq = {}\tmean freq = {}".format(baseDebug, eventName, printFreqMin, printFreqMax, meanFreq))

# get today's date
now = datetime.datetime.now()
nowDateHyphen = now.strftime("%d-%m-%Y")
nowDateSlash = now.strftime("%d/%m/%Y")

# get pdf folder for today
todayPDFFolder = eventPDFFolder + nowDateHyphen + "/"

# check if there's folder for date
if(not os.path.isdir(todayPDFFolder)) :
    print("{}PDF folder for today's session [{}] of event [{}] doesn't exist.".format(baseDebug, nowDateHyphen, eventName))
    quit()

# check if folder is empty
if len(os.listdir(todayPDFFolder)) == 0:
    print("{}PDF folder for today's session [{}] of event [{}] is empty.".format(baseDebug, nowDateHyphen, eventName))
    quit()

# get pdfs to prints
PDFsToPrint = os.listdir(todayPDFFolder)

# get info about today's status
timeStart = ""
timeEnd = ""
for sess in scheduleData["sessions"]:
        if(sess["date"] == nowDateSlash) :
            # get times
            timeStart = sess["timeStart"]
            timeEnd = sess["timeEnd"]

# debug
print("{}Working with session [{}] of event [{}] with boundaries [{} -> {}] and {} files to print.".format(baseDebug, nowDateSlash, eventName, timeStart, timeEnd, len(PDFsToPrint)))

# check if log file exists
if(not os.path.isfile(printLogFile)) :
    # create file
    with open(printLogFile, "a"):
        ""

    #
    print("{}Log file for session [{}] of event [{}] doesn't exist. Creating it.".format(baseDebug, nowDateHyphen, eventName))

# set entry point in log
numberInLog = max(1, fileLen(printLogFile))

# get times as datetime
timeStart_datetime = datetime.datetime.strptime(nowDateHyphen + " " + timeStart, "%d-%m-%Y %H:%M")
timeEnd_datetime = datetime.datetime.strptime(nowDateHyphen + " " + timeEnd, "%d-%m-%Y %H:%M")

# get time differences
sessionLength = timeEnd_datetime - timeStart_datetime
sessionLength = sessionLength.total_seconds()
timeToSession = timeStart_datetime - now
timeToSession = timeToSession.total_seconds()

# check if we are within the bounds
if(timeToSession < 0 and abs(timeToSession) > sessionLength) :
    print("{}Starting script out of bounds for session [{}] of event [{}].".format(baseDebug, nowDateHyphen, eventName))
    quit()

# compute tme to wait
timeToWait = max(0, timeToSession)

# debug
print("{}Waiting {} seconds for session [{}] of event [{}].".format(baseDebug, int(timeToWait), nowDateHyphen, eventName))

# wait
time.sleep(timeToWait)

# loop through all PDFs and print
incrPDF = 1
for pdf in PDFsToPrint:
    # ignore files that have been printed already
    if(incrPDF <= numberInLog) :
        incrPDF = incrPDF + 1
        continue

    # get time
    now = datetime.datetime.now()
    now = now.strftime("%H:%M")

    # get id of tweet
    tweetId = pdf.split(".")[0].split("_")[1]

    # print file
    #os.startfile(pdf, 'print')

    # debug
    print("{}#{}\tat time [{}]\ttweet id [{}] for session [{}] of event [{}].".format(baseDebug, incrPDF, now, tweetId, nowDateHyphen, eventName))

    # incr
    incrPDF = incrPDF + 1

    # write log
    with open(printLogFile, "a") as f:
        f.write(nowDateHyphen + "\t" + tweetId + "\t" + now + "\n")

    # wait
    timeToWait = random.uniform(printFreqMin, printFreqMax) * 60
    print("{}Waiting {} seconds.".format(baseDebug, int(timeToWait)))
    time.sleep(timeToWait)

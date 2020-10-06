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
if(len(sys.argv) != 2 and len(sys.argv) != 3) :
    print("{}Script needs exactly either 1 argument that is the name of the event or 2 with option to TESTPRINT.".format(baseDebug))
    quit()

# check if testprint
testPrint = False
if(len(sys.argv) == 3 and sys.argv[2] == "TESTPRINT") :
    testPrint = True

# set testprintfile
testPrintFolder = "../../DATA/others/"
testPrintFileName   = "testPrintFile.pdf"
testPrintFile = testPrintFolder + testPrintFileName

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
numberInLog = fileLen(printLogFile)

# get times as datetime
timeStart_datetime = datetime.datetime.strptime(nowDateHyphen + " " + timeStart, "%d-%m-%Y %H:%M")
timeEnd_datetime = datetime.datetime.strptime(nowDateHyphen + " " + timeEnd, "%d-%m-%Y %H:%M")

# get time differences
sessionLength = timeEnd_datetime - timeStart_datetime
sessionLength = sessionLength.total_seconds()
timeToSession = timeStart_datetime - now
timeToSession = timeToSession.total_seconds()

# get readable now
nowTimeReadable = now.strftime("%H:%M:%S")

# check if we are within the bounds
if(timeToSession < 0 and abs(timeToSession) > sessionLength) :
    print("{}Starting script at [{}] is out of bounds for session [{}] of event [{}].".format(baseDebug, nowTimeReadable, nowDateHyphen, eventName))
    quit()

# compute tme to wait
timeToWait = max(0, timeToSession)

# debug
print("{}Waiting {} seconds for session [{}] of event [{}].".format(baseDebug, int(timeToWait), nowDateHyphen, eventName))

# wait
time.sleep(timeToWait)

# loop through all PDFs and print
incrPDF = 0
for pdf in PDFsToPrint:
    # ignore files that have been printed already
    if(incrPDF < numberInLog) :
        incrPDF = incrPDF + 1
        continue

    # get time
    now_datetime = datetime.datetime.now()
    now = now_datetime.strftime("%H:%M:%S")

    # set print file
    PDFToPrintName = pdf
    PDFToPrintPath = eventPDFFolder + pdf
    if(testPrint) :
        PDFToPrintPath      = testPrintFile
        PDFToPrintName      = testPrintFileName

    # get id of tweet
    PDFToPrintName = PDFToPrintName.split(".")[0]

    # print file
    #os.startfile(PDFToPrintPath, 'print')

    # debug
    print("{}#{}\tat time [{}]\ttweet id [{}] for session [{}] of event [{}].".format(baseDebug, incrPDF + 1, now, PDFToPrintName, nowDateHyphen, eventName))

    # incr
    incrPDF = incrPDF + 1

    # write log
    with open(printLogFile, "a") as f:
        f.write(nowDateHyphen + "\t" + PDFToPrintName + "\t" + now + "\n")

    # wait
    timeToWait = random.uniform(printFreqMin, printFreqMax) * 60
    nextPrintAt_datetime = now_datetime + datetime.timedelta(seconds = timeToWait)
    nextPrintAt = nextPrintAt_datetime.strftime("%H:%M:%S")

    # check if last print
    if(incrPDF == len(PDFsToPrint)) :
        print("{}That was the last PDF to print for session [{}] of event [{}]. Quitting.".format(baseDebug, nowDateHyphen, eventName))
        break

    # check if out of bounds
    if(nextPrintAt_datetime > timeEnd_datetime) :
        timeEndReadable = timeEnd_datetime.strftime("%H:%M:%S")
        print("{}Next print at [{}] will be past endTime [{}] for session [{}] of event [{}]. Quitting.".format(baseDebug, nextPrintAt, timeEndReadable, nowDateHyphen, eventName))
        break

    # wait
    print("{}Waiting {} seconds. Next print at [{}].".format(baseDebug, int(timeToWait), nextPrintAt))
    time.sleep(timeToWait)

import os
import sys

# define base debug
baseDebug = "[cleanLogForEvent]\t"

# check for inputs
if(len(sys.argv) != 3) :
    print("{}Script needs exactly either 2 argument that is the name of the event and the session to clean from log.".format(baseDebug))
    quit()

# set up folder
eventsFolder = "../../DATA/events/"

# get event
eventName = sys.argv[1]
eventFolder = eventsFolder + eventName + "/"

# set file
printLogFile    = eventFolder + eventName + "_printlog.txt"

# get session
sessionName = sys.argv[2]

# check if --all
if(sessionName == "--all"):
    with open(printLogFile, "w") as f:
        f.write("")
    print("{}Cleaned printLog file of event [{}]. Cleaned everything.".format(baseDebug, eventName))
    quit()

# check if event exists
if(not os.path.isdir(eventFolder)) :
    print("{}Folder for event [{}] doesn't exist.".format(baseDebug, eventName))
    quit()

# get all entries of  log file
with open(printLogFile, "r") as f:
    entries = f.readlines()

# keep only the ones that are not from specified session
entriesToKeep = [e for e in entries if e.split("\t")[0] != sessionName]

# get number of match
numMatch = len(entries) - len(entriesToKeep)

# rewrite log file with the kept entries
with open(printLogFile, "w") as f:
    f.writelines(entriesToKeep)

# debug
print("{}Cleaned printLog file of event [{}]. Found {} matches for entry [{}].".format(baseDebug, eventName, numMatch, sessionName))

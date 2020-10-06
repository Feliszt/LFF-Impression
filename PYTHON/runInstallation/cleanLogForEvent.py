import os
import sys

# define base debug
baseDebug = "[cleanLogForEvent]\t"

# check for inputs
if(len(sys.argv) != 2) :
    print("{}Script needs exactly either 1 argument that is the name of the event.".format(baseDebug))
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

# set file
printLogFile    = eventFolder + eventName + "_printlog.txt"

# clean log file
with open(printLogFile, "w") as f:
    f.write("")

# debug
print("{}Cleaned printLog file of event [{}].".format(baseDebug, eventName))

import json
import os

# set event
eventName = "OE2020"
logFile = "../../DATA/events/{}/pre_printlog.json".format(eventName)
printedFile = "../../DATA/events/{}/{}_printed.txt".format(eventName, eventName)
pdfFolder = "../../DATA/events/{}/pdfs/".format(eventName)

#
counter = 0
with open(logFile, 'r') as f_in :
    # get session
    data = json.load(f_in)
    sessions = data["sessions"]

    # loop through all sessions
    for session in sessions :
        # list files in pdf folder for session
        sessionFolder = "{}{}/".format(pdfFolder, session["date"].replace("/", "-"))
        pdfFiles = [f for f in os.listdir(sessionFolder) if len(f.split("_")) < 3]

        # loop through all actual printed files
        for i in range(1, session["last_print"] + 1) :
            # extract tweet id from file name
            tweetId = pdfFiles[i-1].split("_")[1].split(".")[0]
            lineToWrite = "{}\t{}\n".format(session["date"], tweetId)
            counter = counter + 1

            with open(printedFile, 'a') as f_out :
                f_out.write(lineToWrite)

print(counter)

#
#   -- This script goes through each tweet and if it has pictures,
#   -- download them
#

from os import listdir
from os.path import isfile, join
import json
import requests
import time

# set folders
folderToProcess = "../../DATA/fromChecker/"
folderToSave = "../../DATA/images/"

# get files
onlyfiles = [f for f in listdir(folderToProcess) if isfile(join(folderToProcess, f))]

# loop through files
numImageTotal = 0
tweetTotalTotal = 0
for file in onlyfiles :

    # get file name
    fileName = file.split('.')[0]

    # load file
    with open(folderToProcess + file, "r", encoding="utf8") as dataFile:
        # load json that is in file
        tweets = json.load(dataFile)["tweets"]
        tweetTotal = len(tweets)
        tweetTotalTotal = tweetTotalTotal + tweetTotal

        # loop through all tweets
        tweetNum = 0
        for tweet in tweets :
            # incr
            tweetNum = tweetNum + 1

            # image state
            imageState = ""
            if(tweet["has_image"]) :
                imageState = "has image."
            else :
                imageState = "does not have image."

            # if tweet has image, we download it
            if(tweet["has_image"]) :
                # get number of images for this tweet
                numImage = len(tweet["images"])
                numImageTotal = numImageTotal + numImage
                idImage = 1

                # loop through all images
                for im in tweet["images"] :
                    print("[{}]\timage {} / {}\t{}".format(tweet["id"], idImage, numImage, im["link"]))

                    # download image
                    try :
                        imgData = requests.get(im["link"])
                    except :
                        print("Error fetching image.")
                        break

                    # save image
                    with open("{}{}_{}.jpg".format(folderToSave, tweet["id"], idImage), 'wb') as imgFile :
                        imgFile.write(imgData.content)

                    # wait 1 second
                    time.sleep(1)

                    # incr
                    idImage = idImage + 1

            #
            print("[{}] {} / {} ({}) {}".format(file, tweetNum, tweetTotal, tweet["id"], imageState))

print("{} images and {} tweets.".format(numImageTotal, tweetTotalTotal))

#
#   -- This script goes through each tweet and if it has pictures,
#   -- download them
#

import os
import json
import requests
import time

# set folders
checkerFolder = "../../DATA/fromChecker/"
imageFolder = "../../DATA/images/"

# get files
onlyfiles = [f for f in os.listdir(checkerFolder) if os.path.isfile(os.path.join(checkerFolder, f))]

# loop through files
numImageTotal = 0
tweetTotalTotal = 0
for file in onlyfiles :

    # get file name
    fileName = file.split('.')[0]
    fileNameJustDate = fileName[:-8]

    # load file
    with open(checkerFolder + file, "r", encoding="utf8") as dataFile:
        # load json that is in file
        tweets = json.load(dataFile)["tweets"]
        tweetTotal = len(tweets)
        tweetTotalTotal = tweetTotalTotal + tweetTotal

        # loop through all tweets
        tweetNum = 0
        for tweet in tweets :
            # incr
            tweetNum = tweetNum + 1

            # print info
            baseDebug = "{} / {} of {}".format(tweetNum, tweetTotal, fileName)
            print("{}\t[{}]".format(baseDebug, tweet["id"]))

            # image state
            imageState = ""
            if(tweet["has_image"]) :
                imageState = "has image."
            else :
                imageState = "does not have image."

            # we check for images, and download them
            if(tweet["has_image"]) :
                # get number of images for this tweet
                numImage = len(tweet["images"])
                numImageTotal = numImageTotal + numImage
                idImage = 1

                # show debug
                print("{}\tTweet has {} images.".format(baseDebug, numImage))

                # loop through all images
                for im in tweet["images"] :
                    baseDebugImage = "image {} / {}".format(idImage, numImage);
                    print("{}\t{}\tlink [{}]".format(baseDebug, baseDebugImage, im["link"]))

                    # download image
                    try :
                        imgData = requests.get(im["link"])
                        time.sleep(1)
                    except requests.exceptions.RequestException as e:
                        print("{}\t{}\t{}".format(baseDebug, baseDebugImage, e))
                        break

                    # get folder to save the image in and create it if it doesn't exist
                    imgSubFolder = imageFolder + fileNameJustDate
                    if not os.path.exists(imgSubFolder):
                        os.makedirs(imgSubFolder)

                    imgPath = "{}/{}_{}.jpg".format(imgSubFolder, tweet["id"], idImage)
                    print("{}\t{}\tsaving at [{}]".format(baseDebug, baseDebugImage, imgPath))
                    with open(imgPath, 'wb') as imgFile :
                        imgFile.write(imgData.content)

                    # incr
                    idImage = idImage + 1

print("{} images and {} tweets.".format(numImageTotal, tweetTotalTotal))

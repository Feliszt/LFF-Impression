from os import listdir
from os.path import isfile, join

# specify folder
folder = "D:/PERSO/_CREA/rar/_DEV/PYTHON/automaticTweetStreamer/json/"

# get files
onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]

# loop through all files
datePrev = ""
for f in onlyfiles :
    date = f.split('_')[0]
    with open(folder + date + '.json', 'a') as outfile:
        with open(folder + f, 'r') as infile :
            lines = infile.readlines()
            outfile.writelines(lines)

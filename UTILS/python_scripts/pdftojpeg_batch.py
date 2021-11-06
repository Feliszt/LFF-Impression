# must install imagemagick and ghostscript for this to work

import os

# set folders
folder_to_process = "../../DATA/events/PLEIADES2021/pdfs/"
folder_to_populate = "../../DATA/pdfs_to_jpegs/"
to_match = "bare"

#
folders = [f for f in os.listdir(folder_to_process)]

# loop through folders
for folder in folders :

    if folder == ".gitkeep" :
        continue

    # set folder name
    folder_full = folder_to_process + folder + "/"

    # list files
    files = [f for f in os.listdir(folder_full) if os.path.isfile(os.path.join(folder_full, f))]
    files_jpeg = []

    # loop through files
    for file in files :

        # discard not pdfs
        ext = file.split('.')[-1]
        file_name = file.split('.')[0]
        if(ext != "pdf") :
            continue

        # discard files that don't match
        ending = file_name.split("_")[-1]
        if (ending != to_match) :
            continue

        # perform conversion
        print("Processing {}".format(file_name))
        files_jpeg.append(file_name + ".jpg")
        os.system("convert.exe -density 200 {} -quality 90 {}".format(folder_full + file, folder_to_populate + file_name + ".jpg"))

    # resize everything with ffmpeg
    for file in files_jpeg :
        file_name = file.split('.')[0]
        os.system("ffmpeg -i {} -vf scale=-1:1920 -q:v 1 {}".format(folder_to_populate + file, folder_to_populate + file_name + "_.jpg"))
        os.remove(folder_to_populate + file)

import math

hours = range(0, 24)

for h in hours :
    if(h >= 0 and h < 6):
        hMapped = 1
    if(h >= 6 and h < 12):
        hMapped = 2
    if(h >= 12 and h < 18):
        hMapped = 3
    if(h >= 18 and h < 24):
        hMapped = 4
    print(str(h) + "\t" + str(hMapped))

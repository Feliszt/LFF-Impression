
# set event
eventName = "OE2020"
logFile = "../../DATA/events/{}/{}_tweetsLog.txt".format(eventName, eventName)

#
ids = []
with open(logFile, 'r') as f:
    lines = f.readlines()

    for l in lines:
        id = l.strip('\n').split(' ')[1];
        ids.append(id)

ids_less_duplicates = set(ids)

print("original list : {}\twithout duplicates : {}".format(len(ids_less_duplicates), len(ids)))

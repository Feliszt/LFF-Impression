#
#   --- Tells time every second ---
#

import datetime
import time

while True :
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("[TELLTIME]\t" + current_time)
    time.sleep(1)

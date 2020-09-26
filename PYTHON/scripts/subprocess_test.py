import sys
import subprocess

tellTime = subprocess.Popen([sys.executable, "tellTime.py"])
tellTime.communicate()

print("1234")

poll = tellTime.poll()
if poll == None:
    print("not finished.")
else:
    print("finished.")

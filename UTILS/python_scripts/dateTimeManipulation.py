import datetime
import pytz
from dateutil.parser import parse
from dateutil.tz import tzoffset
from dateutil.tz import UTC
import time

time_str = "Tue Mar 23 15:23:27 +0000 2021"

dt = parse(time_str)
dt.astimezone(UTC)

print(-time.timezone)

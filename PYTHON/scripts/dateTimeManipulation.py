import datetime

now = datetime.datetime.now()
dt_string = now.strftime("%d-%m-%Y_%Hh%M")

print(dt_string)

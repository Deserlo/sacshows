import datetime
from datetime import date, timedelta

#today = datetime.date.today()


#yesterday = today - datetime.timedelta(days=1)

#print(yesterday)
today = datetime.datetime.now()
print("today:", today)
yesterday = today - datetime.timedelta(days=1.5)
print("yesterday", yesterday)
print(today.weekday())
next = yesterday + datetime.timedelta(days=yesterday.weekday(), weeks=1)


#next = today + datetime.timedelta(days=-today.weekday(), weeks=1)
print("next", next)


def alldays(today):
    d = today
    f = d + timedelta(days = (4 - d.weekday()) % 7)
    sa = d + timedelta(days = (5 - d.weekday()) % 7)
    su = d + timedelta(days = (6 - d.weekday()) % 7, weeks=1)
    print(f, sa, su)

alldays(today)
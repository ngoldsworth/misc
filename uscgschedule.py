import datetime as dt

t = [
   (dt.datetime(year=2022, month=9,day=20), dt.datetime(year=2022, month=11,day=10)),
   (dt.datetime(year=2022, month=9,day=27), dt.datetime(year=2022, month=11,day=18)),
   (dt.datetime(year=2022, month=10,day=4), dt.datetime(year=2022, month=11,day=22)),
   (dt.datetime(year=2022, month=10,day=11), dt.datetime(year=2022, month=12,day=2)),
   (dt.datetime(year=2022, month=10,day=18), dt.datetime(year=2022, month=12,day=9)),
   (dt.datetime(year=2022, month=10,day=25), dt.datetime(year=2022, month=12,day=16)),
   (dt.datetime(year=2022, month=11,day=1), dt.datetime(year=2022, month=12,day=22))
]

print([t2 - t1 for t1, t2 in t])

print(dt.date(year=2023, month=2, day=14) + dt.timedelta(52))
import datetime as dt

start = dt.date(2022, 12, 31)
week = dt.timedelta(weeks=1)
loss_per_week = 2

w0 = 208

j = 0

# calculate estimated weight
date_in_question = dt.date(2023, 4, 7)

loss = loss_per_week * (date_in_question - start)/week

print(w0 - loss)
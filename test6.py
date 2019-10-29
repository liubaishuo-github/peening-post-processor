import datetime

dt = datetime.datetime.now()
print(type(dt))
print(dt)
time_str = dt.strftime('%b-%d-%Y  %H:%M:%S')

print(time_str)

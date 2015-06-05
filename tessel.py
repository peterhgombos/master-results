#!/usr/bin/python
import csv
import sys
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import math

raw_data = []
raw_dates = []
dateformat = "%Y-%m-%d %H:%M:%S.%f"

t = datetime.strptime(sys.argv[2], "%H:%M:%S.%f")
program_time = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second, microseconds=t.microsecond)
t = datetime.strptime(sys.argv[3], "%H:%M:%S.%f")
experiment_time = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second, microseconds=t.microsecond)
t = datetime.strptime(sys.argv[4], "%H:%M:%S.%f")
start_time = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second, microseconds=t.microsecond)

with open(sys.argv[1]) as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';')
    for row in spamreader:
        raw_dates.append(datetime.strptime(row[0].strip("\xef\xbb\xbf"), dateformat))
        raw_data.append(float(row[1].replace(',','.')))



start = raw_dates[0] + start_time


dates = raw_dates[min(range(len(raw_dates)), key=lambda i: abs(raw_dates[i]-start)):]
data = raw_data[min(range(len(raw_dates)), key=lambda i: abs(raw_dates[i]-start)):]


experiment_end = dates[0] + experiment_time
data = data[0:min(range(len(dates)), key=lambda i: abs(dates[i]-experiment_end))+1]
duration = dates[len(data)] - dates[0]
samples_per_second = len(data)/duration.seconds

samples_per_run = int(math.ceil(samples_per_second * program_time.seconds))

samples_per_reset = int(math.ceil(samples_per_second * 12.8))

# powerdata = [data[x:x+samples_per_reset] for x in range(samples_per_run, len(data), samples_per_run+samples_per_reset)]
powerdata = [ data[x:x+samples_per_run] for x in range(0, len(data), samples_per_run+samples_per_reset)]




powerdata = [item for sublist in powerdata for item in sublist]
runs = [ sum(powerdata[x:x+samples_per_run]) for x in range(0, len(powerdata), samples_per_run)]

print "average power usage of run " + str( np.average(runs[:-1]))
print "aproximate running time of program (seconds) " + str(program_time.seconds)
print "aproximate running time of experiment (seconds) " + str(experiment_time.seconds)
print "start time " + str(start_time)
print "number of runs " + str(len(runs))


# plt.plot(raw_data)
#
# plt.show()

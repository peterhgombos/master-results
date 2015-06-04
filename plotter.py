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

t = datetime.strptime(sys.argv[2], "%H:%M:%S")
program_time = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
t = datetime.strptime(sys.argv[3], "%H:%M:%S")
experiment_time = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)

with open(sys.argv[1]) as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';')
    for row in spamreader:
        raw_dates.append(datetime.strptime(row[0], dateformat))
        raw_data.append(float(row[1].replace(',','.')))

experiement_end = raw_dates[0] + experiment_time
data = raw_data[0:min(range(len(raw_dates)), key=lambda i: abs(raw_dates[i]-experiement_end))+1]

powerdata = filter(lambda x: x > 0.3900, data)
duration = raw_dates[len(data)] - raw_dates[0]

samples_per_second = len(data)/duration.seconds

samples_per_run = int(math.ceil(samples_per_second * program_time.seconds))


runs = [ sum(powerdata[x:x+samples_per_run]) for x in range(0, len(powerdata), samples_per_run)]

print "average power usage of run " + str( np.average(runs[:-1]))
print "aproximate running time of program (seconds) " + str(program_time)
print "aproximate running time of experiment (seconds) " + str(experiment_time)

# plt.plot(data)
# plt.show()

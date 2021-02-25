import datetime
import random
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
import matplotlib.dates as dates
import argparse
from github import Github
import requests
import os
import numpy as np

# make up some data
x = [datetime.datetime.now() + datetime.timedelta(hours=i) for i in range(12)]


SMALL_SIZE = 20
MEDIUM_SIZE = 30
BIGGER_SIZE = 40

plt.rc('font', size=SMALL_SIZE, family='serif')
plt.rc('axes', titlesize=BIGGER_SIZE, labelsize=MEDIUM_SIZE)
plt.rc('xtick', labelsize=SMALL_SIZE)
plt.rc('ytick', labelsize=SMALL_SIZE)
plt.rc('legend', fontsize=SMALL_SIZE)
plt.rc('figure', titlesize=BIGGER_SIZE)

# plot
plot_w = 18.0
plot_h = 9.0

date1 = datetime.datetime(2020, 4, 2)
date2 = datetime.datetime(2020, 4, 6)
delta = datetime.timedelta(hours = 6)
datess = drange(date1, date2, delta)
y = [i+random.gauss(0,1) for i,_ in enumerate(datess)]

# using some dummy data for this example

test = np.arange(46101, 46101-50 ,-1)
print(test)
xs = test
ys = np.random.normal(loc=2.0, scale=0.8, size=50)

#plt.style.use('seaborn')

fig, ax = plt.subplots(figsize=(plot_w, plot_h))
#plt.figure(figsize=(plot_w, plot_h))

date_from = f'{date1.day} {date1.strftime("%B")} {date1.year}'
date_to = f'{x[-1].day} {x[-1].strftime("%B")} {x[-1].year}'

plt.plot(xs, ys, color='b', marker='o')
ticks = []
counter = 0
for i in xs:
    counter += 1
    if counter == 5:
        ticks.append(i)
        counter = 0

plt.xticks(ticks)
plt.grid(True)
fig.text(0.1, 0.02, date_from)
fig.text(0.9, 0.02, date_to, horizontalalignment='right')
#ax.plot_date(dates, y, color='b')

#font_size = int(os.getenv('INPUT_FONT_SIZE'))
plt.title(f'Last 50 builds')
plt.ylabel("Build time (min)")
plt.xlabel("Build runs")

#ax.set_xlabel("Run number")

plt.show()

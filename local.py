import datetime
import random
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
import argparse
from github import Github
import requests
import os


# make up some data
x = [datetime.datetime.now() + datetime.timedelta(hours=i) for i in range(12)]


SMALL_SIZE = 20
MEDIUM_SIZE = 30
BIGGER_SIZE = 40

plt.rc('font', family='serif')
plt.rc('axes', titlesize=BIGGER_SIZE, labelsize=MEDIUM_SIZE)
plt.rc('xtick', labelsize=SMALL_SIZE)
plt.rc('ytick', labelsize=SMALL_SIZE)
plt.rc('legend', fontsize=SMALL_SIZE)
plt.rc('figure', titlesize=BIGGER_SIZE)

# plot
plot_w = 18.0
plot_h = 9.0
fig = plt.figure(figsize=(plot_w, plot_h))

plt.grid(True)

ax1 = fig.add_subplot()
date1 = datetime.datetime(2020, 4, 2)
date2 = datetime.datetime(2020, 4, 6)
delta = datetime.timedelta(hours = 6)
dates = drange(date1, date2, delta)
y = [i+random.gauss(0,1) for i,_ in enumerate(dates)]

ax1.plot_date(dates, y, color='b')

# ax1.set_xlim(dates[0], dates[-1])
# ax1.xaxis.set_major_locator(DayLocator())
# ax1.xaxis.set_minor_locator(HourLocator(range(0, 25, 6)))
# ax1.xaxis.set_major_formatter(DateFormatter('% Y-% m-% d'))

# ax1.fmt_xdata = DateFormatter('% Y-% m-% d % H:% M:% S')


fig.autofmt_xdate()
ax2 = ax1.twiny()
ax2.plot(range(16), y) # Create a dummy plot
#plt.gcf().autofmt_xdate()


#font_size = int(os.getenv('INPUT_FONT_SIZE'))
plt.title('Title')
ax2.set_xlabel("")
ax1.set_xlabel("Run number")
plt.ylabel("Build time (min)")

plt.show()

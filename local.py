import datetime
import random
import matplotlib
import matplotlib.pyplot as plt
import argparse
from github import Github
import requests
import os


run_nums = range(0, 100)
timings = range(0, 100)

SMALL_SIZE = 20
MEDIUM_SIZE = 30
BIGGER_SIZE = 40

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=BIGGER_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
plt.rc('font', family='serif')
# plot
plot_w = 18.0
plot_h = 9.0
plt.figure(figsize=(plot_w, plot_h))
plt.plot(run_nums, timings, color='b', marker='o')
plt.grid(True)



#font_size = int(os.getenv('INPUT_FONT_SIZE'))
plt.title('Title')
plt.xlabel("Run number")
plt.ylabel("Build time (min)")

plt.show()

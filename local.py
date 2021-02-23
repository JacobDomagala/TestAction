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

plt.rc('font', family='serif')
plt.rc('axes', titlesize=BIGGER_SIZE, labelsize=MEDIUM_SIZE)
plt.rc('xtick', labelsize=SMALL_SIZE)
plt.rc('ytick', labelsize=SMALL_SIZE)
plt.rc('legend', fontsize=SMALL_SIZE)
plt.rc('figure', titlesize=BIGGER_SIZE)

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

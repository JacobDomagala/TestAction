import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import argparse
from github import Github
import numpy as np
import os
import requests
import csv
from datetime import date
import pandas as pd

# Get file name from user
parser = argparse.ArgumentParser()
parser.add_argument('-t', '--time', help='Build time', required=True)
parser.add_argument('-r', '--run_id', help='Run ID', required=True)
parser.add_argument('-o', '--output', help='Output file name', required=True)
graph_file_name = parser.parse_args().output

new_build_time = parser.parse_args().time
new_run_num = parser.parse_args().run_id
new_date = date.today().strftime("%d %b %Y")

print(f"Build time is {new_build_time} RUN_ID is {new_run_num} date is {new_date}")

time_in_min = int(new_build_time[0: new_build_time.index("m")])
time_in_seconds = int(new_build_time[new_build_time.index("m") + 1: new_build_time.index(".")])
total_time_seconds = time_in_seconds + time_in_min * 60

print(f"Build time minutes {time_in_min} in seconds is {time_in_seconds} total time {total_time_seconds}")

# Input variables from Github action
GITHUB_TOKEN = os.getenv('INPUT_GITHUB_TOKEN')
REPO_NAME = os.getenv('INPUT_REPO')
WORKFLOW_NAME = os.getenv('INPUT_WORKFLOW')
BRANCH_NAME = os.getenv('INPUT_BRANCH')
REQUESTED_N_LAST_BUILDS = int(os.getenv('INPUT_NUM_LAST_BUILD'))
GRAPH_TITLE = os.getenv('INPUT_TITLE', '')
X_LABEL = os.getenv('INPUT_X_LABEL')
Y_LABEL = os.getenv('INPUT_Y_LABEL')
GRAPH_WIDTH = float(os.getenv('INPUT_GRAPH_WIDTH'))
GRAPH_HEIGHT = float(os.getenv('INPUT_GRAPH_HEIGHT'))
MAX_HISTORY_OF_BUILDS = 200
print(f'Repo={REPO_NAME} Workflow={WORKFLOW_NAME}')

MAX_ROWS = 50
FILE_NAME = "last_builds.csv"
df = pd.read_csv(FILE_NAME)
last_builds = df.tail(MAX_ROWS - 1)
updated = last_builds.append(pd.DataFrame([[total_time_seconds, new_run_num, new_date]], columns=['time','run_num','date']))

timings = updated['time'].tolist()
run_nums = updated['run_num'].tolist()
dates = updated['date'].tolist()

print(f"build times = {timings}")
print(f"run nums = {run_nums}")

total_run_time = sum(timings)
last_n_runs = updated.shape[0]
updated.to_csv(FILE_NAME, index=False)

SMALL_SIZE = 15
MEDIUM_SIZE = 25
BIGGER_SIZE = 35

plt.rc('font', size=MEDIUM_SIZE, family='serif')
plt.rc('axes', titlesize=BIGGER_SIZE, labelsize=MEDIUM_SIZE)
plt.rc('xtick', labelsize=SMALL_SIZE)
plt.rc('ytick', labelsize=SMALL_SIZE)
plt.rc('legend', fontsize=SMALL_SIZE)
plt.rc('figure', titlesize=BIGGER_SIZE)

# plot
fig, ax = plt.subplots(figsize=(GRAPH_WIDTH, GRAPH_HEIGHT))
plt.plot(run_nums, timings, color='b', marker='o')
plt.grid(True)

fig.text(0.05,0.02, dates[0])
fig.text(0.95,0.02, dates[-1], horizontalalignment='right')

plt.title(GRAPH_TITLE)
plt.xlabel(X_LABEL)
plt.ylabel(Y_LABEL)

plt.savefig(graph_file_name)

average_time = total_run_time / last_n_runs

BUILD_TIME = timings[-1]
BADGE_COLOR = "green" if BUILD_TIME <= average_time else "red"
print(f"Last build time = {BUILD_TIME} average build = {average_time} color = {BADGE_COLOR} ")
url = f"https://img.shields.io/badge/vt:develop%20build%20time-{format(BUILD_TIME,'.1f')}%20min-{BADGE_COLOR}.svg"
print(f'Beginning file {url}')
r = requests.get(url)
open('build_status_badge.svg', 'wb').write(r.content)

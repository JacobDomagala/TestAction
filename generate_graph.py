import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import argparse
from github import Github
import numpy as np
import os
import wget

# Get file name from user
parser = argparse.ArgumentParser()
parser.add_argument('-o', '--output', help='Output file name', required=True)
graph_file_name = parser.parse_args().output

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

print(f'Repo={REPO_NAME} Workflow={WORKFLOW_NAME}')

g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)
workflow = repo.get_workflow(id_or_name=WORKFLOW_NAME)

# Data to be plotted
timings = []
run_nums = []
dates = []


workflow_runs = workflow.get_runs()


print(f'workflow_runs.totalCount={workflow_runs.totalCount} and requested_last_runs={REQUESTED_N_LAST_BUILDS}')

last_n_runs = min(REQUESTED_N_LAST_BUILDS, workflow_runs.totalCount)

print(f'last_n_runs={last_n_runs}')

run_count = 0

for run in workflow_runs:
    if(run.head_branch == BRANCH_NAME and run.status == 'completed'):
        run_timing = run.timing()

        # Convert ms to min
        timings.append(run_timing.run_duration_ms / 60000.0)
        dates.append(run.created_at)
        run_nums.append(run.run_number)

        print(f"run_number:{run.run_number} status:{run.status} on branch:{run.head_branch} created at:{run.created_at} took:{run_timing.run_duration_ms}ms")
        run_count+=1
    else:
        print(f'Discarding run:{run.run_number} status:{run.status} branch:{run.head_branch}')

    if run_count >= last_n_runs:
        break

#dates = matplotlib.dates.date2num(run_nums)
#matplotlib.pyplot.plot_date(dates, values)

SMALL_SIZE = 15
MEDIUM_SIZE = 25
BIGGER_SIZE = 35

plt.rc('font', size=MEDIUM_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=BIGGER_SIZE)    # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
plt.rc('font', family='serif')           # font family

# plot
#plt.style.use('seaborn')

fig, ax = plt.subplots(figsize=(GRAPH_WIDTH, GRAPH_HEIGHT))

#plt.plot_date(dates, timings, color='b')
fig.text(0.05,0.02, f'{dates[-1].day} {dates[-1].strftime("%B")} {dates[-1].year }')
fig.text(0.95,0.02, f'{dates[0].day} {dates[0].strftime("%B")} {dates[0].year }', horizontalalignment='right')

ax.plot(run_nums, timings, 'bo-')
ax.grid(True)

#plt.gcf().autofmt_xdate()

ticks = []
counter = 0
for i in run_nums:
    counter += 1
    if counter == 5:
        ticks.append(i)
        counter = 0

plt.xticks(ticks)
plt.title(GRAPH_TITLE)
plt.xlabel(X_LABEL)
plt.ylabel(Y_LABEL)

plt.savefig(graph_file_name)

print('Beginning file download with wget module')

BUILD_TIME = "50min"
BADGE_COLOR = "green"

url = f'https://img.shields.io/badge/vt:develop%20build%20time-${BUILD_TIME}-${BADGE_COLOR}.svg'
wget.download(url, 'build_status_badge.svg')

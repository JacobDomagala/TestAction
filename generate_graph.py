import matplotlib.pyplot as plt
import argparse
from github import Github
import os

# Get file name from user
parser = argparse.ArgumentParser()
parser.add_argument('-o', '--output', help='Output file name', required=True)
graph_file_name = parser.parse_args().output

token = os.getenv('INPUT_GITHUB_TOKEN')
repo_name = os.getenv('INPUT_REPO', os.getenv('GITHUB_REPOSITORY'))
workflow_name = os.getenv('INPUT_WORKFLOW')

g = Github(token)
repo = g.get_repo(f"{repo_name}")
workflow = repo.get_workflow(id_or_name=workflow_name)

# Data to be plotted
timings = []
run_ids = []

workflow_runs = workflow.get_runs(status="success", branch="develop")
requested_last_runs = int(os.getenv('INPUT_NUM_LAST_BUILD'))

print(f'workflow_runs.totalCount={workflow_runs.totalCount} and requested_last_runs={requested_last_runs}')

if workflow_runs.totalCount >= requested_last_runs:
    last_n_runs = requested_last_runs
else:
    last_n_runs = workflow_runs.totalCount

print(f'last_n_runs={last_n_runs}')

for run in workflow_runs[:last_n_runs]:
    run.timing()
    print(f"workflow_run:{run.workflow_id} with ID:{run.id} took:{run.timing().run_duration_ms}ms ")
    # Convert ms to sec
    timings.append(run.timing().run_duration_ms / 60000.0)
    run_ids.append(run.run_number)

# plot
plt.figure(figsize=(12,9))
plt.plot(run_ids, timings, color='b', marker='o')
plt.grid(True)
plt.title(os.getenv('INPUT_TITLE', ''))
plt.xlabel("Run number")
plt.ylabel("Build time (min)")

plt.savefig(graph_file_name)

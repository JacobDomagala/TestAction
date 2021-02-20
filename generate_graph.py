import matplotlib.pyplot as plt
import argparse
from github import Github
import os

# Get file name from user
parser = argparse.ArgumentParser()
parser.add_argument('-o', '--output', help='Output file name', required=True)
graph_file_name = parser.parse_args().output

token = os.getenv('INPUT_GITHUB_TOKEN')
repo_name = os.getenv('GITHUB_REPOSITORY')
workflow_name = os.getenv('INPUT_WORKFLOW')
g = Github(token)
repo = g.get_repo(f"{repo_name}")
workflow = repo.get_workflow(id_or_name=workflow_name)

# Data to be plotted
timings = []
dates = []

workflow_runs = workflow.get_runs(status="success")
for run in workflow_runs:
    run.timing()
    print(f"workflow_run:{run.workflow_id} with ID:{run.id} took:{run.timing().run_duration_ms}ms ")
    # Convert ms to sec
    timings.append(run.timing().run_duration_ms / 1000.0)
    dates.append(run.head_branch)

# plot
plt.plot(dates, timings, color='b', marker='o')
plt.grid(True)
plt.title("Develop build times")
plt.xlabel("Commit SHA")
plt.ylabel("Build time (seconds)")

plt.savefig(graph_file_name)

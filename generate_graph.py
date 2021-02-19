import matplotlib.pyplot as plt
import argparse
from github import Github
import os

token = os.getenv('INPUT_GITHUB-TOKEN')
repo_name = os.getenv('GITHUB_REPOSITORY')
workflow_name = os.getenv('INPUT_WORKFLOW-NAME')
g = Github(token)
repo = g.get_repo(f"{repo_name}")
workflow = repo.get_workflow(id_or_name=workflow_name)

timings = []
workflow_runs = workflow.get_runs(status="success")
for run in workflow_runs:
    run.timing()
    print(f"workflow_run:{run.workflow_id} with ID:{run.id} took:{run.timing().run_duration_ms}ms ")
    # Convert ms to sec
    timings.append(run.timing().run_duration_ms / 1000.0)

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--output', help='Output file name', required=True)
args = parser.parse_args()

# make up some data
x = range(workflow_runs.totalCount)

# plot
plt.plot(x, timings, color='b', marker='o')
plt.grid(True)
plt.title("Develop build times")
plt.xlabel("Run number")
plt.ylabel("Build time (seconds)")

plt.savefig(args.output)

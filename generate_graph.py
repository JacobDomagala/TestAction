import datetime
import matplotlib
import matplotlib.pyplot as plt
import argparse
from github import Github
import os

token = os.getenv('GH_TOKEN')
repo_name = os.getenv('GITHUB_REPOSITORY')
g = Github(token)
repo = g.get_repo(f"{repo_name}")
workflow = repo.get_workflow(id_or_name="test.yml")
print(f"Workflow ID = {workflow.id}")

print("Going with PyGithub")
timings = []
for run in workflow.get_runs(status="success"):
    run.timing()
    print(f"workflow_run:{run.workflow_id} with ID:{run.id} took:{run.timing().run_duration_ms}ms ")
    # Convert ms to sec
    timings.append(run.timing().run_duration_ms / 1000.0)

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--output', help='Output file name', required=True)
args = parser.parse_args()

# make up some data
x = range(workflow.get_runs(status="success").totalCount)

# plot
plt.plot(x, timings, color='b', marker='o')
plt.grid(True)
plt.xlabel("Run number")
plt.ylabel("Build time (seconds)")

plt.savefig(args.output)

import datetime
import random
import matplotlib
import matplotlib.pyplot as plt
import argparse
from github import Github
import requests
import os

#token = os.getenv('GH_TOKEN', '...')
repo_name = "JacobDomagala/TestRepo"
g = Github("JacobDomagala", "Szambo1234!@#$")
repo = g.get_repo(f"{repo_name}")
workflow = repo.get_workflow(id_or_name="test.yml")
print(f"Workflow ID = {workflow.id}")

print("Going with PyGithub")
timings = []
for run in workflow.get_runs(status="success"):
    run.timing()
    print(f"workflow_run:{run.workflow_id} with ID:{run.id} took:{run.timing().run_duration_ms}ms ")
    timings.append(run.timing().run_duration_ms)

parser = argparse.ArgumentParser()
parser.add_argument('-o','--output',help='Output file name', required=True)
args = parser.parse_args()

x = range(workflow.get_runs(status="success").totalCount)

# plot
plt.plot(x, timings)
plt.figure(figsize=(12, 9))
plt.grid(True, color="#93a1a1", alpha=0.3)
plt.xlabel("Run number")
plt.ylabel("Build time ms")

plt.show()

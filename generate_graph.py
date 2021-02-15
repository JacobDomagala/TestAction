import datetime
import random
import matplotlib
import matplotlib.pyplot as plt
import argparse
from github import Github
import requests
import os
from pprint import pprint

token = os.getenv('GH_TOKEN', '...')
repo_name = os.getenv('GITHUB_REPOSITORY')
g = Github(token)
repo = g.get_repo(f"{repo_name}")
workflow = repo.get_workflow(id_or_name="test.yml")
print(f"Workflow ID = {workflow.id}")
worflow_runs = repo.get_workflow_runs()


query_url = f"https://api.github.com/repos/{repo_name}/actions/workflows/{workflow.id}/runs"
print(f"Query URL = {query_url}")
# params = {
#     "state": "open",
# }
# headers = {'Authorization': f'token {token}'}
r = requests.get(query_url)
#pprint(r.json())
r_json = r.json()
timings = []
for i in r_json["workflow_runs"]:
    run_data = requests.get(f"https://api.github.com/repos/{repo_name}//actions/runs/{i['id']}/runs")
    run_data_json = run_data.json()
    print(f"workflow_run:{i['run_number']} with ID:{i['id']} took:{run_data_json['run_duration_ms']}ms and check_suite_id:{i['check_suite_id']}")
    timings.append(run_data_json['run_duration_ms'])


parser = argparse.ArgumentParser()
parser.add_argument('-o','--output',help='Output file name', required=True)
args = parser.parse_args()

# make up some data
x = range(r_json["total_count"])

# plot
plt.plot(x, timings)
# beautify the x-labels
#plt.gcf().autofmt_xdate()

plt.savefig(args.output)

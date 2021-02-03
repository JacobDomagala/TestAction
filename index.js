const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    // `who-to-greet` input defined in action metadata file
    const owner = core.getInput('owner');
    const repo = core.getInput('repo');
    const run_id = core.getInput('run_id');
    console.log(`Going with /repos/${owner}/${repo}/actions/runs/${run_id}/timing !`);
    const time = (new Date()).toTimeString();


    [rv] = await octokit.request('GET /repos/{owner}/{repo}/actions/runs/{run_id}/timing', {
      owner: owner,
      repo: repo,
      run_id: run_id
    })

    console.log(`${rv}`)

    core.setOutput("time", time);
  } catch (error) {
    core.setFailed(error.message);
  }
}

run()
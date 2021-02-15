// const core = require('@actions/core');
// const github = require('@actions/github');
// const { request } = require("@octokit/request");

// async function run() {
//   try {
//     // `who-to-greet` input defined in action metadata file
//     const owner = core.getInput('owner');
//     const repo = core.getInput('repo');
//     const run_id = core.getInput('run_id');
//     console.log(`Going with /repos/${owner}/${repo}/actions/runs/${run_id}/timing !`);
//     const time = (new Date()).toTimeString();

//     // GET https://api.github.com/repos/<org>/<repo>/check-suites/<check_suite_id>/check-runs

//     // Get workflow_id
//     // https://api.github.com/repos/JacobDomagala/DGame/actions/workflows

//     // Get all run_id for given workflow
//     // https://api.github.com/repos/JacobDomagala/DGame/actions/workflows/2745476/runs
//     const result = await request('GET /repos/{owner}/{repo}/actions/runs/{run_id}/runs', {
//       owner: owner,
//       repo: repo,
//       run_id: run_id
//     })

//     console.log(`Run duration=${result.data.run_duration_ms}`)

//     core.setOutput("time", result.data.run_duration_ms);
//   } catch (error) {
//     core.setFailed(error.message);
//   }
// }

// run()

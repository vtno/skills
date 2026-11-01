# How to brief the author

Start one new agent for this PR on the base branch selected in the loop. Put every fact the agent needs into the instructions. Do not rely on an earlier chat for any of those facts.

After the skills install, load the engineering-rules skill. Put these commands in the instructions as well:

- Read the plan on the issue. Build only the named plan step. Leave every other plan step for a later PR.
- Summarize the interfaces, the helpers, and the test fakes that the merged PRs already provide. Build the new plan step on those interfaces, those helpers, and those fakes. Do not create any of those interfaces, those helpers, or those fakes again.
- In the PR description, write a short summary. Add a link to the plan. Do not copy the plan into the PR.
- Before you finish, run every check in the engineering-rules skill. Report the PR URL and the interface the PR adds. Report the lines added, the lines removed, and the result of each run. Do not merge.

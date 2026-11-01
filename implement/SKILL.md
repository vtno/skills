---
name: implement
description: Implement one step of a multi-PR plan, or a single PR, with an author agent. Then run a review and fix loop with a separate report-only reviewer until there are no blockers. Give the user a ready-to-merge PR link. Use when the user says "implement the next step", "do the next PR", or asks for a PR with a review loop.
---

# How to implement one plan step

Take one plan step to a PR that has no blockers in review. The user merges. Only when the user explicitly tells you to merge, merge.

## Collect the inputs

Collect these facts before you start:

- The repository and the base branch.
- The location of the plan, and the plan step to build.
- The user's preferences for models and for agents, when the user has stated them.

Read the repository's current name before you use that name. A repository can be renamed. The plan is usually a GitHub issue.

## Build and review the PR

1. **Confirm that the user merged the previous PR.**

   When this plan step has no previous PR, do item 2 on the base branch.

   When a previous PR exists, read that PR before item 2. If the user merged that PR, do item 2 on the base branch that contains that PR. If the user has not merged that PR:

   - Tell the user.
   - Stop the task.

2. **Start a new author agent.**

   Start one new agent for this PR on the base branch. Write every fact the agent needs into the instructions. Do not rely on an earlier chat for any of those facts.

   Give the agent these build rules:

   - Read the plan on the issue.
   - Build only the named plan step.
   - Leave every other plan step for a later PR.
   - Summarize the interfaces, the helpers, and the test fakes that the merged PRs already provide.
   - Build the new plan step on those interfaces, those helpers, and those fakes.
   - Do not create any of those interfaces, those helpers, or those fakes again.
   - Keep this PR small.
   - Build the innermost layer first.
   - Build each next layer only after the inner layers exist.
   - Connect the layers last.
   - Define each layer's interface by what the caller of that layer needs.
   - Add a behaviour or an interface only when that behaviour or that interface helps a test.
   - Prefer a fake that you write by hand to a mocking library.
   - Write tests that cover what the plan step does.
   - Only when a further test can catch a defect that the other tests miss, add that test.
   - Do not write a test that sleeps.
   - Do not write a test that depends on a time window.
   - Write a short summary in the PR description.
   - Add a link to the plan in the PR description.
   - Do not copy the plan into the PR.

   Give the agent these finish rules:

   - Run the formatter check.
   - Compile with warnings as errors.
   - Run the full test suite at least three times.
   - Use a different seed for each run.
   - Run one of the three runs in serial, not in parallel.
   - Report the PR URL and the interface the PR adds.
   - Report the lines added, the lines removed, and the result of each run.
   - Do not merge.

3. **Review with a separate agent.**

   Use an agent other than the author agent as the reviewer. Keep the reviewer report-only. A report-only reviewer writes the review and does not change the PR.

   Forbid these actions:

   - Do not let the reviewer commit.
   - Do not let the reviewer comment on the PR.
   - Do not let the reviewer approve.
   - Do not let the reviewer merge.

   Tell the reviewer to fetch the PR. Tell the reviewer to reset the local branch to the PR head. The reviewer then does the work below:

   - Find an abstraction that no caller needs, such as a callback, an option, or a helper.
   - Find tests that are unnecessary, redundant, or flaky.
   - Flag incorrect code. Look for bugs, races, leaks, and wrong error paths.
   - Run the test suite three times.
   - Label each finding `BLOCKER`, `SHOULD-FIX`, or `NIT`.
   - For each finding, give the file and the line as `file:line`. Give a concrete fix for that finding.
   - End the review with the line `BLOCKERS: <n>`.

4. **Repeat until the author agent fixes the blockers and the real bugs.**

   If the review lists a `BLOCKER`, send that finding and the concrete fix to the same author agent. If a `SHOULD-FIX` is a real bug, send that finding and the concrete fix to the same author agent. When the author agent pushes, run the same reviewer on the new head. The reviewer marks each previous finding fixed, partially fixed, or not fixed. Repeat both the send and the review while either a `BLOCKER` remains or a `SHOULD-FIX` is a real bug. Do not tell the user about an intermediate round.

5. **Handle each nit.**

   If findings remain, and every one of them is a `NIT`, list those findings in the final message. Offer to fix them in the final message. Only when the user tells you to fix the `NIT` findings, fix them. When you fix them, run the same reviewer again. If the new review has a `BLOCKER`, repeat item 4. If the new review has a `SHOULD-FIX` that is a real bug, repeat item 4.

6. **Tell the user the result.**

   Tell the user in one message. Include these parts:

   - The PR link.
   - One or two sentences on what the PR does.
   - The final test results.
   - Any `NIT` you did not fix, and any decision the user still has to make.
   - The statement that the PR is ready to merge.
   - The plan step you start after the user merges.

## Judge scope, tests, and size

Use these judgments:

- Keep the PR to the named plan step. If the reviewer tells you to move work to a later PR, ask the user before you move the work.
- If the only way to test a fix is to add a large new interface, skip the test. Say why you skipped the test.
- If the PR is large, say in the final message that the PR is large.

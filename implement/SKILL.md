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

## Run the loop

1. **Confirm that the user merged the previous PR.**

   When this plan step has no previous PR, do item 2 on the base branch. When a previous PR exists, read that PR before item 2. If the user merged that PR, do item 2 on the base branch that contains that PR. If the user has not merged that PR, tell the user and stop the task.

2. **Start a new author agent.**

   Follow the [author brief](references/author-brief.md).

3. **Review with a separate agent.**

   Follow the [review brief](references/review-brief.md).

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

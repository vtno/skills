---
name: implement
description: Implement one step of a multi-PR plan, or a single PR, with an author agent. Then run a review and fix loop with a separate report-only reviewer until no hard violation, wrong or missing requirement, or real bug remains. Give the user a ready-to-merge PR link. Use when the user says "implement the next step", "do the next PR", or asks for a PR with a review loop.
---

# How to implement one plan step

Take one plan step to a PR with no hard violation, wrong or missing requirement, or real bug left in review. The user merges. Only when the user explicitly tells you to merge, merge.

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

4. **Repeat until the required findings are gone.**

   Send the same author agent any finding that is a hard standards violation, a wrong or missing spec requirement, or a real bug. When that agent pushes, run the same reviewer on the new head. Tell the reviewer the previous findings so the reviewer can say which are fixed. Repeat until none of those findings remain. Do not tell the user between rounds. The reviewer must not prompt the user.

5. **Report judgement-call smells.**

   Report leftover judgement-call smells in the final message, and mark them optional. Fix a smell only when the user asks. When you do fix one, run the same reviewer again. If that review has a hard standards violation, a wrong or missing spec requirement, or a real bug, repeat item 4.

6. **Tell the user the result.**

   Tell the user in one message. Include these parts:

   - The PR link.
   - One or two sentences on what the PR does.
   - The final test results.
   - Any judgement-call smell you did not fix, and any decision the user still has to make.
   - The statement that the PR is ready to merge.
   - The plan step you start after the user merges.

## Judge scope, tests, and size

Use these judgments:

- Keep the PR to the named plan step. If the reviewer tells you to move work to a later PR, ask the user before you move the work.
- If the only way to test a fix is to add a large new interface, skip the test. Say why you skipped the test.
- If the PR is large, say in the final message that the PR is large.

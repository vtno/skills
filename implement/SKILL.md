---
name: implement
description: Implement one step of a multi-PR plan (or a single PR) with an author agent, then run a review -> fix loop with a separate report-only reviewer until there are no blockers, and hand the user a ready-to-merge PR link. Use when the user says "implement the next step", "do the next PR", or asks for a PR with a review loop.
---

# Implement: PR -> review loop

Takes one PR from start to a clean review. The user merges. Never merge unless they explicitly say so.

## Inputs

- Repository and base branch. Verify the repo's current name first; repos get renamed.
- Where the plan lives (usually a GitHub issue holding the multi-PR plan) and which step to build.
- Any model or agent preferences the user has for coding agents.

## Steps

1. **Check the previous PR is merged.** Read the previous PR and confirm it is merged before starting the next step, since the new branch must start from the base branch with it included. If it is not merged, tell the user and stop.

2. **Start a fresh author agent for this PR** on the base branch (one new agent per PR). Its instructions must be self-contained:
   - Read the plan on the issue and build only the named step; other steps stay out of scope.
   - Summarize what earlier merged PRs provide (interfaces, helpers, test fakes) so it builds on them instead of re-creating them.
   - Engineering rules: small isolated PRs; build from the innermost layer outward, wiring last; define each layer's interface from the caller's point of view; use behaviours/interfaces only where they help testing; prefer hand-written fakes over mocking libraries; proper but not bloated test coverage; no sleep-based or timing-window tests.
   - PR description: a short summary plus a link to the plan on the issue. Never copy the plan into the PR.
   - Before finishing: run the formatter check, a compile with warnings as errors, and the full test suite at least 3 times with different seeds (one run serial). Report the PR URL, the resulting interface, line deltas, and the run results. Do not merge.

3. **Review with a separate agent**, report-only: no commits, no PR comments, no approval or merge. Tell it to fetch and reset to the PR head, then:
   - find unnecessary abstraction (callbacks, options, helpers no caller needs),
   - find unnecessary, redundant, or flaky tests,
   - flag incorrect code (bugs, races, leaks, wrong error paths),
   - run the suite 3 times,
   - output BLOCKER / SHOULD-FIX / NIT, each with file:line and a concrete fix, and end with a line `BLOCKERS: <n>`.

4. **Loop until clean.** If the review has blockers or a should-fix that is a real bug, send the items (with the reviewer's concrete fixes) back to the same author agent. When it pushes, re-run the same reviewer on the new head and have it verify each previous item as fixed / partially / not fixed. Repeat until `BLOCKERS: 0` and no real-bug should-fix remains. Do not ping the user on intermediate rounds.

5. **Nits.** If only nits remain, list them in the final message and offer to fix them. Fix only if the user says so, then re-review.

6. **Ping the user** with:
   - the PR link,
   - what the PR does in a sentence or two,
   - the final test results,
   - any remaining nits or judgment calls,
   - that it is ready to merge, and which plan step you'd start after they merge.

## Notes

- Keep scope tight. If the reviewer suggests moving work to a later PR, that is the user's call.
- If a fix needs a large new seam only to make it testable, skip the test and say why.
- If the PR grows large, say so honestly in the final message.

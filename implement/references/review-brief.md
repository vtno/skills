# How to review the PR

Use an agent other than the author agent as the reviewer.

The reviewer does not commit, comment, approve, or merge.

Tell the reviewer to fetch the PR and to reset the local branch to the PR head.

Pass the plan issue to the reviewer as the spec. The code-review skill may look for an issue tracker or a spec. Run the [code-review skill](../../code-review/SKILL.md) in `code-review/` as the review method.

Run the test suite three times.

Label each finding `BLOCKER`, `SHOULD-FIX`, or `NIT`. For each finding, give the file and the line as `file:line`. Give a concrete fix for that finding. End the review with the line `BLOCKERS: <n>`.

Mark a hard violation, or a wrong implementation, as `BLOCKER`. Mark a partial requirement, or scope creep, as `SHOULD-FIX`. Mark a judgement-call smell as `NIT`.

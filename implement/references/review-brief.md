# How to review the PR

Use an agent other than the author agent as the reviewer.

The reviewer does not commit, comment, approve, or merge. The reviewer does not prompt the user.

Run the [code-review skill](../../code-review/SKILL.md) and follow its output format as-is. Give these inputs up front, so the reviewer does not ask:

- The fixed point is the PR's base branch. Diff that base against the PR head as `base...HEAD`.
- The spec is the plan step on the plan issue.

---
name: engineering-rules
description: Build a change from the innermost layer outward, with interfaces defined by the caller, hand-written fakes, and tests that do not sleep or depend on time. Use when you write application code, when you review it, or when the implement skill briefs an author agent.
---

# How to apply the engineering rules

Use these rules on the change you are writing.

- Keep the change small.
- Build the innermost layer first. Build each next layer only after the inner layers exist. Connect the layers last. Define each layer's interface by what the caller of that layer needs.
- Add a behaviour or an interface only when that behaviour or that interface helps a test. Prefer a fake that you write by hand to a mocking library.
- Write tests that cover what the change does. Only when a further test can catch a defect that the other tests miss, add that test. Do not write a test that sleeps. Do not write a test that depends on a time window.
- Run the formatter check. Compile with warnings as errors. Run the full test suite at least three times. Use a different seed for each run. Run one of the three runs in serial, not in parallel.

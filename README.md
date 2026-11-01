# skills

Agent skills live in top-level folders. A loader finds each skill at `<name>/SKILL.md`.

| Skill | Notes |
| --- | --- |
| [`technical-writing`](technical-writing/SKILL.md) | Vendored from pstack. Layered writing standard. Applies `unslop`. |
| [`unslop`](unslop/SKILL.md) | Vendored from pstack. Cuts AI tells from writing. |
| [`code-review`](code-review/SKILL.md) | Vendored from mattpocock/skills. Reviews a diff on standards and spec. |
| [`implement`](implement/SKILL.md) | One plan step, then a report-only review loop. |
| [`engineering-rules`](engineering-rules/SKILL.md) | Inner layer first, caller-defined interfaces, hand-written fakes. |

Vendored skills, upstream commits, and licenses are recorded in [VENDORED.md](VENDORED.md). Do not edit those folders here. Re-sync them with [`scripts/sync-vendor.sh`](scripts/sync-vendor.sh). Optional `--pstack-ref` and `--mattpocock-ref` (or `PSTACK_REF` and `MATTPOCOCK_REF`) select upstream refs. Both default to `main`.

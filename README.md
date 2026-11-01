# skills

Agent skills live in top-level folders. A loader finds each skill at `<name>/SKILL.md`.

| Skill | Notes |
| --- | --- |
| [`technical-writing`](technical-writing/SKILL.md) | Vendored from pstack. Layered writing standard. Applies `unslop`. |
| [`unslop`](unslop/SKILL.md) | Vendored from pstack. Cuts AI tells from writing. |
| [`code-review`](code-review/SKILL.md) | Vendored from mattpocock/skills. Reviews a diff on standards and spec. |

Vendored skills, upstream commits, and licenses are recorded in [VENDORED.md](VENDORED.md). Do not edit those folders here. Re-sync them with [`scripts/sync-vendor.sh`](scripts/sync-vendor.sh). Optional `--pstack-ref` and `--mattpocock-ref` (or `PSTACK_REF` and `MATTPOCOCK_REF`) select upstream refs. Both default to `main`.

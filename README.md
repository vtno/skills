# skills

Agent skills live in top-level folders. A loader finds each skill at `<name>/SKILL.md`.

| Skill | Notes |
| --- | --- |
| [`technical-writing`](technical-writing/SKILL.md) | Vendored from pstack. Layered writing standard. Applies `unslop`. |
| [`unslop`](unslop/SKILL.md) | Vendored from pstack. Cuts AI tells from writing. |

Vendored skills, the upstream commit, and the license are recorded in [VENDORED.md](VENDORED.md). Do not edit those folders here. Re-sync them with [`scripts/sync-vendor.sh`](scripts/sync-vendor.sh). Pass an optional upstream ref; the default is `main`.

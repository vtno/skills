# Vendored upstream files

These folders are copied verbatim from [cursor/plugins](https://github.com/cursor/plugins). Do not edit them in this repository. Change them upstream, then re-sync.

| Folder | Upstream path | Upstream repo | Commit | License |
| --- | --- | --- | --- | --- |
| `technical-writing/` | `pstack/skills/technical-writing/` | https://github.com/cursor/plugins | `ae5650febf4320793844c12c4adaa937f417f8da` | MIT ([LICENSES/pstack-LICENSE](LICENSES/pstack-LICENSE)) |
| `unslop/` | `pstack/skills/unslop/` | https://github.com/cursor/plugins | `ae5650febf4320793844c12c4adaa937f417f8da` | MIT ([LICENSES/pstack-LICENSE](LICENSES/pstack-LICENSE)) |

The MIT license text is [LICENSES/pstack-LICENSE](LICENSES/pstack-LICENSE), copied from upstream `pstack/LICENSE`.

Vendored folders must not be edited locally. Send changes upstream and re-sync instead:

```bash
scripts/sync-vendor.sh
scripts/sync-vendor.sh <ref>
```

`<ref>` is an optional upstream branch, tag, or commit. The default is `main`. The script replaces `technical-writing/`, `unslop/`, and `LICENSES/pstack-LICENSE`, then writes the fetched commit into the table above.

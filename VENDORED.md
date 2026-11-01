# Vendored upstream files

These folders are copied verbatim from upstream. Do not edit them in this repository. Change them upstream, then re-sync.

| Folder | Upstream path | Upstream repo | Commit | License |
| --- | --- | --- | --- | --- |
| `technical-writing/` | `pstack/skills/technical-writing/` | https://github.com/cursor/plugins | `ae5650febf4320793844c12c4adaa937f417f8da` | MIT ([LICENSES/pstack-LICENSE](LICENSES/pstack-LICENSE)) |
| `unslop/` | `pstack/skills/unslop/` | https://github.com/cursor/plugins | `ae5650febf4320793844c12c4adaa937f417f8da` | MIT ([LICENSES/pstack-LICENSE](LICENSES/pstack-LICENSE)) |
| `code-review/` | `skills/engineering/code-review/` | https://github.com/mattpocock/skills | `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d` | MIT ([LICENSES/mattpocock-skills-LICENSE](LICENSES/mattpocock-skills-LICENSE)) |

License texts:

- [LICENSES/pstack-LICENSE](LICENSES/pstack-LICENSE), MIT, copied from `pstack/LICENSE` in [cursor/plugins](https://github.com/cursor/plugins).
- [LICENSES/mattpocock-skills-LICENSE](LICENSES/mattpocock-skills-LICENSE), MIT, copied from `LICENSE` in [mattpocock/skills](https://github.com/mattpocock/skills).

Vendored folders must not be edited locally. Send changes upstream and re-sync instead:

```bash
scripts/sync-vendor.sh
scripts/sync-vendor.sh --pstack-ref <ref> --mattpocock-ref <ref>
```

Each ref is an optional upstream branch, tag, or commit. The default for both is `main`. The same refs can be set with `PSTACK_REF` and `MATTPOCOCK_REF`. The script replaces `technical-writing/`, `unslop/`, `code-review/`, and the license files, then writes each fetched commit into the matching rows above.

#!/usr/bin/env bash
# Re-sync vendored pstack skills from https://github.com/cursor/plugins.
# Usage: scripts/sync-vendor.sh [ref]
#   ref is a branch, tag, or commit. Default: main.
# Copies technical-writing/, unslop/, and LICENSES/pstack-LICENSE,
# then writes that commit SHA into VENDORED.md. Idempotent.
set -euo pipefail

if [[ $# -gt 1 ]]; then
  echo "usage: scripts/sync-vendor.sh [ref]" >&2
  exit 1
fi

REF="${1:-main}"
REPO_URL="https://github.com/cursor/plugins.git"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENDORED="${ROOT}/VENDORED.md"

if [[ ! -f "$VENDORED" ]]; then
  echo "sync-vendor: missing ${VENDORED}" >&2
  exit 1
fi

export GIT_TERMINAL_PROMPT=0

tmpdir="$(mktemp -d)"
cleanup() {
  rm -rf "$tmpdir"
}
trap cleanup EXIT

clone="${tmpdir}/plugins"
git init -q "$clone"
git -C "$clone" remote add origin "$REPO_URL"
git -C "$clone" sparse-checkout init --no-cone
git -C "$clone" sparse-checkout set --skip-checks \
  "pstack/skills/technical-writing" \
  "pstack/skills/unslop" \
  "pstack/LICENSE"
git -C "$clone" fetch --depth 1 --filter=blob:none origin "$REF"
git -C "$clone" checkout --detach --quiet FETCH_HEAD

src_tw="${clone}/pstack/skills/technical-writing"
src_un="${clone}/pstack/skills/unslop"
src_license="${clone}/pstack/LICENSE"

if [[ ! -f "${src_tw}/SKILL.md" || ! -f "${src_un}/SKILL.md" || ! -f "$src_license" ]]; then
  echo "sync-vendor: upstream tree at ${REF} is missing a vendored path" >&2
  exit 1
fi

sha="$(git -C "$clone" rev-parse HEAD)"
if [[ ! "$sha" =~ ^[0-9a-f]{40}$ ]]; then
  echo "sync-vendor: unexpected commit SHA: ${sha}" >&2
  exit 1
fi

updated="${tmpdir}/VENDORED.md"
awk -v sha="$sha" '
  {
    gsub(/`[0-9a-f]{40}`/, "`" sha "`")
    print
  }
' "$VENDORED" > "$updated"

if ! grep -q "$sha" "$updated"; then
  echo "sync-vendor: VENDORED.md has no backtick-wrapped 40-hex commit to update" >&2
  exit 1
fi

replace_dir() {
  local src="$1"
  local dest="$2"
  case "$dest" in
    "${ROOT}/technical-writing"|"${ROOT}/unslop") ;;
    *)
      echo "sync-vendor: refusing to replace ${dest}" >&2
      exit 1
      ;;
  esac
  rm -rf "$dest"
  mkdir -p "$dest"
  cp -a "${src}/." "${dest}/"
}

replace_dir "$src_tw" "${ROOT}/technical-writing"
replace_dir "$src_un" "${ROOT}/unslop"
mkdir -p "${ROOT}/LICENSES"
cp -f "$src_license" "${ROOT}/LICENSES/pstack-LICENSE"

if cmp -s "$VENDORED" "$updated"; then
  :
else
  cp -f "$updated" "$VENDORED"
fi

echo "sync-vendor: technical-writing/ unslop/ LICENSES/pstack-LICENSE @ ${sha}"

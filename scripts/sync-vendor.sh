#!/usr/bin/env bash
# Re-sync vendored skills from their upstream repos.
# Usage: scripts/sync-vendor.sh [--pstack-ref REF] [--mattpocock-ref REF]
#   Each ref is a branch, tag, or commit. Default: main.
#   The same defaults can be set with PSTACK_REF and MATTPOCOCK_REF.
# Copies technical-writing/, unslop/, code-review/, and the license files,
# then writes each commit SHA into the matching VENDORED.md rows. Idempotent.
set -euo pipefail

PSTACK_REF="${PSTACK_REF:-main}"
MATTPOCOCK_REF="${MATTPOCOCK_REF:-main}"
PSTACK_URL="https://github.com/cursor/plugins.git"
MATTPOCOCK_URL="https://github.com/mattpocock/skills.git"

usage() {
  echo "usage: scripts/sync-vendor.sh [--pstack-ref REF] [--mattpocock-ref REF]" >&2
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --pstack-ref)
      if [[ $# -lt 2 ]]; then
        usage
        exit 1
      fi
      PSTACK_REF="$2"
      shift 2
      ;;
    --mattpocock-ref)
      if [[ $# -lt 2 ]]; then
        usage
        exit 1
      fi
      MATTPOCOCK_REF="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "sync-vendor: unknown argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

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

fetch_sparse() {
  local dest="$1"
  local url="$2"
  local ref="$3"
  shift 3
  git init -q "$dest"
  git -C "$dest" remote add origin "$url"
  git -C "$dest" sparse-checkout init --no-cone
  git -C "$dest" sparse-checkout set --skip-checks "$@"
  git -C "$dest" fetch --depth 1 --filter=blob:none origin "$ref"
  git -C "$dest" checkout --detach --quiet FETCH_HEAD
}

require_sha() {
  local sha="$1"
  local label="$2"
  if [[ ! "$sha" =~ ^[0-9a-f]{40}$ ]]; then
    echo "sync-vendor: unexpected ${label} commit SHA: ${sha}" >&2
    exit 1
  fi
}

pstack_clone="${tmpdir}/plugins"
matt_clone="${tmpdir}/mattpocock-skills"

fetch_sparse "$pstack_clone" "$PSTACK_URL" "$PSTACK_REF" \
  "pstack/skills/technical-writing" \
  "pstack/skills/unslop" \
  "pstack/LICENSE"
fetch_sparse "$matt_clone" "$MATTPOCOCK_URL" "$MATTPOCOCK_REF" \
  "skills/engineering/code-review" \
  "LICENSE"

src_tw="${pstack_clone}/pstack/skills/technical-writing"
src_un="${pstack_clone}/pstack/skills/unslop"
src_pstack_license="${pstack_clone}/pstack/LICENSE"
src_review="${matt_clone}/skills/engineering/code-review"
src_matt_license="${matt_clone}/LICENSE"

if [[ ! -f "${src_tw}/SKILL.md" || ! -f "${src_un}/SKILL.md" || ! -f "$src_pstack_license" ]]; then
  echo "sync-vendor: pstack tree at ${PSTACK_REF} is missing a vendored path" >&2
  exit 1
fi
if [[ ! -f "${src_review}/SKILL.md" || ! -d "${src_review}/agents" || ! -f "$src_matt_license" ]]; then
  echo "sync-vendor: mattpocock tree at ${MATTPOCOCK_REF} is missing a vendored path" >&2
  exit 1
fi

pstack_sha="$(git -C "$pstack_clone" rev-parse HEAD)"
matt_sha="$(git -C "$matt_clone" rev-parse HEAD)"
require_sha "$pstack_sha" "pstack"
require_sha "$matt_sha" "mattpocock"

updated="${tmpdir}/VENDORED.md"
awk -v psha="$pstack_sha" -v msha="$matt_sha" '
  {
    if (index($0, "https://github.com/cursor/plugins")) {
      gsub(/`[0-9a-f]{40}`/, "`" psha "`")
    } else if (index($0, "https://github.com/mattpocock/skills")) {
      gsub(/`[0-9a-f]{40}`/, "`" msha "`")
    }
    print
  }
' "$VENDORED" > "$updated"

count_rows() {
  local url="$1"
  local sha="$2"
  grep -F "$url" "$updated" | grep -c -F "$sha" || true
}

pstack_rows="$(count_rows "https://github.com/cursor/plugins" "$pstack_sha")"
matt_rows="$(count_rows "https://github.com/mattpocock/skills" "$matt_sha")"
if [[ "$pstack_rows" -ne 2 || "$matt_rows" -ne 1 ]]; then
  echo "sync-vendor: VENDORED.md rows did not update (pstack=${pstack_rows}, mattpocock=${matt_rows})" >&2
  exit 1
fi

replace_dir() {
  local src="$1"
  local dest="$2"
  case "$dest" in
    "${ROOT}/technical-writing"|"${ROOT}/unslop"|"${ROOT}/code-review") ;;
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
replace_dir "$src_review" "${ROOT}/code-review"
mkdir -p "${ROOT}/LICENSES"
cp -f "$src_pstack_license" "${ROOT}/LICENSES/pstack-LICENSE"
cp -f "$src_matt_license" "${ROOT}/LICENSES/mattpocock-skills-LICENSE"

if ! cmp -s "$VENDORED" "$updated"; then
  cp -f "$updated" "$VENDORED"
fi

echo "sync-vendor: technical-writing/ unslop/ LICENSES/pstack-LICENSE @ ${pstack_sha}"
echo "sync-vendor: code-review/ LICENSES/mattpocock-skills-LICENSE @ ${matt_sha}"

#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if ! command -v rg >/dev/null 2>&1; then
  echo "ERROR: ripgrep (rg) is required for this safety scan." >&2
  exit 2
fi

patterns=(
  '/''Users/'
  'gho_[A-Za-z0-9_]+'
  'github_pat_[A-Za-z0-9_]+'
  '-----BEGIN [A-Z ]*PRIVATE KEY-----'
)

if [[ -n "${PUBLIC_SAFETY_EXTRA_PATTERNS:-}" ]]; then
  IFS=$'\n' read -r -d '' -a extra_patterns <<<"${PUBLIC_SAFETY_EXTRA_PATTERNS}" || true
  for pattern in "${extra_patterns[@]}"; do
    [[ -n "$pattern" ]] && patterns+=("$pattern")
  done
fi

failed=0
for pattern in "${patterns[@]}"; do
  if rg -n --hidden -g '!.git/**' -g '!Saved/**' -g '!Intermediate/**' -g '!DerivedDataCache/**' -- "$pattern" "$repo_root"; then
    failed=1
  fi
done

if [[ "$failed" -ne 0 ]]; then
  echo "ERROR: public repo safety scan found personal path/name or secret-like patterns." >&2
  exit 1
fi

echo "Public repo safety scan passed."

#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
uproject="$repo_root/HotelNightShift.uproject"

required_files=(
  "$uproject"
  "$repo_root/REQUIRED.md"
  "$repo_root/SECURITY.md"
  "$repo_root/Config/DefaultGame.ini"
  "$repo_root/Config/DefaultEngine.ini"
  "$repo_root/Ledgers/ASSET_LICENSE_LEDGER.md"
  "$repo_root/Ledgers/PLACEHOLDER_LEDGER.md"
  "$repo_root/HOTEL_LEVEL_PLAN.md"
  "$repo_root/FIRST_PRODUCT_SLICE.md"
)

for path in "${required_files[@]}"; do
  if [[ ! -f "$path" ]]; then
    echo "ERROR: Missing required file: $path" >&2
    exit 1
  fi
done

python3 -m json.tool "$uproject" >/dev/null

if rg -n 'genre not locked|genre pending|Deep Research|Before Genre Lock|After Deep Research|candidate genre' "$repo_root" -g '!.git/**' -g '!Tools/smoke_project_files.sh'; then
  echo "ERROR: Found obsolete genre-unlocked planning text." >&2
  exit 1
fi

"$repo_root/Tools/check_public_repo_safety.sh"

echo "Project file smoke check passed."

#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
uproject="${UPROJECT:-$repo_root/HotelNightShift.uproject}"

if [[ -z "${UE_EDITOR:-}" ]]; then
  echo "ERROR: Set UE_EDITOR to your local UnrealEditor executable path." >&2
  echo "Example: export UE_EDITOR=\"<engine-root>/Engine/Binaries/Mac/UnrealEditor\"" >&2
  exit 2
fi

if [[ ! -x "$UE_EDITOR" ]]; then
  echo "ERROR: UE_EDITOR is not executable: $UE_EDITOR" >&2
  exit 2
fi

if [[ ! -f "$uproject" ]]; then
  echo "ERROR: .uproject not found: $uproject" >&2
  exit 2
fi

exec "$UE_EDITOR" "$uproject" "$@"

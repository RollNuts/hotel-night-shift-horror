# Tools

Public-safe helper scripts for the Unreal project.

These scripts must not contain personal local paths, credentials, paid-service hooks, or private platform data.

## Scripts

- `check_public_repo_safety.sh`: scans the repository for common personal-path and secret-token patterns before pushing.
- `open_unreal_editor.sh`: opens the `.uproject` with an Unreal Editor executable supplied through `UE_EDITOR`.
- `smoke_project_files.sh`: validates the public-safe project baseline without launching the editor.

For local-only personal-name checks, pass newline-separated patterns through `PUBLIC_SAFETY_EXTRA_PATTERNS` instead of committing private names into the repository.

## Unreal Editor Path

Set `UE_EDITOR` locally before using editor launch scripts:

```bash
export UE_EDITOR="<engine-root>/Engine/Binaries/Mac/UnrealEditor"
Tools/open_unreal_editor.sh
```

Do not commit your real local engine path.

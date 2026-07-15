---
name: xcode-simulator-sandbox
description: Locate target application sandboxes on the iOS Simulator, inspect/query SQLite databases, and view or edit plist preference files (UserDefaults).
---

# Xcode Simulator Sandbox (xcode-simulator-sandbox)

Use this skill to view, modify, and audit SQLite databases, Plists, and User Defaults inside booted iOS Simulator application sandboxes for testing and debugging.

## When to Trigger This Skill

Trigger this skill when:
- Locating data directories and app containers for simulator-installed apps.
- Querying, updating, or auditing app database state (SQLite, CoreData, GRDB).
- Reading, writing, or deleting user preferences (UserDefaults) stored in plists.
- Pre-seeding database or preferences states for test automation (such as snapshot tests).

## Core Rules & Best Practices

- **Terminate the app before mutating**: Always terminate the target app process using `xcrun simctl terminate booted <bundle_id>` before editing SQLite databases or plists. Mutating files while the app is active can cause data corruption or be overwritten when the app flushes its state to disk.
- **Always backup first**: Create a timestamped copy of any file before executing writes or destructive updates:
  ```bash
  cp "$FILE" "${FILE}.bak.$(date +%s)"
  ```
- **Never edit binary plists as text**: Plist preferences inside the simulator are typically stored in binary format. Always use `plutil` or the helper script `sandbox_tool.py` to read/write them to avoid corruption.
- **Locate container dynamically**: Do not hardcode container paths, as Simulator UUIDs and paths are regenerated across builds and boots. Always resolve them dynamically using the bundle ID.

## Execution Workflow

### 1. Locate the Container Path
- Find the application sandbox directory:
  ```bash
  python3 scripts/sandbox_tool.py container-path <bundle_id>
  ```

### 2. View and Edit preferences (UserDefaults)
- Plist preferences are stored under `Library/Preferences/<bundle_id>.plist`.
- **Print**: `python3 scripts/sandbox_tool.py plist print -b <bundle_id>`
- **Set Key**: `python3 scripts/sandbox_tool.py plist set -b <bundle_id> <key> <value> --type <type>`
- **Delete Key**: `python3 scripts/sandbox_tool.py plist delete -b <bundle_id> <key>`

### 3. Query SQLite Databases
- SQLite databases are typically in `Documents/` or `Library/Application Support/`.
- **List Tables**: `python3 scripts/sandbox_tool.py sqlite -b <bundle_id> -p <relative_path> tables`
- **Query**: `python3 scripts/sandbox_tool.py sqlite -b <bundle_id> -p <relative_path> query "SELECT * FROM ..."`
- *Note: Run destructive queries (DELETE, DROP) only after explicit user approval.*

## Related Files

- Sandbox Helper: [scripts/sandbox_tool.py](scripts/sandbox_tool.py)
- Sample SQL Schema: [resources/schema_sample.sql](resources/schema_sample.sql)
- Usage Examples: [examples/usage_examples.md](examples/usage_examples.md)
- Plist/SQLite Reference: [references/plist_sqlite_ref.md](references/plist_sqlite_ref.md)

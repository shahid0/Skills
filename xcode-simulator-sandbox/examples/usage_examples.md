# Sandbox Inspector Usage Examples

This guide provides concrete command examples and scenarios for using the `sandbox_tool.py` script.

## Table of Contents
1. [Locating Sandbox Containers](#1-locating-sandbox-containers)
2. [Inspecting and Modifying User Defaults (Plists)](#2-inspecting-and-modifying-user-defaults-plists)
3. [Querying and Auditing SQLite Databases](#3-querying-and-auditing-sqlite-databases)

---

## 1. Locating Sandbox Containers

Find the filesystem path of the target application data container on the default booted simulator.

### Retrieve Data Container Path
```bash
python3 scripts/sandbox_tool.py container-path com.example.todoapp
```
**Example Output:**
```text
/Users/macbookpro/Library/Developer/CoreSimulator/Devices/4A16F4F9-E43B-49E8-AC36-61D328C697B7/data/Containers/Data/Application/E3E8C1C8-580F-4554-A6A4-F2D741CECE14
```

### Retrieve App Bundle Container Path
To locate the application binary itself:
```bash
python3 scripts/sandbox_tool.py container-path com.example.todoapp --type app
```

---

## 2. Inspecting and Modifying User Defaults (Plists)

The iOS `UserDefaults` API persists key-value data under the `Library/Preferences/<bundle_id>.plist` path inside the app's data container.

### Print All Preferences (as JSON)
```bash
python3 scripts/sandbox_tool.py plist print -b com.example.todoapp
```

### Read a Specific Preference Key
```bash
python3 scripts/sandbox_tool.py plist get -b com.example.todoapp has_completed_onboarding
```

### Set/Modify Preference Values
The tool automatically attempts to cast the value. You can override with `--type`.

- **String:**
  ```bash
  python3 scripts/sandbox_tool.py plist set -b com.example.todoapp current_theme "dark" --type string
  ```
- **Boolean:**
  ```bash
  python3 scripts/sandbox_tool.py plist set -b com.example.todoapp has_completed_onboarding "true" --type bool
  ```
- **Integer / Float:**
  ```bash
  python3 scripts/sandbox_tool.py plist set -b com.example.todoapp launch_count "42" --type int
  ```
- **JSON Object (Dictionary/Array):**
  ```bash
  python3 scripts/sandbox_tool.py plist set -b com.example.todoapp user_profile '{"name": "Alice", "premium": true}' --type json
  ```

### Delete a Preference Key
```bash
python3 scripts/sandbox_tool.py plist delete -b com.example.todoapp cached_auth_token
```

---

## 3. Querying and Auditing SQLite Databases

Many iOS applications use SQLite for persistence (directly, or via CoreData / SwiftData / GRDB).

### List All Tables
```bash
python3 scripts/sandbox_tool.py sqlite -b com.example.todoapp -p "Documents/TodoDatabase.sqlite" tables
```

### View Database Schema
```bash
python3 scripts/sandbox_tool.py sqlite -b com.example.todoapp -p "Documents/TodoDatabase.sqlite" schema
```

### Show Specific Table Schema
```bash
python3 scripts/sandbox_tool.py sqlite -b com.example.todoapp -p "Documents/TodoDatabase.sqlite" schema todo_items
```

### Run Custom SQL Queries
Use double quotes around your queries. By default, results are printed in a clean text-based table format.

- **Standard Table Format (Default):**
  ```bash
  python3 scripts/sandbox_tool.py sqlite -b com.example.todoapp -p "Documents/TodoDatabase.sqlite" query "SELECT id, title, completed FROM todo_items WHERE completed = 1"
  ```
  **Example Output:**
  ```text
  id | title                 | completed
  ---+-----------------------+----------
  1  | Set up repository     | 1        
  3  | Implement database    | 1        
  ```

- **JSON Output Format:**
  Useful for passing results to other tools or processes.
  ```bash
  python3 scripts/sandbox_tool.py sqlite -b com.example.todoapp -p "Documents/TodoDatabase.sqlite" query "SELECT * FROM todo_items" --format json
  ```

### Dump Table Contents
```bash
python3 scripts/sandbox_tool.py sqlite -b com.example.todoapp -p "Documents/TodoDatabase.sqlite" dump todo_items
```

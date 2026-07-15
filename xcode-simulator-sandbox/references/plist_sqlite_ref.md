# Plist File Conversion & SQLite Technical Guide

This document covers technical details regarding Property List (plist) files and SQLite database formats in the iOS Simulator environment.

---

## Part 1: Property List (plist) Formats & Conversion

Property lists (`.plist` files) are used by Apple operating systems to store structured serialization data, such as app preferences (`UserDefaults`) and metadata (`Info.plist`).

### Plist Formats
Apple uses three primary plist formats:
1. **Binary (`binary1`)**: A compact, binary representation. It is the default format for iOS preferences and is highly optimized for read performance. It is not human-readable in raw text.
2. **XML (`xml1`)**: A standard, UTF-8 XML document. It is human-readable and editable in text editors.
3. **OpenStep**: A legacy text-based format, now largely deprecated but sometimes seen in Xcode project files (`.pbxproj`).

### Plist Conversion using CLI
You can use macOS's built-in `plutil` utility to read, validate, or convert plist files:

- **View plist contents directly in stdout (formatted as JSON or XML):**
  ```bash
  plutil -p file.plist
  ```
- **Convert binary plist to XML (for text editing):**
  ```bash
  plutil -convert xml1 file.plist
  ```
- **Convert XML plist to binary (for iOS standard storage):**
  ```bash
  plutil -convert binary1 file.plist
  ```
- **Validate plist syntax:**
  ```bash
  plutil -lint file.plist
  ```

---

## Part 2: SQLite Databases & Write-Ahead Logging (WAL)

Most iOS persistence libraries (CoreData, SwiftData, GRDB, Realm) store data in SQLite databases. 

### SQLite Sidecar Files
When inspecting SQLite databases in the sandbox, you will often find three files with matching base names:
1. `Database.sqlite`: The main database file.
2. `Database.sqlite-wal`: The Write-Ahead Log file.
3. `Database.sqlite-shm`: The Shared Memory file.

### Understanding WAL Mode
Write-Ahead Logging (WAL) is the default journaling mode for SQLite on modern iOS. 
- **How it works:** Instead of writing changes directly to the main database file, SQLite appends transactions to the `-wal` file. Readers read from both the main file and the `-wal` file to get the current state.
- **Checkpointing:** Periodically, SQLite copies changes from the `-wal` file back into the main database file. This process is called a "checkpoint".
- **Inspection Caveat:** If you copy or read only the main `Database.sqlite` file, **you may miss the most recent transactions** stored in the `-wal` file. You must copy/read all three files (`.sqlite`, `.sqlite-wal`, `.sqlite-shm`) together to maintain database integrity.

### SQLite Pragma Commands for Audits
When inspecting databases, standard SQLite `PRAGMA` commands can be used to query state:

- **Check Integrity:**
  Returns `ok` or a list of errors.
  ```sql
  PRAGMA integrity_check;
  ```
- **Get Journaling Mode:**
  ```sql
  PRAGMA journal_mode;
  ```
- **Force Checkpoint:**
  Forces all transactions in the `-wal` file to be committed to the main `.sqlite` file.
  ```sql
  PRAGMA wal_checkpoint(FULL);
  ```
- **Database Index Info:**
  Show indices on a table.
  ```sql
  PRAGMA index_list(table_name);
  ```

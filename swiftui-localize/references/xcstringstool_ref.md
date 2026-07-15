# xcstringstool Reference Guide

`xcstringstool` is Apple's official command line utility to extract, compile, sync, and print Xcode String Catalogs (`.xcstrings`).

## Commands and Usage

### 1. `extract`
Extracts localizable strings from source code files (Swift, SwiftUI, Objective-C).

```bash
xcrun xcstringstool extract [<options>] [<source-files> ...] --output-directory <output-directory>
```

#### Major Options:
- `-o, --output-directory <output-directory>`: The directory to place output `.stringsdata` or `.xcstrings` files (Required).
- `--output-format <format>`: Output format (default is `stringsdata`, but `xcstrings` or `strings` can be specified).
- `--append`: When writing `xcstrings` or `strings`, appends/merges new strings instead of overwriting the output file.
- `--SwiftUI`: Extract from various SwiftUI APIs (e.g., `Text`, `Button`, etc.).
- `--SwiftUI-Text`: Extract from SwiftUI `Text` (legacy genstrings-style).
- `--modern-localizable-strings`: Extract from modern localization APIs like `String(localized:)`, `AttributedString(localized:)`, and `LocalizedStringResource`.
- `--legacy-localizable-strings`: Extract from standard legacy macros like `NSLocalizedString`.
- `--table <table>`: Restrict extraction to specific string tables.

---

### 2. `compile`
Compiles an `.xcstrings` file into build products (`.strings` and `.stringsdict`).

```bash
xcrun xcstringstool compile <input-file> --output-directory <output-directory> [options]
```

#### Major Options:
- `-o, --output-directory <output-directory>`: Directory for compiled build files (Required).
- `-f, --format <format>`: Compilation output format (options: `stringsAndStringsdict`, `stringsdictOnly`; default: `stringsAndStringsdict`).
- `-l, --language <language>`: Limit compilation to specific language codes. Specify multiple times to compile multiple languages.
- `--serialization-format <format>`: Representation of individual files (options: `text`, `binary`; default: `text`).
- `--dry-run`: Prints a list of compilation paths without writing anything to disk.

---

### 3. `list-missing` (Custom Helper Concept)
While `xcstringstool` itself doesn't have a direct `list-missing` command, the catalog is stored in plain text JSON, which allows utilities (like `xcstrings_helper.py`) to easily parse the structure, locate missing locales, and extract them for localization.

---

### 4. `sync`
Updates an `.xcstrings` catalog with the keys found in `.stringsdata` files.

```bash
xcrun xcstringstool sync <xcstrings> ... --stringsdata <stringsdata> ... [--skip-marking-strings-stale]
```

#### Major Options:
- `--stringsdata`: Specifies one or more `.stringsdata` files containing the keys extracted from the codebase.
- `--skip-marking-strings-stale`: Prevents marking keys as stale or deleting them from the `.xcstrings` file when not present in the `.stringsdata`.

---

### 5. `print`
Prints all keys represented in an `.xcstrings` catalog file.

```bash
xcrun xcstringstool print <input-file>
```

---

### 6. `generate-symbols`
Generates Swift symbols or code for manually defined strings, enabling compile-time safety.

```bash
xcrun xcstringstool generate-symbols <input-file>
```

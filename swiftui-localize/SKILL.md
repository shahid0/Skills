---
name: "swiftui-localize"
description: "Extract, translate, and sync SwiftUI String Catalogs (.xcstrings) using xcstringstool and context-aware agentic translation."
---

# SwiftUI Localization (swiftui-localize)

Use this skill to extract, translate, and maintain SwiftUI String Catalogs (`.xcstrings`) using a combination of Xcode's command line tools and context-aware LLM translations.

## When to Trigger This Skill

Trigger this skill when the user requests any of the following tasks:
- Localizing a SwiftUI app or specific views.
- Translating the app into a new language/locale (e.g., Spanish, German, French).
- Syncing or updating String Catalogs (`.xcstrings`) after adding new UI views.
- Finding and fixing untranslated keys in the codebase.
- Compiling or verifying that string catalogs are valid.

## Step-by-Step Execution Workflow

Follow this systematic process to perform SwiftUI localizations:

### 1. Locate or Initialize the String Catalog
- Locate the existing `.xcstrings` file in the project (usually named `Localizable.xcstrings` inside the project's localization folder or alongside source files).
- If no `.xcstrings` catalog exists, copy the base template from `resources/template.xcstrings` to your target project localization directory, naming it appropriately (e.g., `Localizable.xcstrings`).

---

### 2. Extract New Strings from Code
- Scan the target SwiftUI views and source files to extract localizable strings.
- Run the extraction helper script to parse and update the catalog:
  ```bash
  python3 scripts/xcstrings_helper.py extract \
    --source-files <path_to_source_dir_or_files> \
    --xcstrings-path <path_to_xcstrings_file>
  ```
- *Note:* This calls `xcrun xcstringstool extract` under the hood to pull new keys and developer comments from SwiftUI views, `String(localized:)`, and `NSLocalizedString` calls.

---

### 3. Identify Untranslated Keys
- Identify which keys are missing translations for your target locale (e.g., `es` for Spanish) by running:
  ```bash
  python3 scripts/xcstrings_helper.py list-missing \
    --xcstrings-path <path_to_xcstrings_file> \
    --locale <locale_code> \
    --json
  ```
- Save the JSON output to a file on disk (e.g., `missing_es.json`) — do not try to pass it as a shell argument.
- If there are no missing keys, you are done!

---

### 4. Gather Surrounding Code Context
For every untranslated key, locate its occurrence in the Swift/SwiftUI codebase using a grep or pattern search:
1. Find the file name and line number where the key is used.
2. Read the surrounding 10–15 lines of code to understand:
   - **UI Hierarchy:** Is this key inside a `Button`, a `Text` title, a description `Label`, or a `NavigationTitle`?
   - **User Interface State:** Is it a screen title, placeholder, alert message, dynamic value, list cell, or toast notification?
   - **Variables/Interpolations:** Does it use string interpolation (e.g., `\(name)`)? If so, understand what values will be injected.
   - **Developer Comments:** Read any localization comments (e.g. `Text("Welcome", comment: "Header label")`).

---

### 5. Generate Context-Aware Translations

> [!IMPORTANT]
> **Do NOT generate translations by naive string substitution.** Translation must be agent-mediated using the full code context gathered in Step 4. A simple programmatic or "find and replace" translation will produce incorrect results — it has no understanding of UI context, form factor, or grammar.

For each untranslated key, construct your translations with full context awareness:
- **Tone/Style:** Maintain consistent tone (e.g., casual vs. formal) across the app.
- **Form Factor:** Keep button labels and navigation titles concise to prevent layout overflow or clipping on small screens.
- **Interpolation Specifiers:** Ensure SwiftUI formatting tokens (like `%@`, `%d`, `%lld`, `%arg`) are **exactly preserved** in the target language. Never translate or reorder tokens. Example: `"Hello, %@!"` → German: `"Hallo, %@!"` ✓ (token preserved).
- **Format Specifier Mapping:**

  | SwiftUI Token | Type | Rule |
  | :--- | :--- | :--- |
  | `%@` | String | Always preserve as-is |
  | `%d` / `%lld` | Integer | Always preserve as-is |
  | `%f` | Floating-point | Always preserve as-is |
  | `%arg` | Generic | Always preserve as-is |

- **Plural & Gender Forms:** Many languages require plural or gender variants. Use the structured variations format in `xcstrings` when translating for languages like Arabic (6 plural forms), Russian (3 forms), or German (gendered articles).

  For example, a translated plural key in Spanish should be structured as:
  ```json
  {
    "one": { "stringUnit": { "state": "translated", "value": "%lld elemento" } },
    "other": { "stringUnit": { "state": "translated", "value": "%lld elementos" } }
  }
  ```
  Pass this structured dict as the value for the key in the translations JSON file.

- **Grammar/Accents:** Deliver high-quality, grammatically correct translations with appropriate accents and diacritics (e.g., `é`, `ñ`, `ü`). Accents are not optional — they affect meaning and grammar.
- **Locale Subtleties:** Distinguish locale variants: `es` (Spain Spanish) vs. `es-419` (Latin American Spanish), `zh-Hans` (Simplified Chinese) vs. `zh-Hant` (Traditional Chinese).

---

### 6. Merge Translations into Catalog

> [!IMPORTANT]
> **Translations MUST be saved to a JSON file on disk** before merging. Do not pass large JSON as a shell argument — it is unreliable and shell-escaping prone. Write a temp file, then pass the file path:

```bash
# Save translations to a temp JSON file first
cat > ./translations_es.json << 'EOF'
{
  "Continue": "Continuar",
  "Cancel": "Cancelar",
  "Welcome, %@!": "¡Bienvenido, %@!"
}
EOF

# Then merge from the file
python3 scripts/xcstrings_helper.py merge \
  --xcstrings-path <path_to_xcstrings_file> \
  --locale es \
  --translations ./translations_es.json
```

---

### 7. Compile and Verify
- Compile the updated catalog to verify there are no JSON syntax errors, missing brackets, or structural issues:
  ```bash
  python3 scripts/xcstrings_helper.py compile \
    --xcstrings-path <path_to_xcstrings_file>
  ```
- Check that the exit status is `0` and verify the output.
- If compilation fails, inspect the error message from `xcstringstool` and fix the malformed entry before re-running.

---

## Related Files

- Helper Script: [scripts/xcstrings_helper.py](scripts/xcstrings_helper.py)
- Template Catalog: [resources/template.xcstrings](resources/template.xcstrings)
- Usage Examples: [examples/usage_example.md](examples/usage_example.md)
- xcstringstool Reference: [references/xcstringstool_ref.md](references/xcstringstool_ref.md)

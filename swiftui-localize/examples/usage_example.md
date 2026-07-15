# SwiftUI Localization Workflow Example

This example demonstrates how to extract, locate, translate, merge, and verify SwiftUI strings using the `swiftui-localize` skill.

---

## 1. Extract Strings from Source Code
Run the `extract` command to scan Swift files/directories and populate or update the `.xcstrings` catalog file.

```bash
python3 scripts/xcstrings_helper.py extract \
  --source-files ./Sources/MySwiftUIApp \
  --xcstrings-path ./Sources/MySwiftUIApp/Localizable.xcstrings
```

*This command will recursively parse the directory and merge any new strings found in SwiftUI views or modern localized string initializers into the `Localizable.xcstrings` catalog.*

---

## 2. List Missing Translations
Find out which strings are missing translations for a specific target locale (e.g., Spanish `"es"`).

```bash
python3 scripts/xcstrings_helper.py list-missing \
  --xcstrings-path ./Sources/MySwiftUIApp/Localizable.xcstrings \
  --locale es \
  --json
```

### Sample Output:
```json
{
  "sourceLanguage": "en",
  "targetLanguage": "es",
  "missingCount": 2,
  "missing": [
    {
      "key": "Welcome to the localized app",
      "comment": "Welcome message on home screen"
    },
    {
      "key": "Tap me!",
      "comment": ""
    }
  ]
}
```

---

## 3. Agentic Context-Aware Translation
The agent uses the missing keys list, inspects the codebase (specifically looking at the SwiftUI files where the missing keys reside to get structural, UI, and semantic context), and calls the LLM to generate highly context-aware translations.

### Example Agent Translation Process:
1. Locate where `"Tap me!"` is defined in `./Sources/MySwiftUIApp/ContentView.swift`:
   ```swift
   Button(action: {}) {
       Text("Tap me!")
   }
   ```
2. Realize it is a button action text.
3. Translate `"Tap me!"` to Spanish as `"¡Púlsame!"` or `"¡Presióname!"` based on context.
4. Translate `"Welcome to the localized app"` to Spanish as `"Bienvenido a la aplicación localizada"`.

---

## 4. Merge Translations Back
Once translations are generated, merge them back into the `.xcstrings` catalog:

```bash
python3 scripts/xcstrings_helper.py merge \
  --xcstrings-path ./Sources/MySwiftUIApp/Localizable.xcstrings \
  --locale es \
  --translations '{"Welcome to the localized app": "Bienvenido a la aplicación localizada", "Tap me!": "¡Púlsame!"}'
```

---

## 5. Compile and Verify Catalog
Finally, verify that the updated catalog compiles cleanly using Xcode's engine.

```bash
python3 scripts/xcstrings_helper.py compile \
  --xcstrings-path ./Sources/MySwiftUIApp/Localizable.xcstrings
```

### Output:
```text
Compiling catalog: ./Sources/MySwiftUIApp/Localizable.xcstrings
Verification: Catalog compiled successfully with no syntax or structure errors.
```

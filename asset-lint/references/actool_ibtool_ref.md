# actool & ibtool Reference Guide

This reference document compiles documentation on the command-line usage, diagnostic outputs, and troubleshooting procedures for Xcode's Asset Catalog compiler (`actool`) and Interface Builder compiler (`ibtool`).

---

## 1. actool (Asset Catalog Compiler)

`actool` compiles asset catalogs (`.xcassets`) into runtime binary files (such as `Assets.car`) and partial `Info.plist` files containing app icon declarations.

### Command Syntax

```bash
xcrun actool <input_catalog_path> \
  --compile <output_directory_path> \
  --platform <platform_name> \
  --minimum-deployment-target <version> \
  [--app-icon <name>] \
  [--output-partial-info-plist <plist_path>] \
  --output-format xml1 \
  --errors --warnings --notices
```

### Key Arguments
*   **`--compile <path>`**: Output directory where compiled products (`Assets.car`, etc.) will be written.
*   **`--platform <name>`**: Targeted platform. Common values: `iphoneos`, `iphonesimulator`, `macosx`, `appletvos`, `watchos`.
*   **`--minimum-deployment-target <target>`**: iOS/macOS version limit (e.g., `14.0`).
*   **`--app-icon <name>`**: Name of the target AppIcon asset to be validated and compiled as the primary app icon (e.g., `AppIcon`).
*   **`--output-partial-info-plist <path>`**: Location to output partial plist containing generated metadata (like icon names).
*   **`--output-format xml1`**: Formats stdout as standard XML plist, which is easily parsed by scripting environments.

### Diagnostic Plist Keys
*   **`com.apple.actool.document.errors`** / **`com.apple.actool.errors`**: Critical compiler failures that stop the build (e.g., missing mandatory images, corrupt catalog JSONs).
*   **`com.apple.actool.document.warnings`** / **`com.apple.actool.warnings`**: Compilation warnings (e.g., unassigned images, incorrect size scales, name spaces).
*   **`com.apple.actool.document.notices`** / **`com.apple.actool.notices`**: Diagnostic feedback items.

---

## 2. ibtool (Interface Builder Compiler)

`ibtool` compiles Interface Builder storyboards (`.storyboard`) and XIBs (`.xib`) into runtime-optimized nib files (`.storyboardc` and `.nib`).

### Command Syntax

```bash
xcrun ibtool <input_file_path> \
  --compile <output_file_path> \
  --target-device <device> \
  --minimum-deployment-target <version> \
  --output-format xml1 \
  --errors --warnings --notices
```

### Key Arguments
*   **`--compile <path>`**: Output compiled storyboard compiler bundle (`.storyboardc` folder) or nib file (`.nib` file).
*   **`--target-device <device>`**: Sets layout targets (e.g., `iphone`, `ipad`).
*   **`--output-format xml1`**: Standard XML plist output format on stdout.

### Other Useful Commands

#### Extract Localizable Strings
To extract all user-facing strings for localization from a storyboard or XIB:
```bash
xcrun ibtool --export-strings-file <output_strings_file> <input_ib_file>
```

#### Localized Strings Validation
If `ibtool` fails to compile a localized storyboard or XIB due to errors in string catalogs or translation files, you should lint your `.strings` files using `plutil`:
```bash
plutil -lint path/to/Localizable.strings
```

### Diagnostic Plist Keys
*   **`com.apple.ibtool.errors`**: Severe layout compilation failures (e.g., broken subclass links, syntax issues).
*   **`com.apple.ibtool.warnings`**: Layout and structural warnings.
    *   *Autolayout / Constraints:* E.g. "Frame for 'Button' will be different at run time", "Ambiguous layout for view".
    *   *Localization:* E.g. "The identifier 'x-y-z' is not localized."
*   **`com.apple.ibtool.notices`**: Diagnostic notices.

---

## 3. Common Troubleshooting Procedures

### 1. Active Xcode Command Line Tools Path
If `xcrun` commands fail with compilation tool issues or "developer path not found" (Exit Code 72), check the active developer path:
```bash
xcode-select -p
```
If it is pointing to the wrong Xcode version or command line tools folder, update it:
```bash
sudo xcode-select -s <xcode-app>/Contents/Developer
```

### 2. Linting Strings Files (Syntax Check)
Interface Builder string extraction can occasionally output malformed strings files containing invalid characters, which cause compilations to fail silently. Always validate the syntax of `.strings` files before merging:
```bash
plutil -lint Localizable.strings
```
Expected output:
```text
Localizable.strings: OK
```
If there are errors, it will print:
```text
Localizable.strings: Old-style plist parser error on line 12 : Expecting ';'
```

# `xcresulttool` Command Reference

Xcode Result Bundle Tool (`xcresulttool`) is a command-line utility used to query, export, merge, and compare the contents of `.xcresult` bundles generated during Xcode builds and tests.

---

## 1. Subcommands Overview

### `get`
Gets the contents of a result bundle.
*   **Syntax**: `xcrun xcresulttool get [subcommand] --path <path> [options]`
*   **Subcommands**:
    *   `object` (default): Prints the raw/JSON object graph. (Pass `--format json` to get JSON).
    *   `test-results`: Get high-level test details, destinations, and failures.
        *   `summary`: High-level counts and test run results (JSON output by default).
        *   `tests`: Tree of test suites, test cases, and their execution status.
        *   `test-details`: In-depth parameters and results for a specific test identifier.
        *   `activities`: Detailed activity/interaction trees (e.g. for UI tests).
    *   `build-results`: High-level build actions, warnings, and compiler issues.
    *   `log`: Extracts build logs or test execution logs.

### `export`
Exports files, diagnostics, coverage reports, or attachments from a result bundle.
*   **Syntax**: `xcrun xcresulttool export [subcommand] --path <path> --output-path <output-path> [options]`
*   **Subcommands**:
    *   `attachments`: Exports screenshots, logs, and other attachments associated with the test run.
    *   `diagnostics`: Exports system diagnostic reports.
    *   `coverage`: Extracts code coverage data.

### `merge`
Combines multiple `.xcresult` bundles into a single bundle.
*   **Syntax**: `xcrun xcresulttool merge <input-path-1> <input-path-2> ... --output-path <output-path>`

### `compare`
Compares two result bundles (a target bundle against a baseline bundle) to identify differences in test outcomes, warnings, or build errors.
*   **Syntax**: `xcrun xcresulttool compare --path <target-path> --baseline-path <baseline-path> [options]`

---

## 2. Common Command Recipes

### Extract all failure summaries in raw JSON
```bash
xcrun xcresulttool get --path PathToResults.xcresult --format json
```
To find failing tests inside the returned JSON structure:
- Root level: `.issues.testFailureSummaries._values[]`
- Action level: `.actions._values[].actionResult.issues.testFailureSummaries._values[]`

Key properties of each failure:
- `.testCaseName._value`: The test class and method (e.g., `MyTests.testExample()`).
- `.message._value`: The exact failure message/assertion description.
- `.documentLocationInCreatingWorkspace.url._value`: A file path pointing to the file and line number where the failure occurred. E.g.: `Tests/MyTests.swift#CharacterRangeLen=0&EndingLineNumber=42&StartingLineNumber=42` (Note: Xcode line numbers in URLs are 0-indexed).

### Export test screenshots and failure attachments
```bash
xcrun xcresulttool export attachments \
  --path PathToResults.xcresult \
  --output-path ./AttachmentsOutput \
  --only-failures
```
This writes the attachments and generates a `manifest.json` file inside the output directory mapping files to their tests:
```json
[
  {
    "testIdentifier": "MyTests/testExample()",
    "testIdentifierURL": "...",
    "attachments": [
      {
        "exportedFileName": "screenshot_1.png",
        "suggestedHumanReadableName": "Screenshot",
        "isAssociatedWithFailure": true,
        "deviceName": "iPhone 15",
        "deviceId": "..."
      }
    ]
  }
]
```

### Get high-level test counts and results
```bash
xcrun xcresulttool get test-results summary --path PathToResults.xcresult
```
Outputs:
- `.totalTestCount`: Total tests run.
- `.passedTests`: Number of passing tests.
- `.failedTests`: Number of failing tests.
- `.skippedTests`: Number of skipped tests.

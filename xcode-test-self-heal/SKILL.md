---
name: xcode-test-self-heal
description: Run iOS/macOS test suites using xcodebuild, parse failures from .xcresult bundles with xcresulttool, and perform self-healing code edits to resolve test failures.
---

# Xcode Test Self-Healing (xcode-test-self-heal)

Use this skill to automate running Xcode-based test suites (iOS/macOS), parse detailed failure reports from the resulting `.xcresult` files, and iteratively apply fixes to the codebase in a self-healing loop.

## When to Trigger This Skill

Trigger this skill when:
- Running iOS or macOS unit and UI tests.
- Troubleshooting crashing or failing Xcode test cases during verification or build phases.
- Extracting and analyzing test attachments (such as screenshots or system logs) from failed test runs.
- Automating a self-healing cycle where tests are executed, failures analyzed, changes proposed, and verified.

## Execution Workflow

### 1. Execute Tests and Parse Failures
- Run the test runner parser to execute tests and parse detailed failure objects to JSON:
  ```bash
  python3 scripts/xcresult_parser.py \
    --workspace <path_to_xcworkspace> \
    --scheme <scheme_name> \
    --destination <destination_string> \
    --output-report ./build/test_report.json
  ```
- *Note: Additional flags are forwarded directly to `xcodebuild`.*

### 2. Analyze the Output Report
- Open and inspect the generated `./build/test_report.json` to find failing tests.
- For each failure, note the target file (`file_path`), line number (`line_number`), and assertion message (`message`).
- Inspect any failed UI screenshots exported by the parser.

### 3. Diagnose and Apply Fixes
- Locate the failing file path and read the surrounding code context.
- Formulate a clear hypothesis for the failure and present the proposed diff to the user.
- Apply the narrowest possible correction to resolve the issue. Do not perform sweeping refactors during a self-heal cycle.

### 4. Verify and Iterate
- Re-run the parser script to execute the tests again.
- **Limit iterations**: If a test cannot be successfully healed after **3 attempts**, halt the loop, document your attempts, and ask the user for guidance.

## Related Files

- Test Parser: [scripts/xcresult_parser.py](scripts/xcresult_parser.py)
- Default Config: [resources/test_options.json](resources/test_options.json)
- Usage Examples: [examples/usage_examples.md](examples/usage_examples.md)
- xcresulttool Reference: [references/xcresulttool_ref.md](references/xcresulttool_ref.md)

# Asset-Lint Usage Examples

This guide demonstrates how to integrate `compile_auditor.py` into your iOS/macOS development workflow.

---

## 1. Local Audits (Manual Invocation)

You can run the script manually from the terminal to inspect all asset catalogs, storyboards, and XIB files in your repository.

### Run on specific asset catalogs and storyboards
```bash
python3 scripts/compile_auditor.py \
  --assets path/to/Assets.xcassets \
  --storyboards path/to/Base.lproj/Main.storyboard path/to/Base.lproj/LaunchScreen.storyboard
```

### Scan entire directories recursively
If you pass a directory to `--storyboards`, the script will recursively find all `.storyboard` and `.xib` files:
```bash
python3 scripts/compile_auditor.py \
  --assets $(find . -name "*.xcassets") \
  --storyboards ./MyXcodeProject \
  --platform iphonesimulator \
  --minimum-deployment-target 15.0
```

### Output as JSON for CI or further processing
```bash
python3 scripts/compile_auditor.py \
  --assets path/to/Assets.xcassets \
  --format json \
  --severity warning
```

### Fail builds on warnings or errors (Strict mode)
Use the `--strict` flag to return a non-zero exit status if warnings or errors are found:
```bash
python3 scripts/compile_auditor.py \
  --assets path/to/Assets.xcassets \
  --strict
```

---

## 2. Git Pre-Commit Hook Integration

To prevent broken asset catalogs or constraint warnings from being committed to your repository, you can set up a Git pre-commit hook that runs `compile_auditor.py` only on **staged files**.

Create or update `.git/hooks/pre-commit` and add the following bash script:

```bash
#!/bin/bash
# Pre-commit hook to audit staged assets and Interface Builder files

# Find all staged files matching the relevant extensions
STAGED_ASSETS=$(git diff --cached --name-only --diff-filter=ACM | grep '\.xcassets$' | tr '\n' ' ')
STAGED_IBS=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(storyboard|xib)$' | tr '\n' ' ')

# Path to the auditor script
AUDITOR_PATH="scripts/compile_auditor.py"

# If no relevant files are staged, skip audit
if [ -z "$STAGED_ASSETS" ] && [ -z "$STAGED_IBS" ]; then
    exit 0
fi

CMD="python3 $AUDITOR_PATH --strict"

if [ -n "$STAGED_ASSETS" ]; then
    CMD="$CMD --assets $STAGED_ASSETS"
fi

if [ -n "$STAGED_IBS" ]; then
    CMD="$CMD --storyboards $STAGED_IBS"
fi

echo "🔍 Running asset-lint audit on staged files..."
eval $CMD
RESULT=$?

if [ $RESULT -ne 0 ]; then
    echo "❌ Pre-commit hook failed: Asset or layout validation errors found."
    exit 1
fi

echo "✅ Asset-lint validation passed."
exit 0
```

Make sure the hook is executable:
```bash
chmod +x .git/hooks/pre-commit
```

---

## 3. Xcode Build Phase Integration

By default, the script outputs in standard Xcode issue format:
`file:line: severity: [category] description`

This means you can add a **Run Script Phase** to your Xcode project target, and any warnings/errors will show up directly in Xcode's **Issue Navigator** side-panel and inline in the Storyboard code view.

### Steps to Integrate:
1. Open your project in Xcode.
2. Select your Target under the Project settings.
3. Navigate to **Build Phases** tab.
4. Click the `+` icon and choose **New Run Script Phase**.
5. Rename the phase to `[Lint] Asset & Storyboard Audit`.
6. Position the phase early in the list (e.g., right after "Dependencies" or "Headers").
7. Paste the following script into the text area:

```bash
# Xcode Build Phase integration for asset-lint
AUDITOR_PATH="scripts/compile_auditor.py"

# Find files relative to the project root
ASSETS=$(find "${SRCROOT}" -name "*.xcassets" -type d)
STORYBOARDS="${SRCROOT}"

# Run linter
python3 "$AUDITOR_PATH" \
  --assets $ASSETS \
  --storyboards "$STORYBOARDS" \
  --platform "${PLATFORM_NAME}" \
  --minimum-deployment-target "${IPHONEOS_DEPLOYMENT_TARGET}" \
  --severity warning
```

Now, every time you build the project in Xcode, any misaligned constraints or asset warnings will show up as native Xcode warnings!

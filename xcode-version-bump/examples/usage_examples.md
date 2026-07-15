# Build Pipeline Usage Examples

This reference guide provides usage patterns, command syntax, and sample log outputs for the automated Xcode version bumping and IPA export pipeline.

---

## 1. BASIC USAGE SCENARIOS

### A. Incremental Build Bump (Dry Run)
Validate options and inspect the exact Xcode commands without modifying any files or launching builds:
```bash
./scripts/build_pipeline.sh \
  -w MyApp.xcworkspace \
  -s MyAppScheme \
  -e resources/ExportOptions.plist \
  -b build \
  --dry-run
```

### B. Increment Build Number & Run Pipeline
Bump the project build version (`agvtool bump`) and generate a production-ready `.ipa` file:
```bash
./scripts/build_pipeline.sh \
  -w MyApp.xcworkspace \
  -s MyAppScheme \
  -e resources/ExportOptions.plist \
  -b build \
  -o ./build/releases
```

### C. Set Specific Marketing Version & Build
Set the marketing version (e.g., `2.1.0`) and trigger archiving and exporting:
```bash
./scripts/build_pipeline.sh \
  -w MyApp.xcworkspace \
  -s MyAppScheme \
  -e resources/ExportOptions.plist \
  -b marketing \
  -m 2.1.0
```

### D. Full Version Release (Both build and marketing bumps)
Increment the build number AND set a new marketing version simultaneously:
```bash
./scripts/build_pipeline.sh \
  -w MyApp.xcworkspace \
  -s MyAppScheme \
  -e resources/ExportOptions.plist \
  -b both \
  -m 2.2.0
```

---

## 2. CI/CD INTEGRATION EXAMPLES

### A. GitHub Actions Workflow
Incorporate the script into a GitHub runner:
```yaml
name: iOS Release Build

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: macos-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - name: Set up Xcode
        uses: maxim-lobanov/setup-xcode@v1
        with:
          xcode-version: '15.0'

      - name: Import Signing Certificates & Profiles
        run: |
          # Import certs/profiles to keychain here...

      - name: Run Build and Export Pipeline
        run: |
          # Extract tag version
          TAG_VERSION=${GITHUB_REF#refs/tags/v}
          chmod +x .agents/skills/auto-version-bump/scripts/build_pipeline.sh
          
          .agents/skills/auto-version-bump/scripts/build_pipeline.sh \
            -w MyApp.xcworkspace \
            -s Runner \
            -e .agents/skills/auto-version-bump/resources/ExportOptions.plist \
            -b both \
            -m "$TAG_VERSION" \
            -o ./build/ipa
```

### B. Fastlane Integration
You can invoke the shell script from a Fastfile lane:
```ruby
lane :ship_ipa do |options|
  version = options[:version]
  
  sh("../../.agents/skills/auto-version-bump/scripts/build_pipeline.sh " \
     "-w MyApp.xcworkspace " \
     "-s MyAppScheme " \
     "-e ../../.agents/skills/auto-version-bump/resources/ExportOptions.plist " \
     "-b both " \
     "-m #{version} " \
     "-o ./build/ipa")
end
```

---

## 3. SAMPLE LOGS

### Successful Execution Output
```text
=== Xcode Build & Version Bump Pipeline ===
Verifying Apple Generic Versioning build settings...
Verified: Apple Generic Versioning is enabled.
Navigating to project directory: /Users/macbookpro/Projects/MyApp
Running: agvtool bump
Setting version of project MyApp to:
    102

Updating CFBundleVersion in Info.plist(s)...

Updated CFBundleVersion in MyApp.xcodeproj/../MyApp/Info.plist to 102
Creating compilation archive...
User defaults from command line:
    IDEArchivePathOverride = /Users/macbookpro/Projects/MyApp/build/output/MyAppScheme.xcarchive

Prepare build
...
** ARCHIVE SUCCEEDED **

Exporting signed IPA package...
2026-07-14 13:20:10.123 xcodebuild[5678:90123] [MT] IDEDistribution: -[IDEDistributionLogging _createLoggingBundleAtPath:]: Created distribution logs at path /var/folders/.../MyAppScheme_2026-07-14_13-20-10.xcdistributionlogs
Exported MyAppScheme.ipa to /Users/macbookpro/Projects/MyApp/build/output
** EXPORT SUCCEEDED **

=== Build pipeline completed successfully ===
Archive: ./build/output/MyAppScheme.xcarchive
Export Output: ./build/output
```

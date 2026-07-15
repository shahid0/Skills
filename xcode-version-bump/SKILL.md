---
name: xcode-version-bump
description: Bump application build and marketing versions using agvtool, and compile, archive, and sign native packages (IPAs) using xcodebuild.
---

# Xcode Version Bump & Build Pipeline (xcode-version-bump)

Use this skill to manage Apple iOS/macOS application versioning using the Apple Generic Versioning tool (`agvtool`), and automate compiling, archiving, and exporting signed application packages (IPAs) via `xcodebuild`.

## When to Trigger This Skill

Trigger this skill when:
- Setting or incrementing app marketing version strings (e.g., `1.2.3`) or build numbers (e.g., `103`).
- Preparing a project build for beta distribution (TestFlight) or release.
- Generating native archives (`.xcarchive`) and exporting signed IPAs or PKGs.
- Debugging Xcode code-signing, team IDs, provisioning profiles, and ExportOptions configurations during build steps.

## Core Rules & Best Practices

- **Apple Generic Versioning**: Ensure target projects have `VERSIONING_SYSTEM` set to `apple-generic` in their build settings before running `agvtool` commands.
- **Run in Project Directory**: `agvtool` commands must be run in the folder containing the `.xcodeproj` file.
- **Never discard working changes**: This build pipeline operates on current disk states. Never execute commands that clean or reset uncommitted files (like `git clean` or `git stash`) without explicit user permission.
- **Explicit signing options**: Always specify explicit paths to `ExportOptions.plist`, Team IDs, and target schemes. Avoid using default assumptions to prevent code-signing failures.

## Execution Workflow

### 1. Version Increment and Querying
- Check current project build and marketing versions:
  ```bash
  agvtool what-version
  agvtool what-marketing-version
  ```
- Increment the build number:
  ```bash
  agvtool bump
  ```
- Set specific versions:
  ```bash
  agvtool new-version -all <build_number>
  agvtool new-marketing-version <version_string>
  ```

### 2. Compilation and Archiving
- Build and generate the `.xcarchive` container:
  ```bash
  xcodebuild archive \
    -workspace <workspace_path> \
    -scheme <scheme_name> \
    -configuration Release \
    -archivePath <archive_destination_path>
  ```

### 3. Package Exporting
- Export the signed application package (IPA):
  ```bash
  xcodebuild -exportArchive \
    -archivePath <archive_path> \
    -exportOptionsPlist <export_options_plist_path> \
    -exportPath <output_directory_path>
  ```

## Related Files

- Build Pipeline Script: [scripts/build_pipeline.sh](scripts/build_pipeline.sh)
- Export Template: [resources/ExportOptions.plist](resources/ExportOptions.plist)
- Usage Examples: [examples/usage_examples.md](examples/usage_examples.md)
- agvtool & xcodebuild Reference: [references/agvtool_xcodebuild_ref.md](references/agvtool_xcodebuild_ref.md)

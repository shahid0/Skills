---
name: xcode-ui-snapshots
description: Automate user interface screenshot capture across multiple simulator devices, light/dark appearances, dynamic text sizes, and status bar overrides for visual regression testing or marketing.
---

# Xcode UI Snapshots (xcode-ui-snapshots)

Use this skill to automate screenshot capture of SwiftUI or Flutter screens on various iOS simulator devices under multiple display conditions (appearances, dynamic text sizes) and with a standardized status bar configuration.

## When to Trigger This Skill

Trigger this skill when:
- Designing or running visual regression tests to verify UI layout stability across code modifications.
- Generating app store screenshots or marketing visual assets at specific resolutions.
- Auditing UI layouts under accessibility settings (e.g. extreme dynamic text sizes).
- Setting up automated snapshot pipelines utilizing simulator status bar overrides.

## Core Rules & Best Practices

- **Seeded, Deterministic Content**: Screenshots must show deterministic, reproducible states. Seed mock data or use launch arguments (`--UITesting`, `--ResetState`, `--SeedMockData`) to load fixed fixture datasets rather than relying on live network data or dynamic values (like dates/times).
- **Post-Run State Restoration**: Always restore the simulator's display state upon completion (even on errors). Leaving override configurations active can corrupt subsequent testing sessions.
  ```bash
  # Reset display defaults
  xcrun simctl ui booted appearance light
  xcrun simctl ui booted content_size default
  xcrun simctl status_bar booted clear
  ```
- **Allow Sequential Booting**: When generating a matrix across different device sizes, allow the boot scripts to run sequentially rather than spinning up multiple heavy simulator instances concurrently.

## Execution Workflow

### 1. Build the Target App
- Build the app for the simulator destination:
  - **Native (iOS)**: `xcodebuild -workspace MyApp.xcworkspace -scheme MyApp -sdk iphonesimulator -derivedDataPath build_output build`
  - **Flutter**: `flutter build ios --simulator`

### 2. Configure the Matrix
- Define target devices, appearances, dynamic text sizes, and status bar settings inside `resources/matrix_config.json`.

### 3. Run the Screenshot Automation
- Execute the snapshot automation wrapper script:
  ```bash
  python3 scripts/snapshot_matrix.py \
    --config resources/matrix_config.json \
    --output-dir "./snapshots/v1"
  ```

### 4. Verify & Compare Layouts
- Perform visual regression comparison (such as via Pillow or ImageMagick) to check for text truncation, layout overlaps, or alignment issues across different appearances and text sizes.

## Related Files

- Snapshot Runner: [scripts/snapshot_matrix.py](scripts/snapshot_matrix.py)
- Matrix Config: [resources/matrix_config.json](resources/matrix_config.json)
- Usage Examples: [examples/usage_examples.md](examples/usage_examples.md)
- simctl UI Reference: [references/simctl_ui_ref.md](references/simctl_ui_ref.md)

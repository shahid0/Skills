---
name: xcode-devicectl
description: Enforce best practices when managing, querying, and automating physical Apple devices (iOS, iPadOS, tvOS, watchOS) using devicectl. Use when pairing, deploying, installing apps, launching processes, collecting logs, or diagnosing physical devices.
---

# Xcode Devicectl (xcode-devicectl)

Use this skill as the canonical standard for interacting with and automating physical iOS, iPadOS, watchOS, and tvOS devices using Xcode's `devicectl` command-line utility.

## When to Trigger This Skill

Trigger this skill whenever the user is:
- Interacting with physical Apple devices from the command line.
- Deploying, installing, or uninstalling applications on physical devices.
- Launching, terminating, or monitoring processes on physical devices.
- Collecting logs, sysdiagnose, or running diagnostics on connected devices.
- Querying device capabilities, pairing status, or list of connected hardware.
- Scripting iOS automation workflows for real devices (as opposed to simulators which use `simctl`).

## Core Rules & Best Practices

- **Always use JSON output for scripting**: The human-readable standard output of `devicectl` is not a stable API and will break under updates. Always pass the `--json-output <file>` option in scripts or automation.
- **Utilize the wrapper script**: For programmatic runs, use `scripts/devicectl_json.py` to handle the JSON generation and retrieval automatically.
- **Differentiate from Simulator automation**: Use `devicectl` only for physical devices. For simulator automation, refer to `simctl` workflows and related skills.

## Execution Workflow

### 1. Identify Connected Devices
- List all connected and paired physical devices using the wrapper script:
  ```bash
  python3 scripts/devicectl_json.py list devices
  ```
- Match by device identifier (UDID) or name to target a specific hardware target.

### 2. Perform Device Operations
- Deploy, launch, control, or diagnose the target device using the stable wrapper API:
  - **Install App**: `python3 scripts/devicectl_json.py device install app --device <id> --path <app_path>`
  - **Launch App**: `python3 scripts/devicectl_json.py device process launch --device <id> --bundle-id <bundle_id>`
  - **Collect Diagnostics**: `python3 scripts/devicectl_json.py diagnose collect sysdiagnose --device <id>`

### 3. Parse JSON Results Programmatically
- Read and parse the generated JSON file from the wrapper execution.
- Access the `result` dictionary and standard keys to determine operation success or to extract target properties.

## Related Files

- Helper Wrapper: [scripts/devicectl_json.py](scripts/devicectl_json.py)
- Apple Source Matrix: [references/apple-source-matrix.md](references/apple-source-matrix.md)
- Usage Examples: [examples/usage_examples.md](examples/usage_examples.md)

---
name: xcode-simulator-automation
description: Automate iOS Simulator lifecycles, app operations (install, launch, uninstall), coordinates spoofing, mock push notifications, and video recording.
---

# Xcode Simulator Automation (xcode-simulator-automation)

Use this skill as the canonical guide and tool reference for automating Apple iOS Simulator lifecycles, app lifecycle events, push notification mocking, GPS coordinate overrides, and recording demonstration videos.

## When to Trigger This Skill

Trigger this skill when:
- Booting, managing, or creating iOS simulator runtimes programmatically.
- Automating application installation, execution, and termination on simulators.
- Mocking push notifications using local payloads to test receiver delegates.
- Overriding simulator location settings (GPS coordinates) to simulate geofences or user travel.
- Capturing screen recording videos of simulator interactions.

## Core Rules & Best Practices

- **Never assume simulator status**: Do not guess boot states. Always use `xcrun simctl bootstatus <device> -b` to boot and block until the simulator is fully responsive.
- **Explicit authorization for runtimes**: Downloading iOS/watchOS platform runtimes involves multiple gigabytes of downloads. **Never trigger runtimes download without explicit user approval**.
- **Send push via local payloads**: Test push notifications without APNs setup by passing localized JSON payload structures directly using `xcrun simctl push`.
- **Graceful screen capture termination**: When recording simulator videos, send a `SIGINT` (kill signal -2) to stop the record process. This ensures video metadata is properly finalized, preventing file corruption.
- **Teardown on exit**: Always clean up GPS overrides, screen recording processes, and delete temporary simulator instances at the end of the session to keep developer environment states clean.

## Execution Workflow

### 1. Boot Device Runtimes
- List available runtimes and booted devices:
  ```bash
  xcrun simctl list devices | grep Booted
  ```
- Boot and wait for the target simulator:
  ```bash
  xcrun simctl bootstatus "iPhone 15" -b
  ```

### 2. Control App Lifecycles
- Deploy and control simulator application bundles:
  - **Install**: `xcrun simctl install <device> <path_to_app>`
  - **Launch**: `xcrun simctl launch <device> <bundle_id>`
  - **Terminate**: `xcrun simctl terminate <device> <bundle_id>`

### 3. Mock Location and Notifications
- **Location Override**: `xcrun simctl location <device> set <latitude>,<longitude>`
- **Push Notification**: `xcrun simctl push <device> <bundle_id> <payload_path>`

### 4. Capture Simulator Video
- Start video capture:
  ```bash
  xcrun simctl io <device> recordVideo <output_path>
  ```
- Gracefully stop by sending `SIGINT` to the recording PID.

## Related Files

- Automation Wrapper: [scripts/sim_manager.sh](scripts/sim_manager.sh)
- Payload Template: [resources/push_payload_template.json](resources/push_payload_template.json)
- Usage Examples: [examples/usage_examples.md](examples/usage_examples.md)
- simctl Commands Reference: [references/simctl_commands.md](references/simctl_commands.md)

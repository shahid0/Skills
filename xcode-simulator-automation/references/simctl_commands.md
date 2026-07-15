# Xcode Simctl Commands Reference

`simctl` is the command line utility used to control iOS, watchOS, and tvOS simulators from the macOS terminal.

## Core Commands Syntax
```bash
xcrun simctl <subcommand> [arguments]
```

## Subcommand List

| Subcommand | Description | Example |
| :--- | :--- | :--- |
| `list` | List available devices, device types, runtimes, or device pairs. | `xcrun simctl list devices` |
| `boot` | Boot a device or device pair. | `xcrun simctl boot "iPhone 15"` |
| `bootstatus` | Monitors a device and prints boot status until it finishes booting. | `xcrun simctl bootstatus booted -b` |
| `shutdown` | Shutdown a device. | `xcrun simctl shutdown booted` |
| `create` | Create a new device. | `xcrun simctl create "My iPhone" com.apple.CoreSimulator.SimDeviceType.iPhone-15` |
| `delete` | Delete specified devices, unavailable devices, or all devices. | `xcrun simctl delete unavailable` |
| `erase` | Erase a device's contents and settings (factory reset). | `xcrun simctl erase booted` |
| `install` | Install an app on a device. | `xcrun simctl install booted MyApp.app` |
| `uninstall` | Uninstall an app from a device. | `xcrun simctl uninstall booted com.example.myapp` |
| `launch` | Launch an application by identifier on a device. | `xcrun simctl launch booted com.example.myapp` |
| `terminate` | Terminate an application by identifier on a device. | `xcrun simctl terminate booted com.example.myapp` |
| `listapps` | Show the installed applications on the simulator. | `xcrun simctl listapps booted` |
| `appinfo` | Show information about an installed application. | `xcrun simctl appinfo booted com.example.myapp` |
| `get_app_container` | Print the container path of the installed app. | `xcrun simctl get_app_container booted com.example.myapp` |
| `push` | Send a simulated remote push notification. | `xcrun simctl push booted com.example.myapp push.json` |
| `location` | Control or override a device's simulated location. | `xcrun simctl location booted set 37.7749,-122.4194` |
| `io` | Perform I/O operations (screenshot, record video, screen settings). | `xcrun simctl io booted recordVideo video.mp4` |
| `privacy` | Grant, revoke, or reset privacy permissions (photos, camera, etc). | `xcrun simctl privacy booted grant photos com.example.myapp` |
| `status_bar` | Set or clear status bar overrides (time, battery, network bars). | `xcrun simctl status_bar booted override --time "9:41"` |
| `openurl` | Open a URL or deep link in the simulator. | `xcrun simctl openurl booted myapp://profile` |
| `pbcopy` | Copy standard input onto the device pasteboard. | `echo "Hello" \| xcrun simctl pbcopy booted` |
| `pbpaste` | Print the device pasteboard contents. | `xcrun simctl pbpaste booted` |
| `addmedia` | Add photos, videos, or contacts to the simulator library. | `xcrun simctl addmedia booted photo.jpg` |
| `getenv` | Print an environment variable from a running device. | `xcrun simctl getenv booted PATH` |
| `spawn` | Spawn a process in the device environment. | `xcrun simctl spawn booted log show` |
| `keychain` | Manipulate a device's keychain. | `xcrun simctl keychain booted add-internet-password ...` |
| `diagnose` | Collect diagnostic information and logs. | `xcrun simctl diagnose` |
| `runtime` | Manage simulator runtimes (delete, list, etc.). | `xcrun simctl runtime list` |
| `ui` | Get or set UI options (e.g. appearance light/dark mode). | `xcrun simctl ui booted appearance dark` |

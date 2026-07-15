# Apple Source Matrix

## Primary sources

- Xcode CLI tools overview: https://developer.apple.com/documentation/xcode/xcode-command-line-tool-reference
- Command-line tool selection and `devicectl` example: https://developer.apple.com/documentation/xcode/configuring-command-line-tools-settings

## First-party CLI evidence

Shipped `devicectl` help states:

- JSON output written to a user-provided file is the only supported scripting interface.
- Subcommands cover `device`, `diagnose`, `list`, and `manage`.
- Device-facing operations include install, notification, orientation, process control, reboot, uninstall, and sysdiagnose.

## Grounded claims this skill may rely on

- `devicectl` is an Xcode-only CLI surface for Core Device functionality.
- Real-device automation should be built around JSON output files, not terminal text.


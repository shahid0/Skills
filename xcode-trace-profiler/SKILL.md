---
name: xcode-trace-profiler
description: Record low-level performance traces using xctrace, export them to structured XML/JSON format, and identify CPU, memory, and rendering bottlenecks.
---

# Xcode Trace Profiler (xcode-trace-profiler)

Use this skill to record, export, and analyze performance trace documents for SwiftUI and Flutter applications running on macOS or iOS targets using Xcode's `xctrace` command-line utility.

## When to Trigger This Skill

Trigger this skill when:
- Investigating main-thread blocks, UI frame drops, rendering stutters, or animation hitches.
- Counting SwiftUI view body evaluation frequency or auditing thread concurrency.
- Measuring CPU hotspot execution paths in native code or Dart isolates.
- Profiling memory allocations and checking for memory leaks in running applications.
- Automating performance regressions tests using script-driven `xctrace` profiling.

## Core Rules & Best Practices

- **Simulator app launching limitation**: You cannot launch iOS Simulator apps directly using `xctrace record --launch`. You must first boot the simulator, launch the app via `simctl launch`, retrieve the app's PID, and then run `xctrace record --attach <PID>`.
- **Target release builds**: Always profile Flutter and native iOS targets built in `profile` or `release` configurations. Profiling debug builds will yield skewed performance statistics due to JIT and debugging overhead.
- **Leaks require separate templates**: Time Profiling template tracks CPU execution time. Memory leak checking must be run via the `Leaks` or `Allocations` templates.
- **Table of contents schema matching**: `xctrace` outputs binary files. To parse them, export the table of contents (`--toc`) first to identify the XML xpath schema before doing targeted data exports.

## Execution Workflow

### 1. Launch App and Retrieve PID
- Boot simulator and start your application:
  ```bash
  xcrun simctl launch booted <bundle_id>
  ```
- Retrieve the process ID (PID):
  ```bash
  xcrun simctl spawn booted launchctl list | grep <bundle_id>
  ```

### 2. Record Performance Trace
- Run `xctrace` by attaching to the PID:
  ```bash
  xcrun xctrace record \
    --template "Time Profiler" \
    --attach <PID> \
    --time-limit 15s \
    --output recording.trace
  ```

### 3. Export to XML
- Generate table of contents schema structure:
  ```bash
  xcrun xctrace export --input recording.trace --toc
  ```
- Export specific data tables using the schema XPath:
  ```bash
  xcrun xctrace export \
    --input recording.trace \
    --xpath '/trace-toc/run[@number="1"]/data/table[@schema="time-profile"]' \
    --output data.xml
  ```

### 4. Analyze CPU/Memory Data
- Use the script analyzer tool to parse XML data and identify heavy calls:
  ```bash
  python3 scripts/trace_analyzer.py --input-trace recording.trace --top 15
  ```

## Related Files

- Trace Analyzer: [scripts/trace_analyzer.py](scripts/trace_analyzer.py)
- Default Templates: [resources/default_templates.json](resources/default_templates.json)
- Usage Examples: [examples/usage_examples.md](examples/usage_examples.md)
- xctrace Reference: [references/xctrace_templates.md](references/xctrace_templates.md)

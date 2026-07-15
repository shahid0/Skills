# Profiling and Analysis Usage Examples

This guide contains common command line examples for recording, exporting, and analyzing performance traces using `xctrace` and the `trace_analyzer.py` tool.

## Using `xctrace` Directly

### 1. Record CPU Profile of a Running Process
To attach to an active process (e.g., PID `1234` or process name `MySwiftUIApp`) and capture CPU hotspots for 15 seconds:
```bash
xcrun xctrace record --template "Time Profiler" --attach 1234 --time-limit 15s --output app_profile.trace
```

### 2. Record App Launch and Pre-Main Performance
To launch a compiled application bundle and capture allocations during startup:
```bash
xcrun xctrace record --template "Allocations" --launch -- /path/to/MySwiftUIApp.app
```

### 3. List Available Profiling Templates
```bash
xcrun xctrace list templates
```

### 4. Export Table of Contents (To Detect Schema Name)
```bash
xcrun xctrace export --input app_profile.trace --toc --output toc.xml
```

### 5. Export specific schema to XML (e.g., `time-profile`)
```bash
xcrun xctrace export --input app_profile.trace \
  --xpath '/trace-toc/run[@number="1"]/data/table[@schema="time-profile"]' \
  --output time_profile.xml
```

---

## Using `trace_analyzer.py`

The wrapper script `trace_analyzer.py` automates the record-export-analyze pipeline.

### 1. Record and Analyze a Command Immediately
Record CPU usage of a command (e.g., a Python compilation script or executable) and print the top CPU-consuming functions:
```bash
python scripts/trace_analyzer.py --template "Time Profiler" --launch -- /usr/bin/python3 -c "import time; time.sleep(1)"
```

### 2. Profile a Running SwiftUI/Flutter App by PID/Name
Attach to a running process named `MyFlutterApp` for 10 seconds, export the profile, and analyze it:
```bash
python scripts/trace_analyzer.py --attach MyFlutterApp --time-limit 10s --output profile.trace
```

### 3. Analyze an Existing `.trace` File
If you have already recorded a `.trace` file using Xcode Instruments or `xctrace`, you can analyze it directly:
```bash
python scripts/trace_analyzer.py --input-trace my_app_recording.trace --top 30
```

### 4. Output Results in JSON Format
For programmatic integration (e.g., CI/CD checks or dashboards):
```bash
python scripts/trace_analyzer.py --input-trace my_app_recording.trace --json
```

### 5. Limit Analysis to a Custom XPath
If you want to extract a specific run or table manually:
```bash
python scripts/trace_analyzer.py --input-trace profile.trace \
  --xpath '/trace-toc/run[@number="2"]/data/table[@schema="time-profile"]'
```

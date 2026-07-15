# Xcode Devicectl Usage Examples

This document provides examples for automating physical Apple devices (iOS, iPadOS, tvOS, watchOS) using `devicectl`.

## Core Concept: JSON Scripting Interface

Apple explicitly states that the human-readable standard output of `devicectl` is unstable and subject to change. For scripting and automation, you **must** use the JSON output file interface by passing the `--json-output <path>` flag.

To simplify this, a helper wrapper `scripts/devicectl_json.py` is provided to run `devicectl` commands while automatically writing output to a temporary JSON file and outputting its location.

---

## 1. Listing Connected Devices

Find all physical devices connected to the host (via USB or network).

### Using the Python Wrapper
```bash
python3 scripts/devicectl_json.py list devices
```

### Raw Command
```bash
xcrun devicectl list devices --json-output /tmp/devices.json
```

### Parsing the Output
The generated JSON contains a `result` dictionary with a list of devices under `devices`:
```json
{
  "result": {
    "devices": [
      {
        "identifier": "00008101-001C34A90A28001E",
        "connectionProperties": {
          "transportType": "wired"
        },
        "deviceProperties": {
          "name": "Work iPhone",
          "osBuildUpdate": "21F79",
          "osVersionNumber": "17.5.1",
          "platform": "ios"
        }
      }
    ]
  }
}
```

---

## 2. Installing an Application (.app / .ipa)

Install a built app bundle onto a targeted physical device.

### Using the Python Wrapper
```bash
python3 scripts/devicectl_json.py device install app --device "00008101-001C34A90A28001E" --path build/Build/Products/Debug-iphoneos/MyApp.app
```

### Raw Command
```bash
xcrun devicectl device install app --device "00008101-001C34A90A28001E" --json-output /tmp/install_result.json build/Build/Products/Debug-iphoneos/MyApp.app
```

---

## 3. Launching an Application

Launch an installed app by its bundle identifier on the physical device.

### Using the Python Wrapper
```bash
python3 scripts/devicectl_json.py device process launch --device "00008101-001C34A90A28001E" --bundle-id com.example.myapp
```

### Raw Command
```bash
xcrun devicectl device process launch --device "00008101-001C34A90A28001E" --json-output /tmp/launch_result.json com.example.myapp
```

---

## 4. Collecting Sysdiagnose

Collect a diagnostic log from the targeted physical device.

### Using the Python Wrapper
```bash
python3 scripts/devicectl_json.py diagnose collect sysdiagnose --device "00008101-001C34A90A28001E"
```

### Raw Command
```bash
xcrun devicectl diagnose collect sysdiagnose --device "00008101-001C34A90A28001E" --json-output /tmp/sysdiagnose_result.json
```

---

## 5. Scripted JSON Parsing (Python Example)

Here is a Python snippet showing how to run `devicectl` via the wrapper and programmatically parse the JSON result:

```python
import json
import subprocess
import tempfile

def get_connected_iphones():
    with tempfile.NamedTemporaryFile(suffix=".json") as tmp:
        # Run devicectl to output to a temporary JSON file
        cmd = [
            "xcrun", "devicectl",
            "--json-output", tmp.name,
            "list", "devices"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError("Failed to list devices via devicectl")
            
        # Parse the JSON output
        data = json.load(tmp)
        
        devices = data.get("result", {}).get("devices", [])
        iphones = [
            d for d in devices 
            if d.get("deviceProperties", {}).get("platform") == "ios"
        ]
        return iphones

# Example usage
for phone in get_connected_iphones():
    print(f"Found iPhone: {phone['deviceProperties']['name']} ({phone['identifier']})")
```

# Sim-Automation Usage Examples

This guide provides examples for simulating push notifications, overriding GPS locations, and recording screens using the `sim_manager.sh` script or raw `simctl` commands.

---

## 1. Booting and Setup

Boot a device (e.g. "iPhone 15") and wait for it to be fully booted.

```bash
./scripts/sim_manager.sh boot "iPhone 15"
```

---

## 2. Mock Push Notifications

Send a simulated remote push notification to a booted simulator.

### Using the script:
```bash
./scripts/sim_manager.sh push booted com.example.myapp ./resources/push_payload_template.json
```

### Using raw `simctl` command:
```bash
xcrun simctl push booted com.example.myapp ./resources/push_payload_template.json
```

---

## 3. Override GPS Coordinates

Set the simulator's location to specific GPS coordinates.

### Using the script (set to San Francisco):
```bash
./scripts/sim_manager.sh location booted set 37.7749 -122.4194
```

### Using raw `simctl` command:
```bash
xcrun simctl location booted set 37.7749,-122.4194
```

### Clearing GPS Overrides:
```bash
./scripts/sim_manager.sh location booted clear
```

---

## 4. Screen Recording (MP4)

Record the simulator screen directly to an MP4 video file.

### Recording for a specific duration (e.g., 10 seconds):
```bash
./scripts/sim_manager.sh record booted output.mp4 10
```

### Recording interactively:
```bash
# This will record until you press Ctrl+C
./scripts/sim_manager.sh record booted interactive_demo.mp4
```

---

## 5. App Lifecycle Workflow

A complete pipeline to boot, install, launch, test (via push/location), and terminate:

```bash
# 1. Boot iPhone 15
./scripts/sim_manager.sh boot "iPhone 15"

# 2. Install App
./scripts/sim_manager.sh install booted ./MyApp.app

# 3. Launch App with custom arguments
./scripts/sim_manager.sh launch booted com.example.myapp --verbose --debug

# 4. Set Location
./scripts/sim_manager.sh location booted set 40.7128 -74.0060

# 5. Push Notification
./scripts/sim_manager.sh push booted com.example.myapp ./resources/push_payload_template.json

# 6. Terminate App
./scripts/sim_manager.sh terminate booted com.example.myapp
```

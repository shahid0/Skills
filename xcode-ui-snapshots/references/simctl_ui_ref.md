# Apple simctl UI and Status Bar Command Reference

This document catalogs the command-line options and parameters for modifying the simulator appearance, content size, dynamic contrast, and status bar status.

---

## 1. simctl ui

Get or Set UI configurations on booted simulators.

### Usage
```bash
xcrun simctl ui <device> <option> [<arguments>]
```
Replace `<device>` with a specific simulator UDID, name, or `"booted"`.

### Supported Options

#### A. Appearance (`appearance`)
Modify the light or dark system theme.
- **Get theme status:**
  ```bash
  xcrun simctl ui <device> appearance
  ```
- **Set theme:**
  ```bash
  xcrun simctl ui <device> appearance light
  xcrun simctl ui <device> appearance dark
  ```

#### B. Increase Contrast (`increase_contrast`)
Enable/disable High Contrast accessibility features.
- **Get contrast status:**
  ```bash
  xcrun simctl ui <device> increase_contrast
  ```
- **Set contrast mode:**
  ```bash
  xcrun simctl ui <device> increase_contrast enabled
  xcrun simctl ui <device> increase_contrast disabled
  ```

#### C. Preferred Content Size / Dynamic Type (`content_size`)
Change the user's Dynamic Type size category for typography scaling.
- **Get preferred size:**
  ```bash
  xcrun simctl ui <device> content_size
  ```
- **Set size category:**
  ```bash
  xcrun simctl ui <device> content_size <size_category>
  ```
- **Adjust size relative to current:**
  ```bash
  xcrun simctl ui <device> content_size increment
  xcrun simctl ui <device> content_size decrement
  ```

##### Valid Content Sizes
- **Standard Range:**
  - `extra-small`
  - `small`
  - `medium`
  - `large`
  - `extra-large`
  - `extra-extra-large`
  - `extra-extra-extra-large`
- **Accessibility/Extended Range:**
  - `accessibility-medium`
  - `accessibility-large`
  - `accessibility-extra-large`
  - `accessibility-extra-extra-large`
  - `accessibility-extra-extra-extra-large`

---

## 2. simctl status_bar

Overriding simulator status bar components (clock, network type, signal strength, battery status) to maintain unified marketing screenshots or clean visual baselines.

### Usage
```bash
xcrun simctl status_bar <device> [list | clear | override <arguments>]
```

### Supported Operations

#### A. List Current Overrides
```bash
xcrun simctl status_bar <device> list
```

#### B. Clear Overrides (Reset to system default)
```bash
xcrun simctl status_bar <device> clear
```

#### C. Set Overrides (`override`)
Apply specific visual overrides to status bar components. Combine one or more flags below:

##### Flags:
- `--time <string>`
  Set the device clock time (e.g. `"09:41"`). Passing a valid ISO date string also modifies the simulator system date.
- `--dataNetwork <type>`
  Modify the cellular carrier data icon. Supported values:
  `hide`, `wifi`, `3g`, `4g`, `lte`, `lte-a`, `lte+`, `5g`, `5g+`, `5g-uwb`, `5g-uc`
- `--wifiMode <mode>`
  Specify status of the Wi-Fi icon. Supported values:
  `searching`, `failed`, `active`
- `--wifiBars <int>`
  Specify the number of Wi-Fi indicator signal bars (`0` to `3`).
- `--cellularMode <mode>`
  Specify the cellular signal mode. Supported values:
  `notSupported`, `searching`, `failed`, `active`
- `--cellularBars <int>`
  Specify the cellular signal indicator bars (`0` to `4`).
- `--operatorName <string>`
  Customize the carrier operator name label. Use `""` for empty.
- `--batteryState <state>`
  Set battery power status. Supported values:
  `charging`, `charged`, `discharging`
- `--batteryLevel <int>`
  Set battery percentage integer (`0` to `100`).

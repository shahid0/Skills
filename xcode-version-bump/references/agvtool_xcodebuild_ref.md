# Xcode Versioning & build pipeline Reference

This reference covers configurations, build settings, tools, and troubleshooting steps related to Apple Generic Versioning, `agvtool`, and `xcodebuild` distribution archiving and signing.

---

## 1. APPLE GENERIC VERSIONING

Xcode supports two main build settings for version management:
- **`MARKETING_VERSION`** (Bundle Versions Short / `CFBundleShortVersionString`):
  Represented as a semantic version (e.g., `1.0.0`, `2.3.1`). This is the public-facing version shown to users in the App Store.
- **`CURRENT_PROJECT_VERSION`** (Bundle Version / `CFBundleVersion`):
  An integer or decimal (e.g., `1`, `42`, `1002`). This is the internal build number used to distinguish builds of the same marketing version.

### Required Build Settings
To utilize `agvtool`, your project's `.xcodeproj` must be configured with the following build settings:

| Build Setting | Value | Description |
| :--- | :--- | :--- |
| `VERSIONING_SYSTEM` | `apple-generic` | Configures the project to use Apple's Generic Versioning system. |
| `CURRENT_PROJECT_VERSION` | e.g. `1` | The starting integer for build versions. |
| `MARKETING_VERSION` | e.g. `1.0.0` | The starting marketing version. |

---

## 2. agvtool MECHANICS

`agvtool` reads your Xcode project file (`project.pbxproj`) and updates the build settings or `Info.plist` files of your targets.

### Key Rules and Requirements
1. **Directory Location**: You must run `agvtool` from the directory containing your project's `.xcodeproj` file.
2. **plist Configuration**: If `agvtool` cannot locate your `Info.plist` or target configurations, verify that the `INFOPLIST_FILE` build setting correctly points to the path of your targets' `Info.plist`.
3. **Multi-Target Synchrony**: When using `agvtool bump`, it increments the `CURRENT_PROJECT_VERSION` setting at the project level, which propagates to all targets referencing it.

### Commands Quick-Reference
- **Check current versions**:
  ```bash
  agvtool what-version
  agvtool what-marketing-version
  ```
- **Increment build number by 1**:
  ```bash
  agvtool bump
  ```
- **Set specific build version**:
  ```bash
  agvtool new-version -all <build_number>
  ```
- **Set specific marketing version**:
  ```bash
  agvtool new-marketing-version <version_string>
  ```

---

## 3. xcodebuild ARCHIVING & EXPORTING

The Xcode command-line tool `xcodebuild` generates archives and signed IPAs using a two-step process.

### Step 1: Archiving
Compiles all targets under a selected scheme and packages them into a `.xcarchive` directory containing the compiled binaries, debug symbols (dSYMs), and package metadata.
```bash
xcodebuild archive \
  -workspace MyApp.xcworkspace \
  -scheme MyAppScheme \
  -configuration Release \
  -archivePath build/MyApp.xcarchive
```

### Step 2: Exporting
Unpacks the `.xcarchive`, signs the binaries with specified provisioning profiles and certificates, and packs them into a `.ipa` file. This step requires an `ExportOptions.plist` configuration file.
```bash
xcodebuild -exportArchive \
  -archivePath build/MyApp.xcarchive \
  -exportOptionsPlist ExportOptions.plist \
  -exportPath build/output
```

---

## 4. ExportOptions.plist KEY CONFIGURATIONS

The export options plist dictates how the final IPA is packaged and signed. Below are the essential keys:

- **`method`** (String, Required):
  Defines the distribution target.
  - `app-store`: For App Store Connect production uploads.
  - `ad-hoc`: For distribution to registered test devices.
  - `enterprise`: For In-House enterprise distribution.
  - `development`: For testing/debugging builds.
  - `developer-id`: For macOS Developer ID distribution.
- **`signingStyle`** (String, Optional):
  - `automatic`: Let Xcode resolve signing assets.
  - `manual`: Explicitly map profiles.
- **`provisioningProfiles`** (Dictionary, Required for manual signing):
  Maps Bundle IDs to Provisioning Profile names or UUIDs:
  ```xml
  <key>provisioningProfiles</key>
  <dict>
      <key>com.company.app</key>
      <string>Company App Store Profile</string>
  </dict>
  ```
- **`signingCertificate`** (String, Optional for manual signing):
  The certificate name or SHA-1 hash to use (e.g., `"Apple Distribution"` or `"Apple Development"`).

---

## 5. TROUBLESHOOTING COMMON ERRORS

### "agvtool: error: count not find Info.plist"
- **Cause**: The project versioning settings or target definitions contain an incorrect or relative path to target `Info.plist` files that `agvtool` cannot parse.
- **Solution**: Open Xcode, verify that the "Info.plist File" (`INFOPLIST_FILE`) path under Build Settings is relative to the project directory and correctly formatted.

### "Code signing blocked: No profile found matching..."
- **Cause**: The certificate or profile listed in `ExportOptions.plist` doesn't match the bundle identifier, or doesn't exist on the host machine.
- **Solution**: Run `security find-identity -p codesigning -v` to list available certificates, and ensure your provision profile is installed under `./Library/MobileDevice/Provisioning Profiles/`.

### "xcodebuild: error: The scheme 'MyApp' is not shared"
- **Cause**: The scheme has not been marked as "Shared" in Xcode's "Manage Schemes" sheet.
- **Solution**: Open the project in Xcode, navigate to `Product -> Scheme -> Manage Schemes...`, check the "Shared" box next to your scheme, and commit the resulting `.xcscheme` file to git.

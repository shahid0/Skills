# Custom Snapshot Matrix Usage Examples

This guide contains examples for executing screenshot matrices and setting up visual regression testing or comparison checks.

---

## 1. Quick Capture (Command Line)

You can run the script directly from the terminal by providing command-line overrides for your app:

```bash
# Run on currently booted simulator, capturing light and dark appearances
python3 /Users/macbookpro/.agents/skills/ui-snapshot-matrix/scripts/snapshot_matrix.py \
  --app-bundle-id "com.example.MyApp" \
  --appearances light dark \
  --content-sizes medium accessibility-large \
  --output-dir "./matrix_screenshots"
```

---

## 2. Config File Driven Capture (Recommended)

Run the script by referencing the predefined JSON config file. This ensures consistent parameters are shared across the team:

```bash
python3 /Users/macbookpro/.agents/skills/ui-snapshot-matrix/scripts/snapshot_matrix.py \
  --config /Users/macbookpro/.agents/skills/ui-snapshot-matrix/resources/matrix_config.json \
  --output-dir "./v1_releases"
```

---

## 3. Visual Regression & Comparison Checks

To run comparative visual audits between two version builds (e.g. `v1_releases` vs. `v2_releases`), you can use standard image comparison commands.

### Option A: ImageMagick `compare` Command
If you have ImageMagick installed, use the `compare` command to highlight the differences as a red/magenta overlay:

```bash
# Compare light mode, standard size on iPhone 17 Pro
compare \
  v1_releases/screenshot_iPhone_17_Pro_light_medium.png \
  v2_releases/screenshot_iPhone_17_Pro_light_medium.png \
  diffs/diff_iPhone_17_Pro_light_medium.png
```

If the images match perfectly, the command exits with `0`. If they differ, it exits with `1`.

### Option B: Python-based Pixel-by-Pixel Comparator
A simple Python script using `Pillow` can compare the images programmatically:

```python
#!/usr/bin/env python3
import sys
from PIL import Image, ImageChops

def compare_images(img1_path, img2_path, diff_path):
    img1 = Image.open(img1_path).convert("RGB")
    img2 = Image.open(img2_path).convert("RGB")
    
    if img1.size != img2.size:
        print(f"Size mismatch: {img1.size} vs {img2.size}")
        return False
        
    diff = ImageChops.difference(img1, img2)
    bbox = diff.getbbox()
    
    if bbox:
        print(f"Visual differences detected! Saving diff to {diff_path}")
        diff.save(diff_path)
        return False
    else:
        print("Images match perfectly.")
        return True

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: compare.py <img1> <img2> <diff_output>")
        sys.exit(1)
    
    success = compare_images(sys.argv[1], sys.argv[2], sys.argv[3])
    sys.exit(0 if success else 1)
```

---

## 4. Script Shell Integration (CI/CD)

Integrate this into an Xcode post-build action or local git pre-commit/pre-push script:

```bash
#!/bin/bash
set -e

echo "Building app for simulator target..."
xcodebuild -workspace MyApp.xcworkspace \
           -scheme MyApp \
           -sdk iphonesimulator \
           -derivedDataPath build_output \
           build

echo "Installing app onto booted simulator..."
xcrun simctl install booted build_output/Build/Products/Debug-iphonesimulator/MyApp.app

echo "Running snapshot matrix..."
python3 /Users/macbookpro/.agents/skills/ui-snapshot-matrix/scripts/snapshot_matrix.py \
  --app-bundle-id "com.example.MyApp" \
  --config /Users/macbookpro/.agents/skills/ui-snapshot-matrix/resources/matrix_config.json \
  --output-dir "./snapshots/latest"
```

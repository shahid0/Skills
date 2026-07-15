---
name: swift-typed-assets
description: Enforce best practices for referencing and loading asset catalog resources (images, colors) in Swift, SwiftUI, UIKit, AppKit, or Objective-C. Trigger when loading images/colors, referencing assets, adding new assets, or auditing asset resources (ColorResource, ImageResource).
---

# Swift Typed Assets (swift-typed-assets)

Use this skill as the canonical standard for loading and referencing image and color assets in Apple framework projects. It enforces compiler-checked typed resources (`ImageResource` and `ColorResource`) over unsafe, error-prone raw strings.

## When to Trigger This Skill

Trigger this skill whenever the user is:
- Loading or referencing images and colors in Swift, SwiftUI, UIKit, AppKit, or Objective-C.
- Adding new color or image assets to `.xcassets` catalogs and referencing them in code.
- Auditing, reviewing, or refactoring asset usage patterns.
- Migrating legacy string-based asset lookups (e.g., `UIImage(named: "logo")`, `Color("primary")`) to compiler-checked typed resources.
- Configuring Xcode build settings related to asset symbols.

## Core Rules & Best Practices

- **Never use raw strings for asset lookups** (e.g., `Image("name")` or `UIColor(named: "name")`) if the project uses Xcode 15+. Always prefer compiler-checked typed resource initializers.
- **Ensure assets exist**: Always confirm the asset is present in the `.xcassets` catalog before referencing its generated symbol name in code.
- **Direct symbol extensions** (e.g., `Color.brandBlue` or `UIImage.avatarIcon`) require `ASSETCATALOG_COMPILER_GENERATE_SWIFT_ASSET_SYMBOL_EXTENSIONS` to be enabled (`YES`) in the target's build settings.
- **Objective-C support**: In Objective-C targets, import `#import "GeneratedAssetSymbols.h"` and use the generated `ACImageName` and `ACColorName` string constant macros.

## Execution Workflow

### 1. Verify Asset Symbols Settings
- Verify that asset symbol generation is enabled in the project (it is on by default unless `ASSETCATALOG_COMPILER_GENERATE_ASSET_SYMBOLS=NO` is set).
- Check if direct symbol extensions are enabled in the build configuration if direct extensions are desired.

### 2. Implement Using Resource Initializers (Canonical Way)
- Use the typed initializer forms when referencing colors and images:
  - **SwiftUI**: `Image(.myImage)`, `Color(.myColor)`
  - **UIKit**: `UIImage(resource: .myImage)`, `UIColor(resource: .myColor)`
  - **AppKit**: `NSImage(resource: .myImage)`, `NSColor(resource: .myColor)`
  - **Objective-C**: Import `GeneratedAssetSymbols.h` and use `ACImageNameMyImage` or `ACColorNameMyColor`.

### 3. Scan and Refactor Legacy Code
- Use the helper script to identify legacy string-based lookups that should be updated to typed resources:
  ```bash
  python3 scripts/scan_typed_asset_usage.py <project-root>
  ```
- Refactor the findings to use the resource initializers.

### 4. Verify & Build
- Verify the project builds without errors.
- Ensure appearance-sensitive (light/dark mode) and localized assets are preserved correctly.

## Related Files

- Helper Scanner: [scripts/scan_typed_asset_usage.py](scripts/scan_typed_asset_usage.py)
- Apple Source Matrix: [references/apple-source-matrix.md](references/apple-source-matrix.md)
- Usage Examples: [examples/migration_examples.md](examples/migration_examples.md)

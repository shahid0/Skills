# Swift Typed Assets Migration Examples

This document provides before-and-after examples for migrating from string-based asset lookups to compiler-checked typed resources (`ColorResource` and `ImageResource`).

---

## 1. SwiftUI

SwiftUI supports typed resource lookups natively. You can pass the generated resources directly into the `Image` and `Color` initializers.

### Images

**Before (String-based):**
```swift
Image("profile-avatar")
Image("action_send")
```

**After (Compiler-checked):**
```swift
Image(.profileAvatar)
Image(.actionSend)
```

### Colors

**Before (String-based):**
```swift
Color("brand-primary")
Color("status-active")
```

**After (Compiler-checked):**
```swift
Color(.brandPrimary)
Color(.statusActive)
```

---

## 2. UIKit

UIKit uses the `resource` parameter label on initializers to distinguish typed resource loading.

### UIImages

**Before (String-based):**
```swift
let avatar = UIImage(named: "profile-avatar")
let sendIcon = UIImage(named: "action_send")
```

**After (Compiler-checked):**
```swift
let avatar = UIImage(resource: .profileAvatar)
let sendIcon = UIImage(resource: .actionSend)
```

### UIColors

**Before (String-based):**
```swift
let primaryColor = UIColor(named: "brand-primary")
let activeColor = UIColor(named: "status-active")
```

**After (Compiler-checked):**
```swift
let primaryColor = UIColor(resource: .brandPrimary)
let activeColor = UIColor(resource: .statusActive)
```

---

## 3. AppKit

AppKit supports resource initializers similar to UIKit.

### NSImages

**Before (String-based):**
```swift
let avatar = NSImage(named: "profile-avatar")
```

**After (Compiler-checked):**
```swift
let avatar = NSImage(resource: .profileAvatar)
```

### NSColors

**Before (String-based):**
```swift
let primaryColor = NSColor(named: "brand-primary")
```

**After (Compiler-checked):**
```swift
let primaryColor = NSColor(resource: .brandPrimary)
```

---

## 4. Objective-C

Xcode generates a C-compatible header containing symbol string constants.

To use them:
1. Import `#import "GeneratedAssetSymbols.h"`.
2. Use the generated `ACImageName` and `ACColorName` macro definitions.

**Before:**
```objc
UIImage *avatar = [UIImage imageNamed:@"profile-avatar"];
UIColor *primaryColor = [UIColor colorNamed:@"brand-primary"];
```

**After:**
```objc
#import "GeneratedAssetSymbols.h"

UIImage *avatar = [UIImage imageNamed:ACImageNameProfileAvatar];
UIColor *primaryColor = [UIColor colorNamed:ACColorNameBrandPrimary];
```

---

## 5. Direct Symbol Extensions (Opt-in)

If the build setting `ASSETCATALOG_COMPILER_GENERATE_SWIFT_ASSET_SYMBOL_EXTENSIONS` is enabled, Xcode generates direct static extensions on `Color`, `UIImage`, etc.

**After (With Extensions Enabled):**
```swift
// SwiftUI
let background: Color = .brandPrimary

// UIKit
let avatarView = UIImageView(image: .profileAvatar)
```

> [!WARNING]
> Do not use direct symbol extensions unless you are certain the `ASSETCATALOG_COMPILER_GENERATE_SWIFT_ASSET_SYMBOL_EXTENSIONS` build setting is set to `YES`. Otherwise, the code will fail to compile.

# Apple Source Matrix

## Primary sources

- Xcode 15 release notes asset-symbol section: https://developer.apple.com/documentation/xcode-release-notes/xcode-15-release-notes
- `ColorResource`: https://developer.apple.com/documentation/developertoolssupport/colorresource
- `ImageResource`: https://developer.apple.com/documentation/developertoolssupport/imageresource
- `UIColor.init(resource:)`: https://developer.apple.com/documentation/uikit/uicolor/init(resource:)
- `UIImage.init(resource:)`: https://developer.apple.com/documentation/uikit/uiimage/init(resource:)
- `NSColor.init(resource:)`: https://developer.apple.com/documentation/appkit/nscolor/init(resource:)
- `SwiftUI.Image.init(_:)`: https://developer.apple.com/documentation/swiftui/image/init(_:)

## Grounded claims this skill may rely on

- Xcode 15 generates Swift and Objective-C symbols for each color and image in an asset catalog.
- Swift asset symbols are static properties on `ColorResource` and `ImageResource`.
- Apple's Xcode 15 release notes explicitly show `Color(.spaceGray)`, `UIColor(resource: .spaceGray)`, `NSColor(resource: .spaceGray)`, `Image(.appleLogo)`, `UIImage(resource: .appleLogo)`, and `NSImage(resource: .appleLogo)`.
- Direct symbol extensions such as `Color.spaceGray` and `UIImage.appleLogo` require the opt-in build setting `ASSETCATALOG_COMPILER_GENERATE_SWIFT_ASSET_SYMBOL_EXTENSIONS=YES`.
- Objective-C asset symbols are provided as string constants in `GeneratedAssetSymbols.h`.
- Asset symbols are enabled by default unless `ASSETCATALOG_COMPILER_GENERATE_ASSET_SYMBOLS=NO`.


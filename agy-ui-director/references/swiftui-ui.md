# SwiftUI UI Playbook

Use this playbook when generating or refining iOS/SwiftUI user interfaces.

---

## 1. File Placement & Architecture

Maintain a clean separation of concerns and build modular systems rather than one-off screens:
- **Feature Screen:** `Features/<Feature>/Views/<ScreenName>.swift`
- **Feature Components:** `Features/<Feature>/Views/Component/<ComponentName>.swift`
- **Reusable UI Components:** `DesignSystem/Components/<ComponentName>.swift`
- **Design Tokens/Theme:** `DesignSystem/Theme/<TokenName>.swift`
- **Color Assets:** `Assets.xcassets/<ColorToken>.colorset` (accessed via resource compiler keys)

Enforce **one primary Swift type per file**, naming the file after the primary declaration.

---

## 2. Mathematical Determinism & Proportional Scaling

To prevent loose, guessing-game layout structures, use mathematical proportions mapped from a defined **Base Design Canvas Size** (e.g. Width `393` / Height `852` pt):

### A. Dynamic Scaling in Viewports
Scale view coordinates proportionally relative to the reference base screen width using container frames or local measurements:
```swift
struct ProportionalLayoutView: View {
    var body: some View {
        GeometryReader { geometry in
            let screenWidth = geometry.size.width
            // Calculate a card width representing exactly 85% of the screen
            let cardWidth = screenWidth * 0.85
            // Scale a base padding of 24pt relative to a 393pt base canvas width
            let adaptivePadding = (screenWidth / 393.0) * 24.0
            
            VStack(spacing: adaptivePadding) {
                RoundedRectangle(cornerRadius: outerCardRadius)
                    .fill(.ultraThinMaterial)
                    .frame(width: cardWidth, height: 160)
            }
            .padding(.horizontal, adaptivePadding)
        }
    }
}
```

### B. Nested Corner Radii Math
Maintain shape harmony by computing nested radii mathematically: `OuterRadius = InnerRadius + PaddingOffset`. This ensures elements fit perfectly inside their cards:
```swift
let outerCardRadius: CGFloat = 24.0
let cardPadding: CGFloat = 16.0
let innerElementRadius: CGFloat = outerCardRadius - cardPadding // Resolves to 8.0
```

---

## 3. Reusable Visual Assets & Layout Snippets

### A. Tactile Press Feedback (Squishy ButtonStyle)
All primary actions must utilize a custom button style to scale down on tap:
```swift
struct SquishyButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .scaleEffect(configuration.isPressed ? 0.95 : 1.0)
            .animation(.spring(response: 0.2, dampingFraction: 0.6), value: configuration.isPressed)
    }
}

extension ButtonStyle where Self == SquishyButtonStyle {
    static var squishy: SquishyButtonStyle { SquishyButtonStyle() }
}
```

### B. Premium Depth (Layered Tactile Shadow)
Stack soft, low-opacity shadows for a highly premium floating effect:
```swift
extension View {
    func premiumCardShadow() -> some View {
        self
            .shadow(color: Color.black.opacity(0.03), radius: 16, x: 0, y: 8)
            .shadow(color: Color.black.opacity(0.015), radius: 4, x: 0, y: 2)
    }
}
```

### C. Glassmorphism Card (Liquid Material)
Overlay a subtle 1px border highlight over background materials for edge separation:
```swift
struct PremiumCardBackground: View {
    var body: some View {
        RoundedRectangle(cornerRadius: 20)
            .fill(.ultraThinMaterial)
            .overlay(
                RoundedRectangle(cornerRadius: 20)
                    .stroke(
                        LinearGradient(
                            colors: [.white.opacity(0.18), .clear, .black.opacity(0.04)],
                            startPoint: .topLeading,
                            endPoint: .bottomTrailing
                        ),
                        lineWidth: 1.0
                    )
            )
            .premiumCardShadow()
    }
}
```

---

## 4. Responsive SwiftUI Typography & Layout Stability

Ensure text wraps cleanly, has explicit limits, and card layouts maintain equal heights under dynamic text lengths:

### A. Controlled Line Limits & Truncation
```swift
Text(item.title)
    .font(.headline)
    .lineLimit(2)
    .truncationMode(.tail)
    .multilineTextAlignment(.leading)
```

### B. Auto-Scaling Single-Line Labels
```swift
Text(item.badge)
    .font(.subheadline)
    .lineLimit(1)
    .minimumScaleFactor(0.8)
```

### C. Preventing Vertical Clipping
Use `.fixedSize(horizontal: false, vertical: true)` on text containers inside scroll views to allow SwiftUI to expand heights vertically as text wraps:
```swift
Text(veryLongDescription)
    .font(.body)
    .lineLimit(nil)
    .fixedSize(horizontal: false, vertical: true)
```

### D. Layout Equal Heights
In SwiftUI `Grid` layout, cells automatically match height when using `.frame(maxHeight: .infinity)`:
```swift
Grid(alignment: .leading, horizontalSpacing: 16, verticalSpacing: 16) {
    GridRow {
        PremiumCard(title: "Short Title")
            .frame(maxHeight: .infinity)
        PremiumCard(title: "Very Long Title wrapping onto multiple lines")
            .frame(maxHeight: .infinity)
    }
}
```

### E. Dynamic Type (Adaptive Viewports)
If large accessibility sizes (Dynamic Type) make side-by-side elements overlap or wrap poorly, wrap them in a `ViewThatFits` block to stack vertically automatically:
```swift
ViewThatFits(in: .horizontal) {
    HStack(spacing: 16) {
        Text("Balance")
        Text("$3,420.50").bold()
    }
    VStack(alignment: .leading, spacing: 8) {
        Text("Balance")
        Text("$3,420.50").bold()
    }
}
```

### F. Input Field Validation Shiver (Shake Modifier)
Provide visual validation feedback on forms:
```swift
struct ShakerModifier: ViewModifier {
    var shakes: CGFloat
    
    func body(content: Content) -> some View {
        content
            .offset(x: sin(shakes * .pi * 2) * 8)
            .animation(.spring(response: 0.25, dampingFraction: 0.45), value: shakes)
    }
}

extension View {
    func shake(trigger: CGFloat) -> some View {
        self.modifier(ShakerModifier(shakes: trigger))
    }
}
```

---

## 5. SwiftUI Screen Prompt Add-On

Include this consolidated block in SwiftUI briefs:

```text
SwiftUI-specific UX & Visual constraints:
- Whitespace is a feature: Design with generous, intentional spacing (using strict 8pt spacing multipliers for Padding and stack Spacing parameters, e.g., `VStack(spacing: 24)`). Visual hierarchy must emerge naturally from whitespace alignment and text scale pairings rather than border overlays or dividers.
- Base Design Canvas Scaling: Base calculations must reference a 393x852 pt frame. Use GeometryReader or screen size percentages to compute dynamic paddings and component widths proportionally.
- Nested Corner Radii Math: Enforce exact radius nested relationships (`OuterRadius = InnerRadius + PaddingOffset`). Cards with 16pt padding and 24pt outer radius must utilize 8pt radius inner elements.
- Prune visual clutter: Omit non-essential backgrounds, border shapes, and helper caption blocks. Every element must earn its place on the screen.
- Layout bones & Native APIs: Connect the UI directly to native SwiftUI views. Use `.navigationTitle("Title")` with `.navigationBarTitleDisplayMode(.inline)`, register items via `.toolbar`, and anchor persistent bottom bars using `.safeAreaInset(edge: .bottom)`.
- Interactive states: Apply custom ButtonStyle for tactile "squishy" scale-down press compression (scaling to 0.95). Implement a custom horizontal offset shake modifier (`.shake(trigger:)`) on text input validation errors.
- Typography constraints: Always set explicit `.lineLimit(_:)`, `.truncationMode(_:)`, or `.minimumScaleFactor(_:)`. Allow text to wrap cleanly without vertical clipping by using `.fixedSize(horizontal: false, vertical: true)`. Grid cards must stretch to match tallest sibling height using `.frame(maxHeight: .infinity)`.
- Stacking & Accessibility: Wrap side-by-side structures in a `ViewThatFits` block to stack vertically automatically under large Dynamic Type accessibility font sizes.
- Choreograph state switches using `withAnimation(.spring(response: 0.35, dampingFraction: 0.7))` and native `.redacted(reason: .placeholder)` skeletons to prevent visual layout jumps.
- Meet WCAG AA contrast and ensure minimum touch hits are 44x44 pt.
```

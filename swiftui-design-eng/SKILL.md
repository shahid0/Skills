---
name: swiftui-design-eng
description: SwiftUI UI polish, fluid physics animations, iOS 17+ animation presets, phase/keyframe animators, custom spring values, responsive gestures, and haptic feedback.
---

# SwiftUI Design Engineering (iOS 17+)

This skill encodes Apple's modern fluid design engineering principles specifically for SwiftUI on iOS 17+. Use it to build and review interfaces that respond instantly, handle gesture velocity smoothly, and leverage interactive spring physics.

## The Core Philosophy

In SwiftUI, views should behave like tangible physical objects. Fluid UI depends on instant response, interruptible transitions, automatic momentum preservation, and tactile feedback.

---

## Core Topics & Implementations

### 1. Spring Presets & Parameters
iOS 17 introduces duration and bounce presets (`.smooth`, `.snappy`, `.bouncy`). See [SpringPresets.swift](examples/SpringPresets.swift) for configuration details.

### 2. Scoped Animations
Isolate animations and prevent leakages down the view hierarchy using the scoped `.animation(_:body:)` modifier. See [ScopedAnimations.swift](examples/ScopedAnimations.swift).

### 3. Gesture Velocity Handoff
iOS 17 automatically inherits and blends drag gesture velocity into springs triggered within `.onEnded`. Manual normalization math falls back on `interpolatingSpring`. See [VelocityHandoff.swift](examples/VelocityHandoff.swift).

### 4. Custom Transitions & Hero Animations
Animate views moving across containers using `matchedGeometryEffect` and custom transitions conforming to the iOS 17 `Transition` protocol. See [CustomTransitions.swift](examples/CustomTransitions.swift).

### 5. Metal Shaders
Apply stitchable Metal shaders on the GPU via `.colorEffect`, `.distortionEffect`, and `.layerEffect`. See [MetalShaders.swift](examples/MetalShaders.swift) and the Metal code in [Shaders.metal](examples/Shaders.metal).

### 6. Phase & Keyframe Animators
Orchestrate multi-property timelines and sequence steps using `PhaseAnimator` and `KeyframeAnimator`. See [KeyframeAnimations.swift](examples/KeyframeAnimations.swift).

### 7. Custom Animation curves
Conform to the `CustomAnimation` protocol to calculate custom, frame-by-frame interpolation. See [CustomAnimations.swift](examples/CustomAnimations.swift).

---

## 8. Suppressing Animations via Transactions

To disable transitions programmatically on state updates (replacing the deprecated `.animation(nil)`), mutate the `Transaction`.

```swift
// Disable animations for a single state action
var transaction = Transaction(animation: .none)
transaction.disablesAnimations = true

withTransaction(transaction) {
    isTabActive = 2 // Tab transitions immediately
}

// Or disable animations for an entire view hierarchy
MyView()
    .transaction { transaction in
        transaction.disablesAnimations = true
    }
```

---

## 9. Animatable Data Protocol

To animate custom shapes, drawing paths, or types that SwiftUI doesn't interpolate automatically, implement the `Animatable` protocol and specify `animatableData`.

```swift
struct CircularProgressShape: Shape, Animatable {
    var progress: Double
    
    var animatableData: Double {
        get { progress }
        set { progress = newValue }
    }
    
    func path(in rect: CGRect) -> Path {
        var path = Path()
        // Draw progress arc matching self.progress
        return path
    }
}
```

---

## 10. Scroll View Snapping & Flash Indicators

You can programmatically force target boundaries and dynamically scroll to targeted identifiers.

```swift
struct CustomList: View {
    @State private var scrollID: UUID?
    
    var body: some View {
        ScrollView {
            LazyVStack {
                ForEach(items) { item in
                    ItemRow(item)
                        .id(item.id)
                }
            }
            .scrollTargetLayout()
        }
        .scrollPosition(id: $scrollID)
        .scrollTargetBehavior(.paging)
        .scrollIndicatorsFlash(trigger: scrollID)
    }
}
```

---

## 11. Sensory Feedback (Haptics)

iOS 17 introduced standard, declarative haptic integration directly on views using `.sensoryFeedback`:

```swift
struct FeedbackToggle: View {
    @State private var isOn = false
    
    var body: some View {
        Toggle("Enable", isOn: $isOn)
            .sensoryFeedback(.impact(flexibility: .rigid), trigger: isOn)
    }
}
```

---

## 12. Performance Rules

1.  **Prefer scoped `.animation(_:body:)` over global implicit `.animation(_:value:)`.** This restricts the animation curve scope exclusively to properties declared inside the closure.
2.  **Avoid animating layout recalculations (like frames or paddings).** Animating `.frame(width:height:)` forces SwiftUI to perform expensive layout passes on every frame. Instead, use `.scaleEffect()` or `.offset()`, which are hardware-accelerated.
3.  **Use `.visualEffect` instead of `GeometryReader` where possible.** GeometryReader is heavy and introduces layout-cycle constraints. `.visualEffect` queries geography safely and performs updates on the render thread.
4.  **Harness `drawingGroup()` for complex views.** If you are rendering complex custom drawings, vector animations, or many shapes, apply `.drawingGroup()` to render the view into a single Metal texture.

---

## 13. Review Checklist

When reviewing SwiftUI code, enforce the following corrections:

| Issue | Correct Action | Why |
| :--- | :--- | :--- |
| `.animation(.default)` | Use `.animation(.smooth, value: state)` or `.snappy` | Clear, modern spring presets feel more premium than linear/default easing |
| `withAnimation { state = val }` | Use local scoped `.animation(curve) { view in view.scale(...) }` | Scopes animations to specific properties, preventing animation leaks down the hierarchy |
| Modifying `.frame` or `.padding` in animations | Use `.scaleEffect` or `.offset` | Skips CPU layout passes; processes directly on GPU |
| Modals scaling from center | Keep center origin for modals, but use `transform-origin` for popovers | Keeps popovers anchored to their trigger, improving spatial consistency |
| No active feedback on buttons | Add a custom scale-on-press button style | Tapping must feel tactile and responsive |
| Animation on keyboard/focus transition | Disable or set to zero duration | Keyboard actions must feel instant; animations introduce sluggish lag |
| Plain fade on changing numeric text | Apply `.contentTransition(.numericText())` | Swaps plain fading transitions for premium vertical rolling wheels |
| SF Symbols switching instantly or crossfading | Apply `.contentTransition(.symbolEffect(.replace))` | Morphs/scales symbols smoothly during replacement |
| Using GeometryReader inside scroll lists | Replace with `.scrollTransition` or `.visualEffect` | Prevents CPU layout passes, avoiding stuttering/frame drops |
| Handcrafting complex multi-modifier custom transitions | Conform struct to `Transition` using `TransitionPhase` | Declarative phase tracking ensures clean enter/exit interpolation |
| Synchronizing post-animation logic using DispatchQueue.main.asyncAfter | Add a native `completion:` block to `withAnimation` | Completion blocks execute exactly when the spring physics settle |
| Manually tracking scroll index offsets | Bind scroll index using `.scrollPosition(id:)` with `.scrollTargetLayout()` | Simplifies programmatic viewport scrolling and snapping behaviors |
| Static `.animation(nil)` to disable animations | Wrap state updates in `withTransaction` and set `transaction.disablesAnimations = true` | Natively suppresses animations across downstream views or hierarchies |
| Manual velocity calculations for simple drag transitions | Rely on iOS 17+ automatic gesture velocity inheritance | Standard springs triggered in gesture callbacks automatically inherit the gesture's final velocity |
| Custom paths or shape progress not animating | Conform shape to `Animatable` and set `animatableData` | Enables SwiftUI engine to interpolate non-standard numeric properties |
| Doing custom canvas timing loops on Main Thread | Conform structure to `CustomAnimation` | Offloads timing interpolation calculations to SwiftUI engine loops |
| Using complex nested views for simple bell/mail trigger movements | Apply `.symbolEffect(.bounce)` directly to the image | Leverage standard discrete or indefinite animation effects natively |
| Using deprecated `.cornerRadius(_:)` modifier | Replace with `.clipShape(RoundedRectangle(cornerRadius: ...))` | `.cornerRadius` is deprecated starting in iOS 17.4 |
| Using rectangular `.clipped()` modifier for custom clips | Replace with `.clipShape(Rectangle())` or appropriate shapes | Explicit shapes convey clipping intent clearly and consistently |

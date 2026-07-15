---
name: flutter-design-eng
description: Flutter UI polish, custom spring physics (SpringSimulation), interactive physics-based gestures, responsive layouts, micro-interactions, and visual performance.
---

# Flutter Design Engineering

This skill encodes fluid design engineering principles specifically for Flutter apps. Use it to build and review Flutter layouts that feel tactile, physical, responsive, and performant.

## The Core Philosophy

Flutter's rendering engine allows for pixel-perfect layout and custom physics. Fluid motion in Flutter should feel physical, respect touch velocities, handle boundary collisions with rubber-banding, and avoid frame drops.

---

## Core Topics & Implementations

### 1. Physics-Based Springs
Instead of standard curves, use physics-based spring simulations. See [PhysicsSprings.dart](examples/PhysicsSprings.dart) for custom spring setup.

### 2. Interactive Gestures & Velocity Handoff
Build physical swipe cards by tracking velocity and using an unbounded animation controller. See [InteractiveGestures.dart](examples/InteractiveGestures.dart).

### 3. Playful Button Scale Feedback
Incorporate instant touch-down scale reductions to build high-feedback buttons. See [ScaleButton.dart](examples/ScaleButton.dart).

### 4. Rendering Performance & Frame Rates
Avoid dropped frames by isolating repaints using boundaries and static builders. See [PerformanceOptimization.dart](examples/PerformanceOptimization.dart).

---

## 5. Review Checklist

When reviewing Flutter UI code, enforce the following corrections:

| Issue | Correct Action | Why |
| :--- | :--- | :--- |
| `Curves.easeInOut` on UI animations | Replace with SpringSimulation or the `sprung` package | Springs feel physical and natural; duration curves feel robotic |
| Standard `InkWell` click effect only | Wrap in a tactile scale gesture detector | Scale on press (`scale(0.96)`) gives instant responsiveness |
| Rebuilding entire layouts during animation ticks | Use `RepaintBoundary` and pass static `child` to `AnimatedBuilder` | Prevents rendering jank and drop frames |
| Hard boundaries on scroll or drag | Apply logarithmic resistance / rubber-banding on offsets | Sudden stops feel broken; physical resistance signals bounds naturally |
| Hard-coded positioning coordinates | Use percentage-based positioning (`FractionalTranslation` or `FractionallySizedBox`) | Adapts elegantly to varying screen resolutions and dimensions |
| Animating margins/paddings | Animate `Transform.translate` or offset | Padding animation triggers CPU layout recalculations; transform works directly on the GPU |

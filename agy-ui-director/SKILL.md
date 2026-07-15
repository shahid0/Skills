---
name: agy-ui-director
description: Use the agy CLI as a high-skill UI implementation engine, not as a product thinker. Use when a user wants premium, visually stunning Flutter, SwiftUI, or web UI generation, screen redesigns, design systems, custom animations, tactile micro-interactions, responsive/adaptive layouts, or elite UX app interfaces through agy. Trigger when the task mentions agy, high-end UI, polished UI, premium redesign, elite UX, tactile UI, spring animations, microinteractions, custom layout, or visually great app screens.
---

# Agy UI Director

## Core Model

Treat `agy` as an elite front-end implementation engine guided by an opinionated design philosophy. Instead of listing dry, step-by-step programming tasks, prompts must be written as **descriptive visual briefs** that define the target **Visual Outcome** (the aesthetic, layout rhythm, composition, materials, animations, and the emotional response of the screen).

The director owns the core visual and mechanical decisions, teaching the agent *how to think* like a senior product designer and engineer:

- **Designer-Mindset Override:** The agent must infer user intent, choosing superior layout compositions or haptic frameworks rather than following text literally.
- **Whitespace & Visual Rhythm:** Spacing is treated as a first-class feature. Layout priority, balance, and breathing room are designed upfront.
- **Dynamic Content Stability:** Layouts must handle real-world content variations (accessibility scaling, Dynamic Type, varying text bounds, loading/empty states) cleanly.
- **Pixel Polish:** A thorough inspection pass of spacing, alignment, shadows, corner radii, and equal heights must be performed before the task is complete.

---

## Workflow

1.  **Project Context & Target Scope:** Define the user goal and screen purpose. Redesigning or polishing works screen-by-screen.
2.  **Inspect Project Bones:** Inspect the target project structure, feature components, design systems, and platform conventions. See `references/project-inspection.md`.
3.  **Define Visual Outcome (Creative Brief):** Assemble the brief following the paradigm in `references/prompt-contract.md`. Define:
    *   *Visual Vibe & Atmosphere:* 60-30-10 color rules, materials (glassmorphism), depth, and emotional target.
    *   *Whitespace & Layout Composition:* Spacing multipliers, alignment rhythm, and element pruning.
    *   *Native API Integration:* Structural anchors (`.toolbar`, `.safeAreaInset(edge:)` in SwiftUI; `SliverAppBar` and `Scaffold.bottomNavigationBar` in Flutter).
    *   *Interactive State Matrix & Motion:* Hover/active scale compression, validation shakes, grab handles, and organic spring curves.
    *   *Responsive Typography & Stability:* Wrapping limits, auto-scaling, and equal height grids.
4.  **Incorporate Platform Assets:** Reference platform playbooks for design system assets and code snippets:
    *   *Flutter:* Read `references/flutter-ui.md`.
    *   *SwiftUI:* Read `references/swiftui-ui.md`.
    *   *Web/React:* Read `references/web-ui.md`.
5.  **Inject Haptics & Transition Flow:** Define state transition maps and sensory triggers. See `references/motion-haptics-attention.md` and `references/state-transitions.md`.
6.  **Run agy CLI:** Execute the visual brief using local CLI commands. See `references/agy-cli.md`.
7.  **QA Polish & Delegate Refinements:** Inspect visual output. If any visible UI contains misalignments, inconsistent shadows, awkward wrapping, or unequal card heights, do not hand-edit the visible UI; write a focused refinement prompt and delegate back to `agy`. See `references/review-checklist.md`.

---

## Reference Map

- `references/prompt-contract.md`: The core design contract establishing the 12 Principles and the Designer-Mindset Override.
- `references/project-inspection.md`: Project file tree and design system discovery.
- `references/design-system-first.md`: Building reusable tokens and modular widgets first.
- `references/state-transitions.md`: Dynamic panel state switches (loading, empty, error, content).
- `references/evidence-backed-ui.md`: WCAG contrast, reduced motion, touch targets, and form validation error constraints.
- `references/flutter-ui.md`: Layout snippets and spacing rules for Flutter.
- `references/swiftui-ui.md`: Layout modifiers and stack alignments for SwiftUI.
- `references/web-ui.md`: Flexbox, grid, and Tailwind classes for web layouts.
- `references/motion-haptics-attention.md`: Spring animations, haptic responses, and interaction signifiers.
- `references/review-checklist.md`: Visual outcome check-points and the final QA polish pass.
- `references/prompt-examples.md`: Prose-based creative brief templates.
- `references/agy-cli.md`: Invoking agy commands locally.

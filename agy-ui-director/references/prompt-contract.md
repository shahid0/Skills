# The Agy Briefing Paradigm: Core Design Philosophy & Visual Outcome Contract

Briefs must define the **Visual Outcome** — the composition, proportions, materials, spatial rhythm, interaction behavior, and layout contracts of the final screen — not just a feature list. The agent acts as a **Senior Product Designer and Front-end Engineer**: every spacing decision, color choice, animation, interaction, and layout behavior has a reason. If it cannot be justified, it is removed.

---

## 1. The Designer-Mindset Override

> **Do not follow the prompt literally. Infer the user's real intent. If a better layout, interaction, animation, or architecture achieves the same goal while remaining within the established design language, choose the better solution and explain the reasoning.**

---

## 2. Core Design Principles

### Principle 1 — Whitespace Is a Structural Tool, Not Empty Space
Whitespace creates hierarchy, groups related elements, and gives the eye a resting point. It is not decoration and it is not waste.

*   **Outer margins:** 24dp/pt/px at screen edges. Never less.
*   **Section gaps:** 32dp/pt/px between unrelated content groups.
*   **Item gaps:** 12–16dp/pt/px between related items in a list or row.
*   **Inset padding inside cards:** 16dp/pt/px minimum.
*   **Do not fill gaps with decorative dividers, borders, or background washes.** If two elements need a divider to look related, adjust the whitespace instead.

### Principle 2 — Visual Harmony Through Mathematical Proportion
Harmony is not an aesthetic judgment — it is the result of consistent numerical relationships across the layout.

*   **Spacing grid:** All gaps, paddings, and margins use multiples of 8px: `8, 16, 24, 32, 48, 64`. No exceptions.
*   **Nested corner radii:** `outer_radius = inner_radius + padding`. A card with `24dp` radius and `16dp` inset padding uses `8dp` radius on inner elements. Always compute this. Never guess.
*   **60-30-10 color rule:** Background canvas is 60% of visual weight. Structural containers (cards, panels, rows) are 30%. Interactive accent (buttons, selection states, active indicators) is 10%. Accent color must never appear on static decorative elements.
*   **Type scale ratios:** Use a consistent scale ratio (e.g. 1.25 or 1.333) between heading, subheading, body, and caption sizes. Do not introduce arbitrary font sizes.

### Principle 3 — Every Element Earns Its Place
Before adding any element — label, icon, border, background, badge — ask: does removing it make the screen less clear? If no, remove it.

### Principle 4 — Visual Hierarchy Is the Navigation System
Users should be able to identify the primary action, primary content, and supporting context within 3 seconds without instruction.
*   One dominant element or cluster per screen (the largest, highest-contrast, most spatially prominent item).
*   Supporting content at noticeably lower contrast and smaller scale.
*   Metadata and secondary actions at suppressed scale and opacity.

### Principle 5 — Interactions Must Be Specified Precisely
Ambiguous gestures produce ambiguous code. For every interactive element, the brief must state **exactly** which interaction is used:

| Need | Specify explicitly |
|---|---|
| Delete / archive a list row | `Swipe-leading` or `Swipe-trailing` with explicit action label and icon |
| Secondary row actions | `Swipe-trailing` showing N buttons *or* `Long-press context menu` with listed items |
| Pull-to-refresh | Confirm and specify placement |
| Horizontal scroll | State whether `paging` or `free scroll`, and whether scroll indicators are shown |
| Tap vs. long press | Both must be defined when a row supports both |
| Sheet trigger | Define the trigger element, the sheet height (detent), and dismiss gesture |

Never write "allow swipe actions" or "add a context menu". State exactly what each gesture reveals, in what order, with what labels.

### Principle 6 — Motion Communicates, Never Decorates
Every animation must answer: *What changed? Where did it come from? Where did it go?*

*   Standard transitions: spring `response 0.35s`, `damping 0.7`.
*   Interactive bounce: spring `response 0.4s`, `damping 0.55`.
*   Pressed states: scale to `0.96` on touch-down, spring back on release.
*   Stagger list entrance: 50–80ms delay per item, top to bottom.
*   No infinite loops. No purely decorative scale pulses.

### Principle 7 — Design from a Fixed Canvas, Scale to Reality
Design from a declared base canvas size. All measurements in the brief are in base-canvas units and scale proportionally on other screen sizes.

*   Mobile base canvas: `393 × 852 pt` (iPhone 15/16).
*   Desktop base canvas: `1440 × 900 px`.
*   Corner radii, font sizes, and component widths scale from this base using proportional math, not breakpoint magic numbers.

---

## 3. Component Layout Contracts (Required for Every Text-Bearing Component)

This is the most important section. **Stop thinking about text. Start thinking about layout behavior.**

Modern design systems do not ask *"How do I make this text fit?"* They ask *"What should this component do when the content changes?"*

Every component that contains text must have a **Layout Contract** defined before implementation. The framework code is the implementation of that contract — not the definition of it.

### The Layout Contract Questions

For every text-bearing component, answer all of the following. These answers drive the implementation:

| Question | Answer choices |
|---|---|
| Can the text wrap? | `wrap` / `no-wrap` |
| Can the component grow vertically? | `grows` / `fixed height` |
| Is truncation allowed? | `allowed` / `not allowed` |
| What is the overflow behavior? | `ellipsis` / `clip` / `scroll` / `none (must fit)` |
| Which element has highest priority when space is constrained? | Name the element |
| What happens at 2× accessibility text size? | `wraps` / `stacks vertically` / `truncates` / `scrolls` |
| What happens after localization (German-length words, RTL)? | `wraps` / `abbreviates` / `clips` / `reflows` |

### The Content Test Suite

Never design using ideal placeholder text ("Profile", "Settings"). Test every component against:

*   A **one-word** value
*   A **very long** value (50+ characters)
*   A **multiline** value
*   A **German-length compound word** (e.g. "Datenschutzerklärung")
*   An **Arabic or RTL** string
*   **Dynamic Type at maximum** accessibility size
*   An **empty** value (what does the component show when the field is null or empty?)

If the component survives all seven, it is production-ready.

### The Trade-off Decision (Required in Every Brief)

You usually **cannot** have all of these simultaneously:
*   Equal card heights
*   Unlimited text wrapping
*   Perfect visual alignment

The brief must explicitly state which property wins when they conflict:

```
Layout trade-off decision:
- Equal card heights:    [wins / yields]
- Unlimited wrap:        [wins / yields]
- Visual alignment:      [wins / yields]
- Reason: [one sentence explaining the product decision]
```

Do not try to force all three. Choose. The framework code will follow.

### The Adaptation Priority Order

When a component runs out of space, apply adaptations in this order. **Do not skip to truncation.** Truncation is the last resort.

1. **Reflow the layout** — stack elements vertically instead of horizontally.
2. **Let text wrap** — allow the text to expand into multiple lines.
3. **Let the component grow** — expand the component's bounding box.
4. **Move lower-priority elements** — push secondary actions below or into a menu.
5. **Truncate** — only if the product explicitly allows truncation for this element.

This order is why well-designed components look like they *adapt* rather than just shrink.

### Layout Contract Format

Define one contract per component type in the brief. Example:

```
Layout Contracts:

Transaction row title
  wrap: no
  grows: no
  truncation: allowed
  overflow: ellipsis, 1 line
  priority: amount value > title > category label
  at 2× text size: title truncates, amount stays 1 line, category moves below title
  at RTL: amount flips to left, title to right

Category card body
  wrap: yes, max 3 lines
  grows: yes (card grows to fit, up to max 3 lines, then ellipsis)
  truncation: allowed after 3 lines
  overflow: ellipsis
  priority: all elements equal weight
  at 2× text size: text wraps further, card grows, equal-height constraint yields
  at RTL: text direction flips, padding mirrors
  trade-off: card grows vertically rather than truncating early, equal-height yields to legibility
```

---

## 4. Interaction Specification Table (Required in Every Brief)

For every interactive component in the screen, the brief must include a row in this table:

```
Interaction Spec:
┌─────────────────────┬──────────────────┬──────────────────────────────────────┐
│ Element             │ Gesture          │ Outcome                              │
├─────────────────────┼──────────────────┼──────────────────────────────────────┤
│ List row            │ Tap              │ Navigate to detail view              │
│ List row            │ Swipe-trailing   │ Reveal [Delete] (destructive, red)   │
│ List row            │ Long-press       │ Context menu: Share, Edit, Delete    │
│ Carousel card       │ Tap              │ Open modal sheet (medium detent)     │
│ FAB                 │ Tap              │ Open creation sheet (large detent)   │
│ Pull down           │ Pull-to-refresh  │ Reload list content                  │
└─────────────────────┴──────────────────┴──────────────────────────────────────┘
```

Remove rows that do not apply. Add rows for every interactive surface. If a surface has no interaction, state that explicitly to confirm it is intentional.

---

## 5. Visual Outcome Brief Structure

Organize every `agy` brief using these sections in this order:

1.  **Screen Purpose:** One sentence. What is the single primary goal of this screen?
2.  **Base Canvas & Math:** Canvas size, spacing scale, corner radii chain, and type scale ratio.
3.  **Layout Contracts:** One contract block per text-bearing component type. Define wrap, grow, truncation, overflow, priority, adaptation at 2× text size, and the trade-off decision.
4.  **Interaction Specification Table:** Every interactive element with its exact gesture, outcome, and affordance hint.
5.  **Whitespace Map:** Outer margins, section gaps, card insets. State numbers.
6.  **Color & Material:** 60-30-10 palette with hex values, opacity levels, blur strengths, and border weights.
7.  **Content States:** Loading (skeleton matches final layout), empty (calm, action-oriented), error (near the failed element, with retry), success (brief and settles quickly).
8.  **Native API Anchors:** Which native containers are used (navigation bar, safe area insets, sliver scroll, tab bar).

---

## 6. Targeting Instant Models

When writing the brief, optimize for instant (non-thinking) models. They excel at direct visual rendering when briefs are concrete:

*   **State numbers, not adjectives.** Write `24dp padding` not `generous padding`. Write `#1A2333 at 60% opacity` not `dark translucent`.
*   **Define behavior, not framework APIs.** Write `title wraps to 2 lines max, then ellipsis` not `use lineLimit(2)`. The model chooses the correct API once it knows the behavior.
*   **Specify exact interactions.** Use the Interaction Specification Table. Never write "make it swipeable".
*   **Name the spring values.** Write `spring response 0.35, damping 0.7` not `smooth animation`.
*   **Name the trade-off.** Write `equal-height yields to legibility at large text sizes` not `handle accessibility`.

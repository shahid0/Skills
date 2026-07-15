# Review Checklist: Visual Outcome Verification

Before considering a UI implementation complete, verify every gate below. This is not a style preference check — it is a functional verification that the screen achieves its defined Visual Outcome, honors every component's Layout Contract, and handles real-world content without breaking.

---

## 1. Whitespace as Structure

- All outer screen margins are at least **24dp/pt/px**.
- All section gaps between unrelated content groups are at least **32dp/pt/px**.
- All item gaps within related lists or rows are **12–16dp/pt/px**.
- No divider lines, border separators, or background washes are used where spacing alone suffices.
- Visual hierarchy is readable from spacing and scale differences alone — not from outlines or color fills.

## 2. Mathematical Harmony

- All spacing values are multiples of 8: `8, 16, 24, 32, 48, 64`. No arbitrary values.
- Nested corner radii are mathematically computed: `outer_radius = inner_radius + card_padding`. Verify that inner elements do not visually clip into card corners.
- Color is allocated in the 60-30-10 ratio. Accent color appears only on interactive and selection states — not on static decoration.
- Typography uses a consistent scale ratio between heading, subheading, body, and caption. No sizes are introduced without a clear scale relationship.

## 3. Component Layout Contracts

This is the highest-priority verification gate. Every text-bearing component must be checked against its Layout Contract.

For each component, verify:
- **Wrap:** Does the component wrap or not wrap text, as specified in its contract?
- **Growth:** Does the component grow vertically when content is long, or is it fixed-height as specified?
- **Truncation:** Is truncation applied only where the contract allows it? Is the overflow behavior (ellipsis/clip) the one specified?
- **Priority:** When space is constrained, does the highest-priority element survive intact while lower-priority elements yield?
- **Adaptation order:** Did the layout try to reflow → wrap → grow → move before truncating? Truncation must not be the first response to space pressure.
- **Trade-off honored:** Is the declared trade-off (equal height vs. unlimited wrap vs. visual alignment) respected?

### Content Test Suite — Run Against Every Component

Verify that the component does not break under:
- [ ] A one-word value
- [ ] A 50+ character value
- [ ] A multiline value
- [ ] A long compound word with no spaces (e.g. "Datenschutzerklärung")
- [ ] An RTL/Arabic string
- [ ] Dynamic Type at maximum accessibility size (the largest system font scale)
- [ ] An empty or null value

If any of these cases causes clipping, overflow, misalignment, or layout shift, the component fails this gate. The contract must be re-evaluated and the implementation corrected.

## 4. Interaction Completeness

- Every interactive surface has an explicitly specified gesture from the Interaction Specification Table.
- Swipe actions (leading/trailing) reveal the correct number of action buttons with correct labels, icons, and destructive styling.
- Long-press context menus list the correct items in the correct order.
- Any surface that has no interaction has been explicitly confirmed as intentional (not overlooked).
- Swipeable rows demonstrate the gesture once on first session load (translate-and-return affordance).
- Horizontal carousels show at least 15% of the next card at the trailing edge.

## 5. Pressed and Interactive States

- All tappable surfaces scale to **0.96** on touch-down and spring back on release.
- Disabled states are at **40% opacity** with touch/click events suppressed.
- Loading states use skeleton placeholders that match the exact dimensions of the final content. No generic spinners in the content area.
- Error states appear near the failed element, not as full-screen overlays, unless the failure is global.
- Success states settle quickly (under 1.5 seconds) back to the normal content state.

## 6. Motion Validity

- Every animation communicates a state change. Identify what it communicates. If it communicates nothing, remove it.
- No infinite loops or ambient pulses on non-interactive elements.
- Spring values match the table: standard `0.35 / 0.7`, bounce `0.4 / 0.55`, validation error `0.25 / 0.45`.
- Stagger entrance delay is 50–80ms per item, ordered by visual priority.

## 7. Visual Outcome Fidelity

- The dominant element or cluster on screen is unambiguous at first glance.
- Supporting content is at noticeably lower contrast and smaller scale than primary content.
- Removing any element from the current design makes the screen less clear. If not, remove it.
- The 60-30-10 color split is perceptible: background, container surfaces, and accent are visually distinct layers.

## 8. Platform-Specific Gates

### SwiftUI
- Text containers inside scroll views use `.fixedSize(horizontal: false, vertical: true)` where the contract specifies wrapping.
- Sheets use `.sheet(item:)` not `.sheet(isPresented:)` when associated data exists.
- Side-by-side layouts are wrapped in `ViewThatFits` for Dynamic Type compatibility.

### Flutter
- All scroll layouts use `CustomScrollView` + `Slivers`. No `SingleChildScrollView` wrapping `Column` for long content.
- Safe area inset reads `MediaQuery.of(context).padding` dynamically.
- Equal-height rows use `IntrinsicHeight` + `CrossAxisAlignment.stretch` only when the layout contract specifies equal height wins the trade-off.

### Web / Tailwind
- Grid cards use `items-stretch` and `flex flex-col`. Action buttons are anchored to the bottom using `flex-grow` on the body.
- Text overflow uses `line-clamp-N` for multi-line and `truncate` for single-line, as specified in the contract.
- Focus outlines are explicit: `outline-none focus-visible:ring-2 focus-visible:ring-offset-2`.

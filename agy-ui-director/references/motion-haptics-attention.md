# Motion and Haptics Playbook

Every animation must justify its presence by communicating something the user needs to understand: what changed, where something came from, or where it went. If an animation does not answer one of those questions, it does not belong.

---

## 1. Motion Communicates State Changes

| Change | Expected Animation |
|---|---|
| Screen enters | Stagger items from top, 50–80ms per item, spring `0.35 / 0.7` |
| Sheet opens | Translate from bottom edge, spring `0.35 / 0.7` |
| Sheet dismisses | Translate back to bottom edge |
| Item deletes from list | Height collapses to 0, neighbors slide up |
| Item adds to list | Height expands from 0, spring `0.35 / 0.7` |
| Loading → content | Skeleton crossfades to real content, no layout jump |
| Submit → success | Brief confirmation (scale pop or checkmark swap), then settles |
| Validation error | Input field translates ±8px for 2 cycles, spring `0.25 / 0.45` |
| Expand/collapse section | Chevron rotates 90° or 180°, content height animates |
| Tab switch | Content crossfades or slides in the expected direction |

---

## 2. Spring Physics Reference

All transitions use spring curves. No linear or ease-in-out.

| Use case | Response | Damping |
|---|---|---|
| Standard transitions | `0.35s` | `0.7` |
| Interactive bounce (cards, FAB) | `0.4s` | `0.55` |
| Quick state updates (toggle, selection) | `0.25s` | `0.8` |
| Error shake | `0.25s` | `0.45` |

---

## 3. Pressed State Feedback

All tappable surfaces must respond visually on touch-down. No surface should feel unresponsive.

*   **Scale:** `0.96` on touch-down, `1.0` on release, spring `0.25 / 0.7`.
*   **Opacity shift (secondary):** Optionally drop to 90% opacity on press for text-only buttons.
*   **Minimum tap target:** 44×44 pt (iOS), 48×48 dp (Android/Flutter), 44px (Web).

---

## 4. Haptic Intent

Haptics are causal. They fire because the user did something, not because something appeared.

| Trigger | Haptic |
|---|---|
| Toggle, segment tap, checkbox | Light selection impact |
| Confirm action (delete, send, submit) | Medium impact |
| Task completion, milestone | Success notification |
| Validation failure | Warning notification |

Never trigger haptics on: scroll, load events, timers, or passive data updates.

---

## 5. Interaction Affordances (Teachable Without Instructions)

When a surface supports a non-obvious gesture, show it passively without tooltips or popups:

*   **Swipeable list rows:** On first load, briefly translate the row 20px in the swipe direction and spring back. This runs once per session.
*   **Horizontal carousels:** The last visible card must be clipped at exactly 85% width, leaving 15% of the next card visible. This is the affordance. No arrows required unless content is not scrollable on all devices.
*   **Draggable sheets:** A centered `4×36pt` rounded pill handle is required. It must scale on touch-down (`1.2× width`) and return on release.
*   **Expandable rows:** A chevron icon that rotates 90° or 180° on expand. No other affordance is needed.

---

## 6. What Never to Animate

*   Infinite loops or ambient pulses on non-interactive elements.
*   Shadows or blur strength as hover effects (expensive on mobile).
*   Navigation bars, status bars, or system UI components.
*   Background color transitions that span more than 200ms (users mistake slow transitions for bugs).
*   Anything that plays during pull-to-refresh content rendering (causes jank).

---

## 7. Prompt Add-On Block

```text
Motion & Haptics:
- Every animation must explain a state change. No decorative animations.
- Transitions: spring response 0.35, damping 0.7. Interactive bounce: response 0.4, damping 0.55.
- Pressed state: scale to 0.96 on touch-down, spring to 1.0 on release.
- Stagger list entrance: 50–80ms per item, top to bottom.
- Validation errors: translate ±8px for 2 cycles, spring response 0.25, damping 0.45.
- Swipe-affordance: on first session load, translate swipeable rows 20px and spring back.
- Carousel peek: last visible card clips at 85% width, 15% of next card visible.
- Haptics only on direct user actions. Never on load events or timers.
- Respect prefers-reduced-motion: replace translate/scale animations with opacity crossfades.
```

# Visual Outcome Brief Examples

These examples show how to write briefs for instant (non-thinking) models. Descriptions are concrete: numbers instead of adjectives, exact gesture specs instead of vague "swipeable", hex values instead of color names. Every brief includes a **Layout Contract** for each text-bearing component — this defines component behavior under all content conditions before any framework code is written.

---

## 1. Flutter Screen: Personal Finance Dashboard

```text
Screen file: lib/features/home/presentation/home_screen.dart
Feature widgets: lib/features/home/presentation/widgets/

Designer override: Do not follow this prompt literally. If a better layout or architecture achieves the same goal within this design language, choose it and explain the decision.

─── Screen Purpose ───────────────────────────────────────
Show the user their financial position and make adding a transaction the dominant action.

─── Base Canvas & Math ───────────────────────────────────
Canvas: 393 × 852 dp
Spacing scale: 8, 16, 24, 32, 48, 64 dp only.
Corner radii chain: Cards = 24dp outer. Card padding = 16dp. Inner elements = 8dp. (OuterRadius - Padding = InnerRadius)
Type scale ratio: 1.333 (body 16sp → subheading 21sp → heading 28sp → display 37sp)

─── Layout Contracts ─────────────────────────────────────
Transaction row — merchant name
  wrap: no
  grows: no (row height is fixed at 72dp)
  truncation: allowed
  overflow: ellipsis, 1 line
  priority: amount > merchant name > category label
  at 2× text size: merchant name truncates further, amount stays 1 line, category label hides
  at RTL: amount flips to left edge, merchant name to right, row layout mirrors
  content test: "Al" / "Supermarkt für Lebensmittel und Haushalt GmbH" / empty → ellipsis applies
  trade-off: row height wins. Text truncates before the row grows.

Category card — label
  wrap: no (badge pill, single line)
  grows: no
  truncation: allowed
  overflow: ellipsis
  priority: sole element in pill
  at 2× text size: pill grows in width, text truncates if it would exceed 60% of card width
  at RTL: text direction mirrors, padding stays symmetric
  content test: "Rent" / "Recurring Direct Debit" → truncates in pill
  trade-off: pill width caps at 60% of card. Text truncates before layout breaks.

─── Interaction Specification ────────────────────────────
┌──────────────────────┬─────────────────┬─────────────────────────────────────────────┐
│ Element              │ Gesture         │ Outcome                                     │
├──────────────────────┼─────────────────┼─────────────────────────────────────────────┤
│ Transaction row      │ Tap             │ Open transaction detail sheet (large detent)│
│ Transaction row      │ Swipe-trailing  │ Reveal [Delete] button (red, destructive)   │
│ Transaction row      │ Long-press      │ Context menu: Edit, Duplicate, Delete       │
│ Category card        │ Tap             │ Navigate to category breakdown screen       │
│ Horizontal carousel  │ Swipe           │ Free scroll, no paging, peek = 15% of next  │
│ FAB (+)              │ Tap             │ Open add-transaction sheet (large detent)   │
│ Pull down on list    │ Pull-to-refresh │ Reload transactions, keep existing visible  │
└──────────────────────┴─────────────────┴─────────────────────────────────────────────┘

─── Whitespace Map ───────────────────────────────────────
Outer screen margins: 24dp horizontal, 0dp vertical (content reaches safe area edges).
Gap between hero balance block and card row: 32dp.
Gap between card row and transaction list header: 24dp.
Gap between list rows: 0dp (rows are full-bleed with 16dp inner padding).
Card inner padding: 16dp all sides.
No divider lines between sections. Spacing alone creates the separation.

─── Color & Material ─────────────────────────────────────
Background canvas (60%): #0A0E17, fully opaque.
Card surfaces (30%): #161F30 at 60% opacity, blur 20dp behind. 1dp border: #FFFFFF at 8% opacity.
Interactive accent (10%): #00F2FE. Used on: FAB, active selection state, progress indicators. Nowhere else.
Shadow: two layers — (black 3%, blur 24, y 8) + (black 1.5%, blur 8, y 2).

─── Content States ───────────────────────────────────────
Loading: Skeleton rows at exact final row height (72dp). No spinner in content area.
Empty: Single centered label + primary action button. No illustration unless the design system already includes one.
Error: Inline banner below list header with retry button. Do not replace the whole screen.
Success (after add): FAB shows checkmark for 800ms then returns to plus icon.

─── Native API Anchors ───────────────────────────────────
Entire viewport: CustomScrollView with SliverAppBar + SliverList.
SliverAppBar: collapses balance to inline title on scroll. Uses backdrop blur when collapsed.
Bottom bar: Scaffold.bottomNavigationBar slot. Not a custom floating widget.
Safe area: MediaQuery.of(context).padding.top/.bottom applied. Do not hardcode insets.

─── Real-Content Constraints ─────────────────────────────
Transaction title: maxLines 1, overflow ellipsis.
Category label on card: maxLines 1, overflow ellipsis, minimumScaleFactor 0.85.
Amount field: single line, always right-aligned, never wraps.
Cards in bento grid: CrossAxisAlignment.stretch + IntrinsicHeight. No card taller than its sibling.
Swipe-affordance: on first load, translate transaction rows 20dp trailing and spring back once.
```

---

## 2. SwiftUI Screen: Daily Habit Tracker

```text
Screen file: App/Features/Today/Views/TodayView.swift
Feature components: App/Features/Today/Views/Component/

Designer override: Do not follow this prompt literally. If a better layout or architecture achieves the same goal within this design language, choose it and explain the decision.

─── Screen Purpose ───────────────────────────────────────
Let the user check off habits for today and see their progress at a glance.

─── Base Canvas & Math ───────────────────────────────────
Canvas: 393 × 852 pt
Spacing scale: 8, 16, 24, 32, 48, 64 pt only.
Corner radii chain: Cards = 24pt outer. Card padding = 16pt. Inner elements = 8pt.
Type scale ratio: 1.25 (caption 12pt → body 15pt → subheading 19pt → heading 24pt → display 30pt)

─── Layout Contracts ─────────────────────────────────────
Habit row — title
  wrap: yes, max 2 lines
  grows: yes (row grows to fit up to 2 lines)
  truncation: allowed after 2 lines
  overflow: ellipsis, tail
  priority: completion checkbox > title > streak badge
  at 2× text size: wraps further, row grows, badge moves below title
  at RTL: checkbox moves to right edge, text and badge mirror
  content test: "Run" / "Daily morning meditation and journaling practice" / "Leibnizstraße" → wraps to 2 lines
  adaptation order: wrap → grow → then ellipsis at 3 lines. Never truncate before 2 full lines.
  trade-off: row height grows to preserve legibility. Equal row heights yield.

Habit carousel card — name
  wrap: no
  grows: no (card is fixed proportion of screen width)
  truncation: allowed
  overflow: ellipsis, 1 line
  minimumScaleFactor: 0.82 (shrinks before truncating)
  priority: icon > name > streak count
  at 2× text size: name shrinks to minimum scale factor, then truncates
  at RTL: text mirrors, no layout change
  content test: "Yoga" / "Evening strength training circuit" → scale down then ellipsis
  trade-off: card width is fixed. Text scales then truncates.

─── Interaction Specification ────────────────────────────
┌─────────────────────────┬────────────────┬──────────────────────────────────────────────┐
│ Element                 │ Gesture        │ Outcome                                      │
├─────────────────────────┼────────────────┼──────────────────────────────────────────────┤
│ Habit row               │ Tap            │ Toggle completion state + light haptic       │
│ Habit row               │ Swipe-trailing │ Reveal [Skip] (gray) and [Delete] (red)     │
│ Habit row               │ Long-press     │ Context menu: Edit Habit, Set Reminder, Skip │
│ Habit card (carousel)   │ Tap            │ Open habit detail sheet (medium detent)      │
│ Progress ring           │ Tap            │ No interaction — confirm explicitly static   │
│ Horizontal carousel     │ Swipe          │ Paging scroll. containerRelativeFrame span 10/12 (15% peek) │
│ Bottom completion bar   │ Tap (CTA)      │ Open reflection modal (large detent)         │
│ Pull down on list       │ Pull-to-refresh│ Reload habit status from persistence layer   │
└─────────────────────────┴────────────────┴──────────────────────────────────────────────┘

─── Whitespace Map ───────────────────────────────────────
Outer screen margins: 24pt horizontal.
Gap between progress ring card and carousel: 24pt.
Gap between carousel and habit list: 32pt.
Gap between habit rows: 0pt (rows full-bleed, 16pt inner vertical padding).
Section header to first row: 8pt.
No dividers. Spacing is the separator.

─── Color & Material ─────────────────────────────────────
Background canvas (60%): #F8F9FA, with a soft amber radial gradient (rgba(255,190,100,0.12)) centered top-right at 40% screen width.
Card surfaces (30%): .ultraThinMaterial. 1pt overlay border: LinearGradient from white 18% (top-leading) to clear to black 4% (bottom-trailing).
Interactive accent (10%): #10B981. Used on: completion checkmarks, active streak numbers, primary CTA. Nowhere else.
Shadow: two layers — (black 3%, blur 16, y 8) + (black 1.5%, blur 4, y 2).

─── Content States ───────────────────────────────────────
Loading: .redacted(reason: .placeholder) on the final layout shape. No custom skeleton view.
Empty (no habits): Label + "Add your first habit" button. No illustration.
All complete: Swap list area for a brief congratulations view that settles back to normal in under 2 seconds.
Error loading: Inline message below list header with retry. Do not replace the navigation bar.

─── Native API Anchors ───────────────────────────────────
Navigation title: .navigationTitle("Today"), .navigationBarTitleDisplayMode(.inline).
Toolbar: settings icon in .navigationBarTrailing ToolbarItem.
Bottom completion bar: .safeAreaInset(edge: .bottom). Not a ZStack overlay.
Sheet presentation: .sheet(item: $selectedHabit). Never .sheet(isPresented:) with associated data.

─── Real-Content Constraints ─────────────────────────────
Habit title on row: .lineLimit(2), .truncationMode(.tail).
Habit title on carousel card: .lineLimit(1), .minimumScaleFactor(0.82).
Streak count badge: .lineLimit(1), no scaling — badge resizes to fit.
Grid cards: .frame(maxHeight: .infinity) on each card. Grid row height matches tallest card.
Dynamic Type: progress ring header uses ViewThatFits to stack label and percentage vertically when needed.
Swipe-affordance: On first app launch only, translate swipeable rows 20pt trailing and spring back.
```

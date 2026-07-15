# Flutter UI Playbook

Use this playbook when generating or refining Flutter user interfaces.

---

## 1. File Placement & Architecture

Maintain a clean separation of concerns and build modular systems rather than one-off screens:
- **Feature Screen:** `lib/features/<feature>/presentation/<screen_name>.dart`
- **Feature Widgets:** `lib/features/<feature>/presentation/widgets/<widget_name>.dart`
- **Reusable UI Components:** `lib/design_system/widgets/` (e.g. custom inputs, premium button wrappers)
- **Design Tokens/Theme:** `lib/design_system/theme/`

Enforce **one primary class per file**, naming the file after the class in lowercase snake_case.

---

## 2. Mathematical Determinism & Proportional Scaling

To prevent loose, guessing-game layout structures, use mathematical proportions mapped from a defined **Base Design Canvas Size** (e.g. Width `393` / Height `852` pt):

### A. Responsive Scaling Helper
Define scaling factors dynamically relative to the reference base screen width/height to preserve exact proportions on all screen sizes:
```dart
extension ResponsiveScale on BuildContext {
  double get screenWidth => MediaQuery.of(this).size.width;
  double get screenHeight => MediaQuery.of(this).size.height;

  // Scale value horizontally relative to a base 393dp width (iPhone 15/16 base canvas)
  double scaleWidth(double value) => (screenWidth / 393.0) * value;
  
  // Scale value vertically relative to a base 852dp height
  double scaleHeight(double value) => (screenHeight / 852.0) * value;
}
```

### B. Nested Corner Radii
Maintain shape harmony by computing nested radii mathematically: `OuterRadius = InnerRadius + PaddingOffset`. This ensures elements fit perfectly inside their cards:
```dart
const double outerCardRadius = 24.0;
const double cardPadding = 16.0;
const double innerElementRadius = outerCardRadius - cardPadding; // Resolves to 8.0
```

---

## 3. Reusable Visual Assets & Layout Snippets

### A. Tactile Press Feedback (Squishy UI Wrapper)
Wrap all interactive elements in a custom stateful wrapper to scale down slightly on tap:
```dart
class SquishyButtonWrapper extends StatefulWidget {
  final Widget child;
  final VoidCallback onTap;

  const SquishyButtonWrapper({required this.child, required this.onTap, super.key});

  @override
  State<SquishyButtonWrapper> createState() => _SquishyButtonWrapperState();
}

class _SquishyButtonWrapperState extends State<SquishyButtonWrapper> with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _scaleAnimation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 80),
      reverseDuration: const Duration(milliseconds: 120),
    );
    _scaleAnimation = Tween<double>(begin: 1.0, end: 0.96).animate(
      CurvedAnimation(parent: _controller, curve: Curves.easeInOut),
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTapDown: (_) => _controller.forward(),
      onTapUp: (_) {
        _controller.reverse();
        widget.onTap();
      },
      onTapCancel: () => _controller.reverse(),
      child: ScaleTransition(
        scale: _scaleAnimation,
        child: widget.child,
      ),
    );
  }
}
```

### B. Premium Depth (Layered BoxShadows)
Use soft, layered shadows instead of standard flat elevation:
```dart
final List<BoxShadow> premiumLayeredShadows = [
  BoxShadow(
    color: Colors.black.withOpacity(0.03),
    blurRadius: 24,
    offset: const Offset(0, 8),
  ),
  BoxShadow(
    color: Colors.black.withOpacity(0.015),
    blurRadius: 8,
    offset: const Offset(0, 2),
  ),
];
```

### C. Glassmorphism Card
```dart
ClipRRect(
  borderRadius: BorderRadius.circular(20),
  child: BackdropFilter(
    filter: ImageFilter.blur(sigmaX: 15, sigmaY: 15),
    child: Container(
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.08),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(
          color: Colors.white.withOpacity(0.12),
          width: 1.0,
        ),
      ),
      padding: const EdgeInsets.all(16),
      child: childContent,
    ),
  ),
)
```

---

## 4. Responsive Flutter Typography & Layout Stability

Ensure text wraps cleanly, has explicit limits, and card layouts maintain equal heights under dynamic text lengths:

### A. Controlled Truncation
```dart
Text(
  item.title,
  maxLines: 2,
  overflow: TextOverflow.ellipsis,
  softWrap: true,
  style: Theme.of(context).textTheme.titleMedium,
)
```

### B. Grid Equal Height Layouts
Avoid varying text lengths causing uneven card heights. Inside custom rows or list groups, use flexbox column stretching (`CrossAxisAlignment.stretch`) paired with `IntrinsicHeight` to stretch sibling cards to match the tallest element:
```dart
IntrinsicHeight(
  child: Row(
    crossAxisAlignment: CrossAxisAlignment.stretch, // Forces cards to match height
    children: [
      Expanded(child: PremiumCard(title: 'Short Title')),
      Expanded(child: PremiumCard(title: 'Very Long Title wrapping onto multiple lines')),
    ],
  ),
)
```

### C. Flow-Wrapping Badge Elements
Wrap horizontal metadata arrays in a `Wrap` widget to prevent horizontal overflows (`RenderFlex overflowed`):
```dart
Wrap(
  spacing: 8.0, // horizontal gap
  runSpacing: 4.0, // vertical gap
  children: categories.map((c) => ActionChip(label: Text(c))).toList(),
)
```

### D. Input Validation Shiver (Error Shake)
Provide visual validation feedback on forms:
```dart
class ShakingErrorWrapper extends StatefulWidget {
  final Widget child;
  final Stream<void> triggerStream;

  const ShakingErrorWrapper({required this.child, required this.triggerStream, super.key});

  @override
  State<ShakingErrorWrapper> createState() => _ShakingErrorWrapperState();
}

class _ShakingErrorWrapperState extends State<ShakingErrorWrapper> with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _offsetAnimation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 300),
    );
    _offsetAnimation = TweenSequence<double>([
      TweenSequenceItem(tween: Tween(begin: 0.0, end: 10.0), weight: 1),
      TweenSequenceItem(tween: Tween(begin: 10.0, end: -10.0), weight: 1),
      TweenSequenceItem(tween: Tween(begin: -10.0, end: 6.0), weight: 1),
      TweenSequenceItem(tween: Tween(begin: 6.0, end: -6.0), weight: 1),
      TweenSequenceItem(tween: Tween(begin: -6.0, end: 0.0), weight: 1),
    ]).animate(CurvedAnimation(parent: _controller, curve: Curves.easeInOut));

    widget.triggerStream.listen((_) {
      _controller.forward(from: 0.0);
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _offsetAnimation,
      builder: (context, child) {
        return Transform.translate(
          offset: Offset(_offsetAnimation.value, 0),
          child: widget.child,
        );
      },
      child: widget.child,
    );
  }
}
```

---

## 5. Flutter Screen Prompt Add-On

Include this consolidated block in Flutter briefs:

```text
Flutter-specific UX & Visual constraints:
- Whitespace is a feature: Design with generous, intentional spacing (using strict 8dp spacing multipliers for Paddings and SizedBox gap offsets). Let visual hierarchy emerge naturally from whitespace and scale pairings rather than excessive borders or outline lines.
- Base Design Canvas Scaling: Base calculations must reference a 393x852 dp frame. Scale widths, paddings, and heights proportionally using relative size percentages (e.g. `MediaQuery.of(context).size.width * 0.85`) or a proportional width helper.
- Nested Corner Radii Math: Enforce exact radius nested relationships (`OuterRadius = InnerRadius + PaddingOffset`). Cards with 16dp padding and 24dp outer radius must utilize 8dp radius inner elements.
- Prune visual clutter: Omit non-essential wrappers, card borders, and static helper labels. Every element must earn its place on the screen.
- Layout bones & Native APIs: Use Slivers (SliverAppBar, SliverList, CustomScrollView) to create fluid scrolling transitions rather than nested single-axis list views. Respect safe area metrics using MediaQuery.of(context).padding.top.
- Interactive states: Wrap primary buttons and cards in custom squishy scaling wrappers (compress to 0.96 on tapDown, spring back on tapUp). For inputs, implement a custom horizontal translate shiver animation on validation failure.
- Typography constraints: Always define explicit maxLines, softWrap, and overflow (TextOverflow.ellipsis) behaviors for dynamic text. Card items in horizontal grids must stretch to match vertical heights (using CrossAxisAlignment.stretch or IntrinsicHeight) to prevent uneven card alignments.
- Loading & Switchers: Transition view states (loading, content, empty, error) using AnimatedSwitcher with smooth spring curves. Use skeleton placeholders that match the target content size exactly to prevent visual shifts.
- Meet WCAG AA contrast, support text scaling without clipping, use HapticFeedback.lightImpact on direct user actions, and ensure all tap targets are at least 48x48 dp.
```

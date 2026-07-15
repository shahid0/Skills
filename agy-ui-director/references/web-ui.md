# Web UI Playbook

Use this playbook when generating or refining Web/React/Tailwind user interfaces.

---

## 1. File Placement & Architecture

Maintain a clean separation of concerns and build modular systems:
- **Routes/Pages:** `src/app/` (Next.js App Router) or `src/pages/`
- **Feature Components:** `src/features/<feature>/components/`
- **Reusable UI Components:** `src/components/ui/` (e.g. shadcn primitives)
- **Design Tokens:** Tailwind Config (`tailwind.config.js`) or CSS variables (`src/index.css`)

Enforce **one primary component per file**, naming the file after the component in PascalCase.

---

## 2. Mathematical Determinism & Proportional Scaling

To prevent loose, guessing-game layout structures, use mathematical proportions mapped from a defined **Base Design Canvas Size** (e.g. Width `1440` / Height `900` px):

### A. Dynamic Scaling via CSS Variables
Calculate scaling factor and nested radii dynamically relative to the reference base screen width:
```css
:root {
  --base-canvas-width: 1440;
  
  /* Proportional scale factor relative to standard desktop width */
  --scale-factor: calc(100vw / var(--base-canvas-width));
  
  /* Nested Corner Radii Math: OuterRadius = InnerRadius + PaddingOffset */
  --outer-card-radius: 24px;
  --card-padding: 16px;
  --inner-element-radius: calc(var(--outer-card-radius) - var(--card-padding)); /* 8px */
}
```

### B. Proportional Spacing and Layout (Bones)
In React/HTML, use fractional grid systems, fixed aspect ratios, and padding constraints to preserve composition:
```html
<div class="grid grid-cols-12 gap-6 max-w-[1440px] mx-auto w-full px-6">
  <!-- Asymmetric layout: Sidebar spans 3/12 cols, Main spans 9/12 cols -->
  <aside class="col-span-3 h-full min-h-[400px]">
    <SidebarContent />
  </aside>
  
  <main class="col-span-9 flex flex-col gap-8">
    <!-- Card carousel with aspect ratio constraints -->
    <div class="aspect-[16/9] w-full rounded-[var(--outer-card-radius)] p-[var(--card-padding)] bg-slate-900">
      <div class="rounded-[var(--inner-element-radius)] bg-slate-800 p-4">
        Inner card content
      </div>
    </div>
  </main>
</div>
```

---

## 3. Responsive Web Typography & Layout Stability

Ensure text wraps cleanly, has explicit limits, and card layouts maintain equal heights under dynamic text lengths:

### A. Controlled Truncation and Multi-line Clamping
- **Single-Line Truncation:** Use Tailwind `truncate`.
- **Multi-Line Clamping:** Use Tailwind `line-clamp-N` (e.g. `line-clamp-2`):
```html
<p class="text-sm text-gray-500 line-clamp-2">
  {item.description}
</p>
```

### B. Equal Height Grid Layouts (No Layout Jumps)
Avoid varying text lengths causing uneven card heights. Stretch grid cells to match tallest sibling height:
*   **Grid Stretching:** Set `grid items-stretch`. Use `flex-grow` on card bodies to force action buttons to align perfectly:
```html
<div class="grid grid-cols-1 md:grid-cols-3 items-stretch gap-6">
  <div class="flex flex-col justify-between p-6 bg-white rounded-2xl shadow">
    <h3 class="text-lg font-bold">Short Title</h3>
    <p class="flex-grow text-sm text-gray-600 my-4">Brief body.</p>
    <button class="w-full py-2 bg-blue-600 rounded-xl text-white">Action</button>
  </div>
  <div class="flex flex-col justify-between p-6 bg-white rounded-2xl shadow">
    <h3 class="text-lg font-bold">Very Long Title Wrapping Multiple Lines</h3>
    <p class="flex-grow text-sm text-gray-600 my-4">Longer body that expands card height.</p>
    <button class="w-full py-2 bg-blue-600 rounded-xl text-white">Action</button>
  </div>
</div>
```

### C. Word Wrapping & Text Breaks
Prevent unspaced text (like URLs, raw hashes, or emails) from overflowing card containers. Use `break-words` or `break-all` to force wrapping:
```html
<a href={url} class="text-xs text-blue-500 break-all hover:underline">
  {url}
</a>
```

### D. Fluid Typography Scale (CSS clamp)
For headings that must scale smoothly with the viewport without manual breakpoint overrides, use `clamp()`:
```html
<h1 class="font-bold text-[clamp(1.5rem,4vw,2.5rem)] leading-tight">
  Dynamic Heading
</h1>
```

---

## 4. Web Screen Prompt Add-On

Include this consolidated block in Web briefs:

```text
Web-specific UX & Visual constraints:
- Whitespace is a feature: Design with generous, intentional spacing (using Tailwind spacing scale, e.g., p-8, space-y-6, gap-8). Let visual hierarchy emerge naturally from whitespace alignment and scale differences rather than borders or dividers.
- Base Design Canvas Scaling: Base desktop layouts on a 1440x900 px frame. Use CSS variables or responsive Tailwind grids (`grid-cols-12`, `aspect-*`) to compute paddings and card sizes proportionally.
- Nested Corner Radii Math: Enforce exact radius nested relationships (`OuterRadius = InnerRadius + PaddingOffset`). Cards with 16px padding and 24px outer radius must utilize 8px radius inner elements.
- Prune visual clutter: Omit non-essential backgrounds, card borders, and helper caption blocks. Every element must earn its place on the screen.
- Layout bones: Build clean flexbox and grid layouts. Use grid columns and flex stretching (`items-stretch`, `flex-1`) to align cards and content blocks to equal sibling heights, preventing visual layout jumps.
- Interactive states: Wrap interactive controls in tactile "squishy" classes (`active:scale-[0.96] transition-transform duration-100 ease-out`). Support keyboard accessibility with crisp outlines (`outline-none focus-visible:ring-2 focus-visible:ring-offset-2`).
- Typography constraints: Always set explicit text truncation (`truncate`) or line clamping (`line-clamp-N`). Use `break-words` or `break-all` to prevent unspaced text (URLs, emails) from breaking card containers.
- Transitions: Swap Mutual state layouts (loading, content, empty, error) with smooth CSS transitions or spring-like animations. Skeletons must match final layout dimensions exactly.
- Meet WCAG AA contrast ratios, support text scaling without clipping, and ensure touch hit sizes are at least 44px (preferably 48px).
```

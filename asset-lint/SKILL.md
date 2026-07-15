---
name: "asset-lint"
description: "Compile and audit asset catalogs (actool) and Interface Builder storyboards (ibtool) for warnings and errors."
---

# Asset & Interface Builder Linter Skill (asset-lint)

## Overview

Use this skill to compile, audit, and troubleshoot asset catalogs (`.xcassets`) and Interface Builder documents (`.storyboard`, `.xib`) in iOS, macOS, watchOS, and tvOS projects. It leverages Xcode's command-line tools (`actool`, `ibtool`, `plutil`) to run syntax, layout constraint, color catalog, and localization checks.

> [!IMPORTANT]
> **Understand the two distinct levels of checking this skill performs:**
>
> 1. **Compiler Diagnostics (actool / ibtool):** These are real build-time errors and warnings emitted by Xcode's own asset compiler and IB compiler. They represent broken or invalid assets that will fail in App Store submission or produce a bad user experience. These MUST be fixed.
>
> 2. **Custom Policy Linting (compile_auditor.py + lint_rules.json):** These are agent-defined policy rules (e.g. "every color set must have both Light and Dark variants") that are *not* enforced by the compiler. They are best-practice checks configurable via `resources/lint_rules.json`. Violations are warnings, not blockers, unless your team policy makes them so.
>
> Never conflate the two — do not escalate a policy lint warning as if it were a compiler error.

---

## Required First Moves

1. **Verify Environment**: Check that Xcode developer command line tools are active and running:
   ```bash
   xcode-select -p
   ```
2. **Find Target Assets**: Scan the workspace to locate `.xcassets` directories and Interface Builder files:
   ```bash
   find . -name "*.xcassets"
   find . -name "*.storyboard" -o -name "*.xib"
   ```
3. **Check Custom Rules Configuration**: Ensure `resources/lint_rules.json` exists or pass a custom rules file to target specific warnings. This configures policy checks only, not compiler checks.

---

## Guidelines and Best Practices

### 1. Asset Catalog Compiler Checks (`actool`)
The following are **compiler-enforced** checks. Failures here are build blockers:
*   **Unassigned Children**: Ensure every asset under an image set or color set is assigned to a specific screen scale or device idiom. Unassigned images inflate the compiled application bundle sizes.
*   **Image Dimensions**: Verify that `@1x`, `@2x`, and `@3x` images exactly match their expected scale proportions. E.g., if `@1x` is 20x20 pixels, `@2x` must be 40x40 pixels and `@3x` must be 60x60 pixels.
*   **App Icon Sizes**: Verify that the `AppIcon` asset contains all required sizes for target devices (e.g., iPhone, iPad, Apple Watch) to prevent App Store rejection.
*   **Asset Naming**: Ensure image/color name files do not contain spaces, uppercase-only acronyms that clash, or special characters.

### 2. Asset Catalog Policy Checks (Custom Rules)
The following are **policy-level** checks configurable in `lint_rules.json`. These are warnings, not build failures:
*   **Color Sets**: Ensure every named color catalog contains both Light and Dark appearance variations (and optionally Any Appearance) if dark mode is supported.

### 3. Interface Builder Compiler Checks (`ibtool`)
The following are **compiler-enforced** checks. Failures here are build blockers:
*   **Auto Layout Constraints**: Pay close attention to warnings regarding:
    *   *Ambiguous constraints*: Constraints that don't uniquely define a view's position or size.
    *   *Conflicting constraints*: Constraints that cannot be satisfied simultaneously at runtime.
    *   *Frame mismatches*: Difference between design-time layout frame and runtime Auto Layout frame.
*   **Launch Screen Constraints**:
    *   Launch screens (`LaunchScreen.storyboard`) must contain **only static UI elements**.
    *   They **must not** use custom view subclasses or controllers (doing so will fail compilation or result in a black screen during launch).
    *   Limit launch screen assets to system fonts and images that are pre-loaded in the asset catalog.

### 4. Interface Builder Policy Checks
The following are **policy-level** recommendations:
*   **Localization Warnings**:
    *   Verify that text-based views (UILabels, UIButtons, etc.) in storyboards are linked to unique object IDs in `.strings` files.
    *   Extract strings files regularly to ensure new components are localized:
        ```bash
        xcrun ibtool --export-strings-file NewStrings.strings Main.storyboard
        ```

### 5. Strings & Plist Validation (`plutil`)
*   If compilation fails with mysterious syntax or parsing errors on localization strings, run:
    ```bash
    plutil -lint path/to/*.strings
    ```
    Correct any Old-Style plist parser errors (such as missing semicolons at the end of lines or unescaped quotes).

---

## Workflow

1. **Run Automatic Audit**: Use the compilation linter helper script to check the entire workspace or specific modified files:
   ```bash
   python3 scripts/compile_auditor.py --assets path/to/Assets.xcassets --storyboards path/to/Base.lproj
   ```
2. **Triage the Report**:
   - **Compiler errors/warnings** (`COMPILER_ERROR`, `COMPILER_WARNING` categories): Fix immediately — these will cause build or runtime failures.
   - **Policy warnings** (`POLICY_WARNING` category): Review against team/project standards; prioritize as needed.
3. **Format Output**:
   *   Use `--format text` for standard stdout (compatible with Xcode build phase parsing).
   *   Use `--format json` for CI/CD status collection.
   *   Use `--format markdown` for Pull Request summaries.
4. **Enforce in Hook**: Integrate the pre-commit hook (see [examples/usage_example.md](examples/usage_example.md)) to guarantee no broken layouts are checked into the codebase.

---

## References
*   Command flags & details: [references/actool_ibtool_ref.md](references/actool_ibtool_ref.md)
*   Sample usage templates: [examples/usage_example.md](examples/usage_example.md)
*   Custom lint configuration: [resources/lint_rules.json](resources/lint_rules.json)

---
name: clean-architecture
description: Enforce Feature-Based Clean Architecture and the Facade Pattern across Swift, Kotlin, Dart/Flutter, and TypeScript. Triggers when creating, refactoring, or reviewing codebase structures, defining services or repositories, or applying design patterns.
---

# Feature-Based Clean Architecture & Facade Pattern Guidelines

You are an expert software architect. You MUST enforce a **Feature-Based Clean Architecture** integrated with the **Facade Pattern** across all supported platforms (iOS/Swift, Android/Kotlin/KMP, Flutter/Dart, Web/TypeScript).

---

## 1. REASONING BUDGET (MANDATORY CHAIN-OF-THOUGHT)

Before writing any code, modifying files, or proposing refactoring plans, you MUST outline your reasoning and planning process.

### <reasoning_protocol>
You MUST structure your initial thoughts within `<thinking>` XML tags. Within this block, you MUST:
1. Identify the architectural layers (View, ViewModel, Service, Repository, API, Storage, Core) impacted by the user's request.
2. Search the codebase for duplicate logic, existing models, or partial implementations.
3. List the down-dependency impact and ensure the dependency flow remains strictly downward.
4. Verify that you have read the supplementary reference files under `references/` or `examples/` if you need detailed layer rules or code patterns.
</reasoning_protocol>

---

## 2. OPERATIONAL DIRECTIVES

### <preflight_checks>
* **Search First:** You MUST run a `grep_search` or `list_dir` to verify if similar code, models, or service logic already exist before writing new files.
* **Progressive Context Loading:** If implementing layers or writing facade classes, you MUST read the detailed architectural constraints at [architecture_guide.md](references/architecture_guide.md) and refer to concrete implementation patterns at [cross_platform_patterns.md](examples/cross_platform_patterns.md).
* **Dependency Auditing:** You MUST inspect dependency files (`pubspec.yaml`, `package.json`, `build.gradle.kts`, `Package.swift`) to verify library versions and import scopes before introducing new imports.
</preflight_checks>

### <architectural_constraints>
* **Downward Dependency Flow:** View -> ViewModel -> Service -> Repository -> API Client/Storage -> Core Infrastructure. Lower layers MUST NEVER depend on or import from higher layers.
* **Separation of Concerns:** Views MUST NOT contain business logic or networking. ViewModels MUST NOT build HTTP requests or queries. Services MUST NOT depend on UI frameworks. Repositories MUST hide underlying data sources.
* **One Declaration Per File:** You MUST define exactly one primary class, struct, actor, interface, or enum per source file.
* **Semantic Naming:** You MUST name files exactly after their primary declaration (e.g. `UserRepositoryImpl.kt` for `class UserRepositoryImpl`).
</architectural_constraints>

### <facade_pattern_rules>
* **Repository Facades:** You MUST encapsulate local storage and remote API clients under Repository implementations, presenting a single clean interface to Services.
* **Service Facades:** You MUST coordinate complex multi-repository workflows inside Service classes, exposing a single simplified method to ViewModels.
* **Infrastructure Facades:** You MUST wrap third-party SDK dependencies (Firebase, Sentry, local storage frameworks) under custom interfaces in `Core/` to prevent vendor-specific code from spreading.
</facade_pattern_rules>

---

## 3. STRICT VERIFICATION GATE

### <verification_gate>
Before finalizing your response or completing a task, you MUST verify your work by running the following checks:
- [ ] **Search Validation:** Did you verify that no duplicate files, services, or models were introduced?
- [ ] **Dependency Audit:** Does all code import only downward layers? Circular references MUST be absent.
- [ ] **Facade Wrap:** Are raw API clients, database schemas, and external SDKs properly hidden behind facade interfaces?
- [ ] **Code Readiness:** Is all code fully implemented? You MUST NOT output placeholders, stub methods, or `TODO` comments.
- [ ] **Compilation Pass:** Run the project-specific verification command (e.g., `dart analyze`, `npm run lint`, `gradlew build`, `xcodebuild`) and confirm zero compiler errors or linter warnings.
</verification_checklist>
</verification_gate>

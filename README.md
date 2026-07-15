# Shahid's Agent Skills

[![skills.sh](https://skills.sh/b/shahid0/Skills)](https://skills.sh/shahid0/Skills)

A focused collection of reusable skills for AI coding agents. The repository is organized in the format supported by [skills.sh](https://www.skills.sh/): every skill lives in its own top-level directory and includes a `SKILL.md` definition plus any supporting examples, references, scripts, or resources.

## Install

Install the complete collection:

```bash
npx skills add shahid0/Skills
```

Install one skill only:

```bash
npx skills add shahid0/Skills --skill <skill-name>
```

The commands below install each skill individually.

## Skills

### Architecture and engineering

| Skill | What it does | Install |
| --- | --- | --- |
| [`agentic-se-principles`](./agentic-se-principles/) | Applies CUPID, Clean Architecture, DDD, contract-first design, API-first design, dependency injection, composition over inheritance, and observability-first principles. | `npx skills add shahid0/Skills --skill agentic-se-principles` |
| [`clean-architecture`](./clean-architecture/) | Structures Swift, Kotlin, Flutter, and TypeScript applications with feature-based Clean Architecture and Facade patterns. | `npx skills add shahid0/Skills --skill clean-architecture` |
| [`code-reviewer`](./code-reviewer/) | Reviews code, commits, files, and pull requests for real defects, risks, regressions, and maintainability problems. | `npx skills add shahid0/Skills --skill code-reviewer` |

### UI and design engineering

| Skill | What it does | Install |
| --- | --- | --- |
| [`agy-ui-director`](./agy-ui-director/) | Directs the `agy` CLI to build premium Flutter, SwiftUI, and web interfaces with polished layouts, motion, and micro-interactions. | `npx skills add shahid0/Skills --skill agy-ui-director` |
| [`flutter-design-eng`](./flutter-design-eng/) | Builds tactile Flutter interfaces with spring physics, gesture interactions, responsive layouts, micro-interactions, and performance awareness. | `npx skills add shahid0/Skills --skill flutter-design-eng` |
| [`swiftui-design-eng`](./swiftui-design-eng/) | Creates polished SwiftUI interfaces with fluid springs, gesture velocity handoff, keyframe animations, responsive layouts, and haptics. | `npx skills add shahid0/Skills --skill swiftui-design-eng` |

### Apple resources and localization

| Skill | What it does | Install |
| --- | --- | --- |
| [`asset-lint`](./asset-lint/) | Compiles and audits `.xcassets`, storyboards, XIBs, colors, app icons, constraints, and localization resources with Xcode tools. | `npx skills add shahid0/Skills --skill asset-lint` |
| [`swift-typed-assets`](./swift-typed-assets/) | Replaces fragile string-based asset access with compiler-checked `ImageResource` and `ColorResource` references across Apple platforms. | `npx skills add shahid0/Skills --skill swift-typed-assets` |
| [`swiftui-localize`](./swiftui-localize/) | Extracts, translates, merges, and verifies SwiftUI String Catalogs using `xcstringstool` and context-aware translation workflows. | `npx skills add shahid0/Skills --skill swiftui-localize` |

### Device, simulator, and test workflows

| Skill | What it does | Install |
| --- | --- | --- |
| [`xcode-devicectl`](./xcode-devicectl/) | Manages physical Apple devices with `devicectl`, including pairing, app installation, process launching, logs, and diagnostics. | `npx skills add shahid0/Skills --skill xcode-devicectl` |
| [`xcode-simulator-automation`](./xcode-simulator-automation/) | Boots simulators, installs and launches apps, sends mock pushes, overrides GPS coordinates, and records simulator video. | `npx skills add shahid0/Skills --skill xcode-simulator-automation` |
| [`xcode-simulator-sandbox`](./xcode-simulator-sandbox/) | Locates simulator app containers and safely inspects or edits SQLite databases, plist files, and UserDefaults. | `npx skills add shahid0/Skills --skill xcode-simulator-sandbox` |
| [`xcode-test-self-heal`](./xcode-test-self-heal/) | Runs Xcode tests, parses `.xcresult` failures and attachments, diagnoses causes, and iterates toward narrow fixes. | `npx skills add shahid0/Skills --skill xcode-test-self-heal` |
| [`xcode-ui-snapshots`](./xcode-ui-snapshots/) | Captures UI snapshots across devices, appearances, Dynamic Type sizes, and status bar states for regression testing or marketing assets. | `npx skills add shahid0/Skills --skill xcode-ui-snapshots` |

### Build and performance

| Skill | What it does | Install |
| --- | --- | --- |
| [`xcode-trace-profiler`](./xcode-trace-profiler/) | Records and analyzes `xctrace` performance traces to identify CPU, memory, SwiftUI rendering, concurrency, and Flutter bottlenecks. | `npx skills add shahid0/Skills --skill xcode-trace-profiler` |
| [`xcode-version-bump`](./xcode-version-bump/) | Updates marketing and build versions with `agvtool`, then builds, archives, signs, and exports native application packages with `xcodebuild`. | `npx skills add shahid0/Skills --skill xcode-version-bump` |

## Repository layout

```text
Skills/
├── README.md
├── .gitignore
└── <skill-name>/
    ├── SKILL.md
    ├── agents/       # optional agent metadata
    ├── examples/     # optional usage and code examples
    ├── references/   # optional detailed documentation
    ├── resources/    # optional templates and configuration
    └── scripts/      # optional helper tools
```

## Using a skill

After installation, ask your coding agent to perform a task covered by the skill. The agent will load the matching `SKILL.md` and follow its workflow. Some skills also include executable scripts; read their local usage examples before running commands against a project or device.

## Compatibility and safety

These skills are intended for agents such as Claude Code, Cursor, Windsurf, Codex, and other tools that support the Agent Skills format. Review a skill's instructions and scripts before using it in a sensitive repository or against a physical device. Apple-focused skills generally require Xcode and the relevant command-line tools.

## License

Add the license that matches how you want this collection to be reused.

# Changelog

All notable changes to the Android AI Development Kit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-19

### 🎉 Initial Release

#### Added

**Core Infrastructure**
- Unified `aidk` CLI command with subcommands for all operations
- Python package distribution via PyPI (`pip install android-ai-devkit`)
- Automatic installation to Claude Code projects
- Auto-update checker with 24-hour caching
- Cross-platform installation scripts (Unix/Mac/Windows)

**36 Android Development Skills**
- **Core Architecture** (3): Project setup, Clean Architecture, MVVM
- **UI Development** (4): Jetpack Compose, Navigation, Theming, XML Views
- **Dependency Injection** (2): Hilt, Koin
- **Data Layer** (4): Repository pattern, Room, Retrofit, DataStore
- **JSON Parsing** (2): Moshi, Kotlinx Serialization
- **State Management** (2): StateFlow, One-time events
- **Async & Background** (3): Coroutines, WorkManager, Paging3
- **Testing** (4): Compose testing, Unit testing, MockK, Turbine
- **Build Configuration** (1): Gradle Kotlin DSL
- **Common Features** (5): Permissions, Image loading, Forms validation, List UI, Material Components
- **Utilities** (1): Timber logging
- **Animation** (1): Lottie animations
- **Git Workflow** (4): Atomic commits, SPEC workflow, Conventional commits, Multi-commit features

**Python Automation Tools**
- `aidk spec create` - Interactive/quick SPEC generation with EARS format
- `aidk code generate` - Clean Architecture code generation from SPECs
- `aidk docs sync` - Documentation synchronization and traceability
- `aidk validate` - SPEC document validation
- Automatic Android skill matching from feature descriptions

**CLI Commands**
- `aidk install` - Install skills and tools to projects
- `aidk update` - Check for and install updates
- `aidk version` - Version information
- `aidk skills` - List all available skills
- `aidk spec create/validate` - SPEC management
- `aidk code generate` - Code generation
- `aidk docs sync/verify` - Documentation management
- `aidk info` - System information

**Templates & Examples**
- 3 SPEC templates (feature, API, UI)
- 2 complete example SPECs with generated code
- EARS format requirements (U/S/E/O/N types)

**Documentation**
- Comprehensive README with installation guide
- SPEC-First workflow documentation
- Contribution guidelines
- Real-world usage examples

#### Features

- **SPEC-First Development**: Enforce requirement gathering before implementation
- **Clean Architecture**: Generate three-layer architecture (Domain, Data, Presentation)
- **Traceability**: Automatic SPEC ID tracking in code and tests
- **EARS Format**: Unambiguous requirements (Ubiquitous, State-driven, Event-driven, Optional, Negative)
- **Skill Matching**: AI-powered matching of features to relevant Android skills
- **2025 Best Practices**: Modern Android development with latest libraries
- **Claude Code Integration**: Seamless integration with Claude Code IDE
- **Cross-Platform**: Works on macOS, Linux, and Windows

#### Technical Details

- Python 3.8+ required
- Click-based CLI framework
- Rich terminal formatting
- Jinja2 template engine for code generation
- YAML frontmatter for SPEC metadata
- Semantic versioning
- 24-hour update check caching

---

## [Unreleased]

### Planned Features
- VS Code extension for SPEC management
- Web UI for SPEC creation
- CI/CD templates (GitHub Actions, GitLab CI)
- Multi-module project support
- SPEC version control and diffing
- Tree-sitter based code analysis
- Additional language support (Compose Multiplatform)

---

## Version History

- [1.0.0] - 2025-01-19: Initial release with 36 skills, unified CLI, and PyPI distribution

---

[1.0.0]: https://github.com/yourusername/android-ai-devkit/releases/tag/v1.0.0
[Unreleased]: https://github.com/yourusername/android-ai-devkit/compare/v1.0.0...HEAD

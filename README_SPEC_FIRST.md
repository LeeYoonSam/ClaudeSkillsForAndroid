# SPEC-First Development System

AI-powered SPEC-First development framework for Android applications, combining EARS-format specifications with automated code generation and documentation synchronization.

## Overview

This project extends the Claude Code Android skills with a **SPEC-First development workflow** that ensures:

✅ **Clear Requirements** - EARS format eliminates ambiguity
✅ **Automated Code Generation** - Generate Clean Architecture code from specs
✅ **Perfect Traceability** - Every requirement maps to code and tests
✅ **Living Documentation** - Docs stay synchronized automatically
✅ **Quality Assurance** - Automated validation at every step

---

## Quick Start

### 1. Create a SPEC

```bash
python3 tools/spec_builder.py interactive
```

Follow the interactive prompts to create a structured specification.

### 2. Generate Code

```bash
python3 tools/code_builder.py generate specs/examples/your-feature/SPEC.md \
  --output examples/your-app \
  --package com.yourcompany.app
```

### 3. Sync Documentation

```bash
python3 tools/doc_syncer.py sync specs/examples/your-feature/SPEC.md \
  --code examples/your-app
```

### 4. Validate

```bash
python3 tools/validate_specs.py specs/examples/your-feature/SPEC.md
```

---

## System Architecture

### Three AI Agents

#### 1. **spec-builder** - SPEC Creation Agent
- Analyzes user requirements
- Generates EARS-format specifications
- Auto-matches relevant Android skills
- Creates structured SPEC.md files

#### 2. **code-builder** - Code Generation Agent
- Parses SPEC documents
- Loads related Android skills
- Generates Clean Architecture code
- Creates tests with SPEC ID annotations

#### 3. **doc-syncer** - Documentation Sync Agent
- Verifies SPEC-code alignment
- Updates traceability matrices
- Generates README and architecture diagrams
- Reports implementation status

### EARS Requirements Format

**E**asy **A**pproach to **R**equirements **S**yntax

| Type | Format | Example |
|------|--------|---------|
| **Ubiquitous** | The system shall [requirement] | The system shall validate user email |
| **State-driven** | WHILE [state], the system shall [requirement] | WHILE user is logged in, the system shall show profile |
| **Event-driven** | WHEN [event], the system shall [requirement] | WHEN user clicks login, the system shall authenticate |
| **Optional** | WHERE [feature], the system shall [requirement] | WHERE biometric is enabled, the system shall offer fingerprint |
| **Unwanted** | IF [condition], THEN the system shall NOT [behavior] | IF password is wrong, THEN the system shall NOT log in user |

---

## Project Structure

```
claude-skills/
├── .claude/
│   └── skills/                      # 26 Android skills
│       ├── android-clean-architecture/
│       ├── android-compose-ui/
│       └── ...
│
├── specs/                           # SPEC documents
│   ├── templates/                   # SPEC templates
│   │   ├── feature-spec.md         # Feature specification template
│   │   ├── api-spec.md             # API specification template
│   │   └── ui-spec.md              # UI specification template
│   └── examples/                    # Example SPECs
│       └── user-authentication/
│           ├── SPEC.md             # Main specification
│           ├── README.md           # Implementation status (auto-generated)
│           └── architecture.md     # Architecture diagram (auto-generated)
│
├── tools/                           # Python agents
│   ├── spec_builder.py             # SPEC creation agent
│   ├── code_builder.py             # Code generation agent
│   ├── doc_syncer.py               # Documentation sync agent
│   └── validate_specs.py           # SPEC validation
│
├── docs/
│   └── guides/
│       └── workflow-guide.md       # Complete workflow guide
│
├── examples/                        # Generated code examples
│   └── generated-auth/             # Example: User Authentication
│
├── requirements.txt                 # Python dependencies
├── CONTRIBUTING.md                  # Contribution guidelines
└── README.md                        # Main documentation (Android skills)
```

---

## Features

### 1. SPEC Creation

**Interactive Mode**:
```bash
python3 tools/spec_builder.py interactive
```

**Quick Mode**:
```bash
python3 tools/spec_builder.py create "Feature Name" \
  --purpose "Feature purpose" \
  --requirements "req 1" "req 2" "req 3"
```

**Output**:
- Structured SPEC.md with EARS requirements
- Auto-matched Android skills (from 26 available)
- Unique SPEC ID (e.g., SPEC-001)
- Implementation checklist
- Traceability matrix template

### 2. Code Generation

**Generate Clean Architecture code**:
```bash
python3 tools/code_builder.py generate SPEC.md \
  --output ./output \
  --package com.example.app
```

**Generates**:
- **Domain Layer**: Models, Use Cases, Repository Interfaces
- **Data Layer**: API, DTOs, Repository Implementation
- **Presentation Layer**: ViewModel, State, Compose Screen
- **Tests**: Unit tests with SPEC ID references

**All code includes SPEC ID annotations**:
```kotlin
// SPEC-001: User Authentication
// REQ-001-U-01: Validate user credentials
class LoginUseCase @Inject constructor(
    private val repository: AuthRepository
) {
    suspend operator fun invoke(email: String, password: String): Result<User> {
        // Implementation
    }
}
```

### 3. Documentation Sync

**Verify alignment**:
```bash
python3 tools/doc_syncer.py verify SPEC.md --code ./code
```

**Sync documentation**:
```bash
python3 tools/doc_syncer.py sync SPEC.md --code ./code
```

**Updates**:
- Traceability matrix in SPEC.md
- README.md with implementation status
- Architecture diagram
- Lists implemented vs. missing requirements

### 4. Validation

**Validate single SPEC**:
```bash
python3 tools/validate_specs.py SPEC.md
```

**Validate all SPECs**:
```bash
python3 tools/validate_specs.py --all
```

**Checks**:
- YAML frontmatter structure
- Required sections present
- EARS requirement format
- Requirement ID format
- SPEC ID consistency

---

## Android Skills (26 Total)

### Architecture (3)
- `android-clean-architecture` - Three-layer architecture
- `android-mvvm-architecture` - MVVM with ViewModel
- `android-project-setup` - Project initialization

### UI (7)
- `android-compose-ui` - Jetpack Compose
- `android-compose-navigation` - Navigation
- `android-compose-theming` - Material 3 theming
- `android-compose-testing` - UI testing
- `android-material-components` - Material components
- `android-list-ui` - LazyColumn/RecyclerView
- `android-forms-validation` - Form validation
- `android-xml-views` - XML views

### Dependency Injection (2)
- `android-hilt-di` - Hilt DI
- `android-koin-di` - Koin DI

### Data (4)
- `android-repository-pattern` - Repository pattern
- `android-database-room` - Room database
- `android-networking-retrofit` - Retrofit API
- `android-datastore` - DataStore preferences

### State Management (2)
- `android-stateflow` - StateFlow
- `android-one-time-events` - One-time events

### Async & Background (3)
- `android-coroutines` - Kotlin Coroutines
- `android-workmanager` - Background work
- `android-paging3` - Pagination

### Testing (2)
- `android-compose-testing` - Compose testing
- `android-unit-testing` - Unit testing

### Build (1)
- `android-gradle-config` - Gradle configuration

### Features (2)
- `android-permissions` - Runtime permissions
- `android-image-loading` - Coil/Glide

---

## Workflow Example

### Scenario: Implement User Authentication

#### Step 1: Create SPEC
```bash
python3 tools/spec_builder.py create "User Authentication" \
  --purpose "Enable secure login with email/password" \
  --requirements \
    "validate email format" \
    "validate password strength" \
    "authenticate with backend API" \
    "store session securely" \
    "redirect after login"
```

**Output**: `specs/examples/user-authentication/SPEC.md`
- SPEC ID: SPEC-001
- 5 requirements (REQ-001-U-01 through REQ-001-U-05)
- 7 related skills auto-matched

#### Step 2: Generate Code
```bash
python3 tools/code_builder.py generate \
  specs/examples/user-authentication/SPEC.md \
  --output examples/auth-app \
  --package com.mycompany.auth
```

**Generated**:
- 9 Kotlin source files (domain, data, presentation)
- 1 test file
- All annotated with SPEC IDs

#### Step 3: Implement Logic

Edit generated files to add business logic:
- Implement `LoginUseCase` with validation
- Add API integration in `AuthRepositoryImpl`
- Create UI in `LoginScreen.kt`

#### Step 4: Sync Docs
```bash
python3 tools/doc_syncer.py sync \
  specs/examples/user-authentication/SPEC.md \
  --code examples/auth-app
```

**Result**:
- Traceability matrix shows 5/5 implemented (100%)
- README generated with file list
- Architecture diagram created

#### Step 5: Validate
```bash
python3 tools/validate_specs.py specs/examples/user-authentication/SPEC.md
```

**Output**: ✓ SPEC is valid!

---

## Benchmarked from MoAI-ADK

This system is inspired by [MoAI-ADK](https://github.com/modu-ai/moai-adk) with key features:

| Feature | MoAI-ADK | This Project |
|---------|----------|--------------|
| SPEC-First | ✅ | ✅ |
| EARS Format | ✅ | ✅ |
| AI Agents | 19 agents | 3 focused agents |
| Skills | 125+ general | 26 Android-specific |
| Code Generation | ✅ | ✅ Clean Architecture |
| Living Docs | ✅ | ✅ Traceability matrix |
| Auto Validation | ✅ | ✅ SPEC validation |
| Language | Python, Multi-language | Python + Kotlin |

**Key Differences**:
- **Focused**: Android-only (vs. general purpose)
- **Specialized**: 26 curated Android skills
- **Opinionated**: Clean Architecture enforced
- **Integrated**: Works with existing Claude Code skills

---

## Requirements

### Python Dependencies

```bash
pip install -r requirements.txt
```

```
# Core (no external deps needed for basic operation)
# Optional: For future enhancements
pyyaml>=6.0.1          # YAML parsing
markdown>=3.5.1        # Markdown processing
click>=8.1.7           # CLI framework
rich>=13.7.0           # Terminal formatting
```

### Android Development

- Android Studio (for using generated code)
- Kotlin 2.1.0+
- Gradle 8.0+

---

## Documentation

### Guides

- [**Workflow Guide**](docs/guides/workflow-guide.md) - Complete end-to-end workflow
- [**CONTRIBUTING.md**](CONTRIBUTING.md) - How to contribute
- [**Android Skills README**](README.md) - Original 26 Android skills documentation

### Examples

- [User Authentication SPEC](specs/examples/user-authentication/SPEC.md) - Complete example
- [Generated Code](examples/generated-auth/) - Clean Architecture output

### Templates

- [Feature SPEC Template](specs/templates/feature-spec.md) - Full feature specification
- [API SPEC Template](specs/templates/api-spec.md) - API documentation
- [UI SPEC Template](specs/templates/ui-spec.md) - UI/UX specification

---

## Roadmap

### Phase 1: Foundation ✅ (Current)
- [x] Directory structure
- [x] EARS SPEC templates
- [x] spec_builder agent
- [x] code_builder agent
- [x] doc_syncer agent
- [x] Validation scripts
- [x] Workflow documentation

### Phase 2: Enhancement (Next)
- [ ] Slash commands for Claude Code
- [ ] Interactive skill selection UI
- [ ] SPEC diff tool
- [ ] Code modification (not just generation)
- [ ] Advanced validation rules

### Phase 3: Integration (Future)
- [ ] CI/CD integration examples
- [ ] GitHub Actions workflow
- [ ] VS Code extension
- [ ] SPEC version control
- [ ] Multi-module project support

### Phase 4: Advanced (Future)
- [ ] AI-assisted requirement refinement
- [ ] Automated test generation from scenarios
- [ ] Performance requirement tracking
- [ ] Security requirement validation
- [ ] SPEC → PRD conversion

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- SPEC-First workflow rules
- Code style guidelines
- Pull request process
- Testing requirements

---

## License

MIT License - See LICENSE file

---

## Credits

### Inspired By
- [MoAI-ADK](https://github.com/modu-ai/moai-adk) - SPEC-First TDD framework
- [EARS](https://www.researchgate.net/publication/220437600_Easy_Approach_to_Requirements_Syntax_EARS) - Requirements syntax methodology

### Built With
- Python 3.x
- Kotlin
- Jetpack Compose
- Claude Code

---

## Support

- **Issues**: [GitHub Issues](../../issues)
- **Discussions**: [GitHub Discussions](../../discussions)
- **Examples**: See `specs/examples/` and `examples/`

---

## Quick Reference

### Create SPEC
```bash
python3 tools/spec_builder.py interactive
```

### Generate Code
```bash
python3 tools/code_builder.py generate SPEC.md --output ./app
```

### Sync Docs
```bash
python3 tools/doc_syncer.py sync SPEC.md --code ./app
```

### Validate
```bash
python3 tools/validate_specs.py SPEC.md
```

---

**Transform requirements into production-ready Android apps with AI-powered SPEC-First development.**

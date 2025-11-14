# SPEC-First Development Workflow Guide

Complete guide to the SPEC-First development workflow for Android projects.

## Table of Contents

1. [Overview](#overview)
2. [Workflow Phases](#workflow-phases)
3. [Complete Example](#complete-example)
4. [Best Practices](#best-practices)
5. [Common Issues](#common-issues)

---

## Overview

The SPEC-First workflow ensures clear requirements before implementation, reducing costly rework and maintaining perfect traceability from requirements to code.

### Key Benefits

✅ **Clear Requirements**: EARS format eliminates ambiguity
✅ **No Rework**: Catch issues before coding
✅ **Perfect Traceability**: Every line of code maps to a requirement
✅ **Auto Documentation**: Docs stay in sync automatically
✅ **Quality Gates**: Automated validation ensures consistency

---

## Workflow Phases

```
Phase 1: SPEC Creation
    ↓
Phase 2: Code Generation
    ↓
Phase 3: Documentation Sync
    ↓
Phase 4: Validation
```

### Phase 1: SPEC Creation

**Tool**: `spec_builder.py`

**Input**: Feature description + Requirements

**Output**: Structured SPEC.md with EARS requirements

#### Interactive Mode (Recommended)

```bash
python3 tools/spec_builder.py interactive
```

Follow prompts:
1. Enter feature name
2. Describe purpose
3. List requirements (one per line)
4. Review matched Android skills
5. Confirm and generate

#### Quick Mode

```bash
python3 tools/spec_builder.py create "Feature Name" \
  --purpose "Why this feature exists" \
  --requirements "requirement 1" "requirement 2" "requirement 3"
```

#### What Gets Generated

```
specs/examples/feature-name/
└── SPEC.md
    ├── YAML frontmatter (metadata, skills)
    ├── Overview (purpose, scope)
    ├── Requirements (EARS format)
    │   ├── Ubiquitous (core functionality)
    │   ├── State-driven (conditional)
    │   ├── Event-driven (reactive)
    │   ├── Optional (nice-to-have)
    │   └── Unwanted (error cases)
    ├── User stories
    ├── Architecture (domain, data, presentation)
    ├── Related skills (auto-matched)
    ├── Implementation checklist
    └── Traceability matrix
```

---

### Phase 2: Code Generation

**Tool**: `code_builder.py`

**Input**: SPEC.md file

**Output**: Complete Clean Architecture code

#### Generate Code

```bash
python3 tools/code_builder.py generate \
  specs/examples/feature-name/SPEC.md \
  --output examples/generated-feature \
  --package com.example.app
```

#### What Gets Generated

```
examples/generated-feature/
└── src/
    ├── main/kotlin/com/example/app/
    │   ├── domain/
    │   │   ├── model/
    │   │   │   └── Feature.kt           # Domain model
    │   │   ├── usecase/
    │   │   │   └── GetFeatureUseCase.kt # Business logic
    │   │   └── repository/
    │   │       └── FeatureRepository.kt # Repository interface
    │   ├── data/
    │   │   ├── remote/
    │   │   │   ├── FeatureApi.kt        # Retrofit API
    │   │   │   └── FeatureDto.kt        # DTOs + mappers
    │   │   └── repository/
    │   │       └── FeatureRepositoryImpl.kt
    │   └── presentation/
    │       ├── viewmodel/
    │       │   └── FeatureViewModel.kt  # @HiltViewModel
    │       ├── state/
    │       │   └── FeatureState.kt      # State + Actions + Events
    │       └── ui/
    │           └── FeatureScreen.kt     # Compose UI
    └── test/kotlin/com/example/app/
        └── domain/
            └── FeatureUseCaseTest.kt    # Unit tests
```

#### Code Annotations

Every generated file includes SPEC ID comments:

```kotlin
// SPEC-001: Feature name
// REQ-001-U-01: Specific requirement
class FeatureRepository {
    // Implementation
}
```

---

### Phase 3: Documentation Sync

**Tool**: `doc_syncer.py`

**Input**: SPEC.md + Generated code

**Output**: Updated docs, traceability matrix

#### Sync Documentation

```bash
python3 tools/doc_syncer.py sync \
  specs/examples/feature-name/SPEC.md \
  --code examples/generated-feature
```

#### What Happens

1. **Verification**: Analyzes code for SPEC references
2. **Traceability**: Updates matrix in SPEC.md
3. **README**: Generates feature README
4. **Architecture**: Creates architecture diagram
5. **Reports**: Shows implementation status

#### Generated Documents

```
specs/examples/feature-name/
├── SPEC.md (updated traceability matrix)
├── README.md (implementation status)
└── architecture.md (Clean Architecture diagram)
```

---

### Phase 4: Validation

**Tool**: `validate_specs.py`

**Input**: SPEC.md file(s)

**Output**: Validation report

#### Validate Single SPEC

```bash
python3 tools/validate_specs.py specs/examples/feature-name/SPEC.md
```

#### Validate All SPECs

```bash
python3 tools/validate_specs.py --all
```

#### What Gets Validated

✓ YAML frontmatter structure
✓ Required sections present
✓ EARS requirement format
✓ Requirement ID format (REQ-XXX-Y-ZZ)
✓ SPEC ID consistency
✓ Related skills listed

---

## Complete Example

### Step 1: Create SPEC

```bash
python3 tools/spec_builder.py interactive
```

```
Step 1: Feature Information
Feature name: User Authentication
Purpose: Enable secure login with email/password

Step 2: Requirements
1. validate user email format
2. validate password strength
3. authenticate with backend API
4. store session token securely
5. redirect to home after login
done

Step 3: Identifying related Android skills...
Found 7 related skills:
  1. android-compose-ui (UI): Declarative UI with Jetpack Compose
  2. android-forms-validation (UI): Form input and validation
  3. android-networking-retrofit (Data): REST API with Retrofit
  4. android-datastore (Data): DataStore for preferences
  5. android-hilt-di (DI): Dependency injection with Hilt
  6. android-clean-architecture (Architecture): Three-layer architecture
  7. android-mvvm-architecture (Architecture): MVVM architecture

Step 4: Confirmation
Generate SPEC with these details? (y/n): y

✓ SPEC created successfully!
Location: specs/examples/user-authentication/SPEC.md
SPEC ID: SPEC-001
Requirements: 5
Related Skills: 7
```

### Step 2: Review & Refine SPEC

Open `specs/examples/user-authentication/SPEC.md` and:

1. Add detailed user stories
2. Define data models
3. Specify API contracts
4. Add validation rules
5. Define test criteria

### Step 3: Generate Code

```bash
python3 tools/code_builder.py generate \
  specs/examples/user-authentication/SPEC.md \
  --output examples/auth-app \
  --package com.mycompany.auth
```

```
=== Code Builder ===

Generating code for: User Authentication (SPEC-001)
Related Skills: 7

Generating Domain Layer...
  ✓ Domain layer complete
Generating Data Layer...
  ✓ Data layer complete
Generating Presentation Layer...
  ✓ Presentation layer complete
Generating Tests...
  ✓ Tests complete

✓ Code generation complete!
Output: examples/auth-app
```

### Step 4: Implement Business Logic

Edit generated files to implement actual business logic:

```kotlin
// examples/auth-app/src/main/kotlin/.../domain/usecase/LoginUseCase.kt

@Inject
class LoginUseCase(
    private val repository: AuthRepository
) {
    suspend operator fun invoke(email: String, password: String): Result<User> {
        // REQ-001-U-01: Validate email format
        if (!isValidEmail(email)) {
            return Result.failure(InvalidEmailException())
        }

        // REQ-001-U-02: Validate password strength
        if (!isStrongPassword(password)) {
            return Result.failure(WeakPasswordException())
        }

        // REQ-001-U-03: Authenticate with backend
        return repository.login(email, password)
    }

    private fun isValidEmail(email: String): Boolean {
        return Regex("[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}").matches(email)
    }

    private fun isStrongPassword(password: String): Boolean {
        return password.length >= 8 &&
               password.any { it.isUpperCase() } &&
               password.any { it.isLowerCase() } &&
               password.any { it.isDigit() }
    }
}
```

### Step 5: Sync Documentation

```bash
python3 tools/doc_syncer.py sync \
  specs/examples/user-authentication/SPEC.md \
  --code examples/auth-app
```

```
=== Doc Syncer - Synchronization ===

SPEC: User Authentication (SPEC-001)
Total Requirements: 5

Implementation Status:
  Implemented: 5/5 (100.0%)
  Missing: 0

Implemented Requirements:
  ✓ REQ-001-U-01
    → domain/usecase/LoginUseCase.kt:15
  ✓ REQ-001-U-02
    → domain/usecase/LoginUseCase.kt:20
  ✓ REQ-001-U-03
    → domain/usecase/LoginUseCase.kt:25
  ✓ REQ-001-U-04
    → data/repository/AuthRepositoryImpl.kt:18
  ✓ REQ-001-U-05
    → presentation/viewmodel/AuthViewModel.kt:32

Code Files:
  Source files: 9
  Test files: 1
  Test methods: 3

Updating SPEC traceability matrix...
  ✓ Traceability matrix updated
Generating README...
  ✓ README generated
Generating architecture diagram...
  ✓ Architecture diagram generated

✓ Synchronization complete!
```

### Step 6: Validate

```bash
python3 tools/validate_specs.py specs/examples/user-authentication/SPEC.md
```

```
Validating: specs/examples/user-authentication/SPEC.md

✓ SPEC is valid!
```

---

## Best Practices

### 1. Start Small

Begin with a simple feature to learn the workflow:
- 3-5 requirements
- Single screen
- Basic CRUD operations

### 2. Iterate on SPEC

Don't try to perfect the SPEC immediately:
1. Create initial version
2. Review with team
3. Refine requirements
4. Regenerate code if needed

### 3. Use SPEC IDs Consistently

Always reference SPEC IDs in:
- Code comments
- Commit messages
- Pull request descriptions
- Code reviews

### 4. Keep Skills Updated

As you add new patterns:
1. Update existing skills
2. Create new skills
3. Keep skill descriptions clear

### 5. Automate Validation

Add to CI/CD pipeline:

```yaml
# .github/workflows/validate-specs.yml
name: Validate SPECs

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Validate all SPECs
        run: python3 tools/validate_specs.py --all
```

---

## Common Issues

### Issue: "No requirements found"

**Cause**: Requirements not in EARS format

**Solution**: Ensure requirements follow pattern:
```
- **REQ-001-U-01**: The system shall [requirement]
```

### Issue: "Missing requirements in code"

**Cause**: Code doesn't reference SPEC IDs

**Solution**: Add comments:
```kotlin
// REQ-001-U-01: Validate email
if (!isValidEmail(email)) { ... }
```

### Issue: "Skills not matched correctly"

**Cause**: Feature description doesn't match skill keywords

**Solution**: Use more descriptive feature names:
- ❌ "Login"
- ✅ "User Authentication with Form Validation"

### Issue: "Traceability matrix not updating"

**Cause**: SPEC file doesn't have traceability section

**Solution**: Use latest SPEC template or add manually

---

## Next Steps

1. **Practice**: Create a sample feature end-to-end
2. **Customize**: Adapt templates for your team
3. **Integrate**: Add to your development process
4. **Share**: Train team members on workflow

---

**Need Help?**
- Check [SPEC Writing Guide](./spec-writing-guide.md)
- See [Agent Usage Guide](./agent-usage-guide.md)
- Review example: `specs/examples/user-authentication/`

---

*Part of the SPEC-First Development System*

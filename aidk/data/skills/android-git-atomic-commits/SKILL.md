---
name: android-git-atomic-commits
description: Create atomic commits with conventional commit format and SPEC traceability for Android projects
tier: 1
---

# Android Git: Atomic Commits

Create small, focused commits with conventional commit format and SPEC ID traceability for clean git history and better code review.

## When to Use

- Writing code changes in SPEC-First workflow
- Breaking down large features into reviewable chunks
- Following one logical change per commit principle
- Maintaining traceable commit history
- Preparing commits for code review

## Conventional Commit Format

### Basic Structure

```
<type>(<scope>): <subject>

<body>

Refs: SPEC-XXX, REQ-XXX-Y-ZZ

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Types

**Primary Types:**
- **feat**: New feature implementation
- **fix**: Bug fix
- **refactor**: Code refactoring without functional changes
- **test**: Adding or modifying tests
- **docs**: Documentation changes
- **chore**: Build, dependencies, tooling changes
- **style**: Code formatting, no logic changes
- **perf**: Performance improvements

**Usage:**
```bash
# Feature implementation
git commit -m "feat(auth): Add user login functionality"

# Bug fix
git commit -m "fix(network): Handle null response in API call"

# Refactoring
git commit -m "refactor(repo): Extract data source interface"

# Tests
git commit -m "test(viewmodel): Add login state tests"
```

### Scopes

**Android Scopes:**
- `domain` - Domain layer changes
- `data` - Data layer changes
- `presentation` - Presentation layer changes
- `ui` - UI components
- `viewmodel` - ViewModel changes
- `skills` - Claude Code skills
- `specs` - SPEC documents
- `tools` - Build tools, automation scripts
- `deps` - Dependency updates

**Example:**
```bash
git commit -m "feat(domain): Add GetProductsUseCase

Implements business logic for fetching products with pagination.

Refs: SPEC-002, REQ-002-U-01"
```

## SPEC Traceability

### Commit Message with SPEC ID

```bash
git commit -m "$(cat <<'EOF'
feat(data): Implement ProductRepository

- Add NetworkDataSource for API calls
- Add LocalDataSource for Room caching
- Implement cache-first strategy

Refs: SPEC-002, REQ-002-U-03, REQ-002-S-01

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

### Reference Format

**Single Requirement:**
```
Refs: SPEC-001, REQ-001-U-01
```

**Multiple Requirements:**
```
Refs: SPEC-001, REQ-001-U-01, REQ-001-U-02, REQ-001-E-01
```

**Breaking Change:**
```
BREAKING CHANGE: SPEC-001

Changed API response structure from List to PagingData.
Migrate existing code to use Paging 3 library.

Refs: SPEC-001, REQ-001-U-03
```

## Atomic Commit Best Practices

### Principle: One Logical Change Per Commit

**✅ Good Example:**

```bash
# Commit 1: Domain layer
git add domain/
git commit -m "feat(domain): Add User model and repository interface"

# Commit 2: Data layer
git add data/
git commit -m "feat(data): Implement UserRepository with API integration"

# Commit 3: Presentation layer
git add presentation/
git commit -m "feat(presentation): Add UserProfile ViewModel and State"

# Commit 4: UI
git add ui/
git commit -m "feat(ui): Create UserProfile screen with Compose"

# Commit 5: Tests
git add test/
git commit -m "test(domain): Add UserRepository tests"
```

**❌ Bad Example:**

```bash
# Single commit with everything
git add .
git commit -m "Add user profile feature"
```

### Selective Staging with git add -p

**Stage specific changes interactively:**

```bash
# Review and stage changes hunk by hunk
git add -p UserViewModel.kt

# Options:
# y - stage this hunk
# n - don't stage
# s - split into smaller hunks
# e - manually edit hunk
```

**Example workflow:**

```bash
# You modified UserViewModel.kt with:
# 1. Add new state property
# 2. Fix bug in existing function

# Stage only the state property
git add -p UserViewModel.kt
# Select 'y' for state property hunk
# Select 'n' for bug fix hunk

# Commit the new feature
git commit -m "feat(viewmodel): Add loading state to UserViewModel"

# Stage the bug fix
git add -p UserViewModel.kt
# Select 'y' for bug fix hunk

# Commit the fix
git commit -m "fix(viewmodel): Handle null user in updateProfile"
```

## SPEC-First Commit Workflow

### Step 1: Create Feature Branch

```bash
# After creating SPEC-001
git checkout -b feature/SPEC-001-user-authentication
```

### Step 2: Commit SPEC Document

```bash
git add specs/examples/user-authentication/SPEC.md
git commit -m "docs(SPEC-001): Add user authentication specification

- Define 5 EARS requirements
- Match 7 related Android skills
- Create implementation checklist

Refs: SPEC-001"
```

### Step 3: Implement in Layers (Atomic Commits)

```bash
# Domain layer
git add domain/
git commit -m "feat(SPEC-001): Implement domain layer

- Add User and AuthToken models
- Create AuthRepository interface
- Add LoginUseCase and LogoutUseCase

Refs: SPEC-001, REQ-001-U-01, REQ-001-U-02"

# Data layer
git add data/
git commit -m "feat(SPEC-001): Implement data layer

- Add AuthApi for network calls
- Add TokenManager for secure storage
- Implement AuthRepositoryImpl

Refs: SPEC-001, REQ-001-U-03"

# Presentation layer
git add presentation/
git commit -m "feat(SPEC-001): Implement presentation layer

- Add AuthViewModel with login state
- Define AuthActions and AuthEvents
- Implement login flow

Refs: SPEC-001, REQ-001-E-01"

# UI layer
git add ui/
git commit -m "feat(SPEC-001): Create login UI

- Build LoginScreen with Compose
- Add form validation
- Handle loading and error states

Refs: SPEC-001, REQ-001-E-01"

# Tests
git add test/
git commit -m "test(SPEC-001): Add comprehensive tests

- LoginUseCase unit tests (92% coverage)
- AuthViewModel tests with MockK
- Login UI tests with Compose Test

Refs: SPEC-001"

# Documentation
git add docs/ README.md
git commit -m "docs(SPEC-001): Update documentation

- Sync traceability matrix
- Add authentication guide
- Update README with new feature

Refs: SPEC-001"
```

## Common Patterns

### Feature Implementation Sequence

```bash
# 1. SPEC
docs(SPEC-XXX): Add [feature] specification

# 2. Domain
feat(SPEC-XXX): Implement domain layer

# 3. Data
feat(SPEC-XXX): Implement data layer

# 4. Presentation
feat(SPEC-XXX): Implement presentation layer

# 5. UI
feat(SPEC-XXX): Create [feature] UI

# 6. Tests
test(SPEC-XXX): Add [feature] tests

# 7. Documentation
docs(SPEC-XXX): Update documentation
```

### Dependency Updates

```bash
# Atomic dependency update
git add gradle/libs.versions.toml
git commit -m "chore(deps): Update Kotlin to 2.1.0

Update for new language features and performance improvements.
Compatible with existing codebase."
```

### Refactoring

```bash
# Extract interface
git commit -m "refactor(data): Extract DataSource interface

No functional changes. Improves testability and dependency injection."

# Rename
git commit -m "refactor(domain): Rename UserModel to User

Better naming convention. All usages updated."
```

## Commit Message Templates

### Feature Commit Template

```bash
git commit -m "$(cat <<'EOF'
feat(scope): Add [feature name]

- What was implemented
- Why it was needed
- Any important details

Refs: SPEC-XXX, REQ-XXX-Y-ZZ

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

### Fix Commit Template

```bash
git commit -m "$(cat <<'EOF'
fix(scope): Fix [bug description]

Problem: [What was wrong]
Solution: [How it was fixed]
Impact: [What changed for users]

Refs: SPEC-XXX, REQ-XXX-Y-ZZ

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

### Test Commit Template

```bash
git commit -m "$(cat <<'EOF'
test(scope): Add tests for [feature]

- Test coverage: XX%
- Test scenarios covered
- Edge cases tested

Refs: SPEC-XXX

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

## Verification

### Check Commit Quality

```bash
# View last commit
git log -1 --pretty=format:"%h - %s%n%b"

# View files in last commit
git show --name-only

# Verify commit is atomic (single logical change)
git show

# Check if commit builds
./gradlew build

# Run tests
./gradlew test
```

### Pre-commit Checklist

- [ ] One logical change only
- [ ] Conventional commit format
- [ ] SPEC ID referenced (if applicable)
- [ ] Code compiles
- [ ] Tests pass
- [ ] No unintended files included
- [ ] Commit message is clear and descriptive

## Integration with Tools

### With code_builder.py

```bash
# After generating code
python3 tools/code_builder.py SPEC-001

# Commit generated files atomically
git add domain/
git commit -m "feat(SPEC-001): Add generated domain layer

Generated from SPEC-001 using code_builder.py

Refs: SPEC-001"
```

### With doc_syncer.py

```bash
# After syncing docs
python3 tools/doc_syncer.py SPEC-001

# Commit documentation updates
git add docs/ specs/
git commit -m "docs(SPEC-001): Sync traceability matrix

Updated by doc_syncer.py

Refs: SPEC-001"
```

## Common Mistakes to Avoid

### ❌ Avoid

```bash
# Too large (mixed concerns)
git commit -m "Add feature and fix bugs"

# No context
git commit -m "Update code"

# Missing SPEC reference
git commit -m "feat(auth): Add login" # Missing Refs: SPEC-XXX

# Non-atomic (multiple logical changes)
git commit -m "Add login + refactor database + update deps"

# Wrong scope
git commit -m "feat(random): Add user repository" # Should be feat(data)
```

### ✅ Do

```bash
# Clear, focused, traceable
git commit -m "feat(data): Implement UserRepository

Adds repository pattern for user data with Room and Retrofit.

Refs: SPEC-001, REQ-001-U-03"

# Atomic commits
git commit -m "feat(domain): Add User model"
git commit -m "feat(data): Add UserRepository"
git commit -m "test(domain): Add User model tests"
```

## Tips

1. **Commit early, commit often** - Small commits are easier to review and revert
2. **Use git add -p** - Stage changes selectively for atomic commits
3. **Follow conventional commits** - Enables automated changelog generation
4. **Reference SPEC IDs** - Maintains traceability from requirements to code
5. **Write descriptive messages** - Future you will thank present you
6. **Keep commits buildable** - Each commit should compile and pass tests
7. **Group related changes** - But not unrelated ones, even if in same file

## Related Skills

- `android-git-spec-workflow` - SPEC-First git workflow
- `android-git-conventional-commits` - Conventional commit validation
- `android-git-multi-commit-feature` - Split large features into commits
- `android-clean-architecture` - Architecture for atomic commits
- `android-mvvm-architecture` - Layer-based commit strategy

## References

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Atomic Commits](https://www.freshconsulting.com/insights/blog/atomic-commits/)
- [Git Best Practices](https://git-scm.com/book/en/v2/Distributed-Git-Contributing-to-a-Project)

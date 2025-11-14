---
name: android-git-conventional-commits
description: Conventional commit format specification with validation and automation for Android projects
tier: 1
---

# Android Git: Conventional Commits

Structured commit message format following Conventional Commits specification for automated changelog generation, semantic versioning, and better collaboration.

## When to Use

- All commits in Android projects
- Automated changelog generation
- Semantic version bumping
- CI/CD pipeline integration
- Release note automation
- Git history navigation

## Conventional Commit Specification

### Format Structure

```
<type>(<scope>): <subject>

[optional body]

[optional footer(s)]
```

### Components

#### 1. Type (Required)

Describes the category of change:

| Type | Purpose | Example |
|------|---------|---------|
| `feat` | New feature | Add user login |
| `fix` | Bug fix | Fix null pointer crash |
| `refactor` | Code refactoring | Extract repository interface |
| `perf` | Performance improvement | Optimize image loading |
| `test` | Add/modify tests | Add ViewModel tests |
| `docs` | Documentation | Update README |
| `style` | Code style/formatting | Fix indentation |
| `chore` | Build, deps, config | Update Gradle |
| `ci` | CI/CD changes | Update GitHub Actions |
| `build` | Build system | Configure ProGuard |
| `revert` | Revert previous commit | Revert "Add feature" |

#### 2. Scope (Optional but Recommended)

Indicates what part of codebase is affected:

**Android-Specific Scopes:**
- `domain` - Domain layer
- `data` - Data layer
- `presentation` - Presentation layer
- `ui` - UI components
- `viewmodel` - ViewModel changes
- `repository` - Repository changes
- `api` - API service changes
- `database` - Database changes
- `di` - Dependency injection
- `navigation` - Navigation changes
- `theme` - Theming changes
- `test` - Test-related changes

**SPEC-First Scopes:**
- `specs` - SPEC documents
- `tools` - Automation tools
- `skills` - Claude Code skills

**General Scopes:**
- `deps` - Dependencies
- `gradle` - Gradle configuration
- `ci` - CI/CD
- `docs` - Documentation

#### 3. Subject (Required)

Short description of the change:

**Rules:**
- Use imperative mood ("add" not "added" or "adds")
- Don't capitalize first letter
- No period at the end
- Maximum 50 characters
- Be specific and concise

**✅ Good:**
```
feat(auth): add Google OAuth login support
fix(cart): handle empty cart state correctly
refactor(data): extract network data source interface
```

**❌ Bad:**
```
feat: Added some stuff  # Too vague
Fix: Fixed the bug.  # Capitalized, has period
refactor(repository): Refactored the repository implementation to use new pattern  # Too long
```

#### 4. Body (Optional)

Detailed explanation of the change:

**When to Include:**
- Complex changes needing explanation
- Breaking changes
- Migration instructions
- Context for reviewers

**Format:**
- Separate from subject with blank line
- Wrap at 72 characters
- Explain what and why, not how
- Use bullet points for multiple items

**Example:**
```
feat(data): implement offline-first caching strategy

- Add NetworkBoundResource for single source of truth
- Cache API responses in Room database
- Return cached data when offline
- Sync with network when connection restored

This improves user experience by showing data instantly
and working fully offline.
```

#### 5. Footer (Optional)

Additional metadata:

**Breaking Changes:**
```
BREAKING CHANGE: description of breaking change
```

**Issue References:**
```
Refs: #123, #456
Closes: #789
Fixes: #234
```

**SPEC References:**
```
Refs: SPEC-001, REQ-001-U-01, REQ-001-E-02
```

## Complete Examples

### Feature Commit

```
feat(auth): add biometric authentication support

- Integrate BiometricPrompt API
- Add fallback to PIN authentication
- Store biometric preference in DataStore
- Add UI toggle in settings screen

Supports Android 11+ devices with fingerprint or face unlock.

Refs: SPEC-001, REQ-001-O-01
```

### Bug Fix Commit

```
fix(cart): prevent duplicate items when adding quickly

Problem: Rapid clicks on "Add to Cart" created duplicate entries.
Solution: Debounce click events with 500ms delay.
Impact: Users can no longer accidentally add duplicates.

Fixes: #234
Refs: SPEC-003
```

### Breaking Change Commit

```
feat(api): migrate to Paging 3 for product lists

BREAKING CHANGE: ProductRepository now returns PagingData instead of List

Migration guide:
1. Update repositories to return PagingData
2. Change ViewModels to collect from Pager flow
3. Replace LazyColumn items with items(pager)

This enables better memory management and infinite scrolling.

Refs: SPEC-002, REQ-002-U-05
```

### Refactoring Commit

```
refactor(domain): extract use case interfaces

No functional changes. Improves testability and follows Clean Architecture principles.

- Extract interface for each use case
- Add UseCase base interface
- Update DI modules with bindings

Refs: SPEC-001
```

### Test Commit

```
test(viewmodel): add comprehensive login tests

- Test success scenario with valid credentials
- Test error handling for network failures
- Test loading state transitions
- Test password validation logic
- Coverage: 95% for LoginViewModel

All edge cases covered with MockK and Turbine.

Refs: SPEC-001
```

### Documentation Commit

```
docs(readme): add authentication setup guide

- Document OAuth configuration steps
- Add API key setup instructions
- Include troubleshooting section
- Add code examples for integration

Refs: SPEC-001
```

### Dependency Update Commit

```
chore(deps): update Kotlin to 2.1.0

- Kotlin: 2.0.0 → 2.1.0
- Benefits: Performance improvements, new language features
- Compatibility: All tests passing

No breaking changes in our usage.
```

## Commit Types in Detail

### feat (Feature)

**When to Use:**
- Adding new functionality
- New UI components
- New API endpoints
- New features for users

**Examples:**
```bash
feat(ui): add dark mode support
feat(data): integrate payment gateway API
feat(navigation): add deep linking for products
feat(domain): add GetRecommendationsUseCase
```

### fix (Bug Fix)

**When to Use:**
- Fixing bugs
- Resolving crashes
- Correcting logic errors
- Fixing UI issues

**Examples:**
```bash
fix(ui): correct button alignment on small screens
fix(data): handle null response from API
fix(viewmodel): prevent memory leak in observers
fix(navigation): resolve back stack inconsistency
```

### refactor (Refactoring)

**When to Use:**
- Code restructuring without changing behavior
- Extracting functions/classes
- Renaming for clarity
- Improving code quality

**Examples:**
```bash
refactor(data): extract DataSource interface
refactor(ui): simplify state management logic
refactor(domain): rename User to UserProfile for clarity
refactor(repository): consolidate duplicate caching logic
```

### perf (Performance)

**When to Use:**
- Optimizing algorithms
- Reducing memory usage
- Improving rendering speed
- Database query optimization

**Examples:**
```bash
perf(ui): optimize LazyColumn performance with keys
perf(data): add database indexes for faster queries
perf(image): implement image caching with Coil
perf(viewmodel): reduce unnecessary recompositions
```

### test (Testing)

**When to Use:**
- Adding new tests
- Modifying existing tests
- Improving test coverage
- Adding test utilities

**Examples:**
```bash
test(viewmodel): add LoginViewModel unit tests
test(ui): add ProductList UI tests with Compose Test
test(repository): add integration tests for caching
test(domain): increase use case coverage to 90%
```

### docs (Documentation)

**When to Use:**
- Updating README
- Adding code comments
- Writing guides
- API documentation
- SPEC documents

**Examples:**
```bash
docs(readme): add getting started guide
docs(api): document authentication endpoints
docs(SPEC-001): add user authentication specification
docs(code): add KDoc comments to public APIs
```

### style (Code Style)

**When to Use:**
- Formatting changes
- Fixing linter warnings
- Organizing imports
- Code style consistency

**Examples:**
```bash
style(all): apply ktlint formatting
style(imports): organize and remove unused imports
style(naming): apply consistent naming conventions
style(ui): fix indentation in Compose code
```

### chore (Chore)

**When to Use:**
- Build configuration
- Dependency updates
- Tool configuration
- Generated code updates

**Examples:**
```bash
chore(deps): update AndroidX libraries
chore(gradle): configure build variants
chore(git): add .gitignore entries
chore(tools): update code generation scripts
```

## Validation Rules

### Subject Line Rules

1. **Length:** Maximum 50 characters (hard limit 72)
2. **Case:** Start with lowercase
3. **Mood:** Imperative (add, not added/adds)
4. **Punctuation:** No period at end
5. **Type:** Must be valid type
6. **Format:** Must match pattern `type(scope): subject`

### Body Rules

1. **Separation:** Blank line after subject
2. **Width:** Wrap at 72 characters
3. **Content:** Explain what and why

### Footer Rules

1. **Format:** `Key: Value` or `BREAKING CHANGE:`
2. **Position:** After body with blank line
3. **Breaking changes:** Must start with `BREAKING CHANGE:`

## Automation and Tooling

### Git Commit Template

Create `.gitmessage` in project root:

```
# <type>(<scope>): <subject>
# |<----  Max 50 characters  ---->|

# [optional body]
# |<----   Wrap at 72 characters   ---->|

# [optional footer(s)]
# Refs: SPEC-XXX, REQ-XXX-Y-ZZ
# Fixes: #issue
# BREAKING CHANGE: description

# Types: feat, fix, refactor, perf, test, docs, style, chore, ci, build, revert
# Scopes: domain, data, presentation, ui, viewmodel, repository, api, database, di, navigation, theme, specs, tools, skills, deps, gradle, ci, docs
# Subject: imperative mood, lowercase, no period
# Body: explain what and why
# Footer: BREAKING CHANGE, Refs, Fixes, Closes
```

Configure git to use template:
```bash
git config commit.template .gitmessage
```

### Commitlint Configuration

Install commitlint:
```bash
npm install --save-dev @commitlint/{cli,config-conventional}
```

Create `commitlint.config.js`:
```javascript
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      [
        'feat', 'fix', 'refactor', 'perf', 'test',
        'docs', 'style', 'chore', 'ci', 'build', 'revert'
      ]
    ],
    'scope-enum': [
      2,
      'always',
      [
        'domain', 'data', 'presentation', 'ui', 'viewmodel',
        'repository', 'api', 'database', 'di', 'navigation',
        'theme', 'specs', 'tools', 'skills', 'deps',
        'gradle', 'ci', 'docs'
      ]
    ],
    'subject-case': [2, 'always', 'lower-case'],
    'subject-max-length': [2, 'always', 50],
    'subject-full-stop': [2, 'never', '.'],
    'body-max-line-length': [2, 'always', 72]
  }
};
```

### Husky Pre-commit Hook

Install Husky:
```bash
npm install --save-dev husky
npx husky install
```

Add commit-msg hook:
```bash
npx husky add .husky/commit-msg 'npx --no -- commitlint --edit $1'
```

### Changelog Generation

Use `standard-version` for automated changelogs:

```bash
npm install --save-dev standard-version
```

Configure in `package.json`:
```json
{
  "scripts": {
    "release": "standard-version"
  },
  "standard-version": {
    "types": [
      {"type": "feat", "section": "Features"},
      {"type": "fix", "section": "Bug Fixes"},
      {"type": "perf", "section": "Performance"},
      {"type": "refactor", "section": "Refactoring"},
      {"type": "test", "section": "Tests"},
      {"type": "docs", "section": "Documentation"},
      {"type": "chore", "hidden": true},
      {"type": "style", "hidden": true},
      {"type": "ci", "hidden": true},
      {"type": "build", "hidden": true"}
    ]
  }
}
```

Generate changelog:
```bash
npm run release
```

Output `CHANGELOG.md`:
```markdown
# Changelog

## [1.2.0] - 2025-01-14

### Features
- **auth**: add Google OAuth login support (abc1234)
- **ui**: add dark mode support (def5678)

### Bug Fixes
- **cart**: prevent duplicate items when adding quickly (ghi9012)
- **data**: handle null response from API (jkl3456)

### Performance
- **ui**: optimize LazyColumn performance with keys (mno7890)
```

## Integration with SPEC-First

### SPEC Reference in Commits

**Always include SPEC ID:**
```bash
git commit -m "feat(domain): add Product model

Refs: SPEC-002, REQ-002-U-01"
```

### Commit Sequence for SPEC

```bash
# 1. SPEC Document
docs(SPEC-XXX): add [feature] specification

# 2. Implementation
feat(SPEC-XXX): implement [layer]

# 3. Tests
test(SPEC-XXX): add [feature] tests

# 4. Documentation
docs(SPEC-XXX): update documentation
```

### Breaking Changes with SPEC

```bash
feat(api): migrate to new authentication flow

BREAKING CHANGE: AuthRepository interface changed

Old: suspend fun login(email: String, password: String): User
New: suspend fun login(credentials: Credentials): Result<User>

Migration: Update all login calls to use Credentials object.

Refs: SPEC-001, REQ-001-U-01
```

## Best Practices

### ✅ Do

1. **Use conventional format consistently**
```bash
feat(ui): add product search functionality
```

2. **Include SPEC references**
```bash
Refs: SPEC-002, REQ-002-U-04
```

3. **Write clear subject lines**
```bash
fix(cart): prevent duplicate items on rapid clicks
```

4. **Explain complex changes in body**
```bash
feat(data): implement offline-first caching

Uses NetworkBoundResource pattern for single source of truth.
```

5. **Mark breaking changes clearly**
```bash
BREAKING CHANGE: Repository interface updated
```

### ❌ Avoid

1. **Vague commit messages**
```bash
# Bad
git commit -m "fix stuff"
git commit -m "updates"
git commit -m "WIP"
```

2. **Missing type or scope**
```bash
# Bad
git commit -m "add login feature"  # Missing type
git commit -m "feat: something"    # Too vague
```

3. **Wrong type**
```bash
# Bad
git commit -m "feat(ui): fix button color"  # Should be 'fix'
git commit -m "docs(code): add new feature" # Should be 'feat'
```

4. **Too long subject**
```bash
# Bad (>50 chars)
git commit -m "feat(auth): add comprehensive Google OAuth authentication with biometric fallback support"
```

## Examples by Scenario

### New Feature Development

```bash
# SPEC
docs(SPEC-005): add payment processing specification

# Domain
feat(SPEC-005): implement payment domain models
feat(SPEC-005): add ProcessPaymentUseCase

# Data
feat(SPEC-005): integrate Stripe payment API
feat(SPEC-005): add payment transaction repository

# Presentation
feat(SPEC-005): create PaymentViewModel with state management

# UI
feat(SPEC-005): build payment screen with card input
feat(SPEC-005): add payment confirmation dialog

# Tests
test(SPEC-005): add payment processing tests

# Docs
docs(SPEC-005): update traceability and README
```

### Bug Fix Workflow

```bash
# Fix
fix(cart): resolve cart total calculation error

Problem: Tax was calculated incorrectly for international orders.
Solution: Apply correct tax rate based on shipping country.
Impact: Cart totals now accurate for all regions.

Fixes: #456
Refs: SPEC-003

# Test
test(cart): add tests for international tax calculation

Covers US, EU, and Asia tax scenarios.

Refs: SPEC-003
```

### Refactoring Workflow

```bash
# Refactor
refactor(data): migrate to Kotlin Serialization

Replace Gson with Kotlin Serialization for better Kotlin support.

- Remove Gson dependencies
- Add Kotlinx Serialization plugin
- Update all DTOs with @Serializable
- Configure custom serializers

No functional changes. All tests passing.

# Update tests
test(data): update serialization tests for kotlinx

# Update docs
docs(api): update serialization documentation
```

## Related Skills

- `android-git-atomic-commits` - Creating atomic commits
- `android-git-spec-workflow` - SPEC-First git workflow
- `android-git-multi-commit-feature` - Feature splitting strategy

## References

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [Commitlint](https://commitlint.js.org/)
- [Standard Version](https://github.com/conventional-changelog/standard-version)

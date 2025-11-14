---
name: android-git-spec-workflow
description: Git workflow optimized for SPEC-First Android development with requirement traceability
tier: 1
---

# Android Git: SPEC-First Workflow

Complete git workflow for SPEC-First Android development, from feature branch creation to PR merge with full requirement traceability.

## When to Use

- Starting a new feature with SPEC document
- Following SPEC-First development methodology
- Maintaining traceability from requirements to code
- Creating reviewable feature branches
- Integrating with spec_builder.py and code_builder.py

## Complete SPEC-First Workflow

### Step 1: Create SPEC Document

```bash
# Interactive mode
python3 tools/spec_builder.py interactive

# Quick mode
python3 tools/spec_builder.py create "Product Catalog" \
  --purpose "Display and filter products" \
  --requirements "fetch products from API" \
                 "cache products in local database" \
                 "display product list with images" \
                 "filter products by search query" \
                 "navigate to product detail on click"

# Output: SPEC-002 created at specs/examples/product-catalog/SPEC.md
```

### Step 2: Create Feature Branch

**Branch Naming Convention:**
```
feature/SPEC-{id}-{brief-description}
```

**Examples:**
```bash
# After creating SPEC-001
git checkout -b feature/SPEC-001-user-authentication

# After creating SPEC-002
git checkout -b feature/SPEC-002-product-catalog

# After creating SPEC-015
git checkout -b feature/SPEC-015-payment-processing
```

**Create and commit SPEC:**
```bash
# Create branch
git checkout -b feature/SPEC-002-product-catalog

# Commit SPEC document
git add specs/examples/product-catalog/
git commit -m "$(cat <<'EOF'
docs(SPEC-002): Add product catalog specification

- Define 9 EARS requirements (7 Ubiquitous, 2 Event-driven)
- Match 10 related Android skills
- Create implementation checklist
- Define architecture and data models

Refs: SPEC-002

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

### Step 3: Implement Feature (Layer by Layer)

**Implementation Order:**
1. Domain Layer (Models, UseCases, Repository Interfaces)
2. Data Layer (API, Database, Repository Implementation)
3. Presentation Layer (ViewModel, State, Actions, Events)
4. UI Layer (Compose Screens, Navigation)
5. Tests (Unit, Integration, UI)
6. Documentation (Update README, Sync traceability)

**Domain Layer:**
```bash
# Generate or write domain code
# If using code_builder.py:
python3 tools/code_builder.py SPEC-002 --layer domain

# Commit domain layer
git add src/main/kotlin/**/domain/
git commit -m "$(cat <<'EOF'
feat(SPEC-002): Implement domain layer

- Add Product model with ID, name, price, imageUrl
- Create ProductRepository interface
- Add GetProductsUseCase for fetching with pagination
- Add SearchProductsUseCase for filtering

Refs: SPEC-002, REQ-002-U-01, REQ-002-U-02

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

**Data Layer:**
```bash
# Generate or write data code
python3 tools/code_builder.py SPEC-002 --layer data

# Commit data layer
git add src/main/kotlin/**/data/
git commit -m "$(cat <<'EOF'
feat(SPEC-002): Implement data layer

- Add ProductApi with Retrofit for API calls
- Add ProductEntity and ProductDao for Room caching
- Implement ProductRepositoryImpl with cache-first strategy
- Add ProductDto for API response mapping

Cache strategy: Network first, fallback to cache on error.

Refs: SPEC-002, REQ-002-U-03, REQ-002-S-01

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

**Presentation Layer:**
```bash
# Generate or write presentation code
python3 tools/code_builder.py SPEC-002 --layer presentation

# Commit presentation layer
git add src/main/kotlin/**/presentation/
git commit -m "$(cat <<'EOF'
feat(SPEC-002): Implement presentation layer

- Add ProductListViewModel with StateFlow
- Define ProductListState (Loading, Success, Error, Empty)
- Define ProductListActions (LoadProducts, SearchProducts, RefreshProducts)
- Define ProductListEvents (NavigateToDetail, ShowError)
- Implement product fetching and search logic

Refs: SPEC-002, REQ-002-E-01, REQ-002-U-04

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

**UI Layer:**
```bash
# Write UI code
# Commit UI layer
git add src/main/kotlin/**/ui/
git commit -m "$(cat <<'EOF'
feat(SPEC-002): Create product catalog UI

- Build ProductListScreen with LazyColumn
- Add ProductCard composable with image and details
- Add SearchBar with real-time filtering
- Add pull-to-refresh functionality
- Handle loading, error, and empty states

Refs: SPEC-002, REQ-002-E-01, REQ-002-U-05

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

**Tests:**
```bash
# Write tests
git add src/test/ src/androidTest/
git commit -m "$(cat <<'EOF'
test(SPEC-002): Add comprehensive tests

- GetProductsUseCase unit tests (95% coverage)
- ProductRepositoryImpl tests with MockK
- ProductListViewModel tests with Turbine
- ProductListScreen UI tests with Compose Test
- Test scenarios: success, error, empty, search, refresh

All requirements validated through automated tests.

Refs: SPEC-002

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

**Documentation:**
```bash
# Sync documentation
python3 tools/doc_syncer.py SPEC-002

# Commit documentation updates
git add docs/ specs/ README.md
git commit -m "$(cat <<'EOF'
docs(SPEC-002): Update documentation and traceability

- Sync traceability matrix (9/9 requirements implemented)
- Update README with product catalog feature
- Generate architecture diagram
- Add feature usage guide

Implementation: 100% complete, 95% test coverage.

Refs: SPEC-002

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

### Step 4: Verify Implementation

```bash
# Check git status
git status

# View commit history
git log --oneline feature/SPEC-002-product-catalog

# Run validation
python3 tools/validate_specs.py SPEC-002

# Build project
./gradlew build

# Run tests
./gradlew test

# Check test coverage
./gradlew jacocoTestReport
```

### Step 5: Create Pull Request

```bash
# Push feature branch
git push -u origin feature/SPEC-002-product-catalog

# Create PR with gh CLI
gh pr create --title "feat(SPEC-002): Product Catalog" --body "$(cat <<'EOF'
## Summary
Implements product catalog feature with list view, search, and caching.

## SPEC Traceability
**SPEC ID:** SPEC-002

**Requirements Implemented:**
- ✅ REQ-002-U-01: Fetch products from API
- ✅ REQ-002-U-02: Cache products in local database
- ✅ REQ-002-U-03: Display product list with images
- ✅ REQ-002-U-04: Filter products by search query
- ✅ REQ-002-U-05: Navigate to product detail on click
- ✅ REQ-002-S-01: Show cached data when offline
- ✅ REQ-002-E-01: Handle API errors gracefully
- ✅ REQ-002-O-01: Show empty state when no products
- ✅ REQ-002-O-02: Refresh data on pull-to-refresh

**Implementation:** 9/9 requirements (100%)
**Test Coverage:** 95%

## Architecture
- **Domain:** Product model, GetProductsUseCase, SearchProductsUseCase
- **Data:** Retrofit API, Room cache, Repository with cache-first strategy
- **Presentation:** ProductListViewModel with StateFlow, MVVM pattern
- **UI:** ProductListScreen with Compose, LazyColumn, pull-to-refresh

## Related Skills
- android-clean-architecture
- android-mvvm-architecture
- android-compose-ui
- android-list-ui
- android-networking-retrofit
- android-database-room
- android-repository-pattern
- android-stateflow
- android-coroutines
- android-image-loading

## Testing
- ✅ Unit tests for use cases and repository
- ✅ ViewModel tests with Turbine
- ✅ UI tests with Compose Test
- ✅ All tests passing
- ✅ 95% code coverage

## Screenshots
[Add screenshots of product list, search, loading, error, empty states]

## Checklist
- [x] Code follows Clean Architecture
- [x] All requirements implemented
- [x] Tests written and passing
- [x] Documentation updated
- [x] Traceability matrix synced
- [x] No breaking changes
- [x] PR ready for review

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

## Branch Naming Conventions

### Feature Branches

```bash
feature/SPEC-{id}-{brief-description}
```

**Examples:**
- `feature/SPEC-001-user-authentication`
- `feature/SPEC-002-product-catalog`
- `feature/SPEC-015-payment-processing`
- `feature/SPEC-042-push-notifications`

### Bug Fix Branches

```bash
fix/SPEC-{id}-{bug-description}
# or
fix/{issue-number}-{bug-description}
```

**Examples:**
- `fix/SPEC-001-login-crash`
- `fix/123-null-pointer-in-cart`

### Refactoring Branches

```bash
refactor/SPEC-{id}-{refactor-description}
# or
refactor/{component}-{description}
```

**Examples:**
- `refactor/SPEC-001-extract-auth-repository`
- `refactor/database-migration-to-room`

## Commit Sequence Template

For any SPEC-based feature, follow this sequence:

```bash
# 1. SPEC Document
git commit -m "docs(SPEC-XXX): Add [feature] specification"

# 2. Domain Layer
git commit -m "feat(SPEC-XXX): Implement domain layer"

# 3. Data Layer
git commit -m "feat(SPEC-XXX): Implement data layer"

# 4. Presentation Layer
git commit -m "feat(SPEC-XXX): Implement presentation layer"

# 5. UI Layer
git commit -m "feat(SPEC-XXX): Create [feature] UI"

# 6. Tests
git commit -m "test(SPEC-XXX): Add [feature] tests"

# 7. Documentation
git commit -m "docs(SPEC-XXX): Update documentation"
```

**Expected commits per feature:** 6-8 commits minimum

## Working with SPEC Tools

### Integration with spec_builder.py

```bash
# Create SPEC
python3 tools/spec_builder.py interactive

# Output shows:
# ✓ SPEC created successfully!
# Location: specs/examples/user-authentication/SPEC.md
# SPEC ID: SPEC-001
# Requirements: 5
# Related Skills: 7

# Create branch and commit
git checkout -b feature/SPEC-001-user-authentication
git add specs/examples/user-authentication/
git commit -m "docs(SPEC-001): Add user authentication specification

Refs: SPEC-001"
```

### Integration with code_builder.py

```bash
# Generate code from SPEC
python3 tools/code_builder.py SPEC-001

# Commit generated code layer by layer
git add domain/
git commit -m "feat(SPEC-001): Add generated domain layer

Generated from SPEC-001 using code_builder.py

Refs: SPEC-001"

git add data/
git commit -m "feat(SPEC-001): Add generated data layer

Generated from SPEC-001 using code_builder.py

Refs: SPEC-001"
```

### Integration with doc_syncer.py

```bash
# After implementation, sync docs
python3 tools/doc_syncer.py SPEC-001

# Review changes
git diff docs/ specs/

# Commit documentation updates
git add docs/ specs/
git commit -m "docs(SPEC-001): Sync traceability matrix

Updated by doc_syncer.py

Refs: SPEC-001"
```

### Integration with validate_specs.py

```bash
# Validate SPEC before committing
python3 tools/validate_specs.py SPEC-001

# Output:
# ✓ SPEC-001: Valid
# - Format: OK
# - Requirements: 5 found
# - Traceability: 5/5 mapped
# - Structure: Complete

# If validation passes, commit
git add specs/examples/user-authentication/SPEC.md
git commit -m "docs(SPEC-001): Add user authentication specification"
```

## Multi-Developer Workflow

### Working on Same SPEC

```bash
# Developer 1: Domain layer
git checkout -b feature/SPEC-001-user-authentication
git commit -m "feat(SPEC-001): Implement domain layer"

# Developer 2: Data layer (branch from main)
git checkout -b feature/SPEC-001-data-layer
git commit -m "feat(SPEC-001): Implement data layer"

# Merge domain first, then rebase data layer
git checkout feature/SPEC-001-data-layer
git rebase feature/SPEC-001-user-authentication
```

### SPEC Updates During Development

```bash
# Requirement changes during development
git checkout feature/SPEC-001-user-authentication

# Update SPEC
# Edit specs/examples/user-authentication/SPEC.md

# Commit SPEC update
git commit -m "docs(SPEC-001): Update requirements for OAuth support

Added REQ-001-U-06 for Google OAuth integration.

Refs: SPEC-001"

# Continue implementation with new requirements
```

## Best Practices

### ✅ Do

1. **Create branch immediately after SPEC**
```bash
python3 tools/spec_builder.py create "Feature Name"
git checkout -b feature/SPEC-XXX-feature-name
```

2. **Commit SPEC first**
```bash
git add specs/
git commit -m "docs(SPEC-XXX): Add specification"
```

3. **Follow layer order**
```bash
# Domain → Data → Presentation → UI → Tests → Docs
```

4. **Reference SPEC IDs in all commits**
```bash
Refs: SPEC-001, REQ-001-U-01
```

5. **Keep commits atomic and focused**
```bash
# One layer per commit, one logical change per commit
```

6. **Sync documentation before PR**
```bash
python3 tools/doc_syncer.py SPEC-XXX
git add docs/ specs/
git commit -m "docs(SPEC-XXX): Sync traceability"
```

### ❌ Avoid

1. **Don't skip SPEC document**
```bash
# Bad: Start coding without SPEC
git checkout -b feature/some-feature
```

2. **Don't commit all layers together**
```bash
# Bad: One giant commit
git add .
git commit -m "Add feature"
```

3. **Don't forget SPEC ID references**
```bash
# Bad: No traceability
git commit -m "feat: Add login"
```

4. **Don't mix unrelated changes**
```bash
# Bad: Multiple SPECs in one branch
feature/multiple-features  # Should be separate branches
```

5. **Don't skip tests**
```bash
# Bad: No test commit
feat(SPEC-001): Implement feature  # Missing test(SPEC-001)
```

## Troubleshooting

### Forgot to Create Feature Branch

```bash
# You're on main with uncommitted changes
git status  # Shows modified files

# Create and switch to feature branch
git checkout -b feature/SPEC-XXX-feature-name

# Continue as normal
git add .
git commit -m "feat(SPEC-XXX): ..."
```

### Committed to Wrong Branch

```bash
# You committed SPEC-002 changes to SPEC-001 branch
git log  # Shows commits

# Create correct branch from current position
git checkout -b feature/SPEC-002-correct-branch

# Go back to previous branch and reset
git checkout feature/SPEC-001-wrong-branch
git reset --hard HEAD~1  # Remove the wrong commit
```

### Need to Update SPEC Mid-Development

```bash
# Implementation reveals missing requirements
# Edit SPEC file
vim specs/examples/feature/SPEC.md

# Commit SPEC update
git commit -m "docs(SPEC-XXX): Update requirements

Added REQ-XXX-U-XX for newly discovered need.

Refs: SPEC-XXX"

# Continue with updated requirements
```

## Related Skills

- `android-git-atomic-commits` - Atomic commit best practices
- `android-git-conventional-commits` - Commit message format
- `android-git-multi-commit-feature` - Split features into commits
- `android-clean-architecture` - Layer-based implementation
- `android-mvvm-architecture` - Presentation layer structure

## Tools Integration Summary

| Tool | Purpose | Git Integration |
|------|---------|----------------|
| `spec_builder.py` | Create SPEC | Commit SPEC document |
| `code_builder.py` | Generate code | Commit generated layers |
| `doc_syncer.py` | Sync documentation | Commit doc updates |
| `validate_specs.py` | Validate SPEC | Pre-commit validation |

## References

- CONTRIBUTING.md - SPEC-First contribution guidelines
- README_SPEC_FIRST.md - SPEC-First system overview
- docs/guides/workflow-guide.md - Detailed workflow guide
- docs/guides/real-world-example.md - Complete example

---
name: android-git-multi-commit-feature
description: Split large features into logical, atomic commits for better code review and git history
tier: 1
---

# Android Git: Multi-Commit Feature Development

Break down large features into small, logical, reviewable commits following Clean Architecture layers and SPEC-First methodology.

## When to Use

- Large feature development with multiple components
- Complex changes spanning multiple layers
- Refactoring existing features
- Current situation: Too many uncommitted changes
- Preparing for code review
- Maintaining bisectable git history

## Core Principle: One Logical Change Per Commit

### What is a Logical Change?

A logical change is:
- **Single purpose** - Does one thing well
- **Complete** - Includes everything needed for that change
- **Independent** - Can be understood and reviewed alone
- **Buildable** - Compiles and passes tests
- **Reversible** - Can be reverted without breaking other commits

### Examples

**✅ Good Logical Changes:**
```bash
# Each commit is complete and independent
git commit -m "feat(domain): add Product model"
git commit -m "feat(domain): add ProductRepository interface"
git commit -m "feat(data): implement ProductRepository with Retrofit"
git commit -m "feat(data): add Room caching to ProductRepository"
git commit -m "feat(presentation): create ProductListViewModel"
git commit -m "feat(ui): build ProductListScreen"
git commit -m "test(domain): add ProductRepository tests"
```

**❌ Bad Logical Changes:**
```bash
# Too many unrelated changes
git commit -m "Add product feature and fix login bug and update deps"

# Too granular
git commit -m "Add Product.kt"
git commit -m "Add price field to Product"
git commit -m "Add image field to Product"
```

## Strategy 1: Layer-Based Split

### Clean Architecture Layers

For SPEC-First development, split by architectural layers:

```
1. Domain Layer
   ├── Models
   ├── Use Cases
   └── Repository Interfaces

2. Data Layer
   ├── API/Network
   ├── Database
   ├── Repository Implementation
   └── Data Mapping

3. Presentation Layer
   ├── ViewModel
   ├── State
   ├── Actions
   └── Events

4. UI Layer
   ├── Screens
   ├── Components
   └── Navigation

5. Test Layer
   ├── Unit Tests
   ├── Integration Tests
   └── UI Tests

6. Documentation
   ├── README
   ├── SPEC traceability
   └── Architecture docs
```

### Example: Product Catalog Feature

```bash
# Starting point: All changes uncommitted
git status
# 45 files changed

# Step 1: Domain layer commits
git add domain/model/Product.kt
git commit -m "feat(SPEC-002): add Product domain model

Refs: SPEC-002, REQ-002-U-01"

git add domain/repository/ProductRepository.kt
git commit -m "feat(SPEC-002): add ProductRepository interface

Refs: SPEC-002, REQ-002-U-02"

git add domain/usecase/GetProductsUseCase.kt domain/usecase/SearchProductsUseCase.kt
git commit -m "feat(SPEC-002): add product use cases

- GetProductsUseCase for fetching with pagination
- SearchProductsUseCase for filtering by query

Refs: SPEC-002, REQ-002-U-03"

# Step 2: Data layer commits
git add data/remote/ProductApi.kt data/remote/ProductDto.kt
git commit -m "feat(SPEC-002): add Product API integration

Refs: SPEC-002, REQ-002-U-04"

git add data/local/ProductEntity.kt data/local/ProductDao.kt
git commit -m "feat(SPEC-002): add Product Room database

Refs: SPEC-002, REQ-002-S-01"

git add data/repository/ProductRepositoryImpl.kt
git commit -m "feat(SPEC-002): implement ProductRepository

Cache-first strategy: Check cache, fallback to network.

Refs: SPEC-002, REQ-002-U-05"

# Step 3: Presentation layer commits
git add presentation/state/ProductListState.kt
git commit -m "feat(SPEC-002): define ProductList state

Refs: SPEC-002"

git add presentation/viewmodel/ProductListViewModel.kt
git commit -m "feat(SPEC-002): create ProductListViewModel

Refs: SPEC-002, REQ-002-E-01"

# Step 4: UI layer commits
git add ui/components/ProductCard.kt
git commit -m "feat(SPEC-002): add ProductCard composable

Refs: SPEC-002"

git add ui/screens/ProductListScreen.kt
git commit -m "feat(SPEC-002): build ProductListScreen

Refs: SPEC-002, REQ-002-E-02"

# Step 5: Test commits
git add test/domain/
git commit -m "test(SPEC-002): add domain layer tests

- ProductRepository tests
- Use case tests
Coverage: 92%

Refs: SPEC-002"

git add test/presentation/
git commit -m "test(SPEC-002): add ViewModel tests

Coverage: 88%

Refs: SPEC-002"

# Step 6: Documentation commit
git add docs/ README.md specs/
git commit -m "docs(SPEC-002): update documentation

- Sync traceability matrix
- Update README
- Add architecture diagram

Refs: SPEC-002"

# Result: 13 logical commits instead of 1 giant commit
```

## Strategy 2: Feature-Based Split

### When You Have Multiple Sub-features

Split by user-facing functionality:

```bash
# Feature: Shopping Cart

# Sub-feature 1: Add to cart
git add cart/domain/AddToCartUseCase.kt
git commit -m "feat(cart): add item to cart functionality"

# Sub-feature 2: Update quantity
git add cart/domain/UpdateQuantityUseCase.kt
git commit -m "feat(cart): update item quantity"

# Sub-feature 3: Remove from cart
git add cart/domain/RemoveFromCartUseCase.kt
git commit -m "feat(cart): remove item from cart"

# Sub-feature 4: Calculate total
git add cart/domain/CalculateTotalUseCase.kt
git commit -m "feat(cart): calculate cart total with tax"
```

## Strategy 3: File-Based Selective Staging

### Using git add -p

Interactive staging for precise control:

```bash
# You modified UserViewModel.kt with:
# 1. New state property (feature)
# 2. Bug fix in existing function
# 3. Refactoring of helper method

# Stage hunks interactively
git add -p UserViewModel.kt

# For each hunk:
# y - stage this hunk
# n - skip this hunk
# s - split into smaller hunks
# e - manually edit the hunk
# q - quit

# Select 'y' for state property
# Commit the feature
git commit -m "feat(viewmodel): add loading state to UserViewModel"

# Select 'y' for bug fix
git commit -m "fix(viewmodel): handle null user in updateProfile"

# Select 'y' for refactoring
git commit -m "refactor(viewmodel): extract validation helper method"
```

### Practical Example

```bash
# View unstaged changes
git diff UserRepository.kt

# Output shows:
# +val cache = mutableMapOf<String, User>()    # Feature: caching
# -throw Exception("Error")                    # Fix: better error handling
# +throw UserNotFoundException(id)             # Fix: better error handling
#  fun findUser(id: String) { ... }
# +private fun validateId(id: String) { ... }  # Refactor: extract method

# Stage interactively
git add -p UserRepository.kt

# Hunk 1: cache field
# Stage? y
git commit -m "feat(data): add in-memory cache to UserRepository"

# Hunk 2: error handling
# Stage? y
git commit -m "fix(data): improve error messages in UserRepository"

# Hunk 3: validation method
# Stage? y
git commit -m "refactor(data): extract ID validation method"
```

## Strategy 4: Dependency-Ordered Commits

### Respect Dependencies

Commit in order of dependencies:

```
1. Models (no dependencies)
2. Interfaces (depend on models)
3. Implementations (depend on interfaces)
4. UI (depends on everything)
5. Tests (depends on implementations)
```

**Example:**
```bash
# Correct order
git commit -m "feat(domain): add User model"                    # 1. Model
git commit -m "feat(domain): add UserRepository interface"     # 2. Interface
git commit -m "feat(data): implement UserRepository"           # 3. Implementation
git commit -m "feat(presentation): create UserViewModel"       # 4. ViewModel
git commit -m "feat(ui): build UserProfile screen"             # 5. UI
git commit -m "test(domain): add UserRepository tests"         # 6. Tests
```

**Wrong order (breaks build between commits):**
```bash
# ❌ Bad: UI before ViewModel exists
git commit -m "feat(ui): build UserProfile screen"
git commit -m "feat(presentation): create UserViewModel"  # Now UI doesn't compile
```

## Strategy 5: Current Situation - Too Many Changes

### When You Have 50+ Modified Files

**Step 1: Assess the changes**
```bash
# List all modified files
git status

# See changes by directory
git status | grep modified | cut -d: -f2 | sort

# View diff stats
git diff --stat
```

**Step 2: Group by category**
```bash
# Create groups
# Group 1: Domain layer
# Group 2: Data layer
# Group 3: Presentation layer
# Group 4: UI layer
# Group 5: Tests
# Group 6: Documentation
```

**Step 3: Commit group by group**
```bash
# Domain models
git add domain/model/
git commit -m "feat(SPEC-XXX): add domain models"

# Domain use cases
git add domain/usecase/
git commit -m "feat(SPEC-XXX): add domain use cases"

# Data API
git add data/remote/
git commit -m "feat(SPEC-XXX): add API integration"

# Data database
git add data/local/
git commit -m "feat(SPEC-XXX): add database entities"

# Data repository
git add data/repository/
git commit -m "feat(SPEC-XXX): implement repository"

# Presentation state
git add presentation/state/
git commit -m "feat(SPEC-XXX): define UI states"

# Presentation ViewModel
git add presentation/viewmodel/
git commit -m "feat(SPEC-XXX): create ViewModels"

# UI components
git add ui/components/
git commit -m "feat(SPEC-XXX): add UI components"

# UI screens
git add ui/screens/
git commit -m "feat(SPEC-XXX): build screens"

# Tests
git add test/
git commit -m "test(SPEC-XXX): add comprehensive tests"

# Documentation
git add docs/ README.md
git commit -m "docs(SPEC-XXX): update documentation"
```

## Tools and Commands

### View What Will Be Committed

```bash
# See staged changes
git diff --cached

# See staged files
git diff --cached --name-only

# See unstaged changes
git diff

# See all changes
git diff HEAD
```

### Selective Staging Commands

```bash
# Stage entire file
git add path/to/file.kt

# Stage multiple files
git add file1.kt file2.kt file3.kt

# Stage directory
git add domain/

# Stage by pattern
git add domain/**/*.kt

# Interactive staging
git add -p file.kt

# Stage all in directory with confirmation
git add -i
# Select '2' for Update
# Select files by number
```

### Unstage if Needed

```bash
# Unstage file
git restore --staged file.kt

# Unstage all
git restore --staged .

# Unstage specific hunks
git restore --staged -p file.kt
```

### Verify Before Committing

```bash
# Check what's staged
git diff --cached

# Build to verify commit is buildable
./gradlew assembleDebug

# Run tests to verify commit is working
./gradlew test

# If OK, commit
git commit -m "..."

# If not OK, unstage and fix
git restore --staged .
```

## Commit Size Guidelines

### Ideal Commit Size

- **Lines changed:** 50-200 lines (max 500)
- **Files changed:** 1-5 files (max 10)
- **Time to review:** 5-10 minutes
- **Scope:** Single layer or single feature aspect

### When a Commit is Too Large

**Signs:**
- > 500 lines changed
- > 10 files changed
- Multiple layers mixed
- Takes > 15 minutes to review
- Subject line is vague

**Solution:**
```bash
# Split using git reset
git reset HEAD~1  # Undo last commit, keep changes

# Stage smaller chunks
git add specific/files
git commit -m "feat(scope): specific change"

# Repeat for remaining changes
```

### When a Commit is Too Small

**Signs:**
- < 10 lines changed
- Trivial changes (typos, formatting)
- Should be part of logical change
- Creates noise in history

**Solution:**
```bash
# Combine with next related change
# Or use git commit --amend to add to previous commit
git add more/changes
git commit --amend --no-edit
```

## Best Practices for Multi-Commit Features

### ✅ Do

1. **Plan before coding**
```bash
# Create SPEC first
python3 tools/spec_builder.py create "Feature"
# Plan commit sequence based on layers
```

2. **Commit frequently**
```bash
# After each logical change (1-2 hours work)
git commit -m "feat(layer): specific change"
```

3. **Follow layer order**
```bash
# Domain → Data → Presentation → UI → Tests → Docs
```

4. **Keep commits buildable**
```bash
# After each commit:
./gradlew build
```

5. **Write clear commit messages**
```bash
git commit -m "feat(data): implement ProductRepository

Cache-first strategy with Room.

Refs: SPEC-002, REQ-002-U-03"
```

6. **Reference SPEC IDs**
```bash
Refs: SPEC-XXX, REQ-XXX-Y-ZZ
```

### ❌ Avoid

1. **Giant commits**
```bash
# Bad: Everything in one commit
git add .
git commit -m "Add product feature"
```

2. **Mixed concerns**
```bash
# Bad: Multiple layers together
git commit -m "Add domain, data, and UI for products"
```

3. **Non-buildable commits**
```bash
# Bad: Commit UI before ViewModel exists
git commit -m "Add ProductScreen"  # References non-existent ViewModel
```

4. **Vague messages**
```bash
# Bad
git commit -m "Update files"
git commit -m "Fix stuff"
```

5. **Forgetting tests**
```bash
# Bad: No test commits
feat(domain): add models
feat(data): add repository
feat(ui): add screens
# Missing: test(domain/data/ui): add tests
```

## Recovery Strategies

### Already Made Giant Commit

```bash
# Undo commit but keep changes
git reset HEAD~1

# Now split into logical commits
git add domain/
git commit -m "feat(SPEC-XXX): add domain layer"

git add data/
git commit -m "feat(SPEC-XXX): add data layer"

# etc.
```

### Committed to Wrong Branch

```bash
# On wrong-branch
git log  # Note commit SHA

# Create correct branch from here
git checkout -b correct-branch

# Go back to wrong branch
git checkout wrong-branch

# Remove the commits
git reset --hard HEAD~3  # Remove last 3 commits

# Commits now only on correct-branch
```

### Need to Split Existing Commit

```bash
# Interactive rebase
git rebase -i HEAD~3  # Edit last 3 commits

# Mark commit to split with 'edit'
# Git will stop at that commit

# Reset to before that commit
git reset HEAD~1

# Stage and commit in smaller chunks
git add file1.kt
git commit -m "feat: first part"

git add file2.kt
git commit -m "feat: second part"

# Continue rebase
git rebase --continue
```

## Integration with SPEC-First

### SPEC-Driven Commit Planning

From SPEC requirements, plan commits:

```markdown
## SPEC-002: Product Catalog

### Requirements
- REQ-002-U-01: Fetch products from API
- REQ-002-U-02: Cache in local database
- REQ-002-U-03: Display product list
- REQ-002-E-01: Navigate on click

### Planned Commits
1. docs(SPEC-002): Add specification
2. feat(SPEC-002): Add Product model (REQ-002-U-01)
3. feat(SPEC-002): Add ProductRepository interface (REQ-002-U-01)
4. feat(SPEC-002): Add GetProductsUseCase (REQ-002-U-01)
5. feat(SPEC-002): Implement API integration (REQ-002-U-01)
6. feat(SPEC-002): Implement Room caching (REQ-002-U-02)
7. feat(SPEC-002): Implement repository (REQ-002-U-01, REQ-002-U-02)
8. feat(SPEC-002): Add ProductListViewModel (REQ-002-U-03)
9. feat(SPEC-002): Build ProductListScreen (REQ-002-U-03, REQ-002-E-01)
10. test(SPEC-002): Add comprehensive tests
11. docs(SPEC-002): Update documentation
```

### Traceability Through Commits

Each commit references requirements:

```bash
git log --oneline --grep="SPEC-002"

# Output:
# abc1234 docs(SPEC-002): Update documentation
# def5678 test(SPEC-002): Add comprehensive tests
# ghi9012 feat(SPEC-002): Build ProductListScreen (REQ-002-U-03, REQ-002-E-01)
# jkl3456 feat(SPEC-002): Add ProductListViewModel (REQ-002-U-03)
# ...
```

## Related Skills

- `android-git-atomic-commits` - Atomic commit principles
- `android-git-spec-workflow` - SPEC-First workflow
- `android-git-conventional-commits` - Commit message format
- `android-clean-architecture` - Layer structure for commits
- `android-mvvm-architecture` - Presentation layer commits

## References

- [Atomic Commits](https://www.freshconsulting.com/insights/blog/atomic-commits/)
- [Git Tools - Interactive Staging](https://git-scm.com/book/en/v2/Git-Tools-Interactive-Staging)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

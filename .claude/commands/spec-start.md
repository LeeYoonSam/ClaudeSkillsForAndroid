# Start SPEC-First Development

You are starting a SPEC-First development workflow for implementing a new feature.

## Your Task

Follow these steps in order:

### Step 1: Gather Requirements (Interactive)
Ask the user detailed questions about the feature they want to implement:
- What is the feature name and purpose?
- What are the specific requirements?
- What user stories or use cases are involved?
- Are there any constraints, dependencies, or edge cases?
- What data models or APIs are needed?

Continue asking questions until you have a complete understanding.

### Step 2: Generate SPEC Document
Once you have gathered all necessary information:

1. Run the SPEC builder in interactive mode:
   ```bash
   python3 tools/spec_builder.py interactive
   ```

2. Answer all prompts from the SPEC builder:
   - Feature name
   - Purpose
   - Requirements (one per line, type 'done' when finished)
   - Confirm the matched skills

3. The SPEC builder will:
   - Categorize requirements into EARS format (U/S/E/O/N)
   - Automatically match relevant Android skills
   - Generate a unique SPEC ID (e.g., SPEC-003)
   - Create the SPEC document at `specs/examples/[feature-slug]/SPEC.md`

### Step 3: Create Feature Branch
After the SPEC document is created:

```bash
# Create feature branch with SPEC ID
git checkout -b feature/SPEC-XXX-feature-name

# Commit the SPEC document first
git add specs/
git commit -m "docs(SPEC-XXX): Add [Feature Name] specification

Refs: SPEC-XXX

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### Step 4: Ready for Implementation
Now you can proceed with implementation following Clean Architecture layers:
1. Domain Layer (models, use cases, repository interfaces)
2. Data Layer (API, database, repository implementation)
3. Presentation Layer (ViewModel, state management)
4. UI Layer (Compose screens, components)
5. Tests (unit, UI, integration)
6. Documentation

Each commit should:
- Be atomic (one logical change)
- Reference SPEC and requirement IDs: `Refs: SPEC-XXX, REQ-XXX-Y-ZZ`
- Follow conventional commit format
- Use the android-git-atomic-commits skill

## Important Reminders

- **DO NOT** skip SPEC creation
- **DO NOT** start coding before the SPEC is committed
- **DO** ask clarifying questions
- **DO** use the android-git-spec-workflow skill for guidance

---

**Ready to start? Let's begin by gathering requirements for your feature!**

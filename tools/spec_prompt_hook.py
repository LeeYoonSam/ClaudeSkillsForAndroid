#!/usr/bin/env python3
"""
SPEC-First Prompt Hook

Automatically adds SPEC-First context to user prompts when implementing features.
This hook triggers on UserPromptSubmit and injects reminders about the SPEC-First workflow.

Usage:
    Automatically called by Claude Code via hooks configuration in .claude/settings.local.json
"""

import sys
import json
import re


def should_trigger_spec_reminder(prompt: str) -> bool:
    """
    Check if the user prompt suggests starting new feature implementation work.

    Args:
        prompt: User's input prompt

    Returns:
        True if SPEC-First reminder should be shown
    """
    # Keywords that suggest feature implementation
    trigger_patterns = [
        # English patterns
        r'\b(implement|create|build|add|develop|make)\b.*\b(feature|screen|page|component|function)',
        r'\b(implement|create|build|add|develop)\b',
        r'\bnew\s+(feature|screen|page|component)',

        # Korean patterns
        r'(구현|개발|만들|생성|추가).*\b(기능|화면|페이지|컴포넌트|함수)',
        r'(구현|개발|만들|생성|추가)\s*(해|하)',
        r'새\s*(기능|화면|페이지|컴포넌트)',
    ]

    prompt_lower = prompt.lower()

    for pattern in trigger_patterns:
        if re.search(pattern, prompt_lower, re.IGNORECASE):
            return True

    return False


def generate_spec_first_context() -> str:
    """
    Generate SPEC-First workflow context to inject into the conversation.

    Returns:
        Context string with SPEC-First instructions
    """
    return """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  SPEC-First Development Workflow Reminder
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This project follows SPEC-First development methodology.

BEFORE implementing ANY feature, you MUST:

1️⃣  **Gather Requirements (Interactive)**
   - Ask clarifying questions about the feature
   - Understand user needs, scope, and constraints
   - Identify edge cases and non-functional requirements

2️⃣  **Generate SPEC Document**
   - Run: `python3 tools/spec_builder.py interactive`
   - Create EARS-format requirements (U/S/E/O/N types)
   - Match relevant Android skills automatically
   - Generate unique SPEC ID (e.g., SPEC-001)

3️⃣  **Create Feature Branch**
   - `git checkout -b feature/SPEC-XXX-feature-name`
   - Commit SPEC first: `git add specs/ && git commit -m "docs(SPEC-XXX): Add specification"`

4️⃣  **Implement in Layers** (Clean Architecture)
   - Domain Layer (models, use cases, repository interfaces)
   - Data Layer (API, database, repository implementation)
   - Presentation Layer (ViewModel, state management)
   - UI Layer (Compose screens, components)
   - Tests (unit, UI, integration)
   - Documentation

5️⃣  **Atomic Commits with Traceability**
   - Each commit references SPEC ID: `Refs: SPEC-XXX, REQ-XXX-Y-ZZ`
   - Follow conventional commits: `feat(domain): Add User model`
   - Use android-git-atomic-commits skill

6️⃣  **Validate & Sync**
   - Run: `python3 tools/validate_specs.py --spec SPEC-XXX`
   - Sync documentation: `python3 tools/doc_syncer.py`

📚 **Available Skills:**
   - android-git-spec-workflow: Full SPEC-First workflow guide
   - android-clean-architecture: Three-layer architecture
   - android-mvvm-architecture: ViewModel and state management
   - android-git-atomic-commits: Atomic commit guidelines

🚨 **DO NOT** start coding before creating the SPEC document!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Now, let's start with gathering requirements for your feature...
"""


def main():
    """Main entry point for the UserPromptSubmit hook."""
    try:
        # Read user prompt from stdin
        user_prompt = sys.stdin.read().strip()

        # Check if SPEC-First reminder should be triggered
        if should_trigger_spec_reminder(user_prompt):
            # Generate context
            context = generate_spec_first_context()

            # Output in Claude Code hook format
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "UserPromptSubmit",
                    "additionalContext": context
                }
            }

            print(json.dumps(output))
            sys.exit(0)
        else:
            # No additional context needed
            sys.exit(0)

    except Exception as e:
        # On error, fail silently to not block user prompt
        sys.stderr.write(f"Error in spec_prompt_hook: {e}\n")
        sys.exit(0)


if __name__ == "__main__":
    main()

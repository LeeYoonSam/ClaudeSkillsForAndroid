#!/usr/bin/env python3
"""
SPEC Builder Agent

Generates SPEC documents from user requirements using EARS format.
Automatically identifies related Android skills and creates structured specifications.

Usage:
    python spec_builder.py create "User Authentication"
    python spec_builder.py interactive
"""

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class AndroidSkillMatcher:
    """Matches feature descriptions to relevant Android skills."""

    # Android skills database (from .claude/skills/)
    SKILLS = {
        # Architecture
        "android-clean-architecture": {
            "keywords": ["clean architecture", "layer", "separation", "domain", "presentation", "data"],
            "category": "Architecture",
            "description": "Three-layer architecture pattern"
        },
        "android-mvvm-architecture": {
            "keywords": ["mvvm", "viewmodel", "state", "architecture"],
            "category": "Architecture",
            "description": "MVVM architecture with ViewModel"
        },

        # UI
        "android-compose-ui": {
            "keywords": ["ui", "screen", "compose", "jetpack compose", "composable", "interface"],
            "category": "UI",
            "description": "Declarative UI with Jetpack Compose"
        },
        "android-compose-navigation": {
            "keywords": ["navigation", "screen", "route", "navigate", "deep link"],
            "category": "UI",
            "description": "Navigation between screens"
        },
        "android-compose-theming": {
            "keywords": ["theme", "color", "typography", "material design", "dark mode"],
            "category": "UI",
            "description": "Material 3 theming"
        },
        "android-material-components": {
            "keywords": ["button", "card", "dialog", "material", "component"],
            "category": "UI",
            "description": "Material Design components"
        },
        "android-list-ui": {
            "keywords": ["list", "recyclerview", "lazycolumn", "scroll"],
            "category": "UI",
            "description": "Scrollable lists"
        },
        "android-forms-validation": {
            "keywords": ["form", "input", "validation", "field", "validate"],
            "category": "UI",
            "description": "Form input and validation"
        },
        "android-xml-views": {
            "keywords": ["xml", "view", "legacy", "viewbinding"],
            "category": "UI",
            "description": "XML-based views"
        },

        # Dependency Injection
        "android-hilt-di": {
            "keywords": ["dependency injection", "di", "hilt", "inject", "module"],
            "category": "DI",
            "description": "Dependency injection with Hilt"
        },
        "android-koin-di": {
            "keywords": ["koin", "dependency injection", "di"],
            "category": "DI",
            "description": "Dependency injection with Koin"
        },

        # Data Layer
        "android-repository-pattern": {
            "keywords": ["repository", "data source", "data layer"],
            "category": "Data",
            "description": "Repository pattern"
        },
        "android-database-room": {
            "keywords": ["database", "room", "sql", "local storage", "cache"],
            "category": "Data",
            "description": "Local database with Room"
        },
        "android-networking-retrofit": {
            "keywords": ["api", "network", "retrofit", "http", "rest", "endpoint"],
            "category": "Data",
            "description": "REST API with Retrofit"
        },
        "android-datastore": {
            "keywords": ["preferences", "datastore", "settings", "key-value"],
            "category": "Data",
            "description": "DataStore for preferences"
        },

        # State Management
        "android-stateflow": {
            "keywords": ["state", "stateflow", "flow", "reactive", "observable"],
            "category": "State",
            "description": "State management with StateFlow"
        },
        "android-one-time-events": {
            "keywords": ["event", "navigation event", "one-time", "channel"],
            "category": "State",
            "description": "One-time UI events"
        },

        # Async & Background
        "android-coroutines": {
            "keywords": ["async", "coroutine", "suspend", "background", "thread"],
            "category": "Async",
            "description": "Asynchronous operations with Coroutines"
        },
        "android-workmanager": {
            "keywords": ["background work", "workmanager", "periodic", "sync"],
            "category": "Background",
            "description": "Background tasks with WorkManager"
        },
        "android-paging3": {
            "keywords": ["pagination", "paging", "infinite scroll", "load more"],
            "category": "Data",
            "description": "Pagination with Paging 3"
        },

        # Testing
        "android-compose-testing": {
            "keywords": ["test", "ui test", "compose test", "testing"],
            "category": "Testing",
            "description": "UI testing for Compose"
        },
        "android-unit-testing": {
            "keywords": ["unit test", "testing", "test", "mock"],
            "category": "Testing",
            "description": "Unit testing"
        },

        # Build
        "android-gradle-config": {
            "keywords": ["gradle", "build", "configuration", "dependency"],
            "category": "Build",
            "description": "Gradle build configuration"
        },
        "android-project-setup": {
            "keywords": ["setup", "project", "initialize", "new project"],
            "category": "Setup",
            "description": "Project setup and structure"
        },

        # Common Features
        "android-permissions": {
            "keywords": ["permission", "runtime permission", "access"],
            "category": "Features",
            "description": "Runtime permissions"
        },
        "android-image-loading": {
            "keywords": ["image", "coil", "glide", "picture", "photo"],
            "category": "Features",
            "description": "Image loading with Coil/Glide"
        },

        # JSON Parsing
        "android-json-moshi": {
            "keywords": ["json", "moshi", "parsing", "serialization", "api", "adapter"],
            "category": "JSON",
            "description": "JSON parsing with Moshi"
        },
        "android-json-kotlinx": {
            "keywords": ["json", "kotlin serialization", "serializable", "kotlinx", "serialization"],
            "category": "JSON",
            "description": "Kotlin Serialization"
        },

        # Testing (additional)
        "android-testing-mockk": {
            "keywords": ["mock", "test", "mockk", "testing", "verify", "stub"],
            "category": "Testing",
            "description": "Mocking with MockK"
        },
        "android-testing-turbine": {
            "keywords": ["flow", "test", "turbine", "stateflow", "testing", "await"],
            "category": "Testing",
            "description": "Flow testing with Turbine"
        },

        # Utilities
        "android-logging-timber": {
            "keywords": ["log", "timber", "logging", "debug", "error"],
            "category": "Utilities",
            "description": "Logging with Timber"
        },

        # Animation
        "android-animation-lottie": {
            "keywords": ["animation", "lottie", "animate", "motion", "after effects"],
            "category": "Animation",
            "description": "Lottie animations"
        },

        # Git Workflow
        "android-git-atomic-commits": {
            "keywords": ["git", "commit", "atomic", "conventional", "traceability", "small commits"],
            "category": "Git",
            "description": "Atomic commits with conventional format"
        },
        "android-git-spec-workflow": {
            "keywords": ["git", "spec", "workflow", "branch", "feature branch", "pull request"],
            "category": "Git",
            "description": "SPEC-First git workflow"
        },
        "android-git-conventional-commits": {
            "keywords": ["git", "conventional", "commit message", "changelog", "semantic versioning"],
            "category": "Git",
            "description": "Conventional commit format"
        },
        "android-git-multi-commit-feature": {
            "keywords": ["git", "split", "multi commit", "refactor", "large feature", "code review"],
            "category": "Git",
            "description": "Split features into commits"
        },
    }

    def match_skills(self, feature_description: str, requirements: List[str]) -> List[str]:
        """Match skills based on feature description and requirements.

        Args:
            feature_description: Feature name/description
            requirements: List of requirement descriptions

        Returns:
            List of matched skill names
        """
        text = f"{feature_description} {' '.join(requirements)}".lower()

        matched_skills = []
        for skill_name, skill_data in self.SKILLS.items():
            score = 0
            for keyword in skill_data["keywords"]:
                if keyword in text:
                    score += 1

            if score > 0:
                matched_skills.append((skill_name, score))

        # Sort by score (descending) and return skill names
        matched_skills.sort(key=lambda x: x[1], reverse=True)

        # Always include core architecture skills for substantial features
        core_skills = ["android-clean-architecture", "android-mvvm-architecture", "android-compose-ui"]
        result = []

        # Add matched skills
        for skill, _ in matched_skills:
            if skill not in result:
                result.append(skill)

        # Add core skills if not already included
        for core_skill in core_skills:
            if core_skill not in result:
                result.append(core_skill)

        return result[:10]  # Return top 10 skills


class EARSRequirementGenerator:
    """Generates requirements in EARS format."""

    @staticmethod
    def generate_requirement_id(spec_id: str, req_type: str, number: int) -> str:
        """Generate requirement ID.

        Args:
            spec_id: SPEC ID (e.g., '001')
            req_type: Requirement type (U/S/E/O/N)
            number: Sequential number

        Returns:
            Requirement ID (e.g., 'REQ-001-U-01')
        """
        return f"REQ-{spec_id}-{req_type}-{number:02d}"

    @staticmethod
    def categorize_requirement(requirement: str) -> Tuple[str, str]:
        """Categorize a requirement into EARS format.

        Args:
            requirement: Requirement description

        Returns:
            Tuple of (requirement_type, formatted_requirement)
        """
        req_lower = requirement.lower()

        # Event-driven patterns
        if any(word in req_lower for word in ["when", "on click", "on tap", "trigger", "event"]):
            if not requirement.startswith("WHEN"):
                return "E", f"WHEN [trigger event], the system shall {requirement}"
            return "E", requirement

        # State-driven patterns
        if any(word in req_lower for word in ["while", "during", "in state"]):
            if not requirement.startswith("WHILE"):
                return "S", f"WHILE [in specific state], the system shall {requirement}"
            return "S", requirement

        # Unwanted behaviors
        if any(word in req_lower for word in ["shall not", "must not", "cannot", "should not"]):
            if not requirement.startswith("IF"):
                return "N", f"IF [condition], THEN the system shall NOT {requirement}"
            return "N", requirement

        # Optional features
        if any(word in req_lower for word in ["optional", "if enabled", "where available"]):
            if not requirement.startswith("WHERE"):
                return "O", f"WHERE [feature is enabled], the system shall {requirement}"
            return "O", requirement

        # Default: Ubiquitous requirement
        if not requirement.startswith("The system shall"):
            return "U", f"The system shall {requirement}"
        return "U", requirement


class SpecBuilder:
    """Main SPEC builder class."""

    def __init__(self, project_root: Path):
        """Initialize SPEC builder.

        Args:
            project_root: Root directory of the project
        """
        self.project_root = project_root
        self.specs_dir = project_root / "specs" / "examples"
        self.templates_dir = project_root / "specs" / "templates"
        self.skill_matcher = AndroidSkillMatcher()
        self.ears_generator = EARSRequirementGenerator()

    def get_next_spec_id(self) -> str:
        """Get next available SPEC ID.

        Returns:
            Next SPEC ID (e.g., '001', '002')
        """
        if not self.specs_dir.exists():
            return "001"

        spec_ids = []
        for spec_dir in self.specs_dir.iterdir():
            if spec_dir.is_dir():
                spec_file = spec_dir / "SPEC.md"
                if spec_file.exists():
                    # Extract SPEC ID from frontmatter
                    with open(spec_file, 'r') as f:
                        content = f.read()
                        match = re.search(r'spec_id:\s*SPEC-(\d+)', content)
                        if match:
                            spec_ids.append(int(match.group(1)))

        next_id = max(spec_ids) + 1 if spec_ids else 1
        return f"{next_id:03d}"

    def interactive_mode(self):
        """Run interactive SPEC creation mode."""
        print(f"\n{Colors.HEADER}{Colors.BOLD}=== SPEC Builder - Interactive Mode ==={Colors.ENDC}\n")

        # Step 1: Feature name
        print(f"{Colors.OKCYAN}Step 1: Feature Information{Colors.ENDC}")
        feature_name = input(f"{Colors.BOLD}Feature name:{Colors.ENDC} ").strip()
        if not feature_name:
            print(f"{Colors.FAIL}Error: Feature name is required{Colors.ENDC}")
            return

        # Step 2: Purpose
        purpose = input(f"{Colors.BOLD}Purpose (why this feature):{Colors.ENDC} ").strip()

        # Step 3: Requirements
        print(f"\n{Colors.OKCYAN}Step 2: Requirements{Colors.ENDC}")
        print("Enter requirements (one per line). Type 'done' when finished:")
        requirements = []
        while True:
            req = input(f"{Colors.BOLD}{len(requirements) + 1}.{Colors.ENDC} ").strip()
            if req.lower() == 'done':
                break
            if req:
                requirements.append(req)

        if not requirements:
            print(f"{Colors.FAIL}Error: At least one requirement is needed{Colors.ENDC}")
            return

        # Step 4: Match skills
        print(f"\n{Colors.OKCYAN}Step 3: Identifying related Android skills...{Colors.ENDC}")
        matched_skills = self.skill_matcher.match_skills(feature_name, requirements)

        print(f"\n{Colors.OKGREEN}Found {len(matched_skills)} related skills:{Colors.ENDC}")
        for i, skill in enumerate(matched_skills, 1):
            skill_info = self.skill_matcher.SKILLS.get(skill, {})
            category = skill_info.get("category", "Unknown")
            desc = skill_info.get("description", "")
            print(f"  {i}. {skill} ({category}): {desc}")

        # Step 5: Confirm
        print(f"\n{Colors.OKCYAN}Step 4: Confirmation{Colors.ENDC}")
        confirm = input(f"{Colors.BOLD}Generate SPEC with these details? (y/n):{Colors.ENDC} ").strip().lower()

        if confirm != 'y':
            print(f"{Colors.WARNING}Cancelled{Colors.ENDC}")
            return

        # Generate SPEC
        spec_id = self.get_next_spec_id()
        self.create_spec(
            spec_id=spec_id,
            feature_name=feature_name,
            purpose=purpose,
            requirements=requirements,
            matched_skills=matched_skills
        )

    def create_spec(
        self,
        spec_id: str,
        feature_name: str,
        purpose: str,
        requirements: List[str],
        matched_skills: List[str],
        author: str = "Claude Code"
    ):
        """Create a SPEC document.

        Args:
            spec_id: SPEC ID
            feature_name: Feature name
            purpose: Feature purpose
            requirements: List of requirement descriptions
            matched_skills: List of related skill names
            author: Author name
        """
        # Create directory
        feature_slug = feature_name.lower().replace(" ", "-")
        spec_dir = self.specs_dir / feature_slug
        spec_dir.mkdir(parents=True, exist_ok=True)

        spec_file = spec_dir / "SPEC.md"

        # Categorize requirements
        categorized_reqs = {
            "U": [],  # Ubiquitous
            "S": [],  # State-driven
            "E": [],  # Event-driven
            "O": [],  # Optional
            "N": [],  # Unwanted
        }

        for req in requirements:
            req_type, formatted_req = self.ears_generator.categorize_requirement(req)
            categorized_reqs[req_type].append(formatted_req)

        # Generate requirement IDs
        ears_requirements = []
        req_number = {"U": 1, "S": 1, "E": 1, "O": 1, "N": 1}

        for req_type in ["U", "S", "E", "O", "N"]:
            for req in categorized_reqs[req_type]:
                req_id = self.ears_generator.generate_requirement_id(
                    spec_id, req_type, req_number[req_type]
                )
                ears_requirements.append((req_id, req_type, req))
                req_number[req_type] += 1

        # Generate SPEC content
        content = self._generate_spec_content(
            spec_id=spec_id,
            feature_name=feature_name,
            purpose=purpose,
            ears_requirements=ears_requirements,
            matched_skills=matched_skills,
            author=author
        )

        # Write SPEC file
        with open(spec_file, 'w') as f:
            f.write(content)

        print(f"\n{Colors.OKGREEN}{Colors.BOLD}✓ SPEC created successfully!{Colors.ENDC}")
        print(f"{Colors.OKBLUE}Location: {spec_file}{Colors.ENDC}")
        print(f"{Colors.OKBLUE}SPEC ID: SPEC-{spec_id}{Colors.ENDC}")
        print(f"{Colors.OKBLUE}Requirements: {len(ears_requirements)}{Colors.ENDC}")
        print(f"{Colors.OKBLUE}Related Skills: {len(matched_skills)}{Colors.ENDC}")

    def _generate_spec_content(
        self,
        spec_id: str,
        feature_name: str,
        purpose: str,
        ears_requirements: List[Tuple[str, str, str]],
        matched_skills: List[str],
        author: str
    ) -> str:
        """Generate SPEC document content.

        Args:
            spec_id: SPEC ID
            feature_name: Feature name
            purpose: Feature purpose
            ears_requirements: List of (req_id, req_type, requirement)
            matched_skills: List of related skill names
            author: Author name

        Returns:
            SPEC document content
        """
        today = datetime.now().strftime("%Y-%m-%d")

        # Frontmatter
        content = f"""---
spec_id: SPEC-{spec_id}
feature: {feature_name}
status: draft
version: 1.0.0
author: {author}
date: {today}
related_skills:
"""
        for skill in matched_skills:
            content += f"  - {skill}\n"

        content += """traceability:
  requirements: []
  code_files: []
  test_files: []
---

"""

        # Title and Overview
        content += f"""# {feature_name} Specification

## 1. Overview

**Purpose**: {purpose}

**Scope**:
- In Scope: [To be defined]
- Out of Scope: [To be defined]

**Dependencies**:
- External: [To be defined]
- Internal: [To be defined]

---

## 2. Requirements (EARS Format)

"""

        # Group requirements by type
        req_by_type = {
            "U": ("Ubiquitous Requirements (Core Functionality)", []),
            "S": ("State-Driven Requirements", []),
            "E": ("Event-Driven Requirements", []),
            "O": ("Optional Requirements", []),
            "N": ("Unwanted Behaviors", []),
        }

        for req_id, req_type, req in ears_requirements:
            req_by_type[req_type][1].append((req_id, req))

        # Write requirements
        for req_type, (section_title, reqs) in req_by_type.items():
            if reqs:
                content += f"""### 2.{list(req_by_type.keys()).index(req_type) + 1} {section_title}
"""
                if req_type == "U":
                    content += "*Format: \"The system shall [requirement]\"*\n\n"
                elif req_type == "S":
                    content += "*Format: \"WHILE [state], the system shall [requirement]\"*\n\n"
                elif req_type == "E":
                    content += "*Format: \"WHEN [trigger event], the system shall [requirement]\"*\n\n"
                elif req_type == "O":
                    content += "*Format: \"WHERE [feature is enabled], the system shall [requirement]\"*\n\n"
                elif req_type == "N":
                    content += "*Format: \"IF [condition], THEN the system shall NOT [unwanted behavior]\"*\n\n"

                for req_id, req in reqs:
                    content += f"- **{req_id}**: {req}\n"

                content += "\n"

        # User Stories (template)
        content += """---

## 3. User Stories

### Story 1: [User Story Title]
**As a** [user type]
**I want** [goal/desire]
**So that** [benefit/value]

**Acceptance Criteria**:
- [ ] Given [precondition], when [action], then [expected result]

**Related Requirements**: [REQ IDs]

---

## 4. Architecture (Clean Architecture)

### 4.1 Domain Layer

**Models**:
```kotlin
data class [ModelName](
    val id: String,
    // Add properties based on requirements
)
```

**Use Cases**:
- `Get[Entity]UseCase`: [Description]
- `Create[Entity]UseCase`: [Description]

**Repository Interfaces**:
```kotlin
interface [Entity]Repository {
    suspend fun get[Entity](id: String): Result<[Entity]>
}
```

### 4.2 Data Layer

**API Endpoints**:
- `GET /api/[endpoint]`: [Description]
- `POST /api/[endpoint]`: [Description]

**Database Schema**:
```kotlin
@Entity(tableName = "[table_name]")
data class [Entity]Entity(
    @PrimaryKey val id: String,
    // Fields
)
```

### 4.3 Presentation Layer

**Screens**:
- `[Feature]Screen.kt`: [Description]

**ViewModels**:
```kotlin
@HiltViewModel
class [Feature]ViewModel @Inject constructor() : ViewModel() {
    // Implementation
}
```

---

## 5. Related Skills

This feature uses the following Android skills:

"""

        for skill in matched_skills:
            skill_info = self.skill_matcher.SKILLS.get(skill, {})
            desc = skill_info.get("description", "")
            content += f"- `{skill}`: {desc}\n"

        content += """
---

## 6. Implementation Checklist

### Domain Layer
- [ ] Define domain models
- [ ] Create use cases
- [ ] Define repository interfaces

### Data Layer
- [ ] Implement API service
- [ ] Create database entities
- [ ] Implement repository

### Presentation Layer
- [ ] Create ViewModel
- [ ] Define State, Actions, Events
- [ ] Implement UI screens

### Testing
- [ ] Write unit tests (85%+ coverage)
- [ ] Write UI tests
- [ ] Write integration tests

### Documentation
- [ ] Update README
- [ ] Add code comments with SPEC IDs
- [ ] Generate documentation

---

## 7. Traceability Matrix

| Requirement | Code File | Test File | Status |
|-------------|-----------|-----------|--------|
"""

        for req_id, _, _ in ears_requirements:
            content += f"| {req_id} | [TBD] | [TBD] | ⏳ Pending |\n"

        content += """
**Legend**: ⏳ Pending | 🟢 Implemented | ✅ Tested | ❌ Failed

---

## 8. Notes & Considerations

### Next Steps
1. Review and refine requirements
2. Define detailed user stories
3. Design data models
4. Begin implementation

### Questions to Resolve
- [Question 1]
- [Question 2]

---

**Document Version**: 1.0.0
**Last Updated**: """ + today + """
**Status**: Draft - Ready for review
"""

        return content


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="SPEC Builder - Generate SPEC documents from requirements")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Interactive mode
    subparsers.add_parser("interactive", help="Run in interactive mode")

    # Quick create mode
    create_parser = subparsers.add_parser("create", help="Quick create SPEC")
    create_parser.add_argument("feature_name", help="Feature name")
    create_parser.add_argument("--purpose", "-p", help="Feature purpose")
    create_parser.add_argument("--requirements", "-r", nargs="+", help="Requirements")

    args = parser.parse_args()

    # Find project root
    current_dir = Path.cwd()
    project_root = current_dir
    while project_root != project_root.parent:
        if (project_root / ".claude").exists():
            break
        project_root = project_root.parent
    else:
        print(f"{Colors.FAIL}Error: Could not find project root (no .claude directory){Colors.ENDC}")
        sys.exit(1)

    builder = SpecBuilder(project_root)

    if args.command == "interactive" or args.command is None:
        builder.interactive_mode()
    elif args.command == "create":
        # Quick create mode
        spec_id = builder.get_next_spec_id()
        purpose = args.purpose or "To be defined"
        requirements = args.requirements or ["Define requirements"]
        matched_skills = builder.skill_matcher.match_skills(args.feature_name, requirements)

        builder.create_spec(
            spec_id=spec_id,
            feature_name=args.feature_name,
            purpose=purpose,
            requirements=requirements,
            matched_skills=matched_skills
        )


if __name__ == "__main__":
    main()

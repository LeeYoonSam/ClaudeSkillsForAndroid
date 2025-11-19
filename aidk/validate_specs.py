#!/usr/bin/env python3
"""
SPEC Validator

Validates SPEC.md files for correctness and completeness.

Usage:
    python validate_specs.py specs/examples/user-authentication/SPEC.md
    python validate_specs.py --all
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple

# ANSI colors
class Colors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


class SpecValidator:
    """Validates SPEC documents."""

    REQUIRED_SECTIONS = [
        "## 1. Overview",
        "## 2. Requirements (EARS Format)",
        "## 3. User Stories",
        "## 4. Architecture (Clean Architecture)",
        "## 5. Related Skills",
        "## 6. Implementation Checklist",
        "## 7. Traceability Matrix",
    ]

    REQUIRED_FRONTMATTER_FIELDS = [
        'spec_id',
        'feature',
        'status',
        'version',
        'related_skills',
    ]

    def __init__(self, spec_file: Path):
        """Initialize validator.

        Args:
            spec_file: Path to SPEC.md
        """
        self.spec_file = spec_file
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate(self) -> bool:
        """Validate SPEC file.

        Returns:
            True if valid, False otherwise
        """
        if not self.spec_file.exists():
            self.errors.append(f"File not found: {self.spec_file}")
            return False

        with open(self.spec_file, 'r') as f:
            content = f.read()

        # Validate frontmatter
        self._validate_frontmatter(content)

        # Validate sections
        self._validate_sections(content)

        # Validate requirements
        self._validate_requirements(content)

        # Validate SPEC ID format
        self._validate_spec_id(content)

        # Print results
        self._print_results()

        return len(self.errors) == 0

    def _validate_frontmatter(self, content: str):
        """Validate YAML frontmatter."""
        frontmatter_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)

        if not frontmatter_match:
            self.errors.append("Missing YAML frontmatter")
            return

        frontmatter = frontmatter_match.group(1)

        # Check required fields
        for field in self.REQUIRED_FRONTMATTER_FIELDS:
            if f"{field}:" not in frontmatter:
                self.errors.append(f"Missing required frontmatter field: {field}")

        # Validate related_skills format
        if 'related_skills:' in frontmatter:
            skills_match = re.search(r'related_skills:\n((?:  - .*\n)*)', frontmatter)
            if not skills_match:
                self.warnings.append("No skills listed in related_skills")

    def _validate_sections(self, content: str):
        """Validate required sections."""
        for section in self.REQUIRED_SECTIONS:
            if section not in content:
                self.errors.append(f"Missing required section: {section}")

    def _validate_requirements(self, content: str):
        """Validate requirements format."""
        # Find requirements
        req_pattern = r'-\s+\*\*([A-Z0-9-]+)\*\*:\s+(.+)'
        requirements = re.findall(req_pattern, content)

        if not requirements:
            self.warnings.append("No requirements found")
            return

        # Validate requirement IDs
        for req_id, _ in requirements:
            if not req_id.startswith('REQ-'):
                self.errors.append(f"Invalid requirement ID format: {req_id}")
                continue

            # Format: REQ-XXX-Y-ZZ
            if not re.match(r'REQ-\d+-[USEON]-\d+', req_id):
                self.warnings.append(f"Non-standard requirement ID format: {req_id}")

        # Check for EARS format
        ears_sections = [
            "Ubiquitous Requirements",
            "State-Driven Requirements",
            "Event-Driven Requirements",
        ]

        for section in ears_sections:
            if section not in content:
                self.warnings.append(f"No {section} section found")

    def _validate_spec_id(self, content: str):
        """Validate SPEC ID format."""
        spec_id_match = re.search(r'spec_id:\s*SPEC-(\d+)', content)

        if not spec_id_match:
            self.errors.append("Invalid SPEC ID format")
            return

        spec_id = spec_id_match.group(1)

        # Check if ID is used consistently
        if f"SPEC-{spec_id}" not in content:
            self.warnings.append(f"SPEC ID SPEC-{spec_id} not referenced in document")

    def _print_results(self):
        """Print validation results."""
        print(f"\n{Colors.BOLD}Validating: {self.spec_file}{Colors.ENDC}\n")

        if self.errors:
            print(f"{Colors.FAIL}{Colors.BOLD}Errors:{Colors.ENDC}")
            for error in self.errors:
                print(f"  {Colors.FAIL}✗{Colors.ENDC} {error}")

        if self.warnings:
            print(f"\n{Colors.WARNING}{Colors.BOLD}Warnings:{Colors.ENDC}")
            for warning in self.warnings:
                print(f"  {Colors.WARNING}⚠{Colors.ENDC} {warning}")

        if not self.errors and not self.warnings:
            print(f"{Colors.OKGREEN}{Colors.BOLD}✓ SPEC is valid!{Colors.ENDC}")
        elif not self.errors:
            print(f"\n{Colors.OKGREEN}{Colors.BOLD}✓ SPEC is valid (with warnings){Colors.ENDC}")
        else:
            print(f"\n{Colors.FAIL}{Colors.BOLD}✗ SPEC validation failed{Colors.ENDC}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Validate SPEC documents")
    parser.add_argument("spec_file", nargs='?', help="Path to SPEC.md file")
    parser.add_argument("--all", action="store_true", help="Validate all SPEC files")

    args = parser.parse_args()

    # Find project root
    current_dir = Path.cwd()
    project_root = current_dir
    while project_root != project_root.parent:
        if (project_root / ".claude").exists():
            break
        project_root = project_root.parent
    else:
        print(f"{Colors.FAIL}Error: Could not find project root{Colors.ENDC}")
        sys.exit(1)

    # Determine files to validate
    if args.all:
        specs_dir = project_root / "specs" / "examples"
        spec_files = list(specs_dir.rglob("SPEC.md"))
        if not spec_files:
            print(f"{Colors.WARNING}No SPEC files found{Colors.ENDC}")
            sys.exit(0)
    elif args.spec_file:
        spec_files = [Path(args.spec_file)]
    else:
        parser.print_help()
        sys.exit(1)

    # Validate files
    all_valid = True
    for spec_file in spec_files:
        validator = SpecValidator(spec_file)
        if not validator.validate():
            all_valid = False
        print()

    sys.exit(0 if all_valid else 1)


if __name__ == "__main__":
    main()

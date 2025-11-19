#!/usr/bin/env python3
"""
Doc Syncer Agent

Ensures SPEC, code, and documentation stay synchronized.
Generates documentation, updates traceability matrices, and detects mismatches.

Usage:
    python doc_syncer.py sync specs/examples/user-authentication/SPEC.md --code examples/generated-auth
    python doc_syncer.py verify specs/examples/user-authentication/SPEC.md --code examples/generated-auth
"""

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

# ANSI colors
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


@dataclass
class CodeReference:
    """Reference to code implementing a requirement."""
    file_path: str
    line_number: int
    requirement_id: str


@dataclass
class SyncReport:
    """Synchronization report."""
    spec_id: str
    feature: str
    total_requirements: int
    implemented_requirements: Set[str]
    missing_requirements: Set[str]
    code_files: List[str]
    test_files: List[str]
    mismatches: List[str]


class CodeAnalyzer:
    """Analyzes code for SPEC references."""

    @staticmethod
    def find_spec_references(code_dir: Path) -> Dict[str, List[CodeReference]]:
        """Find all SPEC ID references in code.

        Args:
            code_dir: Directory containing code

        Returns:
            Dict mapping requirement IDs to code references
        """
        references: Dict[str, List[CodeReference]] = {}

        # Find all Kotlin files
        for kt_file in code_dir.rglob("*.kt"):
            with open(kt_file, 'r') as f:
                lines = f.readlines()

            for line_num, line in enumerate(lines, 1):
                # Pattern: // SPEC-XXX or // REQ-XXX-Y-ZZ
                matches = re.findall(r'//\s*((?:SPEC|REQ)-[A-Z0-9-]+)', line)
                for match in matches:
                    if match not in references:
                        references[match] = []

                    references[match].append(CodeReference(
                        file_path=str(kt_file.relative_to(code_dir)),
                        line_number=line_num,
                        requirement_id=match
                    ))

        return references

    @staticmethod
    def find_test_files(code_dir: Path) -> List[str]:
        """Find all test files.

        Args:
            code_dir: Directory containing code

        Returns:
            List of test file paths
        """
        test_dir = code_dir / "src" / "test"
        if not test_dir.exists():
            return []

        return [
            str(f.relative_to(code_dir))
            for f in test_dir.rglob("*Test.kt")
        ]

    @staticmethod
    def count_test_coverage(test_dir: Path) -> int:
        """Count number of test methods.

        Args:
            test_dir: Test directory

        Returns:
            Number of test methods
        """
        count = 0
        for test_file in test_dir.rglob("*Test.kt"):
            with open(test_file, 'r') as f:
                content = f.read()
                # Count @Test annotations
                count += len(re.findall(r'@Test', content))

        return count


class SpecParser:
    """Parses SPEC documents."""

    @staticmethod
    def parse_requirements(spec_file: Path) -> List[str]:
        """Parse requirement IDs from SPEC.

        Args:
            spec_file: Path to SPEC.md

        Returns:
            List of requirement IDs
        """
        with open(spec_file, 'r') as f:
            content = f.read()

        # Pattern: - **REQ-XXX-Y-ZZ**:
        requirements = re.findall(r'-\s+\*\*([A-Z0-9-]+)\*\*:', content)

        # Filter to only REQ- IDs
        return [req for req in requirements if req.startswith('REQ-')]

    @staticmethod
    def parse_metadata(spec_file: Path) -> Dict[str, str]:
        """Parse SPEC metadata.

        Args:
            spec_file: Path to SPEC.md

        Returns:
            Dict of metadata
        """
        with open(spec_file, 'r') as f:
            content = f.read()

        metadata = {}

        # Extract frontmatter
        frontmatter_match = re.search(r'---\n(.*?)\n---', content, re.DOTALL)
        if frontmatter_match:
            frontmatter = frontmatter_match.group(1)

            # Extract fields
            for field in ['spec_id', 'feature', 'version', 'status']:
                match = re.search(rf'{field}:\s*(.+)', frontmatter)
                if match:
                    metadata[field] = match.group(1).strip()

        return metadata


class DocSyncer:
    """Main document synchronization class."""

    def __init__(self, spec_file: Path, code_dir: Path):
        """Initialize doc syncer.

        Args:
            spec_file: Path to SPEC.md
            code_dir: Directory containing generated code
        """
        self.spec_file = spec_file
        self.code_dir = code_dir
        self.spec_dir = spec_file.parent

    def verify(self) -> SyncReport:
        """Verify SPEC-code alignment.

        Returns:
            Sync report
        """
        print(f"\n{Colors.HEADER}{Colors.BOLD}=== Doc Syncer - Verification ==={Colors.ENDC}\n")

        # Parse SPEC
        metadata = SpecParser.parse_metadata(self.spec_file)
        requirements = SpecParser.parse_requirements(self.spec_file)

        print(f"{Colors.OKBLUE}SPEC: {metadata.get('feature', 'Unknown')} ({metadata.get('spec_id', 'Unknown')}){Colors.ENDC}")
        print(f"{Colors.OKBLUE}Total Requirements: {len(requirements)}{Colors.ENDC}\n")

        # Analyze code
        references = CodeAnalyzer.find_spec_references(self.code_dir)
        test_files = CodeAnalyzer.find_test_files(self.code_dir)

        # Find implemented requirements
        implemented = set()
        for req_id in requirements:
            if req_id in references:
                implemented.add(req_id)

        missing = set(requirements) - implemented

        # Find all code files
        code_files = [
            str(f.relative_to(self.code_dir))
            for f in self.code_dir.rglob("*.kt")
            if "/test/" not in str(f)
        ]

        # Create report
        report = SyncReport(
            spec_id=metadata.get('spec_id', 'Unknown'),
            feature=metadata.get('feature', 'Unknown'),
            total_requirements=len(requirements),
            implemented_requirements=implemented,
            missing_requirements=missing,
            code_files=code_files,
            test_files=test_files,
            mismatches=[]
        )

        # Print results
        self._print_verification_results(report, references)

        return report

    def sync(self) -> SyncReport:
        """Synchronize documentation with code.

        Returns:
            Sync report
        """
        print(f"\n{Colors.HEADER}{Colors.BOLD}=== Doc Syncer - Synchronization ==={Colors.ENDC}\n")

        # First verify
        report = self.verify()

        # Update SPEC traceability matrix
        print(f"\n{Colors.OKCYAN}Updating SPEC traceability matrix...{Colors.ENDC}")
        self._update_traceability_matrix(report)

        # Generate README
        print(f"{Colors.OKCYAN}Generating README...{Colors.ENDC}")
        self._generate_readme(report)

        # Generate architecture diagram
        print(f"{Colors.OKCYAN}Generating architecture diagram...{Colors.ENDC}")
        self._generate_architecture_diagram(report)

        print(f"\n{Colors.OKGREEN}{Colors.BOLD}✓ Synchronization complete!{Colors.ENDC}")

        return report

    def _print_verification_results(self, report: SyncReport, references: Dict[str, List[CodeReference]]):
        """Print verification results."""
        # Implementation status
        impl_percentage = (len(report.implemented_requirements) / report.total_requirements * 100) if report.total_requirements > 0 else 0

        print(f"{Colors.OKCYAN}Implementation Status:{Colors.ENDC}")
        print(f"  Implemented: {len(report.implemented_requirements)}/{report.total_requirements} ({impl_percentage:.1f}%)")
        print(f"  Missing: {len(report.missing_requirements)}")

        if report.implemented_requirements:
            print(f"\n{Colors.OKGREEN}Implemented Requirements:{Colors.ENDC}")
            for req_id in sorted(report.implemented_requirements):
                refs = references.get(req_id, [])
                print(f"  ✓ {req_id}")
                for ref in refs:
                    print(f"    → {ref.file_path}:{ref.line_number}")

        if report.missing_requirements:
            print(f"\n{Colors.WARNING}Missing Requirements:{Colors.ENDC}")
            for req_id in sorted(report.missing_requirements):
                print(f"  ✗ {req_id}")

        # Code files
        print(f"\n{Colors.OKCYAN}Code Files:{Colors.ENDC}")
        print(f"  Source files: {len(report.code_files)}")
        print(f"  Test files: {len(report.test_files)}")

        # Test coverage
        test_dir = self.code_dir / "src" / "test"
        if test_dir.exists():
            test_count = CodeAnalyzer.count_test_coverage(test_dir)
            print(f"  Test methods: {test_count}")

    def _update_traceability_matrix(self, report: SyncReport):
        """Update traceability matrix in SPEC."""
        with open(self.spec_file, 'r') as f:
            content = f.read()

        # Find traceability matrix section
        matrix_pattern = r'## 7\. Traceability Matrix\n\n\| Requirement \| Code File \| Test File \| Status \|\n\|-------------|-----------|-----------|--------|\n(.*?)\n\n'
        matrix_match = re.search(matrix_pattern, content, re.DOTALL)

        if not matrix_match:
            print(f"  {Colors.WARNING}Warning: Traceability matrix section not found{Colors.ENDC}")
            return

        # Build new matrix rows
        references = CodeAnalyzer.find_spec_references(self.code_dir)
        new_rows = []

        all_reqs = report.implemented_requirements | report.missing_requirements
        for req_id in sorted(all_reqs):
            code_file = "—"
            test_file = "—"
            status = "⏳ Pending"

            if req_id in report.implemented_requirements:
                refs = references.get(req_id, [])
                if refs:
                    code_file = refs[0].file_path
                    status = "🟢 Implemented"

            new_rows.append(f"| {req_id} | {code_file} | {test_file} | {status} |")

        new_matrix = "\n".join(new_rows)

        # Replace matrix
        new_content = re.sub(
            matrix_pattern,
            f"## 7. Traceability Matrix\n\n| Requirement | Code File | Test File | Status |\n|-------------|-----------|-----------|--------|\n{new_matrix}\n\n",
            content,
            flags=re.DOTALL
        )

        # Write back
        with open(self.spec_file, 'w') as f:
            f.write(new_content)

        print(f"  {Colors.OKGREEN}✓ Traceability matrix updated{Colors.ENDC}")

    def _generate_readme(self, report: SyncReport):
        """Generate README for the feature."""
        readme_path = self.spec_dir / "README.md"

        impl_percentage = (len(report.implemented_requirements) / report.total_requirements * 100) if report.total_requirements > 0 else 0.0

        content = f"""# {report.feature}

## Overview

SPEC ID: {report.spec_id}

## Implementation Status

- **Requirements**: {len(report.implemented_requirements)}/{report.total_requirements} implemented ({impl_percentage:.1f}%)
- **Source Files**: {len(report.code_files)}
- **Test Files**: {len(report.test_files)}

## Requirements

### Implemented

"""

        for req_id in sorted(report.implemented_requirements):
            content += f"- ✅ {req_id}\n"

        if report.missing_requirements:
            content += "\n### Pending\n\n"
            for req_id in sorted(report.missing_requirements):
                content += f"- ⏳ {req_id}\n"

        content += f"""
## Architecture

This feature follows Clean Architecture with three layers:

### Domain Layer
- Models: Pure business objects
- Use Cases: Business logic
- Repository Interfaces: Data access contracts

### Data Layer
- API: Network data source
- DTOs: Data transfer objects
- Repository Implementation: Data access logic

### Presentation Layer
- ViewModel: State management
- State: UI state definitions
- Screen: Compose UI

## Files

### Source Files

"""

        for file_path in sorted(report.code_files):
            content += f"- `{file_path}`\n"

        content += "\n### Test Files\n\n"

        for file_path in sorted(report.test_files):
            content += f"- `{file_path}`\n"

        content += f"""
## References

- [SPEC Document](./SPEC.md)
- [Architecture Diagram](./architecture.md)

---

*Generated by Doc Syncer*
"""

        with open(readme_path, 'w') as f:
            f.write(content)

        print(f"  {Colors.OKGREEN}✓ README generated: {readme_path}{Colors.ENDC}")

    def _generate_architecture_diagram(self, report: SyncReport):
        """Generate architecture diagram."""
        diagram_path = self.spec_dir / "architecture.md"

        content = f"""# {report.feature} - Architecture

## Clean Architecture Layers

```
┌─────────────────────────────────────────────────────┐
│                 Presentation Layer                   │
│  ┌──────────────┐  ┌───────────────────────────┐   │
│  │   Screen     │  │       ViewModel           │   │
│  │  (Compose)   │←→│  (State Management)       │   │
│  └──────────────┘  └───────────────────────────┘   │
└─────────────────────────────┬───────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────┐
│                    Domain Layer                      │
│  ┌──────────────┐  ┌───────────────────────────┐   │
│  │   Models     │  │       Use Cases           │   │
│  │  (Business)  │  │  (Business Logic)         │   │
│  └──────────────┘  └───────────────────────────┘   │
│  ┌──────────────────────────────────────────────┐  │
│  │        Repository Interfaces                  │  │
│  │        (Data Access Contracts)                │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────┬───────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────┐
│                    Data Layer                        │
│  ┌──────────────┐  ┌───────────────────────────┐   │
│  │  API/DAO     │  │  Repository Implementation│   │
│  │ (Data Source)│  │   (Data Access Logic)     │   │
│  └──────────────┘  └───────────────────────────┘   │
│  ┌──────────────────────────────────────────────┐  │
│  │              DTOs / Entities                  │  │
│  │         (Data Transfer Objects)               │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

## Component Breakdown

### Presentation Layer

"""

        # List presentation files
        presentation_files = [f for f in report.code_files if "/presentation/" in f]
        for file_path in presentation_files:
            content += f"- `{file_path}`\n"

        content += "\n### Domain Layer\n\n"

        # List domain files
        domain_files = [f for f in report.code_files if "/domain/" in f]
        for file_path in domain_files:
            content += f"- `{file_path}`\n"

        content += "\n### Data Layer\n\n"

        # List data files
        data_files = [f for f in report.code_files if "/data/" in f]
        for file_path in data_files:
            content += f"- `{file_path}`\n"

        content += f"""
## Dependency Flow

```
Presentation → Domain → Data
     ↓           ↓        ↓
 ViewModel → UseCase → Repository
```

**Key Principle**: Dependencies point inward. Outer layers depend on inner layers, never the reverse.

---

*Generated by Doc Syncer*
"""

        with open(diagram_path, 'w') as f:
            f.write(content)

        print(f"  {Colors.OKGREEN}✓ Architecture diagram generated: {diagram_path}{Colors.ENDC}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Doc Syncer - Synchronize SPEC, code, and docs")
    parser.add_argument("command", choices=["verify", "sync"], help="Command to execute")
    parser.add_argument("spec_file", help="Path to SPEC.md file")
    parser.add_argument("--code", "-c", required=True, help="Code directory")

    args = parser.parse_args()

    # Validate paths
    spec_file = Path(args.spec_file)
    code_dir = Path(args.code)

    if not spec_file.exists():
        print(f"{Colors.FAIL}Error: SPEC file not found: {spec_file}{Colors.ENDC}")
        sys.exit(1)

    if not code_dir.exists():
        print(f"{Colors.FAIL}Error: Code directory not found: {code_dir}{Colors.ENDC}")
        sys.exit(1)

    # Run syncer
    syncer = DocSyncer(spec_file, code_dir)

    if args.command == "verify":
        report = syncer.verify()
        # Exit with error if there are missing requirements
        if report.missing_requirements:
            sys.exit(1)
    elif args.command == "sync":
        syncer.sync()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
AIDK Installer Module

Handles installation of AIDK skills, templates, and tools to Claude Code projects.
Supports both local (project-specific) and global installations.
"""

import json
import shutil
from pathlib import Path
from typing import List, Dict, Optional
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from aidk import SKILLS_DIR, TEMPLATES_DIR, EXAMPLES_DIR, __version__

console = Console()


def find_claude_directory(project_dir: Path) -> Optional[Path]:
    """
    Find the .claude directory in the project.

    Args:
        project_dir: Root directory of the project

    Returns:
        Path to .claude directory, or None if not found
    """
    claude_dir = project_dir / ".claude"

    if not claude_dir.exists():
        console.print(f"⚠️  [yellow]No .claude directory found in: {project_dir}[/yellow]")
        console.print("\n💡 This doesn't look like a Claude Code project.")

        if console.input("\nCreate .claude directory? [Y/n]: ").lower() != 'n':
            claude_dir.mkdir(parents=True, exist_ok=True)
            console.print(f"✅ Created .claude directory at: {claude_dir}")
            return claude_dir
        else:
            return None

    return claude_dir


def install_skills(claude_dir: Path, force: bool = False) -> bool:
    """
    Install all AIDK skills to the Claude Code project.

    Args:
        claude_dir: Path to .claude directory
        force: Overwrite existing files

    Returns:
        True if installation successful
    """
    skills_target = claude_dir / "skills"
    skills_target.mkdir(parents=True, exist_ok=True)

    # Get list of skills
    skills = list(SKILLS_DIR.glob("android-*"))

    if not skills:
        console.print(f"❌ [red]No skills found in: {SKILLS_DIR}[/red]")
        return False

    console.print(f"\n📦 Installing {len(skills)} Android skills...")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Installing skills...", total=len(skills))

        for skill_dir in skills:
            if not skill_dir.is_dir():
                continue

            skill_name = skill_dir.name
            target_skill = skills_target / skill_name

            if target_skill.exists() and not force:
                progress.console.print(f"⏭️  Skipping {skill_name} (already exists)")
                progress.advance(task)
                continue

            try:
                if target_skill.exists():
                    shutil.rmtree(target_skill)

                shutil.copytree(skill_dir, target_skill)
                progress.console.print(f"✅ Installed: {skill_name}")
                progress.advance(task)

            except Exception as e:
                progress.console.print(f"❌ Failed to install {skill_name}: {e}")
                return False

    console.print(f"\n✨ Successfully installed {len(skills)} skills!")
    return True


def install_templates(project_dir: Path, force: bool = False) -> bool:
    """
    Install SPEC templates to the project.

    Args:
        project_dir: Root directory of the project
        force: Overwrite existing files

    Returns:
        True if installation successful
    """
    templates_target = project_dir / "specs" / "templates"
    templates_target.mkdir(parents=True, exist_ok=True)

    templates = list(TEMPLATES_DIR.glob("*.md"))

    if not templates:
        console.print(f"⚠️  [yellow]No templates found in: {TEMPLATES_DIR}[/yellow]")
        return True  # Not a critical error

    console.print(f"\n📄 Installing {len(templates)} SPEC templates...")

    for template_file in templates:
        target_file = templates_target / template_file.name

        if target_file.exists() and not force:
            console.print(f"⏭️  Skipping {template_file.name} (already exists)")
            continue

        try:
            shutil.copy2(template_file, target_file)
            console.print(f"✅ Installed: {template_file.name}")
        except Exception as e:
            console.print(f"❌ Failed to install {template_file.name}: {e}")
            return False

    return True


def install_examples(project_dir: Path, force: bool = False) -> bool:
    """
    Install example SPECs and generated code.

    Args:
        project_dir: Root directory of the project
        force: Overwrite existing files

    Returns:
        True if installation successful
    """
    # Install example SPECs
    specs_target = project_dir / "specs" / "examples"
    specs_target.mkdir(parents=True, exist_ok=True)

    examples = list(EXAMPLES_DIR.glob("*"))

    if not examples:
        console.print(f"⚠️  [yellow]No examples found in: {EXAMPLES_DIR}[/yellow]")
        return True  # Not a critical error

    console.print(f"\n📚 Installing {len(examples)} examples...")

    for example_dir in examples:
        if not example_dir.is_dir():
            continue

        target_dir = specs_target / example_dir.name

        if target_dir.exists() and not force:
            console.print(f"⏭️  Skipping {example_dir.name} (already exists)")
            continue

        try:
            if target_dir.exists():
                shutil.rmtree(target_dir)

            shutil.copytree(example_dir, target_dir)
            console.print(f"✅ Installed: {example_dir.name}")
        except Exception as e:
            console.print(f"❌ Failed to install {example_dir.name}: {e}")
            return False

    return True


def update_claude_settings(claude_dir: Path) -> bool:
    """
    Update Claude Code settings to enable AIDK features.

    Args:
        claude_dir: Path to .claude directory

    Returns:
        True if update successful
    """
    settings_file = claude_dir / "settings.local.json"

    # Create default settings if not exists
    if not settings_file.exists():
        settings = {
            "permissions": {
                "webSearch": {"allowed": True},
                "webFetch": {"allowed": ["*"]},
                "bash": {"allowed": ["*"]},
                "pythonExecutable": "python3"
            },
            "hooks": {
                "userPromptSubmit": {
                    "command": "python3",
                    "args": ["tools/spec_prompt_hook.py"]
                }
            }
        }

        try:
            with open(settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
            console.print(f"\n✅ Created settings file: {settings_file}")
            return True
        except Exception as e:
            console.print(f"\n❌ Failed to create settings: {e}")
            return False

    # Settings file exists - just notify
    console.print(f"\n💡 Settings file already exists: {settings_file}")
    console.print("   Make sure to enable permissions and hooks as needed")
    return True


def install_to_project(
    project_dir: Path,
    include_examples: bool = False,
    force: bool = False
) -> bool:
    """
    Install AIDK to a Claude Code project.

    Args:
        project_dir: Root directory of the project
        include_examples: Include example SPECs and generated code
        force: Overwrite existing files

    Returns:
        True if installation successful
    """
    console.print(f"\n📁 Project directory: {project_dir}")

    # Find or create .claude directory
    claude_dir = find_claude_directory(project_dir)
    if not claude_dir:
        return False

    # Install skills
    if not install_skills(claude_dir, force):
        return False

    # Install templates
    if not install_templates(project_dir, force):
        return False

    # Install examples (optional)
    if include_examples:
        if not install_examples(project_dir, force):
            return False

    # Update settings
    if not update_claude_settings(claude_dir):
        return False

    # Copy tools to project (for hooks)
    tools_target = project_dir / "tools"
    tools_target.mkdir(parents=True, exist_ok=True)

    # Copy spec_prompt_hook.py for the hook
    hook_script = Path(__file__).parent / "spec_prompt_hook.py"
    if hook_script.exists():
        try:
            shutil.copy2(hook_script, tools_target / "spec_prompt_hook.py")
            console.print(f"\n✅ Installed hook script to: {tools_target}")
        except Exception as e:
            console.print(f"\n⚠️  [yellow]Failed to install hook script: {e}[/yellow]")

    return True


def list_skills() -> List[Dict[str, str]]:
    """
    List all available AIDK skills with metadata.

    Returns:
        List of skill dictionaries with name, description, category
    """
    skills = []

    # Define skill categories
    categories = {
        "android-project-setup": "Core Architecture",
        "android-clean-architecture": "Core Architecture",
        "android-mvvm-architecture": "Core Architecture",
        "android-compose-ui": "UI Development",
        "android-compose-navigation": "UI Development",
        "android-compose-theming": "UI Development",
        "android-xml-views": "UI Development",
        "android-hilt-di": "Dependency Injection",
        "android-koin-di": "Dependency Injection",
        "android-repository-pattern": "Data Layer",
        "android-database-room": "Data Layer",
        "android-networking-retrofit": "Data Layer",
        "android-datastore": "Data Layer",
        "android-json-moshi": "JSON Parsing",
        "android-json-kotlinx": "JSON Parsing",
        "android-stateflow": "State Management",
        "android-one-time-events": "State Management",
        "android-coroutines": "Async & Background",
        "android-workmanager": "Async & Background",
        "android-paging3": "Async & Background",
        "android-compose-testing": "Testing",
        "android-unit-testing": "Testing",
        "android-testing-mockk": "Testing",
        "android-testing-turbine": "Testing",
        "android-gradle-config": "Build Configuration",
        "android-permissions": "Common Features",
        "android-image-loading": "Common Features",
        "android-forms-validation": "Common Features",
        "android-list-ui": "Common Features",
        "android-material-components": "Common Features",
        "android-logging-timber": "Utilities",
        "android-animation-lottie": "Animation",
        "android-git-atomic-commits": "Git Workflow",
        "android-git-spec-workflow": "Git Workflow",
        "android-git-conventional-commits": "Git Workflow",
        "android-git-multi-commit-feature": "Git Workflow",
    }

    skill_dirs = sorted(SKILLS_DIR.glob("android-*"))

    for skill_dir in skill_dirs:
        if not skill_dir.is_dir():
            continue

        skill_name = skill_dir.name
        category = categories.get(skill_name, "Other")

        # Try to read description from skill.md
        skill_file = skill_dir / "skill.md"
        description = "Android development skill"

        if skill_file.exists():
            try:
                content = skill_file.read_text()
                # Extract first line or title
                lines = content.strip().split('\n')
                for line in lines:
                    if line.strip() and not line.startswith('#'):
                        description = line.strip()
                        break
            except Exception:
                pass

        skills.append({
            "name": skill_name,
            "description": description,
            "category": category
        })

    return skills


def main():
    """Test installer functionality."""
    import sys

    if len(sys.argv) < 2:
        console.print("Usage: python installer.py <project_dir> [--with-examples] [--force]")
        sys.exit(1)

    project_dir = Path(sys.argv[1])
    include_examples = '--with-examples' in sys.argv
    force = '--force' in sys.argv

    success = install_to_project(project_dir, include_examples, force)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()

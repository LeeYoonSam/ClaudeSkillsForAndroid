#!/usr/bin/env python3
"""
Android AI Development Kit - Unified CLI

Provides a unified command-line interface for all AIDK tools:
- Install/update skills and tools
- Create SPEC documents
- Generate code from SPECs
- Synchronize documentation
- Validate SPECs
"""

import sys
import click
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Import AIDK modules
from aidk import __version__
from aidk.updater import check_for_updates, perform_update
from aidk.installer import install_to_project, list_skills

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="Android AI DevKit")
@click.pass_context
def cli(ctx):
    """
    🤖 Android AI Development Kit (AIDK)

    SPEC-First Android development framework with 36 specialized skills,
    automated SPEC generation, code generation, and documentation sync.
    """
    # Check for updates in the background (cached for 24 hours)
    if ctx.invoked_subcommand not in ['update', 'version']:
        try:
            check_for_updates(silent=True)
        except Exception:
            # Silently ignore update check failures
            pass


@cli.command()
@click.option('--local', is_flag=True, help='Install to current project (.claude/ directory)')
@click.option('--global', 'global_install', is_flag=True, help='Install globally (default)')
@click.option('--with-examples', is_flag=True, help='Include example SPECs and generated code')
@click.option('--force', is_flag=True, help='Overwrite existing files')
def install(local, global_install, with_examples, force):
    """Install AIDK skills and tools to a Claude Code project."""
    console.print(Panel.fit(
        "📦 [bold cyan]Installing Android AI Development Kit[/bold cyan]",
        border_style="cyan"
    ))

    if local or not global_install:
        # Install to current project
        success = install_to_project(
            project_dir=Path.cwd(),
            include_examples=with_examples,
            force=force
        )
        if success:
            console.print("✅ [green]Installation completed successfully![/green]")
            console.print("\n💡 [yellow]Next steps:[/yellow]")
            console.print("  1. Run: [cyan]aidk spec create 'Your Feature Name'[/cyan]")
            console.print("  2. Open your project in Claude Code")
            console.print("  3. All 36 Android skills are now available!")
        else:
            console.print("❌ [red]Installation failed. See errors above.[/red]")
            sys.exit(1)
    else:
        # Global installation
        console.print("ℹ️  AIDK is already installed globally via pip.")
        console.print("\n💡 To install skills to a project, run:")
        console.print("  [cyan]cd your-android-project[/cyan]")
        console.print("  [cyan]aidk install --local[/cyan]")


@cli.command()
@click.option('--check-only', is_flag=True, help='Only check for updates, do not install')
def update(check_only):
    """Check for and install updates."""
    console.print(Panel.fit(
        "🔄 [bold cyan]Checking for Updates[/bold cyan]",
        border_style="cyan"
    ))

    latest_version = check_for_updates(silent=False)

    if latest_version and latest_version != __version__:
        console.print(f"\n✨ New version available: [green]{latest_version}[/green]")
        console.print(f"   Current version: [yellow]{__version__}[/yellow]")

        if not check_only:
            if click.confirm("\nDo you want to update now?", default=True):
                perform_update()
        else:
            console.print("\n💡 To update, run: [cyan]aidk update[/cyan]")
    else:
        console.print(f"✅ You're using the latest version: [green]{__version__}[/green]")


@cli.command()
def version():
    """Show version information and check for updates."""
    console.print(Panel.fit(
        f"[bold cyan]Android AI Development Kit[/bold cyan]\n"
        f"Version: [green]{__version__}[/green]",
        border_style="cyan"
    ))

    # Check for updates
    latest_version = check_for_updates(silent=False)

    if latest_version and latest_version != __version__:
        console.print(f"\n⚠️  New version available: [yellow]{latest_version}[/yellow]")
        console.print("   Run [cyan]aidk update[/cyan] to upgrade")
    else:
        console.print("\n✅ You're up to date!")


@cli.command(name='skills')
def list_skills_cmd():
    """List all available Android skills."""
    console.print(Panel.fit(
        "📚 [bold cyan]Available Android Skills[/bold cyan]",
        border_style="cyan"
    ))

    skills = list_skills()

    if not skills:
        console.print("❌ [red]No skills found. Try reinstalling AIDK.[/red]")
        sys.exit(1)

    # Group skills by category
    categories = {}
    for skill in skills:
        category = skill.get('category', 'Other')
        if category not in categories:
            categories[category] = []
        categories[category].append(skill)

    # Display skills by category
    for category, skills_list in sorted(categories.items()):
        table = Table(title=f"\n{category}", show_header=True, header_style="bold magenta")
        table.add_column("Skill", style="cyan", width=30)
        table.add_column("Description", style="white", width=60)

        for skill in sorted(skills_list, key=lambda x: x['name']):
            table.add_row(skill['name'], skill['description'])

        console.print(table)

    console.print(f"\n📊 Total: [green]{len(skills)}[/green] skills available")


@cli.group()
def spec():
    """SPEC document management commands."""
    pass


@spec.command(name='create')
@click.argument('feature_name')
@click.option('--interactive', '-i', is_flag=True, help='Use interactive mode')
@click.option('--purpose', '-p', help='Feature purpose')
@click.option('--requirements', '-r', multiple=True, help='Requirements (can be specified multiple times)')
def spec_create(feature_name, interactive, purpose, requirements):
    """Create a new SPEC document."""
    from aidk.spec_builder import main as spec_builder_main

    console.print(Panel.fit(
        f"📝 [bold cyan]Creating SPEC: {feature_name}[/bold cyan]",
        border_style="cyan"
    ))

    # Build arguments for spec_builder
    args = ['create', feature_name]

    if interactive:
        args = ['interactive']
    else:
        if purpose:
            args.extend(['--purpose', purpose])
        for req in requirements:
            args.extend(['--requirements', req])

    # Call spec_builder
    sys.argv = ['spec_builder.py'] + args
    spec_builder_main()


@spec.command(name='validate')
@click.argument('spec_file', type=click.Path(exists=True))
def spec_validate(spec_file):
    """Validate a SPEC document."""
    from aidk.validate_specs import main as validate_main

    console.print(Panel.fit(
        f"✅ [bold cyan]Validating SPEC: {spec_file}[/bold cyan]",
        border_style="cyan"
    ))

    # Call validate_specs
    sys.argv = ['validate_specs.py', spec_file]
    validate_main()


@cli.group()
def code():
    """Code generation commands."""
    pass


@code.command(name='generate')
@click.argument('spec_file', type=click.Path(exists=True))
@click.option('--output', '-o', default='./src', help='Output directory for generated code')
@click.option('--package', '-p', default='com.example.app', help='Android package name')
def code_generate(spec_file, output, package):
    """Generate code from a SPEC document."""
    from aidk.code_builder import main as code_builder_main

    console.print(Panel.fit(
        f"⚙️  [bold cyan]Generating code from: {spec_file}[/bold cyan]",
        border_style="cyan"
    ))

    # Call code_builder
    sys.argv = ['code_builder.py', 'generate', spec_file, '--output', output, '--package', package]
    code_builder_main()

    console.print(f"\n✅ [green]Code generated successfully in: {output}[/green]")


@cli.group()
def docs():
    """Documentation management commands."""
    pass


@docs.command(name='sync')
@click.argument('spec_file', type=click.Path(exists=True))
@click.option('--code', '-c', default='./src', help='Code directory to analyze')
def docs_sync(spec_file, code):
    """Synchronize documentation with SPEC and code."""
    from aidk.doc_syncer import main as doc_syncer_main

    console.print(Panel.fit(
        f"🔄 [bold cyan]Syncing docs for: {spec_file}[/bold cyan]",
        border_style="cyan"
    ))

    # Call doc_syncer
    sys.argv = ['doc_syncer.py', 'sync', spec_file, '--code', code]
    doc_syncer_main()

    console.print("\n✅ [green]Documentation synchronized successfully![/green]")


@docs.command(name='verify')
@click.argument('spec_file', type=click.Path(exists=True))
@click.option('--code', '-c', default='./src', help='Code directory to analyze')
def docs_verify(spec_file, code):
    """Verify SPEC-code alignment."""
    from aidk.doc_syncer import main as doc_syncer_main

    console.print(Panel.fit(
        f"🔍 [bold cyan]Verifying alignment: {spec_file}[/bold cyan]",
        border_style="cyan"
    ))

    # Call doc_syncer
    sys.argv = ['doc_syncer.py', 'verify', spec_file, '--code', code]
    doc_syncer_main()


@cli.command()
def info():
    """Display AIDK information and system status."""
    console.print(Panel.fit(
        "[bold cyan]Android AI Development Kit (AIDK)[/bold cyan]\n"
        f"Version: [green]{__version__}[/green]",
        border_style="cyan"
    ))

    # System information
    table = Table(show_header=False, box=None)
    table.add_column("Key", style="cyan")
    table.add_column("Value", style="white")

    table.add_row("Python Version", f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    table.add_row("Platform", sys.platform)

    # Check if in a Claude Code project
    claude_dir = Path.cwd() / ".claude"
    if claude_dir.exists():
        table.add_row("Claude Code Project", "✅ Yes")
        skills_dir = claude_dir / "skills"
        if skills_dir.exists():
            skill_count = len(list(skills_dir.glob("*")))
            table.add_row("Installed Skills", f"{skill_count}")
    else:
        table.add_row("Claude Code Project", "❌ No")

    console.print("\n")
    console.print(table)

    console.print("\n💡 [yellow]Quick Start:[/yellow]")
    console.print("  [cyan]aidk install --local[/cyan]        # Install skills to current project")
    console.print("  [cyan]aidk spec create 'Feature'[/cyan]  # Create a new SPEC")
    console.print("  [cyan]aidk skills[/cyan]                 # List all available skills")


def main():
    """Main entry point for the CLI."""
    try:
        cli()
    except KeyboardInterrupt:
        console.print("\n\n⚠️  [yellow]Operation cancelled by user[/yellow]")
        sys.exit(130)
    except Exception as e:
        console.print(f"\n❌ [red]Error: {str(e)}[/red]")
        sys.exit(1)


if __name__ == '__main__':
    main()

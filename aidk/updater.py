#!/usr/bin/env python3
"""
AIDK Auto-Updater Module

Handles version checking and automatic updates for AIDK.
Uses GitHub releases API to check for new versions.
"""

import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
from rich.console import Console

try:
    import requests
except ImportError:
    requests = None

from aidk import __version__

console = Console()

# GitHub repository information
GITHUB_REPO = "yourusername/android-ai-devkit"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"

# Cache file for update checks (avoid excessive API calls)
CACHE_FILE = Path.home() / ".aidk" / "update_cache.json"
CACHE_DURATION = timedelta(hours=24)


def get_cache() -> Optional[dict]:
    """
    Get cached update check data.

    Returns:
        Cached data dict, or None if cache is invalid/expired
    """
    if not CACHE_FILE.exists():
        return None

    try:
        with open(CACHE_FILE, 'r') as f:
            cache = json.load(f)

        # Check if cache is still valid
        cached_time = datetime.fromisoformat(cache.get('timestamp', ''))
        if datetime.now() - cached_time > CACHE_DURATION:
            return None

        return cache

    except (json.JSONDecodeError, ValueError, KeyError):
        return None


def set_cache(latest_version: str):
    """
    Save update check data to cache.

    Args:
        latest_version: Latest version string
    """
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)

    cache_data = {
        'timestamp': datetime.now().isoformat(),
        'latest_version': latest_version,
        'current_version': __version__
    }

    try:
        with open(CACHE_FILE, 'w') as f:
            json.dump(cache_data, f, indent=2)
    except Exception as e:
        # Silently fail on cache write errors
        pass


def parse_version(version: str) -> tuple:
    """
    Parse semantic version string into tuple for comparison.

    Args:
        version: Version string (e.g., "1.2.3")

    Returns:
        Version tuple (e.g., (1, 2, 3))
    """
    # Remove 'v' prefix if present
    version = version.lstrip('v')

    try:
        parts = version.split('.')
        return tuple(int(p) for p in parts[:3])
    except (ValueError, IndexError):
        return (0, 0, 0)


def check_for_updates(silent: bool = False) -> Optional[str]:
    """
    Check for available updates.

    Args:
        silent: If True, don't print any messages (use cache only)

    Returns:
        Latest version string if available, None otherwise
    """
    # Check cache first
    cache = get_cache()
    if cache:
        latest_version = cache.get('latest_version')
        if latest_version and not silent:
            current = parse_version(__version__)
            latest = parse_version(latest_version)
            if latest > current:
                console.print(
                    f"💡 [dim]New version available: {latest_version} "
                    f"(current: {__version__}). Run 'aidk update' to upgrade.[/dim]"
                )
        return latest_version

    # No cache or expired - check GitHub if not silent
    if silent:
        return None

    if requests is None:
        # requests not available, skip update check
        return None

    try:
        response = requests.get(GITHUB_API_URL, timeout=5)
        response.raise_for_status()

        data = response.json()
        latest_version = data.get('tag_name', '').lstrip('v')

        if latest_version:
            # Update cache
            set_cache(latest_version)

            # Compare versions
            current = parse_version(__version__)
            latest = parse_version(latest_version)

            if latest > current:
                return latest_version
            else:
                return __version__

    except requests.exceptions.RequestException:
        # Network error - silently fail
        return None
    except (json.JSONDecodeError, KeyError):
        # Invalid response - silently fail
        return None


def perform_update():
    """
    Perform automatic update using pip.
    """
    console.print("\n🔄 [cyan]Updating Android AI Development Kit...[/cyan]")

    try:
        # Try to update from PyPI
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", "android-ai-devkit"],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            console.print("✅ [green]Update completed successfully![/green]")
            console.print("\n💡 Changes will take effect on next run.")

            # Clear cache
            if CACHE_FILE.exists():
                CACHE_FILE.unlink()

            return True
        else:
            console.print("❌ [red]Update failed:[/red]")
            console.print(result.stderr)
            return False

    except subprocess.TimeoutExpired:
        console.print("❌ [red]Update timed out. Please try again.[/red]")
        return False
    except Exception as e:
        console.print(f"❌ [red]Update failed: {e}[/red]")
        console.print("\n💡 Try updating manually:")
        console.print("   [cyan]pip install --upgrade android-ai-devkit[/cyan]")
        return False


def get_latest_version_info() -> Optional[dict]:
    """
    Get detailed information about the latest release.

    Returns:
        Release information dict, or None if unavailable
    """
    if requests is None:
        return None

    try:
        response = requests.get(GITHUB_API_URL, timeout=5)
        response.raise_for_status()

        data = response.json()

        return {
            'version': data.get('tag_name', '').lstrip('v'),
            'name': data.get('name', ''),
            'body': data.get('body', ''),
            'published_at': data.get('published_at', ''),
            'html_url': data.get('html_url', ''),
        }

    except (requests.exceptions.RequestException, json.JSONDecodeError, KeyError):
        return None


def show_changelog(from_version: str, to_version: str):
    """
    Show changelog between two versions.

    Args:
        from_version: Current version
        to_version: Target version
    """
    release_info = get_latest_version_info()

    if not release_info:
        console.print("⚠️  [yellow]Could not fetch changelog[/yellow]")
        return

    console.print(f"\n📋 [bold cyan]Changelog ({from_version} → {to_version})[/bold cyan]")
    console.print("─" * 60)

    # Display release notes
    body = release_info.get('body', 'No changelog available.')
    console.print(body)

    console.print("─" * 60)

    # Display release URL
    html_url = release_info.get('html_url')
    if html_url:
        console.print(f"\n🔗 Full release notes: {html_url}")


def main():
    """Test updater functionality."""
    console.print(f"Current version: {__version__}")

    latest = check_for_updates(silent=False)

    if latest:
        console.print(f"Latest version: {latest}")

        if parse_version(latest) > parse_version(__version__):
            console.print("\n✨ Update available!")
            show_changelog(__version__, latest)

            if input("\nUpdate now? [y/N]: ").lower() == 'y':
                perform_update()
        else:
            console.print("\n✅ You're up to date!")
    else:
        console.print("\n⚠️  Could not check for updates")


if __name__ == '__main__':
    main()

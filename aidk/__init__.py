"""
Android AI Development Kit (AIDK)

A comprehensive SPEC-First development framework for Android projects.
Provides 36 specialized Android skills, automated SPEC generation, code generation,
and documentation synchronization tools.
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__license__ = "MIT"

from pathlib import Path

# Package root directory
PACKAGE_ROOT = Path(__file__).parent
DATA_DIR = PACKAGE_ROOT / "data"
SKILLS_DIR = DATA_DIR / "skills"
TEMPLATES_DIR = DATA_DIR / "templates"
EXAMPLES_DIR = DATA_DIR / "examples"

__all__ = [
    "__version__",
    "PACKAGE_ROOT",
    "DATA_DIR",
    "SKILLS_DIR",
    "TEMPLATES_DIR",
    "EXAMPLES_DIR",
]

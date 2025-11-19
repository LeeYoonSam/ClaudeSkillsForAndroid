"""
Setup script for Android AI Development Kit
Provides backward compatibility for older pip versions
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read version from VERSION file
version_file = Path(__file__).parent / "VERSION"
version = version_file.read_text().strip()

# Read long description from README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8")

setup(
    name="android-ai-devkit",
    version=version,
    description="AI-powered SPEC-First Android development framework with 36 specialized skills",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/android-ai-devkit",
    packages=find_packages(exclude=["tests", "tests.*", "docs", "examples"]),
    package_data={
        "aidk": [
            "data/skills/**/*",
            "data/templates/**/*",
            "data/examples/**/*",
        ],
    },
    include_package_data=True,
    install_requires=[
        "pyyaml>=6.0.1",
        "markdown>=3.5.1",
        "jinja2>=3.1.2",
        "click>=8.1.7",
        "rich>=13.7.0",
        "prompt-toolkit>=3.0.43",
        "requests>=2.31.0",
        "colorama>=0.4.6",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-cov>=4.1.0",
            "black>=23.12.0",
            "ruff>=0.1.8",
            "mypy>=1.7.1",
        ],
    },
    entry_points={
        "console_scripts": [
            "aidk=aidk.cli:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    keywords="android ai development-kit spec-first clean-architecture jetpack-compose claude-code",
    project_urls={
        "Documentation": "https://github.com/yourusername/android-ai-devkit/blob/main/README.md",
        "Source": "https://github.com/yourusername/android-ai-devkit",
        "Tracker": "https://github.com/yourusername/android-ai-devkit/issues",
    },
)

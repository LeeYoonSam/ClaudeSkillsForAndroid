#!/bin/bash
#
# Android AI Development Kit - Installation Script (Unix/Mac)
#
# This script installs AIDK globally and optionally to the current project.
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Print colored message
print_message() {
    local color=$1
    shift
    echo -e "${color}$@${NC}"
}

print_header() {
    echo ""
    print_message "$CYAN" "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    print_message "$CYAN" "  🤖 Android AI Development Kit Installer"
    print_message "$CYAN" "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
}

# Check Python installation
check_python() {
    print_message "$CYAN" "📋 Checking Python installation..."

    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        print_message "$GREEN" "✅ Found Python $PYTHON_VERSION"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
        PYTHON_VERSION=$(python --version | cut -d' ' -f2)
        print_message "$GREEN" "✅ Found Python $PYTHON_VERSION"
    else
        print_message "$RED" "❌ Python not found!"
        print_message "$YELLOW" "Please install Python 3.8 or later from https://www.python.org/"
        exit 1
    fi

    # Check Python version (require 3.8+)
    PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d'.' -f1)
    PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d'.' -f2)

    if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
        print_message "$RED" "❌ Python 3.8 or later is required (found $PYTHON_VERSION)"
        exit 1
    fi
}

# Check pip installation
check_pip() {
    print_message "$CYAN" "📦 Checking pip installation..."

    if $PYTHON_CMD -m pip --version &> /dev/null; then
        print_message "$GREEN" "✅ pip is installed"
    else
        print_message "$RED" "❌ pip not found!"
        print_message "$YELLOW" "Installing pip..."
        $PYTHON_CMD -m ensurepip --default-pip || {
            print_message "$RED" "Failed to install pip"
            exit 1
        }
    fi
}

# Install AIDK
install_aidk() {
    print_message "$CYAN" "🚀 Installing Android AI Development Kit..."

    # Check if installing from source or PyPI
    if [ -f "pyproject.toml" ]; then
        # Install from local source
        print_message "$YELLOW" "Installing from local source..."
        $PYTHON_CMD -m pip install -e . || {
            print_message "$RED" "❌ Installation failed!"
            exit 1
        }
    else
        # Install from PyPI
        print_message "$YELLOW" "Installing from PyPI..."
        $PYTHON_CMD -m pip install android-ai-devkit || {
            print_message "$RED" "❌ Installation failed!"
            print_message "$YELLOW" "You can try installing from source:"
            print_message "$YELLOW" "  git clone https://github.com/yourusername/android-ai-devkit.git"
            print_message "$YELLOW" "  cd android-ai-devkit"
            print_message "$YELLOW" "  pip install -e ."
            exit 1
        }
    fi

    print_message "$GREEN" "✅ AIDK installed successfully!"
}

# Verify installation
verify_installation() {
    print_message "$CYAN" "🔍 Verifying installation..."

    if command -v aidk &> /dev/null; then
        AIDK_VERSION=$(aidk version --no-check 2>/dev/null || aidk --version 2>&1 | head -n1)
        print_message "$GREEN" "✅ aidk command is available"
        print_message "$GREEN" "   $AIDK_VERSION"
    else
        print_message "$YELLOW" "⚠️  aidk command not found in PATH"
        print_message "$YELLOW" "   You may need to restart your terminal or add pip's bin directory to PATH"
    fi
}

# Install to current project
install_to_project() {
    if [ -d ".claude" ] || [ -d ".git" ]; then
        echo ""
        read -p "$(print_message $YELLOW 'Install AIDK skills to current project? [Y/n]: ')" -n 1 -r
        echo ""

        if [[ ! $REPLY =~ ^[Nn]$ ]]; then
            print_message "$CYAN" "📂 Installing to current project..."

            # Ask about examples
            read -p "$(print_message $YELLOW 'Include example SPECs? [y/N]: ')" -n 1 -r
            echo ""

            if [[ $REPLY =~ ^[Yy]$ ]]; then
                aidk install --local --with-examples || {
                    print_message "$RED" "❌ Project installation failed"
                    return 1
                }
            else
                aidk install --local || {
                    print_message "$RED" "❌ Project installation failed"
                    return 1
                }
            fi

            print_message "$GREEN" "✅ Skills installed to current project!"
        fi
    fi
}

# Show next steps
show_next_steps() {
    echo ""
    print_message "$GREEN" "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    print_message "$GREEN" "  ✨ Installation Complete!"
    print_message "$GREEN" "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    print_message "$CYAN" "📚 Quick Start:"
    echo ""
    print_message "$YELLOW" "  1. Navigate to your Android project:"
    echo "     cd /path/to/your/android/project"
    echo ""
    print_message "$YELLOW" "  2. Install AIDK skills to the project:"
    echo "     aidk install --local"
    echo ""
    print_message "$YELLOW" "  3. Create your first SPEC:"
    echo "     aidk spec create 'User Authentication'"
    echo ""
    print_message "$YELLOW" "  4. List available skills:"
    echo "     aidk skills"
    echo ""
    print_message "$YELLOW" "  5. Get help:"
    echo "     aidk --help"
    echo ""
    print_message "$CYAN" "📖 Documentation: https://github.com/yourusername/android-ai-devkit"
    echo ""
}

# Main installation flow
main() {
    print_header
    check_python
    check_pip
    install_aidk
    verify_installation
    install_to_project
    show_next_steps
}

# Run main function
main

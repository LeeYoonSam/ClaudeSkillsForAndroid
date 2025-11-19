# Android AI Development Kit - Installation Script (Windows PowerShell)
#
# This script installs AIDK globally and optionally to the current project.
#

# Enable strict mode
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# Print colored message
function Write-ColorMessage {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

function Write-Header {
    Write-Host ""
    Write-ColorMessage "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -Color Cyan
    Write-ColorMessage "  🤖 Android AI Development Kit Installer" -Color Cyan
    Write-ColorMessage "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -Color Cyan
    Write-Host ""
}

# Check Python installation
function Test-Python {
    Write-ColorMessage "📋 Checking Python installation..." -Color Cyan

    $pythonCmd = $null
    $pythonVersion = $null

    # Try python3 first
    try {
        $pythonVersion = & python3 --version 2>&1 | Out-String
        if ($LASTEXITCODE -eq 0) {
            $pythonCmd = "python3"
        }
    } catch {}

    # Try python if python3 not found
    if (-not $pythonCmd) {
        try {
            $pythonVersion = & python --version 2>&1 | Out-String
            if ($LASTEXITCODE -eq 0) {
                $pythonCmd = "python"
            }
        } catch {}
    }

    if (-not $pythonCmd) {
        Write-ColorMessage "❌ Python not found!" -Color Red
        Write-ColorMessage "Please install Python 3.8 or later from https://www.python.org/" -Color Yellow
        exit 1
    }

    Write-ColorMessage "✅ Found $pythonVersion" -Color Green

    # Parse version
    if ($pythonVersion -match "Python (\d+)\.(\d+)\.(\d+)") {
        $major = [int]$matches[1]
        $minor = [int]$matches[2]

        if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 8)) {
            Write-ColorMessage "❌ Python 3.8 or later is required (found $pythonVersion)" -Color Red
            exit 1
        }
    }

    return $pythonCmd
}

# Check pip installation
function Test-Pip {
    param([string]$PythonCmd)

    Write-ColorMessage "📦 Checking pip installation..." -Color Cyan

    try {
        & $PythonCmd -m pip --version 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-ColorMessage "✅ pip is installed" -Color Green
            return $true
        }
    } catch {}

    Write-ColorMessage "❌ pip not found!" -Color Red
    Write-ColorMessage "Installing pip..." -Color Yellow

    try {
        & $PythonCmd -m ensurepip --default-pip
        if ($LASTEXITCODE -eq 0) {
            Write-ColorMessage "✅ pip installed successfully" -Color Green
            return $true
        }
    } catch {
        Write-ColorMessage "❌ Failed to install pip" -Color Red
        exit 1
    }
}

# Install AIDK
function Install-AIDK {
    param([string]$PythonCmd)

    Write-ColorMessage "🚀 Installing Android AI Development Kit..." -Color Cyan

    # Check if installing from source or PyPI
    if (Test-Path "pyproject.toml") {
        # Install from local source
        Write-ColorMessage "Installing from local source..." -Color Yellow
        & $PythonCmd -m pip install -e .

        if ($LASTEXITCODE -ne 0) {
            Write-ColorMessage "❌ Installation failed!" -Color Red
            exit 1
        }
    } else {
        # Install from PyPI
        Write-ColorMessage "Installing from PyPI..." -Color Yellow
        & $PythonCmd -m pip install android-ai-devkit

        if ($LASTEXITCODE -ne 0) {
            Write-ColorMessage "❌ Installation failed!" -Color Red
            Write-ColorMessage "You can try installing from source:" -Color Yellow
            Write-ColorMessage "  git clone https://github.com/yourusername/android-ai-devkit.git" -Color Yellow
            Write-ColorMessage "  cd android-ai-devkit" -Color Yellow
            Write-ColorMessage "  pip install -e ." -Color Yellow
            exit 1
        }
    }

    Write-ColorMessage "✅ AIDK installed successfully!" -Color Green
}

# Verify installation
function Test-Installation {
    Write-ColorMessage "🔍 Verifying installation..." -Color Cyan

    try {
        $version = & aidk --version 2>&1 | Out-String
        if ($LASTEXITCODE -eq 0) {
            Write-ColorMessage "✅ aidk command is available" -Color Green
            Write-ColorMessage "   $version" -Color Green
            return $true
        }
    } catch {}

    Write-ColorMessage "⚠️  aidk command not found in PATH" -Color Yellow
    Write-ColorMessage "   You may need to restart your terminal or add pip's Scripts directory to PATH" -Color Yellow
    return $false
}

# Install to current project
function Install-ToProject {
    if ((Test-Path ".claude") -or (Test-Path ".git")) {
        Write-Host ""
        $response = Read-Host "Install AIDK skills to current project? [Y/n]"

        if ($response -ne "n" -and $response -ne "N") {
            Write-ColorMessage "📂 Installing to current project..." -Color Cyan

            # Ask about examples
            $examplesResponse = Read-Host "Include example SPECs? [y/N]"

            if ($examplesResponse -eq "y" -or $examplesResponse -eq "Y") {
                & aidk install --local --with-examples

                if ($LASTEXITCODE -ne 0) {
                    Write-ColorMessage "❌ Project installation failed" -Color Red
                    return
                }
            } else {
                & aidk install --local

                if ($LASTEXITCODE -ne 0) {
                    Write-ColorMessage "❌ Project installation failed" -Color Red
                    return
                }
            }

            Write-ColorMessage "✅ Skills installed to current project!" -Color Green
        }
    }
}

# Show next steps
function Show-NextSteps {
    Write-Host ""
    Write-ColorMessage "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -Color Green
    Write-ColorMessage "  ✨ Installation Complete!" -Color Green
    Write-ColorMessage "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -Color Green
    Write-Host ""
    Write-ColorMessage "📚 Quick Start:" -Color Cyan
    Write-Host ""
    Write-ColorMessage "  1. Navigate to your Android project:" -Color Yellow
    Write-Host "     cd C:\path\to\your\android\project"
    Write-Host ""
    Write-ColorMessage "  2. Install AIDK skills to the project:" -Color Yellow
    Write-Host "     aidk install --local"
    Write-Host ""
    Write-ColorMessage "  3. Create your first SPEC:" -Color Yellow
    Write-Host "     aidk spec create 'User Authentication'"
    Write-Host ""
    Write-ColorMessage "  4. List available skills:" -Color Yellow
    Write-Host "     aidk skills"
    Write-Host ""
    Write-ColorMessage "  5. Get help:" -Color Yellow
    Write-Host "     aidk --help"
    Write-Host ""
    Write-ColorMessage "📖 Documentation: https://github.com/yourusername/android-ai-devkit" -Color Cyan
    Write-Host ""
}

# Main installation flow
function Main {
    Write-Header

    $pythonCmd = Test-Python
    Test-Pip -PythonCmd $pythonCmd
    Install-AIDK -PythonCmd $pythonCmd
    Test-Installation
    Install-ToProject
    Show-NextSteps
}

# Run main function
try {
    Main
} catch {
    Write-ColorMessage "❌ Installation failed with error: $_" -Color Red
    exit 1
}

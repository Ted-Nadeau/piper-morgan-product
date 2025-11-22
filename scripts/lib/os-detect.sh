#!/usr/bin/env bash

# OS Detection Library for Cross-Platform Shell Scripts
# Version: 1.0.0
# Purpose: Detect OS and provide platform-specific command wrappers
# Supports: macOS, Linux, Windows (Git Bash, WSL, MSYS)

# Detect operating system
detect_os() {
    case "$(uname -s)" in
        Linux*)
            DETECTED_OS="Linux"
            ;;
        Darwin*)
            DETECTED_OS="macOS"
            ;;
        CYGWIN*)
            DETECTED_OS="Windows"
            OS_VARIANT="Cygwin"
            ;;
        MINGW*)
            DETECTED_OS="Windows"
            OS_VARIANT="Git Bash"
            ;;
        MSYS*)
            DETECTED_OS="Windows"
            OS_VARIANT="MSYS"
            ;;
        *)
            DETECTED_OS="Unknown"
            ;;
    esac

    export DETECTED_OS
    export OS_VARIANT="${OS_VARIANT:-}"
}

# Check if running on Windows
is_windows() {
    [ "$DETECTED_OS" = "Windows" ]
}

# Check if running on macOS
is_macos() {
    [ "$DETECTED_OS" = "macOS" ]
}

# Check if running on Linux
is_linux() {
    [ "$DETECTED_OS" = "Linux" ]
}

# Get the appropriate path separator
get_path_separator() {
    if is_windows; then
        echo ";"
    else
        echo ":"
    fi
}

# Get the appropriate path for virtual environment activation
get_venv_activate_path() {
    local venv_path="${1:-.}"

    if is_windows; then
        echo "$venv_path/Scripts/activate"
    else
        echo "$venv_path/bin/activate"
    fi
}

# Activate virtual environment (cross-platform)
activate_venv() {
    local venv_path="${1:-venv}"
    local activate_script

    activate_script=$(get_venv_activate_path "$venv_path")

    if [ ! -f "$activate_script" ]; then
        echo "❌ Virtual environment not found at: $venv_path"
        return 1
    fi

    # Source the activation script
    # shellcheck source=/dev/null
    source "$activate_script"
    return 0
}

# Platform-specific process termination
terminate_process() {
    local pid=$1
    local signal=${2:-TERM}  # Default to SIGTERM

    if is_windows; then
        # Windows: Use taskkill instead of kill
        taskkill /PID "$pid" /F 2>/dev/null || return 1
    else
        # Unix: Use kill with signal
        kill -"$signal" "$pid" 2>/dev/null || return 1
    fi

    return 0
}

# Platform-specific process listing
find_processes() {
    local pattern=$1

    if is_windows; then
        # Windows: Use tasklist with findstr
        tasklist /FI "IMAGENAME eq python.exe" 2>/dev/null | grep -i "$pattern" || true
    else
        # Unix: Use pgrep
        pgrep -f "$pattern" || true
    fi
}

# Open URL in default browser (cross-platform)
open_browser() {
    local url=$1

    if is_macos; then
        open "$url"
    elif is_windows; then
        # Try common Windows commands
        if command -v explorer.exe &>/dev/null; then
            explorer.exe "$url"
        elif command -v start &>/dev/null; then
            start "$url"
        else
            echo "⚠️  Could not open browser automatically on Windows"
            echo "📌 Please open your browser and navigate to: $url"
            return 1
        fi
    elif is_linux; then
        # Try common Linux commands
        if command -v xdg-open &>/dev/null; then
            xdg-open "$url"
        elif command -v gnome-open &>/dev/null; then
            gnome-open "$url"
        elif command -v kde-open &>/dev/null; then
            kde-open "$url"
        else
            echo "⚠️  Could not open browser automatically on Linux"
            echo "📌 Please open your browser and navigate to: $url"
            return 1
        fi
    else
        echo "⚠️  Unknown operating system - cannot open browser"
        echo "📌 Please open your browser and navigate to: $url"
        return 1
    fi
}

# Check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Windows-specific warning
warn_windows_limitations() {
    if is_windows; then
        echo ""
        echo "⚠️  WINDOWS DETECTED: $([ -n "$OS_VARIANT" ] && echo "$OS_VARIANT" || echo "Unknown Windows variant")"
        echo "   For best experience, consider using WSL (Windows Subsystem for Linux)"
        echo "   https://docs.microsoft.com/en-us/windows/wsl/install"
        echo ""
    fi
}

# Initialize OS detection when library is sourced
detect_os

# DEV-OS-DETECT: Add OS Detection to Shell Scripts (#359)

**Priority**: P1 (Developer experience, Windows support)
**Discovered by**: Ted Nadeau (architectural review)
**Effort**: 6-8 hours

## Problem

Shell scripts assume Unix/macOS environment, breaking on Windows (Git Bash, WSL, native).

**Affected scripts**:
- `scripts/start-piper.sh` - Uses Unix-specific commands
- `scripts/stop-piper.sh` - Assumes `ps` and `kill` syntax
- `scripts/run_tests.sh` - Path separators, Python invocation
- Pre-commit hooks - Bash-specific syntax
- Database setup scripts - PostgreSQL commands vary

**Current failures on Windows**:
```bash
$ ./scripts/start-piper.sh
./scripts/start-piper.sh: line 15: lsof: command not found
./scripts/start-piper.sh: line 22: syntax error near unexpected token `('
```

## Impact

- Windows developers must manually translate scripts
- Cannot use automated tooling on Windows
- Blocks Windows CI/CD pipeline
- Violates cross-platform goal
- Forces WSL requirement (not all Windows devs have)

## Solution

Create OS detection library and update all scripts:

```bash
# scripts/lib/os-detect.sh
detect_os() {
    case "$OSTYPE" in
        darwin*)  OS="macos" ;;
        linux*)   OS="linux" ;;
        msys*)    OS="windows" ;; # Git Bash
        cygwin*)  OS="windows" ;; # Cygwin
        win*)     OS="windows" ;; # Windows
        *)        OS="unknown" ;;
    esac
    export DETECTED_OS=$OS
}

# Platform-specific commands
get_process_list() {
    case "$DETECTED_OS" in
        windows)
            tasklist //FI "IMAGENAME eq python.exe"
            ;;
        *)
            ps aux | grep python
            ;;
    esac
}
```

## Acceptance Criteria

### Core Library
- [ ] Create `scripts/lib/os-detect.sh` with OS detection
- [ ] Create platform-specific command wrappers
- [ ] Handle path separator differences (`/` vs `\`)
- [ ] Handle Python invocation differences (`python` vs `python3`)

### Script Updates
- [ ] Update `start-piper.sh` with OS detection
- [ ] Update `stop-piper.sh` with OS detection
- [ ] Update `run_tests.sh` with OS detection
- [ ] Update pre-commit hooks
- [ ] Update database setup scripts

### Platform Testing
- [ ] Test on macOS (native)
- [ ] Test on Linux (Ubuntu 22.04)
- [ ] Test on Windows (Git Bash)
- [ ] Test on Windows (WSL2)
- [ ] Test on Windows (PowerShell with bash emulation)

### Documentation
- [ ] Document supported platforms in README
- [ ] Add Windows setup guide
- [ ] Document WSL vs Git Bash trade-offs
- [ ] Add troubleshooting section

## Implementation Strategy

```bash
#!/bin/bash
# Example: Updated start-piper.sh

# Source OS detection
source "$(dirname "$0")/lib/os-detect.sh"
detect_os

# Platform-specific port check
check_port_8001() {
    case "$DETECTED_OS" in
        windows)
            netstat -an | findstr :8001
            ;;
        macos)
            lsof -i :8001
            ;;
        linux)
            netstat -tuln | grep :8001
            ;;
    esac
}

# Unified Python invocation
run_python() {
    if command -v python3 &> /dev/null; then
        python3 "$@"
    elif command -v python &> /dev/null; then
        python "$@"
    else
        echo "Error: Python not found"
        exit 1
    fi
}
```

## Testing Plan

1. **Unit tests** for OS detection library
2. **Integration tests** on each platform
3. **CI matrix** testing (GitHub Actions on multiple OS)
4. **Developer testing** with volunteer Windows users

## Risk Mitigation

- Maintain backward compatibility (scripts still work on Unix)
- Provide fallback for unknown OS (warn but continue)
- Clear error messages when platform not supported
- Option to force OS detection (`FORCE_OS=windows`)

---

*Note: This improves developer experience and enables Windows contributors, critical for project growth*

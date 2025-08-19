# TLDR Continuous Verification System

## Overview

The TLDR (Too Long; Didn't Run) system provides <0.1 second feedback loops for development work, enabling instant verification after code changes.

## Quick Start

```bash
# Basic usage - context-aware timeouts
./scripts/tldr_runner.py

# Fast validation tests only
./scripts/tldr_runner.py --pattern validation --timeout 0.05

# Integration tests with extended timeout
./scripts/tldr_runner.py --pattern integration --timeout 0.3

# Single file verification
./scripts/tldr_runner.py --single tests/domain/test_models.py
```

## Context-Aware Timeouts

The TLDR system automatically classifies tests and applies appropriate timeouts:

- **Unit tests**: 50ms (domain, services, validation)
- **Integration tests**: 300ms (orchestration, queries, workflows)
- **Infrastructure tests**: 500ms (database, MCP, external services)
- **Performance tests**: 1000ms (load testing, benchmarks)

## Agent-Specific Configuration

### Claude Code Hooks (`.claude/settings.json`)
- **File changes**: 100ms timeout, exit-0-on-timeout for continuous flow
- **Test runs**: 50ms timeout, exit-2-on-failure for error detection
- **Integration checks**: 300ms timeout for comprehensive validation

### Cursor Hooks (`.cursor/settings.json`)
- **File save**: 50ms timeout, single file mode for immediate feedback
- **Test discovery**: Context-aware pattern matching
- **Workflow debug**: 300ms timeout with detailed failure output

## Command Line Options

```bash
./scripts/tldr_runner.py [OPTIONS]

Options:
  --timeout FLOAT           Global timeout (0 = context-aware defaults)
  --pattern TEXT           Filter tests by pattern
  --exit-0-on-timeout      Exit code 0 on timeout (agent hooks)
  --exit-2-on-failure      Exit code 2 on failure (agent differentiation)
  --verbose, -v            Verbose output with details
  --sequential             Run tests sequentially (not parallel)
  --single FILE            Run single test file
```

## Exit Codes

- **0**: All tests passed (or timeout with --exit-0-on-timeout)
- **1**: General errors or mixed results
- **2**: Test failures (with --exit-2-on-failure)
- **124**: Timeout (default timeout exit code)
- **130**: Interrupted by user (Ctrl+C)

## Integration Examples

### Pre-commit Hook
```bash
# .git/hooks/pre-commit
#!/bin/bash
./scripts/tldr_runner.py --timeout 0.1 --exit-2-on-failure
```

### IDE Integration
```bash
# VS Code task
{
  "label": "TLDR Test",
  "type": "shell",
  "command": "./scripts/tldr_runner.py --pattern ${fileBasenameNoExtension} --verbose"
}
```

### Continuous Integration
```bash
# Fast CI feedback
./scripts/tldr_runner.py --timeout 0.05 --pattern unit
./scripts/tldr_runner.py --timeout 0.3 --pattern integration --exit-2-on-failure
```

## Performance Characteristics

- **Startup overhead**: <20ms
- **Parallel execution**: Automatic for multiple tests
- **Memory efficient**: Minimal resource usage
- **Timeout precision**: Sub-100ms accuracy
- **Result caching**: None (always fresh results)

## Troubleshooting

### Timeouts Too Aggressive
```bash
# Increase timeout for specific test types
./scripts/tldr_runner.py --pattern slow_test --timeout 1.0
```

### Tests Not Found
```bash
# Check test discovery
./scripts/tldr_runner.py --verbose | grep "Found"
```

### Agent Hook Issues
```bash
# Test hooks manually
./scripts/tldr_runner.py --single tests/example.py --verbose
```

## Meta-Acceleration Effect

TLDR enables:
1. **Instant feedback** on code changes
2. **Rapid debugging** cycles with immediate test results
3. **Confidence in refactoring** through continuous validation
4. **Workflow completion diagnosis** with targeted test execution
5. **Agent coordination** through differentiated exit codes

The system transforms development from "write code → run tests → wait → debug" to "write code → instant feedback → immediate correction" cycle.

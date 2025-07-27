# Pattern Sweep Process - Usage Guide

## Overview

The Pattern Sweep Process is an automated pattern detection and learning acceleration system integrated with the TLDR Continuous Verification framework. It enables systematic discovery of code patterns, usage patterns, and coordination patterns across the entire codebase.

## Quick Start

```bash
# Basic pattern sweep
PYTHONPATH=. ./scripts/pattern_sweep.py --pattern-sweep-only --verbose

# TLDR with pattern detection
PYTHONPATH=. ./scripts/tldr_runner.py --with-pattern-detection --verbose

# Full integration with usage learning
PYTHONPATH=. ./scripts/tldr_runner.py --with-pattern-detection --learn-usage-patterns
```

## Pattern Categories

### 1. Code Patterns
- **Async Patterns**: `async with session_factory()`, context managers
- **Repository Patterns**: Repository instantiation and usage
- **Test Patterns**: Pytest markers, fixture usage
- **Error Handling**: Graceful degradation, try-except with logging
- **Domain Patterns**: Enum usage, workflow types

### 2. Usage Patterns
- **Methodology Patterns**: Systematic verification usage
- **Success Patterns**: Implementation completion markers
- **Debugging Patterns**: Root cause identification approaches

### 3. Performance Patterns
- **Velocity Patterns**: Rapid implementation timing detection
- **Test Execution**: TLDR timing analytics

### 4. Coordination Patterns
- **Workflow Patterns**: PM ticket completion tracking
- **Agent Coordination**: Multi-agent collaboration patterns

## Results and Storage

Pattern data is stored in `scripts/pattern_sweep_data.json` with:
- **Pattern Definitions**: Description, category, confidence scoring
- **Occurrence Data**: File locations, frequency, examples
- **History Tracking**: Sweep timeline and pattern evolution
- **Learning Data**: New vs updated pattern detection

## Integration with TLDR

The Pattern Sweep integrates seamlessly with the existing TLDR runner:

```bash
# Enhanced TLDR commands
./scripts/tldr_runner.py --with-pattern-detection --pattern "validation"
./scripts/tldr_runner.py --learn-usage-patterns --verbose
```

## Performance

- **Scan Scale**: 10,200+ Python files + 400+ documentation files
- **Scan Duration**: ~21 seconds for full codebase
- **Pattern Detection**: 15+ patterns across 4 categories
- **Storage**: ~500KB JSON with full pattern history

## Compound Learning

Pattern Sweep enables compound learning acceleration by:
1. **Automated Pattern Discovery**: Identifies emerging patterns automatically
2. **Confidence Scoring**: Ranks patterns by frequency and distribution
3. **Learning Persistence**: Tracks pattern evolution over time
4. **Methodology Enhancement**: Enables systematic improvement of development practices

## Examples

### Top Detected Patterns (as of 2025-07-26)
1. **Root cause identification pattern** (314 occurrences, 0.83 confidence)
2. **Async test marker pattern** (220 occurrences, 1.00 confidence)
3. **Systematic verification methodology** (130 occurrences, 0.74 confidence)
4. **Workflow type usage pattern** (154 occurrences, 1.00 confidence)
5. **Repository pattern instantiation** (70 occurrences, 1.00 confidence)

### Usage Pattern Examples
- Detection of "SYSTEMATIC VERIFICATION" methodology usage
- "✅ SUCCESS" implementation completion patterns
- "ROOT CAUSE" problem resolution patterns
- "PM-XXX COMPLETE" coordination patterns

## Integration with Development Workflow

Pattern Sweep enhances the systematic verification methodology by:
- **Pattern-First Development**: Discover existing patterns before implementing
- **Quality Assurance**: Detect antipatterns and ensure consistency
- **Velocity Intelligence**: Learn from high-velocity implementation patterns
- **Self-Improving Process**: Enable methodology evolution through pattern analysis

## Future Enhancements

Planned extensions include:
- **Real-time Pattern Detection**: Integration with file watchers
- **Pattern Suggestions**: AI-powered pattern recommendation
- **Cross-Project Learning**: Pattern sharing across repositories
- **Performance Correlation**: Link patterns to development velocity metrics

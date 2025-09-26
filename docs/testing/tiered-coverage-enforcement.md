# Tiered Coverage Enforcement

## Philosophy

Coverage requirements should match component completion status:
- **Completed work**: High standards (80%+) to ensure quality
- **Active development**: Reasonable baselines (25%+) to encourage testing
- **Legacy code**: Track but don't block (0% acceptable)
- **Overall baseline**: Prevent regression from current state

## Current Tiers (Sept 25, 2025)

### Tier 1: Completed Components (≥80% required)
- `services/orchestration/engine.py` - QueryRouter integration (completed)
- **Status**: Currently 35%, needs improvement
- **Standard**: High coverage for production-ready code

### Tier 2: Active Development (≥25% target)
- `services/orchestration/workflow_factory.py`
- `services/orchestration/coordinator.py`
- **Standard**: Reasonable coverage to encourage testing

### Tier 3: Legacy Code (0% acceptable)
- Files identified as legacy or unused
- **Standard**: Track coverage but don't block development

### Overall Baseline (≥15% required)
- `services/orchestration/*` - Complete module
- **Standard**: Prevent regression from current 15% baseline

## Usage

### Local Testing
```bash
# Check coverage before pushing
python scripts/check_coverage_locally.py

# Quick coverage check
python scripts/coverage_config.py

# Focus on specific file
python -m pytest tests/ --cov=services/orchestration/engine.py --cov-report=term-missing
```

### CI Integration
- Tiered coverage runs after performance tests
- **Failures block**: Completed work below 80%, overall below 15%
- **Warnings only**: Active work below 25%

## Improving Coverage

### For QueryRouter (engine.py → 80%)
Priority areas to test:
1. Initialization with different configurations
2. Error handling scenarios
3. Integration with workflow factory
4. Query routing logic edge cases

### For Active Development
1. Focus on core functionality first
2. Add integration tests for interactions
3. Test happy paths before edge cases

## Updating Tiers

When components are completed:
1. Move from "active" to "completed" tier
2. Update `scripts/coverage_config.py`
3. Ensure coverage meets 80% standard
4. Update this documentation

## Rationale

This tiered approach:
- ✅ Maintains quality for completed work
- ✅ Encourages testing without blocking development
- ✅ Prevents coverage regression
- ✅ Recognizes different component maturity levels
- ✅ Provides clear improvement path

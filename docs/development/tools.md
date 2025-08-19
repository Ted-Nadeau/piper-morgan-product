# Development Tools

This document describes the development tools available in the Piper Morgan codebase.

## Schema Validation Tool (PM-056)

**Location**: `tools/check_domain_db_consistency.py`

### Purpose
Validates consistency between SQLAlchemy database models and domain dataclasses to prevent schema drift and ensure Domain-Driven Design integrity.

### Features
- Automatic model discovery from `services.domain.models` and `services.database.models`
- Field presence validation (detects missing fields in either layer)
- Type compatibility checking (maps Python types to SQLAlchemy types)
- Nullable consistency validation (Optional[] mapping verification)
- Special issue detection (e.g., object_id vs object_position mismatches)
- Comprehensive reporting in text or JSON format

### Usage

```bash
# Basic validation
PYTHONPATH=. python tools/check_domain_db_consistency.py

# Verbose output (shows all models being loaded)
PYTHONPATH=. python tools/check_domain_db_consistency.py --verbose

# JSON output format
PYTHONPATH=. python tools/check_domain_db_consistency.py --format json
```

### Exit Codes
- `0` - Validation passed, no inconsistencies found
- `1` - Validation failed, inconsistencies detected
- `2` - Tool execution error

### Common Issues Detected
- **Missing Fields**: Fields present in domain models but not in database (or vice versa)
- **Type Mismatches**: Incompatible types between layers (e.g., list vs dict, enum mappings)
- **Nullable Mismatches**: Inconsistent Optional[] usage between domain and database
- **Naming Conflicts**: Field naming inconsistencies (e.g., object_id vs object_position)

### Integration with CI/CD
This tool should be run as part of the continuous integration pipeline to catch schema drift early:

```yaml
# Example GitHub Actions workflow
- name: Validate Schema Consistency
  run: |
    PYTHONPATH=. python tools/check_domain_db_consistency.py
```

### Maintenance
When adding new domain models or database tables:
1. Ensure corresponding models exist in both layers
2. Run the validator to check consistency
3. Fix any reported issues before committing

## Other Tools

### Pattern Sweep (`scripts/pattern_sweep.py`)
Standalone automated pattern discovery and learning acceleration tool.
- Usage: `./scripts/run_pattern_sweep.sh --verbose`
- Compound learning acceleration for development workflow optimization

### Database Initialization (`scripts/init_db.py`)
Initialize the PostgreSQL database with proper schema.

---

*Last updated: 2025-08-18* - TLDR deprecated, Pattern Sweep preserved as standalone tool

# PM-056 Schema Validator Tool Documentation

## Overview

The PM-056 Schema Validator Tool (`tools/check_domain_db_consistency.py`) is an automated domain/database schema consistency validator that prevents drift bugs by comparing SQLAlchemy models with domain dataclasses.

## Purpose

- **Prevent Drift Bugs**: Catches schema inconsistencies between domain and database models
- **Type Safety**: Validates field types and prevents object_id vs object_position issues
- **CI/CD Integration**: Provides exit codes for build failure on mismatch
- **Comprehensive Reporting**: Detailed validation reports with field-by-field analysis

## Usage

### Command Line

```bash
# Run schema validation
python tools/check_domain_db_consistency.py

# Exit codes:
# 0 = Success (no inconsistencies found)
# 1 = Failure (inconsistencies detected)
```

### Programmatic Usage

```python
from tools.check_domain_db_consistency import SchemaValidator

validator = SchemaValidator()
validator.load_domain_models()
validator.load_database_models()
is_valid = validator.validate_all_models()
report = validator.generate_report()
```

## Features

### Model Comparison

The tool compares domain dataclasses with SQLAlchemy models:

- **Field Names**: Ensures matching field names between domain and database
- **Field Types**: Validates type consistency (e.g., `str` vs `String`)
- **Nullable Fields**: Checks optional field consistency
- **Primary Keys**: Validates primary key field presence
- **Foreign Keys**: Checks foreign key relationships

### Type Mapping

SQLAlchemy types are mapped to domain types:

| SQLAlchemy Type | Domain Type |
|----------------|-------------|
| `String` | `str` |
| `Text` | `str` |
| `Integer` | `int` |
| `Float` | `float` |
| `Boolean` | `bool` |
| `DateTime` | `datetime` |
| `JSON` | `dict` |
| `Enum` | `enum` |

### Specific Issue Detection

The tool specifically detects known problematic patterns:

- **object_id vs object_position**: Catches type mismatches that caused PM-078 issues
- **Missing Fields**: Identifies fields present in one model but not the other
- **Type Mismatches**: Detects inconsistent field types between models

## Model Mappings

The validator compares these model pairs:

| Domain Model | Database Model |
|--------------|----------------|
| `WorkItem` | `WorkItem` |
| `Workflow` | `Workflow` |
| `Task` | `Task` |
| `Intent` | `Intent` |
| `Product` | `Product` |
| `Feature` | `Feature` |
| `Stakeholder` | `Stakeholder` |
| `Project` | `ProjectDB` |
| `ProjectIntegration` | `ProjectIntegrationDB` |
| `UploadedFile` | `UploadedFileDB` |

## Output Format

### Console Output

```
🔧 PM-056 Schema Validator Tool
========================================

📥 Loading models...
📋 Loaded domain model: WorkItem
📋 Loaded domain model: Workflow
🗄️  Loaded database model: WorkItem
🗄️  Loaded database model: Workflow

🔍 Starting schema validation...

📊 Comparing WorkItem (domain) vs WorkItem (database)
  ✅ Matching fields: 8
  📈 Field counts: Domain=8, Database=8

📊 Comparing Workflow (domain) vs Workflow (database)
  ✅ Matching fields: 6
  📈 Field counts: Domain=6, Database=6

============================================================
PM-056 Schema Validation Report
============================================================

📊 Summary:
  Total model comparisons: 10
  Valid comparisons: 10
  Invalid comparisons: 0

✅ Schema validation passed!
```

### Report Structure

The validation report includes:

- **Summary Statistics**: Total comparisons, valid/invalid counts
- **Errors**: Critical issues that prevent successful validation
- **Warnings**: Non-critical issues that should be addressed
- **Detailed Results**: Field-by-field comparison for each model pair

## CI/CD Integration

### GitHub Actions

```yaml
name: Schema Validation
on: [push, pull_request]

jobs:
  schema-validation:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run schema validation
        run: python tools/check_domain_db_consistency.py
```

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: schema-validation
        name: Schema Validation
        entry: python tools/check_domain_db_consistency.py
        language: system
        pass_filenames: false
```

## Testing

### Running Tests

```bash
# Run schema validator tests
pytest tests/validation/test_pm056_schema_validator.py -v

# Run with coverage
pytest tests/validation/test_pm056_schema_validator.py --cov=tools.check_domain_db_consistency
```

### Test Coverage

The test suite covers:

- **Field Extraction**: Domain and database field extraction
- **Model Comparison**: Matching, missing, and type mismatch detection
- **Specific Issues**: object_id vs object_position detection
- **Report Generation**: Validation report creation
- **Error Handling**: Exception handling and error reporting

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure project root is in Python path
2. **Missing Models**: Check that domain and database models are properly loaded
3. **Type Mapping Issues**: Verify SQLAlchemy type mapping is correct
4. **ForwardRef Issues**: Handle forward references in type annotations

### Debug Mode

```python
# Enable debug output
validator = SchemaValidator()
validator.debug = True
validator.validate_all_models()
```

## Maintenance

### Adding New Models

1. Add domain model to `services/domain/models.py`
2. Add database model to `services/database/models.py`
3. Update model mappings in `validate_all_models()`
4. Add tests for new model comparison

### Updating Type Mappings

1. Modify `_get_sqlalchemy_type_name()` method
2. Add new type mappings to the mapping dictionary
3. Update tests to cover new type mappings

### Extending Issue Detection

1. Add new detection logic to `check_specific_issues()`
2. Update error reporting in the method
3. Add tests for new issue detection

## Related Documentation

- [PM-056 Issue](https://github.com/mediajunkie/piper-morgan-product/issues/67)
- [Domain Models Documentation](../architecture/domain-models-index.md)
- [Database Models Documentation](../architecture/data-model.md)
- CI/CD Pipeline Documentation (to come)

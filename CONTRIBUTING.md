# Contributing Guidelines

## Development Requirements

### Python Version

- **Required**: Python 3.11+
- **Recommended**: Python 3.11.9 (latest stable)

All development must be compatible with Python 3.11. Key features we rely on:

- `asyncio.timeout()` (Python 3.11+ feature)
- Enhanced error messages
- Performance improvements

### Code Quality

- All code must pass with Python 3.11
- Use Python 3.11+ type hints where beneficial
- Async/await patterns must be Python 3.11 compatible

### Testing

```bash
# All tests must pass with Python 3.11
python --version  # Verify 3.11+
pytest tests/ -v

# Check for Python 3.11 compatibility
python -W error::DeprecationWarning -m pytest tests/
```

## Development Workflow

### 1. Environment Setup

```bash
# Ensure Python 3.11 is active
python --version  # Should show 3.11.x

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# OR venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Verify Python 3.11 features
python -c "import asyncio; asyncio.timeout(1.0); print('✅ Python 3.11 ready')"
```

### 2. Code Quality Checks

```bash
# Format code with Black
black .

# Sort imports with isort
isort .

# Lint with flake8
flake8 . --count --exit-zero --max-line-length=100

# Run pre-commit hooks
pre-commit run --all-files
```

### 3. Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test categories
pytest tests/services/ -v  # Service tests
pytest tests/integration/ -v  # Integration tests

# Run with Python 3.11 specific checks
python -W error::DeprecationWarning -m pytest tests/
```

### 4. Known Test Failures Workflow

Piper Morgan uses a **known-failures tracking system** to allow pushes even when some tests are failing, as long as those failures are:
1. **Documented** with clear reason
2. **Tracked** in a bead (issue tracker)
3. **Time-boxed** with expiry date
4. **Categorized** (TDD spec, known bug, or deferred)

#### How It Works

The pre-push hook will:
1. Run the fast test suite (`./scripts/run_tests.sh fast`)
2. If tests fail, check against `.pytest-known-failures`
3. Allow push if all failures are known
4. Block push if new failures are detected
5. Warn about expired or resolved failures

#### Adding a Known Failure

If you need to push with a failing test that's tracked in a bead:

```bash
# Edit .pytest-known-failures file
nano .pytest-known-failures
```

Add an entry following this format:

```yaml
- test_path: "tests/unit/path/to/test_file.py::TestClass::test_method"
  reason: "Clear explanation of why this test is failing"
  bead: "piper-morgan-xyz"  # Must be a valid bead ID
  expires: "2025-12-20"      # Max 30 days from creation
  category: "tdd_spec"       # or "known_bug" or "deferred"
```

**Categories:**
- `tdd_spec`: Test-driven development spec (expected to fail until implementation)
- `known_bug`: Known bug tracked in bead, fix planned
- `deferred`: Work deferred to later sprint, tracked in bead

**Rules:**
- All entries MUST have bead references (for tracking)
- Expiry dates MUST be within 30 days
- Expired entries cause WARNING (not block) - update or remove them
- Resolved tests (now passing) should be removed from the file

#### Validating Known Failures Manually

```bash
# Test the known-failures validation
python scripts/filter_known_failures.py

# Should output:
# ✅ All failures are known - push allowed
# OR
# ❌ NEW FAILURES DETECTED (BLOCKING PUSH)
```

#### Common Scenarios

**Scenario 1: TDD Workflow**
```yaml
- test_path: "tests/unit/services/test_new_feature.py::TestNewFeature::test_method"
  reason: "TDD - NewFeature.method() not implemented yet"
  bead: "piper-morgan-abc"
  expires: "2025-12-15"
  category: "tdd_spec"
```

**Scenario 2: Known Bug**
```yaml
- test_path: "tests/unit/services/test_service.py::TestService::test_edge_case"
  reason: "Bug - service crashes on empty input, tracked for fix"
  bead: "piper-morgan-def"
  expires: "2025-12-10"
  category: "known_bug"
```

**Scenario 3: Deferred Work**
```yaml
- test_path: "tests/integration/test_complex_flow.py::test_end_to_end"
  reason: "Deferred - integration test needs mock data setup"
  bead: "piper-morgan-ghi"
  expires: "2025-12-20"
  category: "deferred"
```

#### Best Practices

✅ **DO:**
- Create a bead BEFORE adding to known-failures
- Use clear, descriptive reasons
- Set realistic expiry dates (max 30 days)
- Remove entries when tests are fixed
- Review warnings about expired entries

❌ **DON'T:**
- Add failures without bead tracking
- Use vague reasons like "broken" or "fails sometimes"
- Set distant expiry dates (>30 days)
- Leave resolved tests in the file
- Ignore expiry warnings

### 5. Docker Validation

```bash
# Build and test Docker containers
docker-compose build
docker-compose up -d

# Verify container Python version
docker-compose exec app python --version  # Should show 3.11.x

# Run tests in container
docker-compose exec app pytest tests/ -v
```

## Pull Request Requirements

### Before Submitting

- [ ] **Code runs successfully** with Python 3.11
- [ ] **All tests pass** with Python 3.11
- [ ] **No deprecation warnings** introduced
- [ ] **Docker builds work** with Python 3.11 base images
- [ ] **Documentation updated** if adding Python 3.11+ features
- [ ] **Code formatted** with Black and isort
- [ ] **Linting passes** with flake8

### Pull Request Template

```markdown
## Description

Brief description of changes

## Python Version Compatibility

- [ ] Tested with Python 3.11+
- [ ] No Python version-specific issues introduced
- [ ] AsyncIO.timeout functionality preserved (if applicable)

## Testing

- [ ] All tests pass locally
- [ ] Docker containers build successfully
- [ ] CI/CD workflows pass

## Documentation

- [ ] README.md updated (if needed)
- [ ] Code comments added for complex logic
- [ ] API documentation updated (if applicable)

## Checklist

- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] No console.log or debug statements left
- [ ] Error handling implemented appropriately
```

## Code Style Guidelines

### Python 3.11 Best Practices

```python
# Use asyncio.timeout() for async operations
import asyncio

async def example_function():
    async with asyncio.timeout(5.0):  # Python 3.11+ feature
        await some_async_operation()

# Use enhanced error messages
try:
    result = await operation()
except Exception as e:
    raise RuntimeError(f"Operation failed: {e}") from e

# Use type hints with Python 3.11 features
from typing import Annotated

def process_data(data: Annotated[dict, "User input data"]) -> dict:
    return {"processed": data}
```

### Async/Await Patterns

```python
# Prefer async context managers
async def resource_management():
    async with asyncio.timeout(10.0):
        async with aiofiles.open('file.txt') as f:
            content = await f.read()
    return content

# Use proper error handling
async def robust_operation():
    try:
        async with asyncio.timeout(5.0):
            result = await external_api_call()
        return result
    except asyncio.TimeoutError:
        logger.warning("Operation timed out")
        return None
    except Exception as e:
        logger.error(f"Operation failed: {e}")
        raise
```

## Common Issues and Solutions

### Python Version Issues

**Problem**: `AttributeError: module 'asyncio' has no attribute 'timeout'`
**Solution**: Ensure Python 3.11+ is active

```bash
python --version  # Check version
pyenv local 3.11.9  # Set correct version
source venv/bin/activate  # Reactivate environment
```

### Docker Issues

**Problem**: Container tests fail with version errors
**Solution**: Rebuild with Python 3.11 base

```bash
docker-compose build --no-cache
docker-compose exec app python --version  # Verify 3.11+
```

### CI/CD Failures

**Problem**: GitHub Actions fail with Python compatibility
**Solution**: Workflows updated to use Python 3.11 - clear cache and retry

## Review Process

### Code Review Checklist

- [ ] **Python 3.11 compatibility** verified
- [ ] **Async patterns** follow best practices
- [ ] **Error handling** is appropriate
- [ ] **Tests** cover new functionality
- [ ] **Documentation** is clear and complete
- [ ] **Performance** considerations addressed
- [ ] **Security** implications considered

### Review Guidelines

- Be constructive and specific
- Focus on code quality and Python 3.11 compatibility
- Consider async/await patterns and error handling
- Verify that new code doesn't introduce version-specific issues

## Getting Help

### Resources

- [Development Setup Guide](docs/development/setup.md)
- [Onboarding Checklist](docs/development/onboarding.md)
- [PM-055 Implementation Package](docs/development/pm-055-step1-implementation-package.md)
- [Architecture Documentation](docs/architecture/)

### Support Channels

- GitHub Issues for bug reports
- Team chat for quick questions
- Code review comments for specific feedback

## Thank You! 🎉

Thank you for contributing to Piper Morgan Platform! Your contributions help make this project better for everyone. The Python 3.11 migration ensures a modern, consistent development experience.

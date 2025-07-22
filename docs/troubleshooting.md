# Troubleshooting Guide

## Python Version Issues

### AsyncIO.timeout AttributeError

**Error**: `AttributeError: module 'asyncio' has no attribute 'timeout'`

**Cause**: Python version < 3.11

**Solution**:

```bash
# Check Python version
python --version

# If < 3.11, install Python 3.11+
pyenv install 3.11.9
pyenv local 3.11.9

# Verify fix
python -c "import asyncio; asyncio.timeout(1.0); print('✅ Fixed')"
```

### Docker Python Version Mismatch

**Error**: Container tests fail with version errors

**Solution**:

```bash
# Rebuild with Python 3.11 base
docker-compose build --no-cache
docker-compose run app python --version  # Verify 3.11+
```

### CI/CD Python Version Failures

**Error**: GitHub Actions fail with Python compatibility

**Solution**: Workflows updated to use Python 3.11 - clear cache and retry

```bash
# Check workflow configuration
cat .github/workflows/test.yml | grep "python-version"
# Should show: python-version: '3.11'
```

## Environment Setup Issues

### Virtual Environment Wrong Python Version

**Problem**: Virtual environment created with wrong Python version

**Solution**:

```bash
# Remove old virtual environment
rm -rf venv

# Create new with Python 3.11
python3.11 -m venv venv
source venv/bin/activate

# Verify version
python --version  # Should show 3.11.x
```

### Dependency Installation Failures

**Problem**: Package installation fails with version conflicts

**Solution**:

```bash
# Deactivate and reactivate virtual environment
deactivate
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### IDE Python Interpreter Issues

**Problem**: IDE not recognizing Python 3.11

**Solution**:

**VS Code**:

1. `Cmd+Shift+P` (macOS) or `Ctrl+Shift+P` (Windows/Linux)
2. "Python: Select Interpreter"
3. Choose Python 3.11 from virtual environment

**PyCharm**:

1. File → Settings → Project → Python Interpreter
2. Add interpreter → Existing environment
3. Select `./venv/bin/python`

## Testing Issues

### Test Failures with Python Version Errors

**Problem**: Tests fail with Python compatibility warnings

**Solution**:

```bash
# Run with Python 3.11 specific checks
python -W error::DeprecationWarning -m pytest tests/

# Check for version-specific issues
python -c "import sys; print(f'Python {sys.version}')"
```

### Async Test Failures

**Problem**: Async tests fail with timeout or context errors

**Solution**:

```bash
# Verify asyncio.timeout availability
python -c "import asyncio; asyncio.timeout(1.0); print('✅ asyncio.timeout available')"

# Run async tests with proper event loop
pytest tests/ -v --asyncio-mode=auto
```

## Docker Issues

### Container Build Failures

**Problem**: Docker build fails with Python version errors

**Solution**:

```bash
# Check Dockerfile Python version
grep "FROM python" services/orchestration/Dockerfile
# Should show: FROM python:3.11-slim-buster

# Rebuild with no cache
docker-compose build --no-cache
```

### Container Runtime Issues

**Problem**: Container fails to start or crashes

**Solution**:

```bash
# Check container logs
docker-compose logs app

# Verify container Python version
docker-compose exec app python --version

# Check container dependencies
docker-compose exec app python -c "import fastapi, sqlalchemy; print('✅ Dependencies OK')"
```

## CI/CD Issues

### GitHub Actions Failures

**Problem**: CI/CD workflows fail with Python version errors

**Solution**:

```bash
# Check workflow configuration
cat .github/workflows/test.yml | grep -A 5 -B 5 "python-version"

# Verify workflow syntax
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/test.yml'))"
```

### Cache Issues

**Problem**: CI/CD cache causing version conflicts

**Solution**: Clear GitHub Actions cache or update cache keys

```yaml
# Check cache configuration in workflows
- name: Cache Python dependencies
  uses: actions/cache@v3
  with:
    key: ${{ runner.os }}-pip-3.11-${{ hashFiles('**/requirements.txt') }}
```

## Performance Issues

### Slow Async Operations

**Problem**: Async operations are slower than expected

**Solution**:

```bash
# Verify Python 3.11 performance features
python -c "
import asyncio
import time

async def test_performance():
    start = time.time()
    async with asyncio.timeout(1.0):
        await asyncio.sleep(0.1)
    print(f'Async operation took: {time.time() - start:.3f}s')

asyncio.run(test_performance())
"
```

### Memory Usage Issues

**Problem**: High memory usage in async operations

**Solution**: Check for proper resource cleanup

```python
# Ensure proper async context management
async def proper_resource_usage():
    async with asyncio.timeout(5.0):
        async with some_resource() as resource:
            result = await resource.operation()
    return result
```

## Common Error Messages and Solutions

### "Module 'asyncio' has no attribute 'timeout'"

- **Cause**: Python < 3.11
- **Solution**: Upgrade to Python 3.11+

### "Python version 3.11 is required"

- **Cause**: Version constraint in pyproject.toml
- **Solution**: Ensure Python 3.11+ is active

### "Docker build failed: unsupported Python version"

- **Cause**: Dockerfile specifies Python 3.11
- **Solution**: Rebuild with Python 3.11 base image

### "CI/CD workflow failed: Python version mismatch"

- **Cause**: Workflow expects Python 3.11
- **Solution**: Check workflow configuration and cache

## Getting Help

### Self-Diagnosis Steps

1. **Check Python version**: `python --version`
2. **Verify asyncio.timeout**: `python -c "import asyncio; asyncio.timeout(1.0)"`
3. **Check virtual environment**: `echo $VIRTUAL_ENV`
4. **Verify dependencies**: `pip list | grep -E "(fastapi|sqlalchemy|pytest)"`
5. **Check Docker version**: `docker-compose exec app python --version`

### Resources

- [Development Setup Guide](docs/development/setup.md)
- [Onboarding Checklist](docs/development/onboarding.md)
- [PM-055 Implementation Package](docs/development/pm-055-step1-implementation-package.md)
- [Contributing Guidelines](CONTRIBUTING.md)

### Support Channels

- **GitHub Issues**: For bug reports and feature requests
- **Team Chat**: For quick questions and troubleshooting
- **Code Review**: For specific implementation issues

## Prevention

### Best Practices

1. **Always verify Python version** before starting development
2. **Use virtual environments** with Python 3.11
3. **Run tests regularly** to catch version issues early
4. **Keep dependencies updated** for Python 3.11 compatibility
5. **Use pre-commit hooks** to catch issues before commit

### Validation Scripts

```bash
#!/bin/bash
# validation.sh - Quick environment validation

echo "=== Environment Validation ==="
echo "Python version: $(python --version)"
echo "Virtual environment: $VIRTUAL_ENV"
python -c "import asyncio; asyncio.timeout(1.0); print('✅ asyncio.timeout available')"
python -c "import fastapi, sqlalchemy, pytest; print('✅ Key dependencies available')"
echo "=== Validation Complete ==="
```

Run this script regularly to ensure your environment is properly configured.

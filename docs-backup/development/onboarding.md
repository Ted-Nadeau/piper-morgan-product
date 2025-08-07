# Developer Onboarding Checklist

## Prerequisites

- [ ] **Python 3.11+** installed and active
  - [ ] Verify with `python --version` (should show 3.11.x)
  - [ ] Verify asyncio.timeout availability: `python -c "import asyncio; asyncio.timeout(1.0)"`
- [ ] **Git** configured with your credentials
- [ ] **Docker** installed and running
- [ ] **IDE/Editor** configured for Python 3.11
  - [ ] VS Code with Python extension
  - [ ] Or PyCharm with Python 3.11 interpreter
- [ ] **GitHub access** to repository

## Environment Setup

- [ ] **Repository cloned**
  ```bash
  git clone https://github.com/yourusername/piper-morgan-platform.git
  cd piper-morgan-platform
  ```
- [ ] **Python 3.11 verified**
  ```bash
  python --version  # Should show Python 3.11.x
  cat .python-version  # Should show 3.11
  ```
- [ ] **Virtual environment created** with Python 3.11
  ```bash
  python -m venv venv
  source venv/bin/activate  # Linux/macOS
  # OR venv\Scripts\activate  # Windows
  ```
- [ ] **Dependencies installed** successfully
  ```bash
  pip install -r requirements.txt
  ```
- [ ] **AsyncIO.timeout functionality verified**
  ```bash
  python -c "import asyncio; asyncio.timeout(1.0); print('✅ Python 3.11 ready')"
  ```

## Development Workflow

- [ ] **Tests pass locally**
  ```bash
  pytest tests/ -v
  ```
- [ ] **Docker containers build** successfully
  ```bash
  docker-compose build
  docker-compose up -d
  ```
- [ ] **Pre-commit hooks installed** and working
  ```bash
  pip install pre-commit
  pre-commit install
  pre-commit run --all-files
  ```
- [ ] **IDE recognizes Python 3.11** type hints
  - [ ] VS Code: Python interpreter set to venv/bin/python
  - [ ] PyCharm: Project interpreter set to Python 3.11

## Validation

- [ ] **Can run application locally**
  ```bash
  python main.py
  # Should start without Python version errors
  ```
- [ ] **Can build and run Docker containers**
  ```bash
  docker-compose exec app python --version  # Should show 3.11.x
  ```
- [ ] **Tests pass in local environment**
  ```bash
  python -m pytest tests/ --tb=short
  ```
- [ ] **AsyncIO features work correctly**
  ```bash
  python -c "
  import asyncio
  async def test_timeout():
      async with asyncio.timeout(1.0):
          await asyncio.sleep(0.1)
  asyncio.run(test_timeout())
  print('✅ AsyncIO.timeout works correctly')
  "
  ```

## Code Quality Tools

- [ ] **Black formatting** works
  ```bash
  black --check .
  ```
- [ ] **isort import sorting** works
  ```bash
  isort --check-only .
  ```
- [ ] **Flake8 linting** passes
  ```bash
  flake8 . --count --exit-zero --max-line-length=100
  ```

## CI/CD Integration

- [ ] **GitHub Actions workflows** are configured
  - [ ] Test workflow uses Python 3.11
  - [ ] Lint workflow uses Python 3.11
  - [ ] Docker workflow validates Python 3.11
- [ ] **Can push changes** to trigger CI
  ```bash
  git add .
  git commit -m "Initial setup"
  git push origin main
  ```

## Documentation Review

- [ ] **README.md** reviewed and understood
- [ ] **Development setup guide** followed
- [ ] **Contributing guidelines** reviewed
- [ ] **Architecture documentation** familiarized
- [ ] **API documentation** reviewed

## Next Steps

- [ ] **Review contributing guidelines** in CONTRIBUTING.md
- [ ] **Set up development branch** for first feature
  ```bash
  git checkout -b feature/your-first-feature
  ```
- [ ] **Complete first development task**
  - [ ] Create a simple test
  - [ ] Make a small code change
  - [ ] Verify tests still pass
  - [ ] Submit a pull request

## Troubleshooting

### Common Issues

**Python Version Issues**:

```bash
# If you see: AttributeError: module 'asyncio' has no attribute 'timeout'
python --version  # Check if < 3.11
# Solution: Install and activate Python 3.11
```

**Docker Issues**:

```bash
# If containers fail to build
docker-compose build --no-cache
docker-compose exec app python --version  # Verify 3.11.x
```

**Test Failures**:

```bash
# If tests fail with version errors
python -W error::DeprecationWarning -m pytest tests/
# Check for Python 3.11 compatibility issues
```

### Getting Help

1. **Check this onboarding guide** for common solutions
2. **Review troubleshooting guide** in docs/development/troubleshooting-guide.md
3. **Check PM-055 implementation package** for Python 3.11 details
4. **Ask the team** in GitHub Issues or team chat
5. **Review CI/CD logs** if GitHub Actions fail

## Success Criteria

You're successfully onboarded when:

- [ ] All tests pass with Python 3.11
- [ ] Docker containers build and run correctly
- [ ] You can make code changes and run tests
- [ ] CI/CD workflows pass on your changes
- [ ] You understand the Python 3.11 requirements
- [ ] You can contribute to the project effectively

## Welcome to the Team! 🎉

Once you've completed this checklist, you're ready to contribute to Piper Morgan Platform. The Python 3.11 migration (PM-055) ensures a modern, consistent development environment for all team members.

**Key Benefits of Python 3.11**:

- ✅ Enhanced async/await performance
- ✅ `asyncio.timeout()` functionality
- ✅ Better error messages and debugging
- ✅ Improved type checking support
- ✅ Consistent environment across all contexts

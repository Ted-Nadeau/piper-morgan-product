# Test Guide: Piper Morgan

**Phase 1: Test Infrastructure Activation**
**Created**: 2025-08-20 by Chief Architect deployment

## Quick Start

```bash
# Quick validation (<5s)
./../../scripts/run_tests.sh smoke

# Development workflow (<30s)
./../../scripts/run_tests.sh fast

# Pre-merge comprehensive testing
./../../scripts/run_tests.sh full

# Weekly coverage analysis
./../../scripts/run_tests.sh coverage
```

## Test Infrastructure Overview

### Smart Test Execution

Our test infrastructure provides **4 execution modes** optimized for different development phases:

| Mode | Duration | Purpose | Use Case |
|------|----------|---------|----------|
| **smoke** | <5s | Quick validation | Pre-commit, rapid feedback |
| **fast** | <30s | Development workflow | Feature development, debugging |
| **full** | Variable | Comprehensive testing | Pre-merge, CI/CD |
| **coverage** | Variable | Analysis + reporting | Weekly reviews, quality audits |

### Test Organization

```
tests/
├── unit/                      # Fast, mocked tests
│   ├── test_domain_models.py  # Core business logic
│   ├── test_shared_types.py   # Enums and constants
│   └── test_services.py       # Service layer logic
├── integration/               # Real database tests (port 5433)
│   ├── test_repositories.py   # Data access layer
│   ├── test_orchestration.py  # Multi-component workflows
│   └── test_api_endpoints.py  # End-to-end API testing
└── orchestration/             # Advanced coordination tests
    ├── test_multi_agent_coordinator.py      # 773 lines, 36 tests
    ├── test_excellence_flywheel_integration.py  # 943 lines
    └── test_excellence_flywheel_unittest.py     # Standalone tests
```

## Excellence Flywheel Integration

### Verification First → Testing

Our testing methodology follows the **Excellence Flywheel** pattern:

1. **Verification First**: Understand existing test coverage before adding new tests
2. **Implementation Second**: Write tests that validate actual functionality
3. **Evidence-based Progress**: All claims backed by test execution output
4. **GitHub Tracking**: Link test enhancements to specific issues

### Meta-Testing Approach

We apply our own methodology to test our methodology:

```bash
# Test the Excellence Flywheel using Excellence Flywheel principles
PYTHONPATH=. python -m pytest tests/orchestration/test_excellence_flywheel_unittest.py -v

# Test Multi-Agent Coordinator using systematic verification
PYTHONPATH=. python -m pytest tests/orchestration/test_multi_agent_coordinator.py -v
```

## Development Workflow

### Daily Development

```bash
# 1. Start development session
source venv/bin/activate
docker-compose up -d

# 2. Before making changes
./../../scripts/run_tests.sh smoke    # Baseline validation

# 3. After implementing feature
./../../scripts/run_tests.sh fast     # Development validation

# 4. Before committing
./../../scripts/run_tests.sh smoke    # Pre-commit check (automated by git hook)

# 5. Before pushing
./../../scripts/run_tests.sh fast     # Pre-push check (automated by git hook)
```

### Git Integration

#### Automated Enforcement

- **Pre-push hook**: Runs `fast` test suite before allowing push
- **Test enforcement hook**: Custom validation with multiple modes
- **Excellence Flywheel reminders**: Integrated into git workflow

#### Manual Validation

```bash
# Custom test enforcement (bypasses git hooks)
.git/hooks/test-enforcement smoke   # Quick validation
.git/hooks/test-enforcement fast    # Development validation
.git/hooks/test-enforcement full    # Comprehensive validation
```

## Test Execution Details

### Smoke Tests (<5 seconds)

**Purpose**: Rapid feedback for development workflow
**Target**: Critical path validation only

```bash
./../../scripts/run_tests.sh smoke
```

**What it tests**:
- Core import validation (domain models, shared types)
- Critical unit tests with 3-second timeout
- Basic syntax and dependency verification

**Performance requirement**: Must complete in <5 seconds

### Fast Tests (<30 seconds)

**Purpose**: Development workflow validation
**Target**: Unit tests + standalone orchestration tests

```bash
./../../scripts/run_tests.sh fast
```

**What it tests**:
- Complete unit test suite with coverage
- Standalone orchestration tests (no database required)
- Performance validation with 10-second timeout per test

**Performance requirement**: Must complete in <30 seconds

### Full Test Suite

**Purpose**: Comprehensive pre-merge validation
**Target**: All tests including integration tests

```bash
./../../scripts/run_tests.sh full
```

**What it tests**:
- Unit tests + integration tests + orchestration tests
- Database-dependent functionality (requires PostgreSQL)
- End-to-end workflow validation
- 30-second timeout per test for integration tests

**Requirements**:
- PostgreSQL running (auto-started via docker-compose)
- Redis running for session management
- Complete environment setup

### Coverage Analysis

**Purpose**: Quality auditing and gap identification
**Target**: Comprehensive coverage reporting

```bash
./../../scripts/run_tests.sh coverage
```

**What it generates**:
- HTML coverage report in `htmlcov/`
- Terminal coverage summary
- Files with <80% coverage highlighted
- Missing line identification

## Test Writing Guidelines

### Unit Test Patterns

```python
# tests/unit/test_example.py
import pytest
from services.domain.models import ExampleModel

class TestExampleModel:
    def test_creation_with_valid_data(self):
        """Test model creation follows domain rules"""
        model = ExampleModel(name="test", value=42)
        assert model.name == "test"
        assert model.value == 42

    def test_validation_enforces_business_rules(self):
        """Test business rule enforcement"""
        with pytest.raises(ValueError, match="Invalid value"):
            ExampleModel(name="test", value=-1)
```

### Integration Test Patterns

```python
# tests/integration/test_example.py
import pytest
from tests.conftest import async_transaction

class TestExampleRepository:
    async def test_create_and_retrieve(self, async_transaction):
        """Test repository CRUD operations"""
        # Use async_transaction fixture for database tests
        repo = ExampleRepository(async_transaction)

        # Test implementation
        created = await repo.create(example_data)
        retrieved = await repo.get_by_id(created.id)

        assert retrieved.name == example_data["name"]
```

### Orchestration Test Patterns

```python
# tests/orchestration/test_example.py
import pytest
from unittest.mock import Mock, AsyncMock

class TestExampleCoordinator:
    async def test_coordination_workflow(self):
        """Test coordination patterns without database"""
        coordinator = ExampleCoordinator()

        # Mock dependencies
        coordinator.agent_pool = Mock()
        coordinator.task_decomposer = Mock()

        # Test coordination logic
        result = await coordinator.coordinate_task(test_task)

        assert result.status == "completed"
        assert len(result.subtasks) > 0
```

## Performance Requirements

### Critical Thresholds

| Test Category | Max Duration | Timeout | Purpose |
|---------------|-------------|---------|---------|
| Smoke Tests | 5 seconds | 3s per test | Rapid feedback |
| Fast Tests | 30 seconds | 10s per test | Development workflow |
| Integration Tests | No limit | 30s per test | Comprehensive validation |
| Individual Unit Tests | 1 second | 3s per test | Rapid iteration |

### Performance Monitoring

The test infrastructure automatically monitors and reports:

- **Execution time**: Each test mode reports total duration
- **Timeout enforcement**: Prevents hanging tests from blocking workflow
- **Performance degradation**: Alerts when smoke tests exceed 5s threshold

## Troubleshooting

### Common Issues

#### "PostgreSQL not running"
```bash
# Solution 1: Start with docker-compose
docker-compose up -d postgres redis

# Solution 2: Check service status
docker-compose ps

# Solution 3: Restart services
docker-compose restart postgres redis
```

#### "Virtual environment not found"
```bash
# Solution: Activate virtual environment
source venv/bin/activate

# Or recreate if missing
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### "PYTHONPATH issues"
```bash
# Solution: Always set PYTHONPATH explicitly
export PYTHONPATH=.
PYTHONPATH=. python -m pytest tests/unit/ -v

# Our test script handles this automatically
./../../scripts/run_tests.sh smoke
```

#### "Import errors in tests"
```bash
# Solution 1: Check module structure
find services/ -name "*.py" | head -10

# Solution 2: Verify imports work manually
python -c "import services.domain.models; print('✅ Import successful')"

# Solution 3: Check for circular imports
python -c "import services; print('✅ Services package loads')"
```

### Test Infrastructure Validation

```bash
# Validate test infrastructure itself
./../../scripts/run_tests.sh smoke   # Should complete in <5s
echo $?                        # Should return 0 for success

# Check git hook integration
.git/hooks/test-enforcement smoke  # Manual hook testing

# Validate coverage infrastructure
./../../scripts/run_tests.sh coverage    # Generate full coverage report
open htmlcov/index.html            # View coverage in browser
```

## Integration with Excellence Flywheel

### Verification First

Before implementing new functionality:

1. **Analyze existing tests**: Understand current coverage
2. **Identify gaps**: Find untested functionality
3. **Plan test strategy**: Determine unit vs integration vs orchestration tests
4. **Implement tests first**: TDD approach for new features

### Evidence-based Progress

All development progress must be backed by:

1. **Passing tests**: `./../../scripts/run_tests.sh fast` must pass
2. **Coverage validation**: New code should maintain >80% coverage
3. **Performance requirements**: Smoke tests <5s, fast tests <30s
4. **Integration validation**: Full test suite passes for releases

### GitHub Tracking

Link test infrastructure work to GitHub issues:

- Test coverage improvements → GitHub issue with evidence
- Performance optimizations → Before/after execution times
- New test infrastructure → Documentation and usage examples

## Advanced Usage

### Custom Test Execution

```bash
# Run specific test file
PYTHONPATH=. python -m pytest tests/unit/test_domain_models.py -v

# Run specific test method
PYTHONPATH=. python -m pytest tests/unit/test_domain_models.py::TestModel::test_creation -v

# Run with custom timeout
PYTHONPATH=. python -m pytest tests/unit/ --timeout=5 -v

# Run with coverage for specific module
PYTHONPATH=. python -m pytest tests/unit/ --cov=services.domain --cov-report=term-missing -v
```

### Parallel Test Execution

```bash
# Install pytest-xdist for parallel execution
pip install pytest-xdist

# Run tests in parallel (for large test suites)
PYTHONPATH=. python -m pytest tests/unit/ -n auto -v
```

### Continuous Integration Integration

```yaml
# .github/workflows/test.yml example
- name: Run smoke tests
  run: ./../../scripts/run_tests.sh smoke

- name: Run fast test suite
  run: ./../../scripts/run_tests.sh fast

- name: Run full test suite
  run: ./../../scripts/run_tests.sh full

- name: Generate coverage report
  run: ./../../scripts/run_tests.sh coverage
```

---

**Note**: This test infrastructure was created as part of **Phase 1: Test Infrastructure Activation** by the Chief Architect on 2025-08-20. For questions or improvements, refer to the Excellence Flywheel methodology and create GitHub issues with evidence-based proposals.

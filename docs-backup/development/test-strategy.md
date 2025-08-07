# Test Strategy and Infrastructure

## Test Infrastructure Troubleshooting

### Connection Pool Hanging Prevention

If tests hang during teardown:

1. Check conftest.py pool configuration:

```python
pool_size=5,           # Not 1
max_overflow=10,       # Allow bursts
pool_recycle=3600      # Refresh connections
```

2. Add engine disposal:

```python
await db.engine.dispose()  # In test cleanup
```

### Symptoms of Infrastructure Issues

- Tests pass individually but hang in batch
- "operation in progress" errors
- Test teardown >30 seconds

### MCP Connection Pool Issues

- Circular import errors during teardown
- Logging errors on closed file handles
- Timeout during pool shutdown

### Prevention Strategies

1. Use timeout handling in fixtures
2. Disable logging during shutdown
3. Force cleanup if timeout occurs
4. Defensive import handling

## Test Execution Patterns

### Unit Tests

```bash
PYTHONPATH=. python -m pytest tests/unit/ -v
```

### Integration Tests

```bash
PYTHONPATH=. python -m pytest tests/integration/ -v
```

### Specific Test Classes

```bash
PYTHONPATH=. python -m pytest tests/unit/test_slack_components.py::TestSlackResponseHandler -v
```

### Coverage Reports

```bash
PYTHONPATH=. python -m pytest tests/ --cov=services --cov-report=term-missing
```

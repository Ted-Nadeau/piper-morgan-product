# Claude Code Agent Prompt: GREAT-3D Phase 0 - Investigation

## Session Log Management
Create new session log: `dev/2025/10/04/2025-10-04-phase0-code-GREAT-3D-investigation.md`

Update with timestamped entries for your work.

## Mission
**Investigate Testing Infrastructure**: Examine existing test structure, coverage, and identify gaps for contract and performance testing.

## Context

**GREAT-3D Goal**: Comprehensive validation of plugin architecture through contract testing, performance benchmarking, and documentation.

**Current State**:
- GREAT-3A/3B/3C complete
- 57/57 tests passing (48 plugin tests + 9 demo tests)
- Plugin system operational with 5 plugins

**Phase 0 Goal**: Understand what exists and what needs to be built.

## Your Tasks

### Task 1: Analyze Existing Test Structure

```bash
cd ~/Development/piper-morgan

# Check test directory structure
tree tests/plugins/ -L 2

# List all test files
ls -la tests/plugins/*.py

# Check for contract tests
grep -r "contract" tests/ --include="*.py"

# Check for performance tests
grep -r "performance\|benchmark" tests/ --include="*.py"
```

**Document**:
- Current test files and their purpose
- Test organization (unit, integration, etc.)
- Any existing contract or performance tests

### Task 2: Check Test Coverage

```bash
# Install coverage if needed
pip install pytest-cov --break-system-packages

# Run coverage analysis
PYTHONPATH=. pytest tests/plugins/ --cov=services.plugins --cov-report=term-missing

# Get detailed report
PYTHONPATH=. pytest tests/plugins/ --cov=services.plugins --cov-report=html
```

**Document**:
- Overall coverage percentage
- Which files have good coverage
- Which files need more coverage
- Missing lines/functions

### Task 3: Identify Contract Test Gaps

**Contract tests verify**: All plugins follow the same contract/interface

**Check if we test**:
```python
# Do we verify all plugins implement interface?
grep -r "PiperPlugin" tests/plugins/

# Do we test metadata completeness?
grep -r "get_metadata" tests/plugins/

# Do we test lifecycle order?
grep -r "initialize.*shutdown" tests/plugins/

# Do we test isolation (no direct imports)?
grep -r "import.*integrations" services/plugins/
```

**Questions to Answer**:
1. Do we verify ALL plugins implement the interface?
2. Do we test metadata is complete for all plugins?
3. Do we verify routers are provided when configured?
4. Do we test lifecycle methods work correctly?
5. Do we verify plugins are isolated (no direct core imports)?

### Task 4: Identify Performance Test Gaps

**Performance tests verify**: System performance with plugins

**Check what exists**:
```bash
# Look for timing tests
grep -r "time\|duration\|performance" tests/ --include="*.py"

# Look for memory tests
grep -r "memory\|profile" tests/ --include="*.py"

# Check startup scripts
ls -la scripts/
```

**Questions to Answer**:
1. Do we measure plugin loading time?
2. Do we measure plugin overhead?
3. Do we test memory usage?
4. Do we benchmark multi-plugin scenarios?
5. Do we have baseline performance metrics?

### Task 5: Review Plugin Interface

```bash
# Read the plugin interface definition
cat services/plugins/plugin_interface.py

# Count interface methods
grep -c "def.*abstractmethod" services/plugins/plugin_interface.py
```

**Document**:
- All required methods
- Expected return types
- Any optional methods
- Interface constraints

### Task 6: Analyze Current Plugins

```bash
# List all plugins
ls -la services/integrations/*/[!test]*_plugin.py

# Check each plugin implements all methods
for plugin in services/integrations/*/[!test]*_plugin.py; do
    echo "=== $plugin ==="
    grep "def get_metadata\|def get_router\|def is_configured\|def initialize\|def shutdown\|def get_status" "$plugin"
done
```

**Document**:
- How many plugins exist (should be 5: slack, github, notion, calendar, demo)
- Which methods each implements
- Any inconsistencies in implementation

### Task 7: Benchmark Planning

**Determine what to measure**:

1. **Plugin Overhead**: Time difference between direct router vs plugin wrapper
2. **Startup Time**: How long to discover/load all plugins
3. **Memory Usage**: Memory difference with 0 vs 5 plugins enabled
4. **Multi-Plugin**: Can all plugins operate simultaneously without conflicts

**Create measurement plan**:
```markdown
## Performance Metrics to Capture

### Plugin Overhead
- Measure: Direct router call vs plugin-wrapped call
- Target: < 50ms overhead
- Method: Time 1000 calls, average

### Startup Time
- Measure: App startup with 0, 1, 5 plugins
- Target: < 2s total startup
- Method: Time from import to ready

### Memory Usage
- Measure: Memory with plugins enabled/disabled
- Target: < 50MB per plugin
- Method: memory_profiler

### Concurrency
- Measure: All 5 plugins handling requests simultaneously
- Target: No resource conflicts
- Method: Concurrent requests to all plugins
```

## Deliverable

Create: `dev/2025/10/04/phase-0-code-GREAT-3D-investigation.md`

Include:
1. **Current Test Structure**: What exists, how organized
2. **Coverage Analysis**: Percentages, gaps, missing areas
3. **Contract Test Gaps**: What needs to be tested
4. **Performance Test Gaps**: What benchmarks needed
5. **Plugin Interface Review**: All methods documented
6. **Plugin Analysis**: All 5 plugins verified
7. **Benchmark Plan**: Metrics, targets, methods

## Success Criteria
- [ ] Test structure documented
- [ ] Coverage measured and gaps identified
- [ ] Contract test needs clear
- [ ] Performance test needs clear
- [ ] Interface fully documented
- [ ] All plugins analyzed
- [ ] Benchmark plan ready

---

**Deploy at 4:46 PM**
**Coordinate with Cursor on test organization strategy**

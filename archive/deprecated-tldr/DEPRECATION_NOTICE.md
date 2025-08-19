# TLDR Deprecated 2025-08-18

## Reason: Ecosystem mismatch - 50ms timeouts unrealistic for Python

### Background
TLDR (Test Loop Developer Rapid) was designed to provide <0.1 second feedback loops for development work, inspired by ultra-fast test runners from compiled languages (Go, Rust, JavaScript).

### Why It Failed
1. **Unrealistic Timeouts**: 50ms unit test timeouts impossible with Python imports and dependencies
2. **Wrong Test Scope**: Tried to run ALL 109 tests instead of curated fast subset
3. **Missing Infrastructure**: No test markers, subset selection, or proper integration
4. **Ecosystem Mismatch**: Ported concepts from compiled languages without adapting to Python reality

### Archaeological Evidence
- Created July 26, 2025 as PM-061
- Never had a successful run documented in any session logs
- 100% timeout/failure rate on all attempts
- No test files marked with @tldr, @smoke, or @fast markers

### Files Archived
- `scripts/tldr_runner.py` - Main TLDR runner (345 lines)
- `scripts/pattern_sweep.py` - Pattern detection integration
- Any related configuration files

### Replacement Strategy (if needed)
If rapid feedback is truly needed:
1. Create `@pytest.mark.smoke` markers on 10-15 truly fast tests
2. Use `pytest -m smoke` (realistic 2-5 second execution)
3. Consider `pytest-watch` for file watching
4. Focus on making subset genuinely fast, not all tests faster

### Lesson Learned
Cargo-culting solutions from other ecosystems without understanding the fundamental constraints leads to failed implementations. Python's import overhead and our integration test architecture make sub-second test feedback impossible without major architectural changes.

**Bottom Line**: Well-intentioned but fundamentally flawed concept that should have been a curated smoke test suite, not a comprehensive test runner with impossible time constraints.

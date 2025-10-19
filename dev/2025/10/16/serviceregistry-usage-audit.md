# ServiceRegistry Usage Audit - Phase 1.6

**Date**: October 16, 2025, 11:35 AM
**Purpose**: Find all ServiceRegistry anti-pattern usage
**Tool**: Serena symbolic indexing

---

## Summary

**Total Files with Imports**: 9
**Total Files with .get_llm() Calls**: 8
**Total Usage Sites**: 17 (9 imports + 8 get calls)

**Categories**:
- Import statements: 9 files
- Static get_llm() calls: 8 files (6 production, 2 documentation)
- Pattern: Lazy-load property pattern (4 files)

---

## Detailed Findings

### PRODUCTION CODE

#### File 1: services/intent_service/classifier.py
**Line 34**: Import statement
```python
from services.service_registry import ServiceRegistry
```

**Line 58**: Lazy-load property
```python
@property
def llm(self):
    """Lazy-load LLM service from ServiceRegistry"""
    if self._llm is None:
        self._llm = ServiceRegistry.get_llm()
    return self._llm
```

**Migration Strategy**: Dependency injection with container fallback
**Priority**: HIGH (discovered in Phase 1.5, blocking intent functionality)

---

#### File 2: services/intent_service/llm_classifier.py
**Line 22**: Import statement
```python
from services.service_registry import ServiceRegistry
```

**Line 65**: Lazy-load property
```python
@property
def llm(self):
    """Lazy-load LLM service from ServiceRegistry"""
    if self._llm is None:
        self._llm = ServiceRegistry.get_llm()
    return self._llm
```

**Migration Strategy**: Dependency injection with container fallback
**Priority**: HIGH (used by classifier)

---

#### File 3: services/knowledge_graph/ingestion.py
**Line 24**: Import statement
```python
from services.service_registry import ServiceRegistry
```

**Line 54**: Lazy-load property
```python
@property
def llm(self):
    """Lazy-load LLM service from ServiceRegistry"""
    if not hasattr(self, "_llm") or self._llm is None:
        self._llm = ServiceRegistry.get_llm()
    return self._llm
```

**Migration Strategy**: Dependency injection with container fallback
**Priority**: MEDIUM (knowledge graph features)

---

#### File 4: services/integrations/github/issue_analyzer.py
**Line 15**: Import statement
```python
from services.service_registry import ServiceRegistry
```

**Line 42**: Lazy-load property
```python
@property
def llm(self):
    """Lazy-load LLM service from ServiceRegistry"""
    if not hasattr(self, "_llm") or self._llm is None:
        self._llm = ServiceRegistry.get_llm()
    return self._llm
```

**Migration Strategy**: Dependency injection with container fallback
**Priority**: MEDIUM (GitHub integration)

---

#### File 5: services/orchestration/engine.py
**Line 73**: Import statement (conditional)
```python
if llm_client is None:
    from services.service_registry import ServiceRegistry
    llm_client = ServiceRegistry.get_llm()
```

**Line 75**: Constructor fallback
```python
llm_client = ServiceRegistry.get_llm()
```

**Migration Strategy**: ALREADY FIXED in Phase 1.5! Now gets from ServiceContainer
**Priority**: LOW (already migrated in initialization.py)
**Note**: This import still exists but is now unreachable due to Phase 1.5 changes

---

#### File 6: services/service_registry.py
**Line 27**: Documentation example
```python
# Usage example in docstring
llm = ServiceRegistry.get_llm()
```

**Migration Strategy**: Update documentation to show ServiceContainer pattern
**Priority**: LOW (just documentation)

---

### TESTS

#### File 7: tests/conftest.py
**Line 51**: Import statement
```python
from services.service_registry import ServiceRegistry
```

**Usage**: Test fixture setup
**Migration Strategy**: Update to use ServiceContainer
**Priority**: HIGH (affects all tests)

---

#### File 8: tests/intent/test_query_fallback.py
**Line 22**: Import statement
```python
from services.service_registry import ServiceRegistry
```

**Usage**: Test setup for LLM service
**Migration Strategy**: Update to use ServiceContainer.reset()
**Priority**: HIGH (test infrastructure)

---

#### File 9: tests/intent/base_validation_test.py
**Line 22**: Import statement
```python
from services.service_registry import ServiceRegistry
```

**Usage**: Test base class
**Migration Strategy**: Update to use ServiceContainer
**Priority**: HIGH (test infrastructure)

---

#### File 10: tests/domain/test_llm_domain_service.py
**Line 8**: Import statement
```python
from services.service_registry import ServiceRegistry
```

**Line 189**: Test assertion
```python
assert ServiceRegistry.get_llm() == mock_llm
```

**Migration Strategy**: Update test to use ServiceContainer
**Priority**: MEDIUM (unit test)

---

### DOCUMENTATION

#### File 11: services/domain/llm_domain_service.py
**Line 27**: Docstring example
```python
# Usage:
#     # Access via ServiceRegistry
#     llm = ServiceRegistry.get_llm()
```

**Migration Strategy**: Update docstring to show ServiceContainer
**Priority**: LOW (just documentation)

---

## Migration Priority

### High Priority (Blocking functionality or tests)
1. **services/intent_service/classifier.py** - IntentClassifier (Phase 1.5 discovery)
2. **services/intent_service/llm_classifier.py** - LLM-based classifier
3. **tests/conftest.py** - Test infrastructure
4. **tests/intent/test_query_fallback.py** - Test setup
5. **tests/intent/base_validation_test.py** - Test base class

### Medium Priority (Used but not critical path)
6. **services/knowledge_graph/ingestion.py** - Knowledge graph features
7. **services/integrations/github/issue_analyzer.py** - GitHub integration
8. **tests/domain/test_llm_domain_service.py** - Unit test

### Low Priority (Documentation, already fixed, or unreachable)
9. **services/orchestration/engine.py** - Already fixed (unreachable code)
10. **services/service_registry.py** - Documentation example
11. **services/domain/llm_domain_service.py** - Docstring example

---

## Migration Patterns

### Pattern 1: Lazy-Load Property (Most Common - 4 files)
**Before**:
```python
@property
def llm(self):
    """Lazy-load LLM service from ServiceRegistry"""
    if self._llm is None:
        self._llm = ServiceRegistry.get_llm()
    return self._llm
```

**After**:
```python
@property
def llm(self):
    """Lazy-load LLM service from ServiceContainer"""
    if self._llm is None:
        from services.container import ServiceContainer
        container = ServiceContainer()
        self._llm = container.get_service('llm')
    return self._llm
```

### Pattern 2: Dependency Injection (Preferred for classes)
**Before**:
```python
class MyClass:
    def __init__(self):
        self._llm = None  # Lazy-loaded later
```

**After**:
```python
class MyClass:
    def __init__(self, llm_service=None):
        if llm_service is None:
            from services.container import ServiceContainer
            container = ServiceContainer()
            llm_service = container.get_service('llm')
        self._llm = llm_service
```

### Pattern 3: Test Fixtures
**Before**:
```python
from services.service_registry import ServiceRegistry
ServiceRegistry.register("llm", mock_llm)
```

**After**:
```python
from services.container import ServiceContainer
ServiceContainer.reset()
container = ServiceContainer()
# Tests should mock at initialization level
```

---

## Statistics

- **Production code files**: 6
- **Test files**: 4
- **Documentation only**: 2
- **Lazy-load pattern**: 4 files
- **Already fixed**: 1 file (orchestration/engine.py)

---

## Next Steps

1. ✅ Audit complete - found all 9 files
2. ⏳ Fix high priority files (5 files)
3. ⏳ Fix medium priority files (3 files)
4. ⏳ Update documentation (2 files)
5. ⏳ Deprecate/remove old ServiceRegistry
6. ⏳ Run tests and validate

---

**Audit Complete**: 11:35 AM
**Ready for Migration**: YES
**Estimated Migration Time**: 45 minutes

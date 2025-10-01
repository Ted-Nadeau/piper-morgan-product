# Agent Prompt: Phase 1B - Router Implementation Testing & Verification

## Mission: Test & Verify Complete GitHubIntegrationRouter Implementation
**Objective**: Ensure all newly implemented router methods work correctly and handle edge cases

## Context from Phase 1A
**Code Agent Task**: Implementing all 14 missing GitHubAgent methods in router
**Your Role**: Verify implementations work, test edge cases, ensure quality
**Critical**: Methods must work for 5 bypassing services that will use them

## Testing Strategy

### Task 1: Router Completeness Verification
```python
# Create: test_router_completeness_verification.py
"""
Verify router has all required methods and they're implemented correctly
"""

def test_router_method_completeness():
    """Verify router has all GitHubAgent methods"""
    from services.integrations.github.github_agent import GitHubAgent
    from services.integrations.github.github_integration_router import GitHubIntegrationRouter

    agent_methods = set(m for m in dir(GitHubAgent) if not m.startswith('_') and callable(getattr(GitHubAgent, m)))
    router_methods = set(m for m in dir(GitHubIntegrationRouter) if not m.startswith('_') and callable(getattr(GitHubIntegrationRouter, m)))

    missing = agent_methods - router_methods

    print(f"GitHubAgent methods: {len(agent_methods)}")
    print(f"Router methods: {len(router_methods)}")

    if missing:
        print(f"❌ Missing methods: {sorted(missing)}")
        return False
    else:
        print("✅ Router has all GitHubAgent methods")
        return True

def test_critical_methods_present():
    """Verify the 5 critical methods used by bypassing services"""
    from services.integrations.github.github_integration_router import GitHubIntegrationRouter

    critical_methods = [
        'get_issue_by_url',
        'get_open_issues',
        'get_recent_issues',
        'get_recent_activity',
        'list_repositories'
    ]

    router = GitHubIntegrationRouter()

    for method in critical_methods:
        if hasattr(router, method) and callable(getattr(router, method)):
            print(f"✅ {method} - present and callable")
        else:
            print(f"❌ {method} - missing or not callable")
            return False

    return True

if __name__ == "__main__":
    print("=== Router Completeness Verification ===")
    completeness_ok = test_router_method_completeness()
    critical_ok = test_critical_methods_present()

    if completeness_ok and critical_ok:
        print("\n🎉 Router implementation verification PASSED")
    else:
        print("\n❌ Router implementation verification FAILED")
```

### Task 2: Router Initialization Testing
```python
# Create: test_router_initialization.py
"""
Test router initializes correctly and handles different configurations
"""

def test_router_basic_initialization():
    """Test router can be initialized without errors"""
    try:
        from services.integrations.github.github_integration_router import GitHubIntegrationRouter
        router = GitHubIntegrationRouter()

        print("✅ Router initialized successfully")
        print(f"   Spatial available: {router.spatial_github is not None}")
        print(f"   Legacy available: {router.legacy_github is not None}")
        print(f"   Use spatial: {router.use_spatial}")
        print(f"   Allow legacy: {router.allow_legacy}")

        return True
    except Exception as e:
        print(f"❌ Router initialization failed: {e}")
        return False

def test_router_method_access():
    """Test all router methods can be accessed without errors"""
    from services.integrations.github.github_integration_router import GitHubIntegrationRouter

    router = GitHubIntegrationRouter()
    methods = [m for m in dir(router) if not m.startswith('_') and callable(getattr(router, m))]

    for method_name in methods:
        try:
            method = getattr(router, method_name)
            print(f"✅ {method_name} - accessible")
        except Exception as e:
            print(f"❌ {method_name} - error accessing: {e}")
            return False

    return True

if __name__ == "__main__":
    print("=== Router Initialization Testing ===")
    init_ok = test_router_basic_initialization()
    access_ok = test_router_method_access()

    if init_ok and access_ok:
        print("\n🎉 Router initialization testing PASSED")
    else:
        print("\n❌ Router initialization testing FAILED")
```

### Task 3: Method Signature Verification
```python
# Create: test_method_signatures.py
"""
Verify router method signatures match GitHubAgent exactly
"""

import inspect

def test_method_signature_consistency():
    """Verify router methods have same signatures as GitHubAgent"""
    from services.integrations.github.github_agent import GitHubAgent
    from services.integrations.github.github_integration_router import GitHubIntegrationRouter

    agent = GitHubAgent()
    router = GitHubIntegrationRouter()

    agent_methods = [m for m in dir(agent) if not m.startswith('_') and callable(getattr(agent, m))]

    signature_mismatches = []

    for method_name in agent_methods:
        if hasattr(router, method_name):
            try:
                agent_method = getattr(agent, method_name)
                router_method = getattr(router, method_name)

                agent_sig = inspect.signature(agent_method)
                router_sig = inspect.signature(router_method)

                if agent_sig != router_sig:
                    signature_mismatches.append({
                        'method': method_name,
                        'agent_sig': str(agent_sig),
                        'router_sig': str(router_sig)
                    })
                    print(f"⚠️  {method_name} signature mismatch:")
                    print(f"    Agent:  {agent_sig}")
                    print(f"    Router: {router_sig}")
                else:
                    print(f"✅ {method_name} - signature matches")

            except Exception as e:
                print(f"❌ {method_name} - error checking signature: {e}")
        else:
            print(f"❌ {method_name} - missing from router")

    return len(signature_mismatches) == 0

if __name__ == "__main__":
    print("=== Method Signature Verification ===")
    signatures_ok = test_method_signature_consistency()

    if signatures_ok:
        print("\n🎉 Method signature verification PASSED")
    else:
        print("\n❌ Method signature verification FAILED")
```

### Task 4: Pattern Consistency Testing
```python
# Create: test_router_patterns.py
"""
Test router follows consistent delegation patterns
"""

def test_delegation_pattern_consistency():
    """Test all methods follow the same delegation pattern"""
    import ast
    import inspect

    from services.integrations.github.github_integration_router import GitHubIntegrationRouter

    router = GitHubIntegrationRouter()
    router_methods = [m for m in dir(router) if not m.startswith('_') and callable(getattr(router, m))]

    # Check each method's source for delegation pattern
    for method_name in router_methods:
        try:
            method = getattr(router, method_name)
            source = inspect.getsource(method)

            # Check for delegation pattern elements
            has_get_preferred = '_get_preferred_integration' in source
            has_warning = '_warn_deprecation_if_needed' in source
            has_runtime_error = 'RuntimeError' in source

            if has_get_preferred and has_warning and has_runtime_error:
                print(f"✅ {method_name} - follows delegation pattern")
            else:
                print(f"⚠️  {method_name} - pattern issues:")
                if not has_get_preferred:
                    print(f"    Missing _get_preferred_integration")
                if not has_warning:
                    print(f"    Missing deprecation warning")
                if not has_runtime_error:
                    print(f"    Missing RuntimeError handling")

        except Exception as e:
            print(f"❌ {method_name} - error checking pattern: {e}")

if __name__ == "__main__":
    print("=== Router Pattern Consistency Testing ===")
    test_delegation_pattern_consistency()
```

### Task 5: Integration Error Handling
```python
# Create: test_error_handling.py
"""
Test router handles integration errors gracefully
"""

def test_no_integration_available():
    """Test router behavior when no integrations are available"""

    # This would require mocking or special test setup
    # For now, verify error messages are informative

    print("=== Error Handling Testing ===")
    print("Note: Full error testing requires mocking integrations")
    print("Verify methods have proper RuntimeError messages")

    from services.integrations.github.github_integration_router import GitHubIntegrationRouter

    # Check error message format in source code
    import inspect

    router = GitHubIntegrationRouter()
    methods = [m for m in dir(router) if not m.startswith('_') and callable(getattr(router, m))]

    for method_name in methods:
        try:
            method = getattr(router, method_name)
            source = inspect.getsource(method)

            if 'RuntimeError' in source and method_name in source:
                print(f"✅ {method_name} - has proper error handling")
            elif 'RuntimeError' in source:
                print(f"⚠️  {method_name} - has RuntimeError but check message format")
            else:
                print(f"❌ {method_name} - missing RuntimeError handling")

        except Exception as e:
            print(f"❌ {method_name} - error checking error handling: {e}")

if __name__ == "__main__":
    test_no_integration_available()
```

## Verification Checklist

### Implementation Quality
- [ ] All GitHubAgent methods present in router
- [ ] Method signatures match exactly
- [ ] Delegation pattern consistent across all methods
- [ ] Proper error handling with informative messages
- [ ] Deprecation warnings implemented correctly

### Critical Methods Priority
- [ ] get_issue_by_url works
- [ ] get_open_issues works
- [ ] get_recent_issues works
- [ ] get_recent_activity works
- [ ] list_repositories works

### Pattern Compliance
- [ ] All methods use _get_preferred_integration()
- [ ] All methods include _warn_deprecation_if_needed() for legacy
- [ ] All methods have RuntimeError for no integration
- [ ] Error messages include method name

### Code Quality
- [ ] No syntax errors
- [ ] No import errors
- [ ] Router initializes successfully
- [ ] All methods accessible

## Reporting Format

```markdown
# Phase 1B Results: Router Implementation Verification

## Completeness Assessment
- Total methods implemented: X/14
- Critical methods working: Y/5
- Pattern consistency: [PASS/FAIL]

## Quality Verification
- Method signatures: [MATCH/MISMATCH]
- Error handling: [ADEQUATE/NEEDS_WORK]
- Delegation pattern: [CONSISTENT/INCONSISTENT]

## Issues Found
[List any implementation issues requiring fixes]

## Readiness for Phase 2
[READY/NEEDS_FIXES]
```

## Success Criteria
- ✅ Router has all 14 GitHubAgent methods
- ✅ Critical 5 methods verified working
- ✅ Pattern consistency across all methods
- ✅ No syntax or import errors
- ✅ Ready for import replacement phase

---

**Deploy after Code agent completes implementation. Focus on quality and pattern consistency.**

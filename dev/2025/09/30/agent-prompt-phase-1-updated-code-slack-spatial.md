# Claude Code Prompt: Phase 1 - Slack Spatial System Investigation

## Mission: Comprehensive Slack Spatial Intelligence Verification

**Context**: Phase 0 confirmed solid foundation with 21 spatial files discovered (11 Slack files: 6 core + 5 tests). Now need to verify the sophisticated Slack spatial coordination system is operational through the SlackIntegrationRouter.

**Objective**: Investigate and verify the 11 Slack spatial files are working correctly, understand the spatial coordination patterns, and test functionality through the router interface.

## Phase 1 Tasks

### Task 1: Slack Spatial Architecture Deep Dive

Based on Phase 0 findings of 11 Slack spatial files, map the complete architecture:

```python
# Comprehensive Slack spatial system mapping
import os
import subprocess
from pathlib import Path

def map_slack_spatial_architecture():
    """Deep dive into Slack spatial intelligence architecture"""

    print("=== SLACK SPATIAL ARCHITECTURE INVESTIGATION ===")

    # Get the 11 Slack spatial files identified in Phase 0
    result = subprocess.run(['find', 'services/', '-path', '*/slack/*', '-name', '*spatial*'],
                          capture_output=True, text=True)
    slack_spatial_files = result.stdout.strip().split('\n') if result.stdout.strip() else []

    print(f"📍 SLACK SPATIAL FILES ANALYSIS ({len(slack_spatial_files)} files):")

    core_files = []
    test_files = []

    for file_path in slack_spatial_files:
        if file_path:
            print(f"\n🔍 ANALYZING: {file_path}")

            # Categorize file type
            if 'test' in file_path.lower():
                test_files.append(file_path)
                print("  📋 TYPE: Test file")
            else:
                core_files.append(file_path)
                print("  🔧 TYPE: Core implementation")

            # Analyze file content for patterns
            try:
                with open(file_path, 'r') as f:
                    content = f.read()

                # Look for key patterns
                lines = content.split('\n')
                classes = [line.strip() for line in lines if line.strip().startswith('class ')]
                functions = [line.strip() for line in lines if line.strip().startswith('def ') and not line.strip().startswith('def __')]
                imports = [line.strip() for line in lines if 'import' in line and 'spatial' in line.lower()]

                print(f"  📊 CLASSES: {len(classes)} found")
                for cls in classes[:3]:  # Show first 3
                    print(f"    - {cls}")

                print(f"  🔧 FUNCTIONS: {len(functions)} found")
                for func in functions[:3]:  # Show first 3
                    print(f"    - {func}")

                if imports:
                    print(f"  📦 SPATIAL IMPORTS: {len(imports)} found")
                    for imp in imports[:2]:
                        print(f"    - {imp}")

                # Look for coordination patterns
                if 'coordinate' in content.lower() or 'orchestrat' in content.lower():
                    print("  🎯 COORDINATION PATTERNS: Found")

                if 'router' in content.lower():
                    print("  🔄 ROUTER INTEGRATION: Found")

            except Exception as e:
                print(f"  ❌ Error analyzing file: {e}")

    print(f"\n📊 SUMMARY:")
    print(f"  Core files: {len(core_files)}")
    print(f"  Test files: {len(test_files)}")
    print(f"  Expected: 6 core + 5 tests = 11 total")
    print(f"  Actual: {len(core_files)} core + {len(test_files)} tests = {len(slack_spatial_files)} total")

    return core_files, test_files

core_files, test_files = map_slack_spatial_architecture()
```

### Task 2: Slack Spatial Coordination Testing

Test the spatial coordination capabilities through the SlackIntegrationRouter:

```python
# Test Slack spatial coordination through router
def test_slack_spatial_coordination():
    """Test Slack spatial system through router interface"""

    print("\n=== SLACK SPATIAL COORDINATION TESTING ===")

    try:
        # Import and instantiate the router
        from services.integrations.slack.slack_integration_router import SlackIntegrationRouter
        slack_router = SlackIntegrationRouter()
        print("✅ SlackIntegrationRouter instantiated successfully")

        # Test spatial adapter access
        if hasattr(slack_router, 'get_spatial_adapter'):
            spatial_adapter = slack_router.get_spatial_adapter()
            if spatial_adapter:
                print("✅ Spatial adapter accessible through router")
                print(f"  Spatial adapter type: {type(spatial_adapter).__name__}")

                # Test spatial methods if available
                spatial_methods = [method for method in dir(spatial_adapter)
                                 if not method.startswith('_') and callable(getattr(spatial_adapter, method))]
                print(f"  Available spatial methods: {len(spatial_methods)}")
                for method in spatial_methods[:5]:  # Show first 5
                    print(f"    - {method}")

            else:
                print("⚠️ Spatial adapter returned None")
        else:
            print("⚠️ get_spatial_adapter method not found")

        # Test router method delegation to spatial system
        router_methods = [method for method in dir(slack_router)
                         if not method.startswith('_') and callable(getattr(slack_router, method))]
        print(f"\n🔧 Router methods available: {len(router_methods)}")

        # Look for spatial-related methods
        spatial_methods = [method for method in router_methods if 'spatial' in method.lower()]
        coord_methods = [method for method in router_methods if any(keyword in method.lower()
                        for keyword in ['coordinate', 'orchestrat', 'manage', 'process'])]

        print(f"  Spatial-related methods: {len(spatial_methods)}")
        for method in spatial_methods:
            print(f"    - {method}")

        print(f"  Coordination methods: {len(coord_methods)}")
        for method in coord_methods[:5]:
            print(f"    - {method}")

    except Exception as e:
        print(f"❌ Error testing spatial coordination: {e}")

test_slack_spatial_coordination()
```

### Task 3: Feature Flag Integration Testing

Test how USE_SPATIAL_SLACK flag controls the spatial system:

```python
# Test feature flag control of spatial system
import os

def test_spatial_flag_control():
    """Test USE_SPATIAL_SLACK flag control"""

    print("\n=== SPATIAL FEATURE FLAG TESTING ===")

    # Save original flag value
    original_flag = os.environ.get('USE_SPATIAL_SLACK')

    try:
        # Test with spatial enabled
        print("🔧 Testing USE_SPATIAL_SLACK=true")
        os.environ['USE_SPATIAL_SLACK'] = 'true'

        # Import router with spatial enabled
        from services.integrations.slack.slack_integration_router import SlackIntegrationRouter
        spatial_router = SlackIntegrationRouter()

        print(f"  Router type with spatial=true: {type(spatial_router).__name__}")

        # Check if spatial capabilities are active
        if hasattr(spatial_router, 'get_spatial_adapter'):
            spatial_adapter = spatial_router.get_spatial_adapter()
            if spatial_adapter:
                print("  ✅ Spatial adapter available when enabled")
            else:
                print("  ⚠️ Spatial adapter None when enabled")

        # Test with spatial disabled
        print("\n🔧 Testing USE_SPATIAL_SLACK=false")
        os.environ['USE_SPATIAL_SLACK'] = 'false'

        # Need to reload to test flag change effect
        # Note: This may require module reloading depending on implementation
        print("  ✅ Flag set to false")
        print("  Note: Module reloading may be needed to test flag effect")

        # Test with no flag (default behavior)
        print("\n🔧 Testing USE_SPATIAL_SLACK unset (default)")
        if 'USE_SPATIAL_SLACK' in os.environ:
            del os.environ['USE_SPATIAL_SLACK']

        print("  ✅ Flag unset, testing default behavior")

    except Exception as e:
        print(f"❌ Error testing feature flag: {e}")

    finally:
        # Restore original flag
        if original_flag:
            os.environ['USE_SPATIAL_SLACK'] = original_flag
        elif 'USE_SPATIAL_SLACK' in os.environ:
            del os.environ['USE_SPATIAL_SLACK']

test_spatial_flag_control()
```

### Task 4: Spatial System Pattern Analysis

Analyze the spatial coordination patterns for documentation:

```python
# Analyze spatial patterns for documentation
def analyze_spatial_patterns():
    """Analyze spatial coordination patterns"""

    print("\n=== SPATIAL COORDINATION PATTERN ANALYSIS ===")

    patterns = {
        'coordination_mechanisms': [],
        'data_flow_patterns': [],
        'integration_points': [],
        'router_interactions': []
    }

    # Analyze core spatial files for patterns
    for file_path in core_files:
        if file_path and os.path.exists(file_path):
            print(f"\n🔍 PATTERN ANALYSIS: {file_path}")

            try:
                with open(file_path, 'r') as f:
                    content = f.read()

                # Look for coordination mechanisms
                if any(keyword in content.lower() for keyword in ['coordinate', 'orchestrat', 'manage', 'sync']):
                    patterns['coordination_mechanisms'].append(file_path)
                    print("  🎯 Coordination mechanism detected")

                # Look for data flow patterns
                if any(keyword in content.lower() for keyword in ['process', 'transform', 'route', 'handle']):
                    patterns['data_flow_patterns'].append(file_path)
                    print("  📊 Data flow pattern detected")

                # Look for integration points
                if any(keyword in content.lower() for keyword in ['router', 'adapter', 'integration', 'bridge']):
                    patterns['integration_points'].append(file_path)
                    print("  🔗 Integration point detected")

                # Look for router interactions
                if 'SlackIntegrationRouter' in content or 'slack_integration_router' in content:
                    patterns['router_interactions'].append(file_path)
                    print("  🔄 Router interaction detected")

            except Exception as e:
                print(f"  ❌ Error analyzing patterns: {e}")

    # Summary of patterns
    print(f"\n📊 PATTERN SUMMARY:")
    for pattern_type, files in patterns.items():
        print(f"  {pattern_type}: {len(files)} files")
        for file_path in files:
            print(f"    - {os.path.basename(file_path)}")

    return patterns

spatial_patterns = analyze_spatial_patterns()
```

### Task 5: Integration Testing with Router

Run comprehensive tests of spatial system through router:

```bash
# Run existing spatial tests
echo "=== RUNNING SLACK SPATIAL TESTS ==="

# Find and run Slack spatial tests
find tests/ -path "*slack*" -name "*spatial*" -name "*.py" | head -5

# Try to run spatial tests if they exist
pytest tests/ -k "slack and spatial" -v || echo "No slack spatial tests found or pytest not configured"

# Test with spatial flag enabled
echo ""
echo "=== TESTING WITH SPATIAL FLAG ENABLED ==="
USE_SPATIAL_SLACK=true python -c "
from services.integrations.slack.slack_integration_router import SlackIntegrationRouter
router = SlackIntegrationRouter()
print('Router with spatial=true:', type(router).__name__)
if hasattr(router, 'get_spatial_adapter'):
    adapter = router.get_spatial_adapter()
    print('Spatial adapter available:', adapter is not None)
    if adapter:
        print('Adapter type:', type(adapter).__name__)
"

# Test router health check if available
echo ""
echo "=== TESTING ROUTER HEALTH ==="
python -c "
from services.integrations.slack.slack_integration_router import SlackIntegrationRouter
router = SlackIntegrationRouter()
if hasattr(router, 'health_check'):
    try:
        health = router.health_check()
        print('Router health check:', health)
    except Exception as e:
        print('Health check error:', e)
else:
    print('No health_check method available')
"
```

## GitHub Evidence Update

```bash
# Update GitHub issue with Phase 1 findings
gh issue comment 194 --body "## Phase 1: Slack Spatial Verification Progress

### Spatial Architecture Analysis ✅
- [X] files analyzed: [list key findings]
- Core spatial files: [X] found
- Test spatial files: [X] found
- Coordination patterns: [discovered patterns]

### Router Integration Testing ✅
- SlackIntegrationRouter spatial access: [working/issues]
- Spatial adapter availability: [status]
- Method delegation: [verified/issues]

### Feature Flag Testing ✅
- USE_SPATIAL_SLACK=true: [behavior]
- USE_SPATIAL_SLACK=false: [behavior]
- Default behavior: [behavior]

### Pattern Analysis ✅
- Coordination mechanisms: [X] files
- Integration points: [X] files
- Router interactions: [findings]

**Status**: [PHASE_1_COMPLETE/IN_PROGRESS/ISSUES_FOUND]
**Evidence**: [paste test results and key outputs]"
```

## Anti-80% Safeguards

**Mandatory Slack Spatial Verification**:
```
Spatial Component | Analyzed | Working | Status
----------------- | -------- | ------- | ------
Core file 1       | [ ]      | [ ]     |
Core file 2       | [ ]      | [ ]     |
Core file 3       | [ ]      | [ ]     |
Core file 4       | [ ]      | [ ]     |
Core file 5       | [ ]      | [ ]     |
Core file 6       | [ ]      | [ ]     |
Test file 1       | [ ]      | [ ]     |
Test file 2       | [ ]      | [ ]     |
Test file 3       | [ ]      | [ ]     |
Test file 4       | [ ]      | [ ]     |
Test file 5       | [ ]      | [ ]     |
TOTAL: 11/11 = 100% REQUIRED
```

## Success Criteria

Phase 1 complete when:
- [✅] All 11 Slack spatial files analyzed and verified working
- [✅] SlackIntegrationRouter provides access to spatial capabilities
- [✅] USE_SPATIAL_SLACK flag controls spatial system behavior
- [✅] Spatial coordination patterns documented
- [✅] Integration tests passing through router
- [✅] GitHub issue #194 updated with evidence

## STOP Conditions

Stop immediately if:
- Fewer than 11 Slack spatial files found (regression)
- SlackIntegrationRouter not providing spatial access
- Feature flags not controlling behavior
- Spatial system fundamentally broken
- Cannot access spatial coordination capabilities

---

**Your Mission**: Verify the sophisticated Slack spatial intelligence system is operational and accessible through the router interface.

**Quality Standard**: Complete verification of all 11 spatial files with evidence of working coordination patterns.

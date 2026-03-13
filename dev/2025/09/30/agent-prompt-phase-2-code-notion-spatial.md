# Claude Code Prompt: Phase 2 - Notion Spatial System Investigation

## Mission: Comprehensive Notion Spatial Intelligence Discovery & Verification

**Context**: Phase 1 confirmed Slack spatial system fully operational (11/11 files). Phase 0 identified 1 Notion spatial file ("intelligence layer"). Now need to investigate Notion spatial capabilities and verify functionality through NotionIntegrationRouter.

**Objective**: Discover the extent of Notion spatial intelligence system, verify functionality through router, and document spatial patterns for knowledge management coordination.

## Phase 2 Tasks

### Task 1: Notion Spatial System Discovery & Analysis

Investigate the Notion spatial intelligence system building on Phase 0 findings:

```python
# Comprehensive Notion spatial system discovery
import os
import subprocess
from pathlib import Path

def discover_notion_spatial_system():
    """Deep dive into Notion spatial intelligence discovery"""

    print("=== NOTION SPATIAL SYSTEM DISCOVERY ===")

    # Find all Notion spatial files (Phase 0 found 1 file)
    result = subprocess.run(['find', 'services/', '-path', '*/notion/*', '-name', '*spatial*'],
                          capture_output=True, text=True)
    notion_spatial_files = result.stdout.strip().split('\n') if result.stdout.strip() else []

    print(f"📍 NOTION SPATIAL FILES ANALYSIS ({len(notion_spatial_files)} files):")

    spatial_files = []

    for file_path in notion_spatial_files:
        if file_path:
            print(f"\n🔍 ANALYZING: {file_path}")
            spatial_files.append(file_path)

            # Analyze file content for spatial intelligence patterns
            try:
                with open(file_path, 'r') as f:
                    content = f.read()

                # Look for key patterns
                lines = content.split('\n')
                classes = [line.strip() for line in lines if line.strip().startswith('class ')]
                functions = [line.strip() for line in lines if line.strip().startswith('def ') and not line.strip().startswith('def __')]
                imports = [line.strip() for line in lines if 'import' in line]

                print(f"  📊 CLASSES: {len(classes)} found")
                for cls in classes:
                    print(f"    - {cls}")

                print(f"  🔧 FUNCTIONS: {len(functions)} found")
                for func in functions[:5]:  # Show first 5
                    print(f"    - {func}")
                if len(functions) > 5:
                    print(f"    ... and {len(functions)-5} more")

                print(f"  📦 IMPORTS: {len(imports)} found")
                for imp in imports[:3]:  # Show first 3
                    print(f"    - {imp}")

                # Look for spatial intelligence patterns
                spatial_keywords = ['spatial', 'coordinate', 'navigate', 'map', 'context', 'intelligence']
                found_patterns = []
                for keyword in spatial_keywords:
                    if keyword.lower() in content.lower():
                        found_patterns.append(keyword)

                if found_patterns:
                    print(f"  🧠 INTELLIGENCE PATTERNS: {', '.join(found_patterns)}")

                # Look for knowledge management patterns
                knowledge_keywords = ['database', 'page', 'block', 'workspace', 'knowledge', 'semantic']
                found_knowledge = []
                for keyword in knowledge_keywords:
                    if keyword.lower() in content.lower():
                        found_knowledge.append(keyword)

                if found_knowledge:
                    print(f"  📚 KNOWLEDGE PATTERNS: {', '.join(found_knowledge)}")

                # Look for router integration
                if 'router' in content.lower() or 'integration' in content.lower():
                    print("  🔄 ROUTER INTEGRATION: Found")

            except Exception as e:
                print(f"  ❌ Error analyzing file: {e}")

    # Look for additional Notion spatial-related files
    print(f"\n🔍 SEARCHING FOR ADDITIONAL NOTION SPATIAL COMPONENTS...")

    # Search for spatial references in all Notion files
    result = subprocess.run(['grep', '-r', 'spatial', 'services/', '--include=*.py'],
                          capture_output=True, text=True)
    spatial_refs = result.stdout.strip().split('\n') if result.stdout.strip() else []

    notion_spatial_refs = [ref for ref in spatial_refs if 'notion' in ref.lower()]

    print(f"📊 NOTION SPATIAL REFERENCES: {len(notion_spatial_refs)} found")
    for ref in notion_spatial_refs[:5]:  # Show first 5
        print(f"  {ref}")

    return spatial_files, notion_spatial_refs

notion_files, spatial_refs = discover_notion_spatial_system()
```

### Task 2: NotionIntegrationRouter Spatial Capabilities Testing

Test Notion spatial functionality through the router:

```python
# Test Notion spatial capabilities through router
def test_notion_spatial_through_router():
    """Test Notion spatial system through NotionIntegrationRouter"""

    print("\n=== NOTION SPATIAL ROUTER TESTING ===")

    try:
        # Import and instantiate the router
        from services.integrations.notion.notion_integration_router import NotionIntegrationRouter
        notion_router = NotionIntegrationRouter()
        print("✅ NotionIntegrationRouter instantiated successfully")

        # Test spatial capabilities
        router_methods = [method for method in dir(notion_router)
                         if not method.startswith('_') and callable(getattr(notion_router, method))]

        print(f"🔧 Router methods available: {len(router_methods)}")

        # Look for spatial-related methods
        spatial_methods = [method for method in router_methods if 'spatial' in method.lower()]
        knowledge_methods = [method for method in router_methods if any(keyword in method.lower()
                           for keyword in ['knowledge', 'semantic', 'context', 'intelligence'])]

        print(f"  📊 Spatial-related methods: {len(spatial_methods)}")
        for method in spatial_methods:
            print(f"    - {method}")

        print(f"  🧠 Knowledge/Intelligence methods: {len(knowledge_methods)}")
        for method in knowledge_methods[:5]:
            print(f"    - {method}")

        # Test router spatial access patterns
        if hasattr(notion_router, 'get_spatial_adapter'):
            spatial_adapter = notion_router.get_spatial_adapter()
            if spatial_adapter:
                print("✅ Spatial adapter accessible through router")
                print(f"  Adapter type: {type(spatial_adapter).__name__}")
            else:
                print("⚠️ Spatial adapter returned None")
        else:
            print("ℹ️ No get_spatial_adapter method (different pattern than Slack)")

        # Test knowledge management capabilities
        knowledge_capabilities = []
        test_methods = ['get_workspace_info', 'search_pages', 'get_database_info',
                       'query_database', 'get_page_content']

        for method_name in test_methods:
            if hasattr(notion_router, method_name):
                knowledge_capabilities.append(method_name)
                print(f"✅ Knowledge method available: {method_name}")

        print(f"\n📚 Knowledge capabilities: {len(knowledge_capabilities)}/{len(test_methods)}")

        return notion_router, spatial_methods, knowledge_capabilities

    except Exception as e:
        print(f"❌ Error testing Notion router: {e}")
        return None, [], []

router, spatial_methods, knowledge_caps = test_notion_spatial_through_router()
```

### Task 3: Feature Flag Integration Testing

Test USE_SPATIAL_NOTION flag control:

```python
# Test Notion spatial feature flag control
import os

def test_notion_spatial_flag_control():
    """Test USE_SPATIAL_NOTION flag control"""

    print("\n=== NOTION SPATIAL FLAG TESTING ===")

    # Save original flag value
    original_flag = os.environ.get('USE_SPATIAL_NOTION')

    try:
        # Test with spatial enabled
        print("🔧 Testing USE_SPATIAL_NOTION=true")
        os.environ['USE_SPATIAL_NOTION'] = 'true'

        # Import router with spatial enabled
        from services.integrations.notion.notion_integration_router import NotionIntegrationRouter
        notion_router = NotionIntegrationRouter()

        print(f"  Router type with spatial=true: {type(notion_router).__name__}")

        # Check spatial configuration
        if hasattr(notion_router, '_should_use_spatial'):
            uses_spatial = notion_router._should_use_spatial()
            print(f"  Uses spatial: {uses_spatial}")
        elif hasattr(notion_router, 'use_spatial'):
            uses_spatial = notion_router.use_spatial
            print(f"  Uses spatial: {uses_spatial}")
        else:
            print("  ⚠️ Cannot determine spatial usage")

        # Test with spatial disabled
        print("\n🔧 Testing USE_SPATIAL_NOTION=false")
        os.environ['USE_SPATIAL_NOTION'] = 'false'

        print("  ✅ Flag set to false - testing behavior change")

        # Test default behavior
        print("\n🔧 Testing USE_SPATIAL_NOTION unset (default)")
        if 'USE_SPATIAL_NOTION' in os.environ:
            del os.environ['USE_SPATIAL_NOTION']

        print("  ✅ Flag unset - testing default behavior")

    except Exception as e:
        print(f"❌ Error testing Notion feature flag: {e}")

    finally:
        # Restore original flag
        if original_flag:
            os.environ['USE_SPATIAL_NOTION'] = original_flag
        elif 'USE_SPATIAL_NOTION' in os.environ:
            del os.environ['USE_SPATIAL_NOTION']

test_notion_spatial_flag_control()
```

### Task 4: Notion Spatial Pattern Analysis

Analyze Notion spatial patterns compared to Slack:

```python
# Compare Notion vs Slack spatial patterns
def analyze_notion_spatial_patterns():
    """Analyze Notion spatial patterns vs Slack comparison"""

    print("\n=== NOTION SPATIAL PATTERN ANALYSIS ===")

    patterns = {
        'file_structure': {},
        'intelligence_patterns': {},
        'knowledge_integration': {},
        'router_patterns': {}
    }

    # Analyze file structure differences
    print("📁 FILE STRUCTURE COMPARISON:")
    print(f"  Slack spatial files: 11 (6 core + 5 tests)")
    print(f"  Notion spatial files: {len(notion_files)}")

    if len(notion_files) < 11:
        print("  🔍 Notion uses fewer files - may be more consolidated architecture")
    elif len(notion_files) > 11:
        print("  🔍 Notion uses more files - may be more granular architecture")
    else:
        print("  🔍 Notion uses similar file count - comparable architecture")

    # Analyze each Notion spatial file for patterns
    for file_path in notion_files:
        if file_path and os.path.exists(file_path):
            print(f"\n🔍 PATTERN ANALYSIS: {file_path}")

            try:
                with open(file_path, 'r') as f:
                    content = f.read()

                # Intelligence patterns
                intelligence_indicators = []
                if 'semantic' in content.lower():
                    intelligence_indicators.append('semantic_processing')
                if 'knowledge' in content.lower():
                    intelligence_indicators.append('knowledge_management')
                if 'context' in content.lower():
                    intelligence_indicators.append('context_awareness')
                if 'embedding' in content.lower():
                    intelligence_indicators.append('embedding_analysis')

                if intelligence_indicators:
                    patterns['intelligence_patterns'][file_path] = intelligence_indicators
                    print(f"  🧠 Intelligence patterns: {', '.join(intelligence_indicators)}")

                # Knowledge integration patterns
                knowledge_indicators = []
                if 'database' in content.lower():
                    knowledge_indicators.append('database_integration')
                if 'page' in content.lower():
                    knowledge_indicators.append('page_processing')
                if 'workspace' in content.lower():
                    knowledge_indicators.append('workspace_coordination')

                if knowledge_indicators:
                    patterns['knowledge_integration'][file_path] = knowledge_indicators
                    print(f"  📚 Knowledge patterns: {', '.join(knowledge_indicators)}")

                # Router integration
                if 'NotionIntegrationRouter' in content or 'notion_integration_router' in content:
                    patterns['router_patterns'][file_path] = 'router_integration'
                    print("  🔄 Router integration detected")

            except Exception as e:
                print(f"  ❌ Error analyzing patterns: {e}")

    # Summary comparison
    print(f"\n📊 NOTION VS SLACK SPATIAL COMPARISON:")
    print(f"  Architecture style: {'Consolidated' if len(notion_files) < 6 else 'Granular'}")
    print(f"  Intelligence focus: {len(patterns['intelligence_patterns'])} files")
    print(f"  Knowledge integration: {len(patterns['knowledge_integration'])} files")
    print(f"  Router integration: {len(patterns['router_patterns'])} files")

    return patterns

notion_patterns = analyze_notion_spatial_patterns()
```

### Task 5: Knowledge Management Integration Testing

Test Notion's knowledge management spatial capabilities:

```bash
# Test Notion knowledge management integration
echo "=== NOTION KNOWLEDGE MANAGEMENT TESTING ==="

# Test with spatial flag enabled
echo "Testing with USE_SPATIAL_NOTION=true..."
USE_SPATIAL_NOTION=true python -c "
from services.integrations.notion.notion_integration_router import NotionIntegrationRouter
router = NotionIntegrationRouter()
print('Router with spatial=true:', type(router).__name__)

# Test knowledge management methods
knowledge_methods = ['get_workspace_info', 'search_pages', 'get_database_info']
for method in knowledge_methods:
    if hasattr(router, method):
        print(f'Knowledge method available: {method}')
    else:
        print(f'Knowledge method missing: {method}')
"

# Test router health if available
echo ""
echo "=== TESTING NOTION ROUTER HEALTH ==="
python -c "
from services.integrations.notion.notion_integration_router import NotionIntegrationRouter
router = NotionIntegrationRouter()
if hasattr(router, 'health_check'):
    try:
        health = router.health_check()
        print('Router health check:', health)
    except Exception as e:
        print('Health check error:', e)
elif hasattr(router, 'is_configured'):
    try:
        configured = router.is_configured()
        print('Router configuration status:', configured)
    except Exception as e:
        print('Configuration check error:', e)
else:
    print('No health/configuration check methods available')
"

# Look for existing Notion spatial tests
echo ""
echo "=== NOTION SPATIAL TEST DISCOVERY ==="
find tests/ -path "*notion*" -name "*spatial*" -type f | head -5
```

## GitHub Evidence Update

```bash
# Update GitHub issue with Phase 2 findings
gh issue comment 194 --body "## Phase 2: Notion Spatial Investigation Progress

### Spatial System Discovery ✅
- Notion spatial files found: [X] files
- File analysis: [details of components]
- Intelligence patterns: [discovered capabilities]
- Knowledge integration: [patterns found]

### Router Integration Testing ✅
- NotionIntegrationRouter spatial access: [working/different_pattern/issues]
- Knowledge management methods: [X available]
- Spatial capabilities: [found/not_found]

### Feature Flag Testing ✅
- USE_SPATIAL_NOTION=true: [behavior]
- USE_SPATIAL_NOTION=false: [behavior]
- Default behavior: [behavior]

### Pattern Analysis ✅
- Architecture comparison to Slack: [consolidated/granular/similar]
- Intelligence patterns: [X] files
- Knowledge management focus: [findings]
- Router integration: [pattern description]

**Status**: [PHASE_2_COMPLETE/IN_PROGRESS/ISSUES_FOUND]
**Evidence**: [paste investigation results and key outputs]"
```

## Anti-80% Safeguards

**Mandatory Notion Spatial Verification**:
```
Notion Component | Discovered | Analyzed | Working | Status
---------------- | ---------- | -------- | ------- | ------
Spatial file 1   | [ ]        | [ ]      | [ ]     |
[Additional files found] | [ ] | [ ]    | [ ]     |
Router integration | [ ]      | [ ]      | [ ]     |
Feature flag control | [ ]    | [ ]      | [ ]     |
Knowledge capabilities | [ ]  | [ ]      | [ ]     |
TOTAL: X/X = 100% REQUIRED
```

## Success Criteria

Phase 2 complete when:
- [✅] All Notion spatial files discovered and analyzed
- [✅] NotionIntegrationRouter spatial capabilities verified
- [✅] USE_SPATIAL_NOTION flag controls behavior
- [✅] Knowledge management integration documented
- [✅] Spatial patterns compared to Slack system
- [✅] GitHub issue #194 updated with evidence

## STOP Conditions

Stop immediately if:
- No Notion spatial system found (contradicts Phase 0)
- NotionIntegrationRouter fundamentally broken
- Cannot access knowledge management capabilities
- Feature flags not working
- Spatial system completely different from expected

---

**Your Mission**: Discover and verify Notion's spatial intelligence system for knowledge management coordination.

**Quality Standard**: Complete documentation of Notion spatial capabilities with evidence of functionality through router interface.

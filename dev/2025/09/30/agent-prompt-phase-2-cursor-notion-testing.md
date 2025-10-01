# Cursor Agent Prompt: Phase 2 - Notion Spatial Testing & Validation

## Mission: Focused Notion Spatial System Testing

**Context**: Phase 1 verified Slack spatial system fully operational (11 files, sophisticated architecture). Phase 0 identified 1 Notion spatial file. Phase 2 requires focused testing to verify Notion spatial capabilities through NotionIntegrationRouter and feature flag control.

**Objective**: Test Notion spatial functionality through router interface, validate USE_SPATIAL_NOTION flag behavior, and compare knowledge management integration patterns to Slack spatial system.

## Phase 2 Testing Tasks

### Task 1: NotionIntegrationRouter Spatial Testing

Test Notion spatial system through the router interface:

```python
# Test Notion spatial functionality through router
def test_notion_spatial_through_router():
    """Test Notion spatial system via NotionIntegrationRouter"""
    
    print("=== NOTION SPATIAL ROUTER TESTING ===")
    
    import os
    
    # Test with spatial enabled
    os.environ['USE_SPATIAL_NOTION'] = 'true'
    
    try:
        from services.integrations.notion.notion_integration_router import NotionIntegrationRouter
        
        # Instantiate router with spatial enabled
        notion_router = NotionIntegrationRouter()
        print("✅ NotionIntegrationRouter instantiated with USE_SPATIAL_NOTION=true")
        
        # Test router methods
        router_methods = [m for m in dir(notion_router) 
                         if not m.startswith('_') and callable(getattr(notion_router, m))]
        print(f"🔧 Router methods available: {len(router_methods)}")
        
        # Look for spatial-related methods
        spatial_methods = [m for m in router_methods if 'spatial' in m.lower()]
        knowledge_methods = [m for m in router_methods if any(keyword in m.lower() 
                           for keyword in ['knowledge', 'semantic', 'context', 'intelligence'])]
        
        print(f"  📊 Spatial-related methods: {len(spatial_methods)}")
        for method in spatial_methods:
            print(f"    - {method}")
        
        print(f"  🧠 Knowledge/Intelligence methods: {len(knowledge_methods)}")
        for method in knowledge_methods[:5]:
            print(f"    - {method}")
        
        # Test spatial adapter access (may be different pattern than Slack)
        if hasattr(notion_router, 'get_spatial_adapter'):
            spatial_adapter = notion_router.get_spatial_adapter()
            if spatial_adapter:
                print("✅ Spatial adapter accessible through router")
                print(f"  Adapter type: {type(spatial_adapter).__name__}")
                
                # Test adapter methods
                adapter_methods = [m for m in dir(spatial_adapter) if not m.startswith('_')]
                print(f"  Available adapter methods: {len(adapter_methods)}")
                for method in adapter_methods[:5]:
                    print(f"    - {method}")
            else:
                print("⚠️ Spatial adapter returned None")
        else:
            print("ℹ️ No get_spatial_adapter method (different pattern than Slack)")
        
        # Test knowledge management capabilities
        knowledge_test_methods = ['get_workspace_info', 'search_pages', 'get_database_info', 
                                'query_database', 'get_page_content', 'is_configured']
        
        available_knowledge = []
        for method_name in knowledge_test_methods:
            if hasattr(notion_router, method_name):
                available_knowledge.append(method_name)
                print(f"✅ Knowledge method available: {method_name}")
        
        print(f"\n📚 Knowledge capabilities: {len(available_knowledge)}/{len(knowledge_test_methods)}")
        
        # Test basic router functionality
        if hasattr(notion_router, 'health_check'):
            try:
                health = notion_router.health_check()
                print(f"✅ Router health check: {health}")
            except Exception as e:
                print(f"⚠️ Router health check error: {e}")
        elif hasattr(notion_router, 'is_configured'):
            try:
                configured = notion_router.is_configured()
                print(f"✅ Router configuration: {configured}")
            except Exception as e:
                print(f"⚠️ Router configuration error: {e}")
        
        return notion_router, spatial_methods, available_knowledge
        
    except Exception as e:
        print(f"❌ Router spatial testing failed: {e}")
        return None, [], []

router, spatial_methods, knowledge_caps = test_notion_spatial_through_router()
```

### Task 2: Feature Flag Behavior Validation

Validate USE_SPATIAL_NOTION flag controls spatial behavior:

```python
# Test Notion feature flag control behavior
def validate_notion_spatial_flag_behavior():
    """Validate USE_SPATIAL_NOTION flag controls behavior"""
    
    print("\n=== NOTION SPATIAL FLAG BEHAVIOR VALIDATION ===")
    
    import os
    import importlib
    import sys
    
    results = {}
    
    # Test scenarios
    test_scenarios = [
        ('true', 'Spatial enabled'),
        ('false', 'Spatial disabled'), 
        (None, 'Default behavior')
    ]
    
    for flag_value, description in test_scenarios:
        print(f"\n🔧 Testing: {description} (USE_SPATIAL_NOTION={flag_value})")
        
        # Set flag
        if flag_value is None:
            if 'USE_SPATIAL_NOTION' in os.environ:
                del os.environ['USE_SPATIAL_NOTION']
        else:
            os.environ['USE_SPATIAL_NOTION'] = flag_value
        
        try:
            # Clear module cache to ensure flag change takes effect
            modules_to_reload = [m for m in sys.modules.keys() if 'notion' in m and 'router' in m]
            for module in modules_to_reload:
                if module in sys.modules:
                    importlib.reload(sys.modules[module])
            
            # Test router behavior
            from services.integrations.notion.notion_integration_router import NotionIntegrationRouter
            test_router = NotionIntegrationRouter()
            
            # Check spatial access (may be different pattern than Slack)
            spatial_available = False
            spatial_method_exists = False
            
            if hasattr(test_router, 'get_spatial_adapter'):
                spatial_method_exists = True
                spatial_adapter = test_router.get_spatial_adapter()
                spatial_available = spatial_adapter is not None
            
            print(f"  Spatial method exists: {spatial_method_exists}")
            print(f"  Spatial adapter available: {spatial_available}")
            
            # Check flag method if available
            uses_spatial = None
            if hasattr(test_router, '_should_use_spatial'):
                uses_spatial = test_router._should_use_spatial()
                print(f"  Uses spatial (internal): {uses_spatial}")
            elif hasattr(test_router, 'use_spatial'):
                uses_spatial = test_router.use_spatial
                print(f"  Uses spatial (property): {uses_spatial}")
            
            # Check configuration status
            configured = None
            if hasattr(test_router, 'is_configured'):
                try:
                    configured = test_router.is_configured()
                    print(f"  Router configured: {configured}")
                except:
                    print(f"  Router configuration: Cannot determine")
            
            results[flag_value] = {
                'spatial_method_exists': spatial_method_exists,
                'spatial_available': spatial_available,
                'uses_spatial': uses_spatial,
                'configured': configured,
                'router_created': True
            }
            
            print(f"  ✅ {description} test successful")
            
        except Exception as e:
            print(f"  ❌ {description} test failed: {e}")
            results[flag_value] = {'error': str(e)}
    
    # Summary
    print(f"\n📊 NOTION FLAG BEHAVIOR SUMMARY:")
    for flag_value, description in test_scenarios:
        result = results.get(flag_value, {})
        if 'error' in result:
            print(f"  {description}: ❌ {result['error']}")
        else:
            spatial = result.get('spatial_available', False)
            method_exists = result.get('spatial_method_exists', False)
            print(f"  {description}: ✅ Method={method_exists}, Spatial={spatial}")
    
    return results

notion_flag_results = validate_notion_spatial_flag_behavior()
```

### Task 3: Knowledge Management Integration Testing

Test Notion's knowledge management spatial integration:

```python
# Test knowledge management integration
def test_notion_knowledge_integration():
    """Test Notion knowledge management spatial integration"""
    
    print("\n=== NOTION KNOWLEDGE MANAGEMENT INTEGRATION ===")
    
    import os
    os.environ['USE_SPATIAL_NOTION'] = 'true'
    
    integration_tests = []
    
    try:
        from services.integrations.notion.notion_integration_router import NotionIntegrationRouter
        router = NotionIntegrationRouter()
        
        # Test 1: Configuration and setup
        print("🔧 Testing configuration and setup...")
        if hasattr(router, 'is_configured'):
            try:
                configured = router.is_configured()
                print(f"  ✅ Configuration check: {configured}")
                integration_tests.append(('configuration_check', True))
            except Exception as e:
                print(f"  ⚠️ Configuration check error: {e}")
                integration_tests.append(('configuration_check', False))
        else:
            print("  ⚠️ No configuration check method")
            integration_tests.append(('configuration_check', None))
        
        # Test 2: Workspace information access
        print("\n🔧 Testing workspace information access...")
        workspace_methods = ['get_workspace_info', 'connect', 'authenticate']
        for method_name in workspace_methods:
            if hasattr(router, method_name):
                print(f"  ✅ Found workspace method: {method_name}")
                integration_tests.append((f'workspace_{method_name}', True))
            else:
                print(f"  ⚠️ Missing workspace method: {method_name}")
                integration_tests.append((f'workspace_{method_name}', False))
        
        # Test 3: Knowledge access capabilities
        print("\n🔧 Testing knowledge access capabilities...")
        knowledge_methods = ['search_pages', 'get_database_info', 'query_database', 
                            'get_page_content', 'list_databases']
        available_knowledge = []
        for method_name in knowledge_methods:
            if hasattr(router, method_name):
                available_knowledge.append(method_name)
                print(f"  ✅ Found knowledge method: {method_name}")
                integration_tests.append((f'knowledge_{method_name}', True))
            else:
                print(f"  ⚠️ Missing knowledge method: {method_name}")
                integration_tests.append((f'knowledge_{method_name}', False))
        
        print(f"\n📊 Knowledge capabilities: {len(available_knowledge)}/{len(knowledge_methods)}")
        
        # Test 4: Spatial intelligence integration
        print("\n🔧 Testing spatial intelligence integration...")
        if hasattr(router, 'get_spatial_adapter'):
            adapter = router.get_spatial_adapter()
            if adapter:
                print("  ✅ Spatial adapter integration working")
                integration_tests.append(('spatial_integration', True))
                
                # Test adapter capabilities
                if hasattr(adapter, 'analyze_knowledge_context'):
                    print("  ✅ Knowledge context analysis available")
                if hasattr(adapter, 'semantic_search'):
                    print("  ✅ Semantic search available")
            else:
                print("  ⚠️ Spatial adapter returns None")
                integration_tests.append(('spatial_integration', False))
        else:
            print("  ℹ️ Different spatial integration pattern (not adapter-based)")
            integration_tests.append(('spatial_integration', None))
        
    except Exception as e:
        print(f"❌ Knowledge integration testing failed: {e}")
    
    # Summary
    print(f"\n📊 KNOWLEDGE INTEGRATION TEST SUMMARY:")
    for test_name, result in integration_tests:
        status = "✅ PASS" if result else "❌ FAIL" if result is not None else "⚠️ SKIP"
        print(f"  {test_name}: {status}")
    
    return integration_tests

knowledge_integration_results = test_notion_knowledge_integration()
```

### Task 4: Notion vs Slack Pattern Comparison

Compare Notion spatial patterns to Slack spatial system:

```python
# Compare Notion vs Slack spatial patterns
def compare_notion_vs_slack_patterns():
    """Compare Notion vs Slack spatial patterns"""
    
    print("\n=== NOTION VS SLACK SPATIAL COMPARISON ===")
    
    comparison = {
        'architecture_style': {},
        'access_patterns': {},
        'functionality_focus': {},
        'integration_approach': {}
    }
    
    # Architecture style comparison
    print("🏗️ ARCHITECTURE STYLE COMPARISON:")
    
    # From Phase 1, we know Slack has 11 files (6 core + 5 tests)
    slack_info = {
        'files': 11,
        'core_files': 6,
        'test_files': 5,
        'pattern': 'granular_specialized'
    }
    
    # Test Notion pattern
    import os
    notion_spatial_files = []
    for root, dirs, files in os.walk('services/'):
        for file in files:
            file_path = os.path.join(root, file)
            if 'notion' in file_path.lower() and 'spatial' in file_path.lower():
                notion_spatial_files.append(file_path)
    
    notion_info = {
        'files': len(notion_spatial_files),
        'pattern': 'consolidated' if len(notion_spatial_files) <= 3 else 'granular'
    }
    
    print(f"  Slack: {slack_info['files']} files ({slack_info['pattern']})")
    print(f"  Notion: {notion_info['files']} files ({notion_info['pattern']})")
    
    if notion_info['files'] < slack_info['files']:
        print("  📊 Notion uses consolidated architecture (fewer files)")
        comparison['architecture_style'] = 'notion_consolidated_vs_slack_granular'
    else:
        print("  📊 Notion uses similar granular architecture")
        comparison['architecture_style'] = 'both_granular'
    
    # Access pattern comparison
    print(f"\n🔗 ACCESS PATTERN COMPARISON:")
    
    # Test Notion access pattern
    try:
        from services.integrations.notion.notion_integration_router import NotionIntegrationRouter
        notion_router = NotionIntegrationRouter()
        
        has_get_spatial_adapter = hasattr(notion_router, 'get_spatial_adapter')
        spatial_methods = [m for m in dir(notion_router) if 'spatial' in m.lower()]
        
        if has_get_spatial_adapter:
            print("  Notion: Uses adapter pattern (like Slack)")
            comparison['access_patterns'] = 'both_use_adapter_pattern'
        elif spatial_methods:
            print("  Notion: Uses direct method pattern (different from Slack)")
            comparison['access_patterns'] = 'notion_direct_vs_slack_adapter'
        else:
            print("  Notion: Uses embedded pattern (integrated in router)")
            comparison['access_patterns'] = 'notion_embedded_vs_slack_adapter'
        
        print(f"  Slack: 9 spatial adapter methods + 3 router methods")
        print(f"  Notion: {len(spatial_methods)} spatial methods")
        
    except Exception as e:
        print(f"  ❌ Cannot determine Notion access pattern: {e}")
    
    # Functionality focus comparison
    print(f"\n🎯 FUNCTIONALITY FOCUS COMPARISON:")
    print("  Slack: Coordination, navigation, messaging spatial intelligence")
    print("  Notion: Knowledge management, semantic analysis, content spatial intelligence")
    
    comparison['functionality_focus'] = {
        'slack': 'coordination_messaging',
        'notion': 'knowledge_semantic'
    }
    
    return comparison

pattern_comparison = compare_notion_vs_slack_patterns()
```

### Task 5: Cross-Validation Preparation

Prepare validation data for Code agent comparison:

```python
# Cross-validation preparation for Notion
def prepare_notion_cross_validation():
    """Prepare validation data for Code agent comparison"""
    
    print("\n=== NOTION CROSS-VALIDATION PREPARATION ===")
    
    validation_data = {
        'router_functionality': {},
        'spatial_access': {},
        'feature_flags': {},
        'knowledge_integration': {},
        'pattern_comparison': {}
    }
    
    # Router functionality validation
    try:
        from services.integrations.notion.notion_integration_router import NotionIntegrationRouter
        router = NotionIntegrationRouter()
        
        validation_data['router_functionality'] = {
            'instantiates': True,
            'type': type(router).__name__,
            'methods_count': len([m for m in dir(router) if not m.startswith('_')])
        }
    except Exception as e:
        validation_data['router_functionality'] = {'error': str(e)}
    
    # Spatial access validation
    import os
    os.environ['USE_SPATIAL_NOTION'] = 'true'
    
    try:
        router = NotionIntegrationRouter()
        
        spatial_data = {
            'has_get_spatial_adapter': hasattr(router, 'get_spatial_adapter'),
            'spatial_methods_count': len([m for m in dir(router) if 'spatial' in m.lower()]),
            'adapter_available': False,
            'adapter_type': None
        }
        
        if hasattr(router, 'get_spatial_adapter'):
            adapter = router.get_spatial_adapter()
            spatial_data['adapter_available'] = adapter is not None
            spatial_data['adapter_type'] = type(adapter).__name__ if adapter else None
        
        validation_data['spatial_access'] = spatial_data
        
    except Exception as e:
        validation_data['spatial_access'] = {'error': str(e)}
    
    # Feature flag validation summary
    validation_data['feature_flags'] = notion_flag_results
    
    # Knowledge integration summary
    validation_data['knowledge_integration'] = {
        'integration_tests': knowledge_integration_results,
        'total_tests_run': len(knowledge_integration_results),
        'passed_tests': len([r for r in knowledge_integration_results if r[1] is True])
    }
    
    # Pattern comparison summary
    validation_data['pattern_comparison'] = pattern_comparison
    
    print("📋 Notion validation data prepared for Code agent comparison:")
    for category, data in validation_data.items():
        print(f"  {category}: {len(data) if isinstance(data, dict) else 'N/A'} items")
    
    return validation_data

notion_cross_validation_data = prepare_notion_cross_validation()
```

## GitHub Evidence Update

```bash
# Update GitHub with Notion testing results
gh issue comment 194 --body "## Phase 2: Cursor Notion Spatial Testing Complete

### Router Functionality Testing ✅
- NotionIntegrationRouter instantiation: [PASS/FAIL]
- Spatial access pattern: [ADAPTER/DIRECT/EMBEDDED]
- Knowledge management methods: [X available / Y tested]

### Feature Flag Validation ✅  
- USE_SPATIAL_NOTION=true: [behavior confirmed]
- USE_SPATIAL_NOTION=false: [behavior confirmed]
- Default behavior: [behavior confirmed]
- Flag control: [WORKING/ISSUES]

### Knowledge Integration Testing ✅
- Configuration capabilities: [working/issues]
- Workspace access: [X methods available]
- Knowledge methods: [X/Y available]
- Spatial integration: [pattern description]

### Pattern Comparison ✅
- Architecture style: [consolidated/granular vs Slack]
- Access pattern: [adapter/direct/embedded vs Slack]
- Functionality focus: [knowledge/semantic vs coordination]

### Cross-Validation Ready ✅
- Router functionality data: [prepared]
- Spatial access data: [prepared]
- Feature flag data: [prepared]
- Knowledge integration data: [prepared]
- Pattern comparison data: [prepared]

**Status**: Notion spatial testing [COMPLETE/ISSUES_FOUND]
**Ready for Code comparison**: YES"
```

## Success Criteria

Phase 2 testing complete when:
- [✅] NotionIntegrationRouter spatial functionality tested
- [✅] USE_SPATIAL_NOTION flag behavior validated
- [✅] Knowledge management integration tested
- [✅] Notion vs Slack pattern comparison completed
- [✅] Cross-validation data prepared
- [✅] GitHub issue updated with test results

## STOP Conditions

Stop and escalate if:
- NotionIntegrationRouter fundamentally broken
- No spatial capabilities found at all
- Knowledge management completely inaccessible
- Feature flags not working
- Cannot instantiate basic components

---

**Your Mission**: Validate Notion spatial system for knowledge management and prepare comprehensive comparison with Slack spatial patterns.

**Quality Standard**: Complete testing of Notion spatial capabilities with evidence - ready for Code agent cross-validation.

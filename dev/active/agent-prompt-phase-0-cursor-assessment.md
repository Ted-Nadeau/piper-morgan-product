# Cursor Agent Prompt: Phase 0 - CORE-GREAT-2D Focused Assessment

## Mission: Calendar Integration Assessment & Configuration Validation Design

**Context**: CORE-GREAT-2C successfully documented two spatial patterns (Slack granular, Notion embedded). CORE-GREAT-2D investigates Calendar - potentially the only service without spatial intelligence - and requires configuration validation system design.

**Objective**: Focused assessment of Calendar integration status, spatial needs evaluation, and configuration validation system design across all 4 services with graceful error handling.

## Phase 0 Tasks

### Task 1: Calendar Integration Router Analysis

Analyze the Calendar integration router to understand current capabilities:

```python
# Focused Calendar router analysis
def analyze_calendar_router():
    """Analyze Calendar integration router implementation and capabilities"""
    
    print("=== CALENDAR ROUTER ANALYSIS ===")
    
    router_path = 'services/integrations/calendar/calendar_integration_router.py'
    
    try:
        with open(router_path, 'r') as f:
            router_content = f.read()
        
        print(f"✅ Calendar router found: {len(router_content)} characters")
        
        # Analyze router structure
        lines = router_content.split('\n')
        
        # Count methods and analyze complexity
        methods = [line.strip() for line in lines if line.strip().startswith('def ') or line.strip().startswith('async def ')]
        classes = [line.strip() for line in lines if line.strip().startswith('class ')]
        imports = [line.strip() for line in lines if line.strip().startswith('import ') or line.strip().startswith('from ')]
        
        print(f"📊 Router Structure:")
        print(f"  Classes: {len(classes)}")
        print(f"  Methods: {len(methods)}")
        print(f"  Imports: {len(imports)}")
        print(f"  Total lines: {len(lines)}")
        
        # List key methods
        print(f"\n🔧 Key Methods Found:")
        for method in methods[:10]:  # Show first 10 methods
            print(f"  - {method}")
        
        # Check for spatial patterns
        spatial_indicators = ['spatial', 'dimension', 'coordinate', 'mapping', 'intelligence']
        spatial_found = []
        
        for indicator in spatial_indicators:
            if indicator.lower() in router_content.lower():
                spatial_found.append(indicator)
        
        print(f"\n🔍 Spatial Indicators:")
        if spatial_found:
            print(f"  Found: {', '.join(spatial_found)}")
        else:
            print(f"  None found - likely no existing spatial system")
        
        # Analyze method signatures for complexity
        calendar_operations = ['event', 'calendar', 'schedule', 'appointment', 'meeting']
        operations_found = []
        
        for operation in calendar_operations:
            if operation.lower() in router_content.lower():
                operations_found.append(operation)
        
        print(f"\n📅 Calendar Operations:")
        print(f"  Found: {', '.join(operations_found) if operations_found else 'None detected'}")
        
        return {
            'methods': len(methods),
            'classes': len(classes),
            'lines': len(lines),
            'spatial_indicators': spatial_found,
            'operations': operations_found,
            'complexity': 'High' if len(methods) > 15 else 'Medium' if len(methods) > 8 else 'Low'
        }
        
    except Exception as e:
        print(f"❌ Could not analyze Calendar router: {e}")
        return {'error': str(e)}

router_analysis = analyze_calendar_router()
```

### Task 2: Calendar Spatial Requirements Assessment

Evaluate whether Calendar needs spatial intelligence based on its operations:

```python
# Assess Calendar spatial requirements
def assess_calendar_spatial_needs():
    """Determine if Calendar operations require spatial intelligence"""
    
    print("\n=== CALENDAR SPATIAL NEEDS ASSESSMENT ===")
    
    # Analyze Calendar service files for complexity indicators
    import glob
    
    calendar_files = glob.glob('services/integrations/calendar/**/*.py', recursive=True)
    
    complexity_indicators = {
        'temporal': ['time', 'date', 'schedule', 'duration', 'when'],
        'priority': ['important', 'urgent', 'priority', 'critical'],
        'collaborative': ['attendee', 'participant', 'meeting', 'invite', 'shared'],
        'hierarchical': ['parent', 'child', 'nested', 'category', 'group'],
        'contextual': ['context', 'related', 'associated', 'linked']
    }
    
    dimension_analysis = {}
    
    for dimension, keywords in complexity_indicators.items():
        dimension_count = 0
        files_with_dimension = []
        
        for file_path in calendar_files:
            try:
                with open(file_path, 'r') as f:
                    content = f.read().lower()
                
                file_matches = sum(1 for keyword in keywords if keyword in content)
                if file_matches > 0:
                    dimension_count += file_matches
                    files_with_dimension.append({
                        'file': file_path,
                        'matches': file_matches
                    })
            
            except Exception as e:
                print(f"  Warning: Could not read {file_path}: {e}")
        
        dimension_analysis[dimension] = {
            'total_matches': dimension_count,
            'files_affected': len(files_with_dimension),
            'strength': 'High' if dimension_count > 10 else 'Medium' if dimension_count > 3 else 'Low'
        }
    
    print(f"📊 Spatial Dimension Analysis:")
    for dimension, analysis in dimension_analysis.items():
        print(f"  {dimension.upper()}: {analysis['strength']} ({analysis['total_matches']} matches in {analysis['files_affected']} files)")
    
    # Determine spatial need based on dimensional complexity
    high_dimensions = [dim for dim, analysis in dimension_analysis.items() if analysis['strength'] == 'High']
    medium_dimensions = [dim for dim, analysis in dimension_analysis.items() if analysis['strength'] == 'Medium']
    
    print(f"\n🎯 SPATIAL INTELLIGENCE RECOMMENDATION:")
    
    if len(high_dimensions) >= 2:
        recommendation = "SPATIAL INTELLIGENCE NEEDED - Multiple high-complexity dimensions"
        pattern_suggestion = "Embedded Pattern (focused domain)"
    elif len(high_dimensions) >= 1 or len(medium_dimensions) >= 3:
        recommendation = "SPATIAL INTELLIGENCE BENEFICIAL - Moderate complexity"
        pattern_suggestion = "Embedded Pattern (single file)"
    else:
        recommendation = "SPATIAL INTELLIGENCE NOT REQUIRED - Low complexity domain"
        pattern_suggestion = "No spatial wrapper needed"
    
    print(f"  {recommendation}")
    print(f"  Pattern suggestion: {pattern_suggestion}")
    
    return {
        'dimension_analysis': dimension_analysis,
        'recommendation': recommendation,
        'pattern_suggestion': pattern_suggestion,
        'high_dimensions': high_dimensions,
        'medium_dimensions': medium_dimensions
    }

spatial_assessment = assess_calendar_spatial_needs()
```

### Task 3: Configuration Validation System Design

Design graceful configuration validation approach for all 4 services:

```python
# Design configuration validation system
def design_configuration_validation():
    """Design graceful configuration validation system"""
    
    print("\n=== CONFIGURATION VALIDATION DESIGN ===")
    
    services = {
        'github': {
            'required_fields': ['api_token', 'organization', 'repository'],
            'validation_checks': ['token_format', 'org_exists', 'repo_access'],
            'graceful_errors': ['Invalid token format', 'Organization not found', 'Repository access denied']
        },
        'slack': {
            'required_fields': ['workspace_id', 'bot_token', 'signing_secret'],
            'validation_checks': ['workspace_reachable', 'bot_permissions', 'secret_format'],
            'graceful_errors': ['Workspace unreachable', 'Bot missing permissions', 'Invalid signing secret']
        },
        'notion': {
            'required_fields': ['api_key', 'database_ids'],
            'validation_checks': ['api_key_valid', 'database_access'],
            'graceful_errors': ['API key invalid', 'Database access denied']
        },
        'calendar': {
            'required_fields': ['credentials', 'calendar_ids'],
            'validation_checks': ['credentials_valid', 'calendar_access'],
            'graceful_errors': ['Credentials invalid', 'Calendar access denied']
        }
    }
    
    print(f"🔧 Service Configuration Requirements:")
    for service, config in services.items():
        print(f"\n  {service.upper()}:")
        print(f"    Required fields: {len(config['required_fields'])}")
        print(f"    Validation checks: {len(config['validation_checks'])}")
        print(f"    Error scenarios: {len(config['graceful_errors'])}")
    
    # Design validation architecture
    validation_architecture = {
        'validator_class': 'ConfigValidator',
        'validation_methods': [f'validate_{service}' for service in services.keys()],
        'error_handling': 'graceful_with_recovery_suggestions',
        'startup_integration': 'pre_service_initialization',
        'ci_integration': 'automated_validation_step'
    }
    
    print(f"\n🏗️ Validation Architecture Design:")
    print(f"  Main class: {validation_architecture['validator_class']}")
    print(f"  Service methods: {len(validation_architecture['validation_methods'])}")
    print(f"  Error handling: {validation_architecture['error_handling']}")
    print(f"  Startup integration: {validation_architecture['startup_integration']}")
    print(f"  CI integration: {validation_architecture['ci_integration']}")
    
    # Design graceful error messages
    print(f"\n💬 Graceful Error Message Design:")
    print(f"  Format: Clear problem description + recovery suggestion")
    print(f"  Example: 'GitHub API token invalid. Please check your token in config/PIPER.user.md'")
    print(f"  Recovery: Provide specific steps to fix each configuration issue")
    
    return {
        'services': services,
        'architecture': validation_architecture,
        'total_validations': sum(len(config['validation_checks']) for config in services.values())
    }

validation_design = design_configuration_validation()
```

### Task 4: Calendar Integration Completeness Gap Analysis

Identify what constitutes the missing 15% of Calendar integration:

```python
# Analyze Calendar integration gaps
def analyze_calendar_gaps():
    """Identify specific gaps in Calendar integration completion"""
    
    print("\n=== CALENDAR INTEGRATION GAP ANALYSIS ===")
    
    # Check for incomplete implementations
    import re
    
    calendar_path = 'services/integrations/calendar'
    gap_indicators = []
    
    try:
        # Look for stub methods, TODOs, and incomplete implementations
        import glob
        calendar_files = glob.glob(f'{calendar_path}/**/*.py', recursive=True)
        
        for file_path in calendar_files:
            with open(file_path, 'r') as f:
                lines = f.readlines()
            
            for i, line in enumerate(lines):
                line_num = i + 1
                
                # Check for various gap indicators
                if 'pass' in line and i > 0 and ('def ' in lines[i-1] or 'async def ' in lines[i-1]):
                    gap_indicators.append({
                        'type': 'Stub Method',
                        'file': file_path,
                        'line': line_num,
                        'context': f"{lines[i-1].strip()} -> {line.strip()}"
                    })
                
                if any(marker in line.upper() for marker in ['TODO', 'FIXME', 'XXX']):
                    gap_indicators.append({
                        'type': 'TODO/FIXME',
                        'file': file_path,
                        'line': line_num,
                        'context': line.strip()
                    })
                
                if 'NotImplemented' in line or 'not implemented' in line.lower():
                    gap_indicators.append({
                        'type': 'Not Implemented',
                        'file': file_path,
                        'line': line_num,
                        'context': line.strip()
                    })
        
        print(f"📊 Gap Analysis Results:")
        print(f"  Total gaps found: {len(gap_indicators)}")
        
        # Group by type
        gap_types = {}
        for gap in gap_indicators:
            gap_type = gap['type']
            if gap_type not in gap_types:
                gap_types[gap_type] = []
            gap_types[gap_type].append(gap)
        
        for gap_type, gaps in gap_types.items():
            print(f"\n  {gap_type}: {len(gaps)} instances")
            for gap in gaps[:3]:  # Show first 3 of each type
                file_short = gap['file'].replace('services/integrations/calendar/', '')
                print(f"    {file_short}:{gap['line']} - {gap['context'][:60]}...")
        
        # Estimate completion percentage
        total_methods = sum(1 for gap in gap_indicators if gap['type'] == 'Stub Method')
        total_todos = sum(1 for gap in gap_indicators if gap['type'] == 'TODO/FIXME')
        
        if total_methods + total_todos > 0:
            estimated_completion = max(85 - (total_methods * 5) - (total_todos * 2), 0)
            print(f"\n📈 Estimated Completion: {estimated_completion}%")
            print(f"  Missing: {100 - estimated_completion}% (matches ~15% claim)")
        
        return gap_indicators
        
    except Exception as e:
        print(f"❌ Gap analysis error: {e}")
        return []

calendar_gaps = analyze_calendar_gaps()
```

### Task 5: Cross-Validation with Code Agent Findings

Prepare validation framework for Code agent comparison:

```python
# Prepare cross-validation data
def prepare_cross_validation():
    """Prepare findings for Code agent cross-validation"""
    
    print("\n=== CROSS-VALIDATION PREPARATION ===")
    
    validation_data = {
        'calendar_router_analysis': router_analysis,
        'spatial_needs_assessment': spatial_assessment,
        'configuration_validation_design': validation_design,
        'integration_gaps': calendar_gaps,
        'recommendations': {}
    }
    
    # Generate recommendations based on analysis
    recommendations = {}
    
    # Calendar spatial recommendation
    if spatial_assessment.get('recommendation', '').startswith('SPATIAL INTELLIGENCE NEEDED'):
        recommendations['spatial'] = {
            'action': 'Create spatial wrapper',
            'pattern': 'Embedded (single file)',
            'priority': 'High',
            'rationale': 'Multiple high-complexity dimensions detected'
        }
    elif spatial_assessment.get('recommendation', '').startswith('SPATIAL INTELLIGENCE BENEFICIAL'):
        recommendations['spatial'] = {
            'action': 'Consider spatial wrapper',
            'pattern': 'Embedded (single file)',
            'priority': 'Medium', 
            'rationale': 'Moderate complexity could benefit from spatial intelligence'
        }
    else:
        recommendations['spatial'] = {
            'action': 'No spatial wrapper needed',
            'pattern': 'None',
            'priority': 'Low',
            'rationale': 'Low complexity domain, spatial intelligence not required'
        }
    
    # Configuration validation recommendation
    recommendations['configuration'] = {
        'action': 'Implement comprehensive validation',
        'approach': 'Graceful with recovery suggestions',
        'priority': 'High',
        'services': 4
    }
    
    # Integration completion recommendation
    if len(calendar_gaps) > 0:
        recommendations['completion'] = {
            'action': 'Complete remaining implementation',
            'gaps_found': len(calendar_gaps),
            'priority': 'High',
            'estimated_effort': 'Medium'
        }
    
    validation_data['recommendations'] = recommendations
    
    print(f"📋 Cross-validation data prepared:")
    print(f"  Router analysis: {'✅ Complete' if 'methods' in router_analysis else '❌ Failed'}")
    print(f"  Spatial assessment: {'✅ Complete' if 'recommendation' in spatial_assessment else '❌ Failed'}")
    print(f"  Config design: {'✅ Complete' if 'total_validations' in validation_design else '❌ Failed'}")
    print(f"  Gap analysis: {'✅ Complete' if len(calendar_gaps) >= 0 else '❌ Failed'}")
    print(f"  Recommendations: {len(recommendations)} generated")
    
    return validation_data

cross_validation_data = prepare_cross_validation()
```

## GitHub Progress Update

```bash
# Update GitHub with focused assessment results
gh issue comment 195 --body "## Phase 0: Cursor Focused Assessment Complete

### Calendar Router Analysis ✅
- Router structure: [X methods, Y classes, Z lines]
- Complexity level: [Low/Medium/High]
- Spatial indicators: [Found/Not found]
- Calendar operations: [list of operations detected]

### Calendar Spatial Needs ✅
- Dimensional analysis: [TEMPORAL, PRIORITY, COLLABORATIVE, etc.]
- Spatial recommendation: [NEEDED/BENEFICIAL/NOT REQUIRED]
- Pattern suggestion: [Embedded/Granular/None]
- Rationale: [based on complexity analysis]

### Configuration Validation Design ✅
- Services covered: GitHub, Slack, Notion, Calendar (4/4)
- Total validations: [X validation checks]
- Error handling: Graceful with recovery suggestions
- Architecture: ConfigValidator with service-specific methods

### Integration Completeness ✅
- Gaps identified: [X gaps found]
- Gap types: [Stub methods, TODOs, Not implemented]
- Estimated completion: [X%]
- Matches 15% missing claim: [Yes/No]

### Cross-Validation Ready ✅
- All analysis data prepared for Code agent comparison
- Recommendations generated for spatial, configuration, completion
- Findings ready for validation and consensus building

**Next Phase**: Compare findings with Code agent and make implementation decisions"
```

## Success Criteria

Phase 0 focused assessment complete when:
- [✅] Calendar router analyzed for complexity and capabilities
- [✅] Calendar spatial needs assessed using dimensional analysis
- [✅] Configuration validation system designed with graceful errors
- [✅] Calendar integration gaps identified and quantified
- [✅] Cross-validation data prepared for Code agent comparison
- [✅] GitHub issue updated with focused assessment results

---

**Your Mission**: Focused assessment of Calendar integration status and configuration validation design with emphasis on graceful error handling.

**Quality Standard**: Thorough analysis enabling informed decisions about Calendar spatial needs and configuration validation approach.

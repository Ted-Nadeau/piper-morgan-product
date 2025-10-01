# Claude Code Prompt: Phase 0 - CORE-GREAT-2D Investigation

## Mission: Calendar Spatial Discovery & GitHub Setup

**Context**: CORE-GREAT-2C successfully verified two spatial patterns (Slack granular, Notion embedded). CORE-GREAT-2D investigates Calendar integration - potentially the only service WITHOUT spatial intelligence - plus configuration validation needs.

**Objective**: Comprehensive investigation of Calendar spatial system status, complete GitHub setup, and assess configuration validation requirements across all 4 services.

## Phase 0 Tasks

### Task 1: GitHub Issue Verification & Setup

```bash
# Verify CORE-GREAT-2D issue exists and details
gh issue view 195

# Update issue with investigation start
gh issue comment 195 --body "## Phase 0: Investigation Started

### Calendar Spatial Discovery
- [ ] Current Calendar structure analyzed  
- [ ] Spatial system search completed
- [ ] Pattern decision framework applied
- [ ] 15% completion gap identified

### Configuration Validation Assessment
- [ ] All 4 services configuration needs documented
- [ ] Current validation state analyzed
- [ ] TBD-API-01 relationship determined
- [ ] Graceful error handling approach designed

**Investigation Phase**: Beginning comprehensive analysis..."
```

### Task 2: Calendar Integration Deep Dive

Perform comprehensive analysis of Calendar integration current state:

```python
# Comprehensive Calendar investigation
def investigate_calendar_integration():
    """Deep dive into Calendar integration status and spatial needs"""
    
    print("=== CALENDAR INTEGRATION INVESTIGATION ===")
    
    # Analyze directory structure
    import os
    calendar_base = 'services/integrations/calendar'
    
    print(f"📁 Calendar Directory Structure:")
    for root, dirs, files in os.walk(calendar_base):
        level = root.replace(calendar_base, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    lines = len(f.readlines())
                print(f"{subindent}{file} ({lines} lines)")
    
    # Search for spatial patterns
    print(f"\n🔍 SPATIAL PATTERN SEARCH:")
    
    # Look for explicit spatial files
    import glob
    spatial_files = glob.glob(f"{calendar_base}/**/spatial*.py", recursive=True)
    print(f"  Explicit spatial files: {len(spatial_files)}")
    for file in spatial_files:
        print(f"    - {file}")
    
    # Search for spatial keywords in Calendar files
    spatial_keywords = [
        'spatial', 'dimension', 'coordinate', 'position', 'mapping',
        'territory', 'context', 'intelligence', 'analyzer'
    ]
    
    calendar_files = glob.glob(f"{calendar_base}/**/*.py", recursive=True)
    spatial_references = {}
    
    for file_path in calendar_files:
        try:
            with open(file_path, 'r') as f:
                content = f.read().lower()
                file_matches = []
                for keyword in spatial_keywords:
                    if keyword in content:
                        # Count occurrences and get context
                        lines = content.split('\n')
                        for i, line in enumerate(lines):
                            if keyword in line:
                                file_matches.append({
                                    'keyword': keyword,
                                    'line_num': i + 1,
                                    'context': line.strip()
                                })
                
                if file_matches:
                    spatial_references[file_path] = file_matches
        except Exception as e:
            print(f"    Error reading {file_path}: {e}")
    
    print(f"  Files with spatial references: {len(spatial_references)}")
    for file_path, matches in spatial_references.items():
        print(f"    {file_path}:")
        for match in matches[:3]:  # Show first 3 matches
            print(f"      Line {match['line_num']}: {match['context'][:60]}...")
    
    return spatial_references

spatial_analysis = investigate_calendar_integration()
```

### Task 3: Calendar Integration Completeness Analysis

Identify the missing 15% of Calendar integration:

```python
# Analyze Calendar integration completeness
def analyze_calendar_completeness():
    """Identify what constitutes the missing 15% of Calendar integration"""
    
    print("\n=== CALENDAR COMPLETION ANALYSIS ===")
    
    # Look for TODO, FIXME, NotImplemented patterns
    import glob
    import re
    
    calendar_files = glob.glob('services/integrations/calendar/**/*.py', recursive=True)
    incomplete_patterns = []
    
    for file_path in calendar_files:
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
                
            for i, line in enumerate(lines):
                # Look for completion markers
                if any(marker in line.upper() for marker in ['TODO', 'FIXME', 'XXX', 'HACK']):
                    incomplete_patterns.append({
                        'file': file_path,
                        'line': i + 1,
                        'content': line.strip(),
                        'type': 'TODO/FIXME'
                    })
                
                # Look for NotImplemented
                if 'NotImplemented' in line or 'not implemented' in line.lower():
                    incomplete_patterns.append({
                        'file': file_path,
                        'line': i + 1,
                        'content': line.strip(),
                        'type': 'NotImplemented'
                    })
                
                # Look for pass statements in methods (potential stubs)
                if re.match(r'\s+pass\s*$', line) and i > 0:
                    # Check if previous line was a method definition
                    prev_line = lines[i-1].strip()
                    if prev_line.endswith(':') and ('def ' in prev_line or 'async def ' in prev_line):
                        incomplete_patterns.append({
                            'file': file_path,
                            'line': i + 1,
                            'content': f"{prev_line} -> {line.strip()}",
                            'type': 'Stub Method'
                        })
        
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
    
    print(f"📊 Incomplete Patterns Found: {len(incomplete_patterns)}")
    
    # Group by type
    by_type = {}
    for pattern in incomplete_patterns:
        pattern_type = pattern['type']
        if pattern_type not in by_type:
            by_type[pattern_type] = []
        by_type[pattern_type].append(pattern)
    
    for pattern_type, patterns in by_type.items():
        print(f"\n  {pattern_type}: {len(patterns)} instances")
        for pattern in patterns[:5]:  # Show first 5
            print(f"    {pattern['file']}:{pattern['line']} - {pattern['content'][:80]}...")
    
    return incomplete_patterns

completeness_analysis = analyze_calendar_completeness()
```

### Task 4: ADR-038 Spatial Pattern Decision Framework

Read and apply the spatial pattern decision framework we created:

```python
# Apply ADR-038 decision framework to Calendar
def apply_spatial_decision_framework():
    """Use ADR-038 to determine Calendar spatial pattern needs"""
    
    print("\n=== ADR-038 SPATIAL PATTERN DECISION ===")
    
    # Read ADR-038 for decision criteria
    try:
        with open('docs/internal/architecture/current/adrs/adr-038-spatial-intelligence-patterns.md', 'r') as f:
            adr_content = f.read()
        
        print("✅ ADR-038 located and read")
        
        # Extract decision criteria from ADR
        if "Pattern Selection Criteria" in adr_content:
            print("📋 ADR-038 Pattern Selection Criteria found")
        
        if "When To Use" in adr_content:
            print("🎯 ADR-038 Usage Guidelines found")
        
    except Exception as e:
        print(f"⚠️ Could not read ADR-038: {e}")
        print("Will proceed with basic decision framework")
    
    # Analyze Calendar characteristics for pattern decision
    print(f"\n🔍 CALENDAR CHARACTERISTICS ANALYSIS:")
    
    # Check Calendar integration router
    try:
        with open('services/integrations/calendar/calendar_integration_router.py', 'r') as f:
            router_content = f.read()
        
        characteristics = {
            'complexity': 'Unknown',
            'use_case': 'Unknown',
            'requirements': [],
            'file_count': len(glob.glob('services/integrations/calendar/**/*.py', recursive=True))
        }
        
        # Analyze router complexity
        if 'class CalendarIntegrationRouter' in router_content:
            lines = router_content.split('\n')
            method_count = len([line for line in lines if 'def ' in line])
            characteristics['method_count'] = method_count
            
            if method_count < 10:
                characteristics['complexity'] = 'Simple to Moderate'
            else:
                characteristics['complexity'] = 'High'
        
        # Determine use case based on methods and imports
        if 'event' in router_content.lower():
            characteristics['use_case'] = 'Event Management'
        if 'schedule' in router_content.lower():
            characteristics['use_case'] = 'Scheduling'
        if 'calendar' in router_content.lower():
            characteristics['use_case'] = 'Calendar Operations'
        
        print(f"  File count: {characteristics['file_count']}")
        print(f"  Complexity: {characteristics['complexity']}")
        print(f"  Use case: {characteristics['use_case']}")
        
        # Apply decision framework
        print(f"\n📝 PATTERN RECOMMENDATION:")
        
        if characteristics['file_count'] < 5 and characteristics['complexity'] == 'Simple to Moderate':
            recommendation = "Embedded Pattern (like Notion)"
            print(f"  ✅ {recommendation}")
            print(f"     Reason: Simple domain, focused functionality")
        elif characteristics['file_count'] > 10 or characteristics['complexity'] == 'High':
            recommendation = "Granular Adapter Pattern (like Slack)"
            print(f"  ✅ {recommendation}")
            print(f"     Reason: Complex domain, multiple concerns")
        else:
            recommendation = "Further Analysis Needed"
            print(f"  ⚠️ {recommendation}")
            print(f"     Reason: Characteristics unclear, need deeper investigation")
        
        return characteristics, recommendation
        
    except Exception as e:
        print(f"⚠️ Could not analyze Calendar router: {e}")
        return {}, "Analysis Failed"

calendar_characteristics, pattern_recommendation = apply_spatial_decision_framework()
```

### Task 5: Configuration Validation Assessment

Assess current configuration state across all 4 services:

```python
# Assess configuration validation needs
def assess_configuration_validation():
    """Analyze current configuration state and validation needs"""
    
    print("\n=== CONFIGURATION VALIDATION ASSESSMENT ===")
    
    services = ['github', 'slack', 'notion', 'calendar']
    config_analysis = {}
    
    # Check main configuration
    try:
        with open('config/PIPER.user.md', 'r') as f:
            config_content = f.read()
        print("✅ Main config file found: config/PIPER.user.md")
    except Exception as e:
        print(f"⚠️ Main config file issue: {e}")
        config_content = ""
    
    # Analyze each service's configuration needs
    for service in services:
        print(f"\n🔧 {service.upper()} Configuration Analysis:")
        
        service_path = f'services/integrations/{service}'
        try:
            # Look for config-related code
            service_files = glob.glob(f'{service_path}/**/*.py', recursive=True)
            config_references = []
            
            for file_path in service_files:
                with open(file_path, 'r') as f:
                    content = f.read()
                    
                # Look for config patterns
                config_patterns = ['config', 'token', 'api_key', 'secret', 'credential']
                for pattern in config_patterns:
                    if pattern in content.lower():
                        config_references.append({
                            'file': file_path,
                            'pattern': pattern,
                            'count': content.lower().count(pattern)
                        })
            
            print(f"  Files with config references: {len(set(ref['file'] for ref in config_references))}")
            
            # Check for existing validation
            validation_exists = any('valid' in content.lower() for file_path in service_files 
                                  for content in [open(file_path, 'r').read()])
            
            config_analysis[service] = {
                'config_references': len(config_references),
                'validation_exists': validation_exists,
                'files_checked': len(service_files)
            }
            
            print(f"  Existing validation: {'✅ Yes' if validation_exists else '❌ No'}")
            
        except Exception as e:
            print(f"  ❌ Error analyzing {service}: {e}")
            config_analysis[service] = {'error': str(e)}
    
    # Look for TBD-API-01
    print(f"\n🔍 TBD-API-01 Search:")
    try:
        import subprocess
        result = subprocess.run(['grep', '-r', 'TBD-API-01', '.'], 
                              capture_output=True, text=True, cwd='.')
        if result.stdout:
            print("✅ TBD-API-01 found:")
            for line in result.stdout.split('\n')[:5]:
                if line.strip():
                    print(f"  {line}")
        else:
            print("❌ TBD-API-01 not found")
    except Exception as e:
        print(f"⚠️ Search error: {e}")
    
    return config_analysis

config_assessment = assess_configuration_validation()
```

## GitHub Progress Update

```bash
# Update GitHub with Phase 0 findings
gh issue comment 195 --body "## Phase 0: Investigation Complete

### Calendar Spatial Analysis ✅
- Directory structure: [X files analyzed]
- Spatial pattern search: [results]
- ADR-038 decision framework applied
- Pattern recommendation: [recommendation]

### Calendar Integration Status ✅
- Completeness analysis: [X incomplete patterns found]
- Missing 15% identified: [specific gaps]
- Implementation readiness: [assessment]

### Configuration Validation ✅
- All 4 services analyzed: GitHub, Slack, Notion, Calendar
- Current validation state: [summary]
- TBD-API-01 status: [found/not found]
- Graceful error requirements: [documented]

**Next Phase**: Calendar spatial decision and implementation planning
**Evidence**: Complete analysis in session log with recommendations"
```

## Success Criteria

Phase 0 complete when:
- [✅] Calendar spatial system status determined (exists/missing/not applicable)
- [✅] Calendar integration 15% gap identified with specifics
- [✅] ADR-038 pattern decision framework applied
- [✅] Configuration validation needs documented for all 4 services
- [✅] TBD-API-01 relationship to configuration determined
- [✅] GitHub issue updated with investigation findings

---

**Your Mission**: Thorough investigation of Calendar spatial status and configuration validation needs across all services.

**Quality Standard**: Time Lord thoroughness - complete understanding before implementation decisions.

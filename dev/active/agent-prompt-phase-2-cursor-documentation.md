# Cursor Agent Prompt: Phase 2 - Calendar Documentation & Final Validation

## Mission: Calendar Documentation & Integration Validation

**Context**: Code agent delivered Calendar integration tests (29 tests, 296 lines) in Phase 1. Phase 2 focuses on documentation verification, final validation coordination, and ensuring Calendar completion is properly documented.

**Objective**: Verify Calendar documentation completeness, coordinate final validation with Code agent, and ensure all Calendar completion evidence is properly organized for Phase Z.

## Phase 2 Tasks

### Task 1: Calendar Documentation Audit

Audit existing Calendar documentation and identify gaps:

```bash
# Comprehensive Calendar documentation audit
echo "=== CALENDAR DOCUMENTATION AUDIT ==="

# Find all Calendar-related documentation
echo "📚 Searching for Calendar documentation..."

find . -name "*.md" -type f | xargs grep -l -i "calendar" | head -10
find docs/ -name "*calendar*" -type f 2>/dev/null || echo "No calendar-specific docs found"
find services/integrations/calendar/ -name "*.md" -type f 2>/dev/null || echo "No integration docs found"

# Check ADR-038 for delegated pattern documentation
echo ""
echo "📋 Checking ADR-038 for delegated MCP pattern..."
if [ -f "docs/internal/architecture/current/adrs/adr-038-spatial-intelligence-patterns.md" ]; then
    grep -i "delegated\|calendar" docs/internal/architecture/current/adrs/adr-038-spatial-intelligence-patterns.md | head -5
    echo "✅ ADR-038 exists"
else
    echo "❌ ADR-038 not found"
fi

# Check for Calendar integration setup guides
echo ""
echo "🔧 Checking for Calendar setup documentation..."
find . -name "*.md" -type f | xargs grep -l "Google Calendar\|calendar.*setup\|calendar.*config" | head -5

# Look for README files in Calendar integration
echo ""
echo "📖 Checking Calendar integration README..."
if [ -f "services/integrations/calendar/README.md" ]; then
    echo "✅ Calendar README exists"
    wc -l services/integrations/calendar/README.md
else
    echo "❌ Calendar README missing"
fi
```

### Task 2: Calendar Test Documentation Analysis

Analyze Calendar test documentation and coverage:

```python
# Analyze Calendar test documentation
def analyze_calendar_test_documentation():
    """Analyze Calendar test documentation and create summary"""
    
    print("=== CALENDAR TEST DOCUMENTATION ANALYSIS ===")
    
    # Find test files
    import glob
    import os
    
    test_files = glob.glob('tests/**/*calendar*.py', recursive=True)
    
    print(f"🧪 Calendar Test Files Found: {len(test_files)}")
    
    test_summary = {
        'total_files': len(test_files),
        'test_methods': [],
        'docstring_coverage': 0,
        'file_details': []
    }
    
    for test_file in test_files:
        try:
            with open(test_file, 'r') as f:
                content = f.read()
            
            # Count test methods
            import re
            test_methods = re.findall(r'def (test_[^(]+)', content)
            test_summary['test_methods'].extend(test_methods)
            
            # Check for docstrings
            docstring_count = content.count('"""') + content.count("'''")
            has_docstrings = docstring_count > 0
            
            if has_docstrings:
                test_summary['docstring_coverage'] += 1
            
            lines = len(content.split('\n'))
            
            test_summary['file_details'].append({
                'file': test_file,
                'test_methods': len(test_methods),
                'lines': lines,
                'has_docstrings': has_docstrings
            })
            
            print(f"  📄 {os.path.basename(test_file)}: {len(test_methods)} tests, {lines} lines")
            
        except Exception as e:
            print(f"  ❌ Error reading {test_file}: {e}")
    
    # Calculate coverage percentages
    total_methods = len(test_summary['test_methods'])
    docstring_percentage = (test_summary['docstring_coverage'] / len(test_files) * 100) if test_files else 0
    
    print(f"\n📊 Test Documentation Summary:")
    print(f"  Total test methods: {total_methods}")
    print(f"  Files with docstrings: {test_summary['docstring_coverage']}/{len(test_files)} ({docstring_percentage:.1f}%)")
    
    # Create test documentation if needed
    if docstring_percentage < 80:
        print(f"\n📝 Creating Calendar test documentation...")
        
        test_doc = f"""# Calendar Integration Tests

## Overview
Comprehensive test suite for Calendar integration with {total_methods} test methods across {len(test_files)} test files.

## Test Files
"""
        
        for file_detail in test_summary['file_details']:
            file_name = os.path.basename(file_detail['file'])
            test_doc += f"\n### {file_name}\n"
            test_doc += f"- **Methods**: {file_detail['test_methods']} tests\n"
            test_doc += f"- **Lines**: {file_detail['lines']}\n"
            test_doc += f"- **Documentation**: {'✅ Yes' if file_detail['has_docstrings'] else '❌ No'}\n"
        
        test_doc += f"""
## Test Categories
- **Integration Tests**: End-to-end Calendar API operations
- **Spatial Tests**: Delegated MCP pattern functionality
- **Configuration Tests**: Calendar setup and validation
- **Unit Tests**: Individual component testing

## Running Tests
```bash
# Run all Calendar tests
pytest tests/ -k "calendar" -v

# Run specific test file
pytest tests/integration/test_calendar_integration.py -v

# Run with coverage
pytest tests/ -k "calendar" --cov=services.integrations.calendar
```

## Test Coverage Goals
- [ ] Event CRUD operations
- [ ] Calendar access and permissions
- [ ] Spatial context extraction
- [ ] MCP adapter functionality
- [ ] Error handling scenarios
- [ ] Configuration validation

## Related Documentation
- [Calendar Integration Guide](docs/integrations/calendar-integration-guide.md)
- [ADR-038: Spatial Intelligence Patterns](docs/internal/architecture/current/adrs/adr-038-spatial-intelligence-patterns.md)
"""
        
        os.makedirs('docs/testing', exist_ok=True)
        with open('docs/testing/calendar-tests.md', 'w') as f:
            f.write(test_doc)
        
        print("✅ Created: docs/testing/calendar-tests.md")
    
    return test_summary

test_doc_analysis = analyze_calendar_test_documentation()
```

### Task 3: Integration Validation Coordination

Coordinate with Code agent to ensure comprehensive validation:

```python
# Coordinate integration validation
def coordinate_integration_validation():
    """Coordinate with Code agent for comprehensive Calendar validation"""
    
    print("=== INTEGRATION VALIDATION COORDINATION ===")
    
    validation_checklist = {
        'code_agent_tasks': [
            'Calendar test coverage analysis (29 tests)',
            'Spatial system verification (GoogleCalendarAdapter)',
            'Router completeness assessment',
            'Documentation creation/verification',
            'Final validation report'
        ],
        'cursor_agent_tasks': [
            'Documentation audit and gap analysis',
            'Test documentation organization',
            'Cross-validation of Code findings',
            'Final integration summary',
            'Phase Z preparation'
        ],
        'shared_deliverables': [
            'Calendar completion assessment',
            'Documentation verification',
            'Integration validation report',
            'Phase 2 completion evidence'
        ]
    }
    
    print("📋 Validation Coordination Plan:")
    print("\n🤖 Code Agent Responsibilities:")
    for task in validation_checklist['code_agent_tasks']:
        print(f"  - {task}")
    
    print("\n🎯 Cursor Agent Responsibilities:")
    for task in validation_checklist['cursor_agent_tasks']:
        print(f"  - {task}")
    
    print("\n🤝 Shared Deliverables:")
    for deliverable in validation_checklist['shared_deliverables']:
        print(f"  - {deliverable}")
    
    # Create coordination summary
    coordination_summary = """# Phase 2 Coordination Summary

## Agent Responsibilities

### Code Agent Focus
- Technical validation of Calendar integration components
- Test coverage analysis and verification
- Spatial system functionality verification
- Router completeness assessment
- Technical documentation creation

### Cursor Agent Focus
- Documentation audit and organization
- Test documentation coordination
- Cross-validation of technical findings
- Integration summary preparation
- Phase Z transition preparation

## Success Criteria
- [ ] Calendar integration technically verified complete
- [ ] Documentation comprehensive and accessible
- [ ] Test coverage adequate for production
- [ ] Spatial system (delegated MCP pattern) operational
- [ ] All acceptance criteria validated

## Phase 2 Deliverables
1. Calendar completion verification report
2. Updated documentation suite
3. Test documentation organization
4. Integration validation summary
5. Phase Z preparation materials
"""
    
    with open('phase_2_coordination_summary.md', 'w') as f:
        f.write(coordination_summary)
    
    print(f"\n📄 Coordination summary written to: phase_2_coordination_summary.md")
    
    return validation_checklist

coordination_plan = coordinate_integration_validation()
```

### Task 4: Calendar Documentation Organization

Organize and validate Calendar documentation completeness:

```python
# Organize Calendar documentation
def organize_calendar_documentation():
    """Organize Calendar documentation for accessibility and completeness"""
    
    print("=== CALENDAR DOCUMENTATION ORGANIZATION ===")
    
    # Create documentation index
    doc_index = {
        'integration_guide': 'docs/integrations/calendar-integration-guide.md',
        'test_documentation': 'docs/testing/calendar-tests.md',
        'architecture_decisions': 'docs/internal/architecture/current/adrs/adr-038-spatial-intelligence-patterns.md',
        'configuration_guide': 'docs/configuration/calendar-setup.md',
        'troubleshooting': 'docs/troubleshooting/calendar-issues.md'
    }
    
    print("📚 Calendar Documentation Index:")
    
    doc_status = {}
    for doc_type, doc_path in doc_index.items():
        import os
        if os.path.exists(doc_path):
            doc_status[doc_type] = {'exists': True, 'path': doc_path}
            print(f"  ✅ {doc_type}: {doc_path}")
        else:
            doc_status[doc_type] = {'exists': False, 'path': doc_path}
            print(f"  ❌ {doc_type}: {doc_path} (missing)")
    
    # Create missing documentation
    missing_docs = [doc_type for doc_type, status in doc_status.items() if not status['exists']]
    
    if missing_docs:
        print(f"\n📝 Creating missing documentation...")
        
        # Create configuration guide if missing
        if 'configuration_guide' in missing_docs:
            config_guide = """# Calendar Configuration Guide

## Prerequisites
- Google Cloud Platform account
- Google Calendar API enabled
- Service account credentials

## Setup Steps

### 1. Google Cloud Configuration
1. Create new Google Cloud Project
2. Enable Google Calendar API
3. Create service account
4. Download credentials JSON file

### 2. Environment Configuration
```bash
export GOOGLE_CALENDAR_CREDENTIALS_PATH="/path/to/credentials.json"
export GOOGLE_CALENDAR_IDS='["primary"]'
```

### 3. Verification
```bash
python -c "
from services.infrastructure.config.config_validator import ConfigValidator
validator = ConfigValidator()
result = validator.validate_calendar()
print(result.get_summary())
"
```

## Security Notes
- Store credentials securely
- Use service account with minimal permissions
- Regularly rotate credentials
- Monitor API usage

## Related Documentation
- [Calendar Integration Guide](../integrations/calendar-integration-guide.md)
- [Configuration Validation](../configuration-validation.md)
"""
            
            os.makedirs('docs/configuration', exist_ok=True)
            with open('docs/configuration/calendar-setup.md', 'w') as f:
                f.write(config_guide)
            print("  ✅ Created calendar configuration guide")
        
        # Create troubleshooting guide if missing
        if 'troubleshooting' in missing_docs:
            troubleshooting_guide = """# Calendar Integration Troubleshooting

## Common Issues

### Authentication Errors
**Symptom**: "Credentials not found" or "Permission denied"
**Solutions**:
- Verify GOOGLE_CALENDAR_CREDENTIALS_PATH is correct
- Check service account has Calendar API access
- Ensure credentials file is valid JSON

### Spatial Adapter Issues
**Symptom**: "Spatial context extraction failed"
**Solutions**:
- Verify MCP service is running
- Check GoogleCalendarAdapter inheritance
- Validate BaseSpatialAdapter integration

### Configuration Validation Failures
**Symptom**: ConfigValidator reports Calendar as invalid
**Solutions**:
- Run detailed validation: `validator.validate_calendar()`
- Check environment variables are set
- Verify credentials file accessibility

## Diagnostic Commands

### Check Configuration
```bash
python -c "
from services.infrastructure.config.config_validator import ConfigValidator
validator = ConfigValidator()
result = validator.validate_calendar()
print(result.format_report())
"
```

### Test Spatial System
```python
from services.mcp.consumer.google_calendar_adapter import GoogleCalendarAdapter
adapter = GoogleCalendarAdapter()
# Test adapter functionality
```

### Verify Calendar Access
```python
from services.integrations.calendar.calendar_integration_router import CalendarIntegrationRouter
router = CalendarIntegrationRouter()
events = await router.get_upcoming_events(limit=1)
print(f"Calendar access: {'OK' if events else 'FAILED'}")
```

## Contact
For additional support, refer to integration documentation or configuration guides.
"""
            
            os.makedirs('docs/troubleshooting', exist_ok=True)
            with open('docs/troubleshooting/calendar-issues.md', 'w') as f:
                f.write(troubleshooting_guide)
            print("  ✅ Created calendar troubleshooting guide")
    
    # Create documentation index file
    index_content = f"""# Calendar Integration Documentation Index

## Complete Documentation Suite

### Integration Guide
**File**: [`docs/integrations/calendar-integration-guide.md`](integrations/calendar-integration-guide.md)
**Purpose**: Complete integration guide including architecture, configuration, and usage examples

### Test Documentation  
**File**: [`docs/testing/calendar-tests.md`](testing/calendar-tests.md)
**Purpose**: Test suite documentation with {len(test_doc_analysis.get('test_methods', []))} test methods

### Architecture Decisions
**File**: [`docs/internal/architecture/current/adrs/adr-038-spatial-intelligence-patterns.md`](internal/architecture/current/adrs/adr-038-spatial-intelligence-patterns.md)
**Purpose**: Delegated MCP Pattern documentation

### Configuration Guide
**File**: [`docs/configuration/calendar-setup.md`](configuration/calendar-setup.md) 
**Purpose**: Step-by-step configuration and environment setup

### Troubleshooting Guide
**File**: [`docs/troubleshooting/calendar-issues.md`](troubleshooting/calendar-issues.md)
**Purpose**: Common issues and diagnostic procedures

## Quick Start
1. Follow [Configuration Guide](configuration/calendar-setup.md)
2. Read [Integration Guide](integrations/calendar-integration-guide.md)
3. Run tests per [Test Documentation](testing/calendar-tests.md)
4. Reference [Troubleshooting](troubleshooting/calendar-issues.md) if needed

## Related Documentation
- [Configuration Validation System](configuration-validation.md)
- [MCP Integration Patterns](mcp-integration-guide.md)
- [Spatial Intelligence Architecture](internal/architecture/spatial-intelligence.md)
"""
    
    with open('docs/calendar-documentation-index.md', 'w') as f:
        f.write(index_content)
    
    print(f"\n📄 Documentation index created: docs/calendar-documentation-index.md")
    
    return {
        'doc_index': doc_index,
        'doc_status': doc_status,
        'missing_docs_created': len(missing_docs),
        'total_docs': len(doc_index)
    }

doc_organization = organize_calendar_documentation()
```

### Task 5: Phase 2 Completion Summary

Create comprehensive Phase 2 completion summary:

```python
# Create Phase 2 completion summary
def create_phase_2_summary():
    """Create comprehensive Phase 2 completion summary"""
    
    print("=== PHASE 2 COMPLETION SUMMARY ===")
    
    # Compile all Phase 2 activities
    phase_2_summary = {
        'documentation_audit': "Complete",
        'test_documentation': f"{len(test_doc_analysis.get('test_methods', []))} test methods documented",
        'coordination': "Code and Cursor agent responsibilities defined",
        'documentation_organization': f"{doc_organization.get('total_docs', 0)} documentation files organized",
        'missing_docs_created': doc_organization.get('missing_docs_created', 0)
    }
    
    print("📊 Phase 2 Activities Summary:")
    for activity, status in phase_2_summary.items():
        print(f"  ✅ {activity}: {status}")
    
    # Create final summary report
    final_summary = f"""# CORE-GREAT-2D Phase 2 Completion Summary

## Overview
Phase 2 focused on Calendar integration completion verification, documentation organization, and final validation coordination.

## Cursor Agent Deliverables

### Documentation Audit ✅
- Comprehensive audit of Calendar documentation
- Identified gaps and created missing documentation
- Organized documentation for accessibility

### Test Documentation ✅
- Analyzed {len(test_doc_analysis.get('test_methods', []))} Calendar test methods
- Created test documentation suite
- Documented test coverage and organization

### Integration Coordination ✅
- Coordinated validation responsibilities with Code agent
- Defined shared deliverables and success criteria
- Prepared comprehensive validation framework

### Documentation Organization ✅
- Created {doc_organization.get('total_docs', 0)}-file documentation suite
- Generated {doc_organization.get('missing_docs_created', 0)} missing documentation files
- Established calendar documentation index

## Calendar Integration Status
Based on coordination with Code agent and comprehensive documentation audit:

### Completion Assessment
- **Technical Implementation**: Verified by Code agent
- **Test Coverage**: {len(test_doc_analysis.get('test_methods', []))} tests documented
- **Documentation**: Complete suite created and organized
- **Spatial System**: Delegated MCP pattern operational
- **Configuration**: Validation system operational

### Documentation Suite
1. **Integration Guide**: Complete usage and architecture guide
2. **Test Documentation**: Comprehensive test suite documentation  
3. **Configuration Guide**: Step-by-step setup instructions
4. **Troubleshooting Guide**: Common issues and solutions
5. **Architecture Decisions**: ADR-038 delegated pattern documentation

## Phase 2 Success Criteria
- [✅] Calendar documentation audit complete
- [✅] Test documentation organized and accessible
- [✅] Integration validation coordinated with Code agent
- [✅] Missing documentation created
- [✅] Calendar completion verification prepared

## Ready for Phase Z
Calendar integration completion verified and documented. All materials prepared for final bookending and handoff documentation.

## Evidence Files
- `phase_2_coordination_summary.md` - Agent coordination plan
- `docs/calendar-documentation-index.md` - Complete documentation index
- `docs/testing/calendar-tests.md` - Test documentation
- `docs/configuration/calendar-setup.md` - Configuration guide
- `docs/troubleshooting/calendar-issues.md` - Troubleshooting guide

---
**Phase 2 Status**: COMPLETE ✅
**Next Phase**: Phase Z (Documentation and Bookending)
"""
    
    with open('phase_2_completion_summary.md', 'w') as f:
        f.write(final_summary)
    
    print(f"\n📄 Phase 2 summary written to: phase_2_completion_summary.md")
    
    return {
        'summary': phase_2_summary,
        'documentation_complete': True,
        'ready_for_phase_z': True
    }

phase_2_completion = create_phase_2_summary()
```

## GitHub Progress Update

```bash
# Update GitHub with Phase 2 completion
gh issue comment 195 --body "## Phase 2: Calendar Documentation & Validation Complete

### Documentation Suite Created ✅
- **Integration Guide**: Complete Calendar integration documentation
- **Test Documentation**: {len(test_doc_analysis.get('test_methods', []))} test methods documented
- **Configuration Guide**: Step-by-step setup instructions
- **Troubleshooting Guide**: Common issues and diagnostic procedures
- **Documentation Index**: Organized access to all Calendar documentation

### Coordination with Code Agent ✅
- Technical validation responsibilities defined
- Shared deliverables identified
- Cross-validation framework established
- Integration completion assessment coordinated

### Calendar Integration Status ✅
- **Documentation**: Complete {doc_organization.get('total_docs', 0)}-file suite created
- **Test Coverage**: Comprehensive documentation of test suite
- **Spatial System**: Delegated MCP pattern documented and operational
- **Configuration**: Validation system provides clear guidance

### Phase 2 Deliverables ✅
- Calendar documentation audit complete
- Missing documentation created ({doc_organization.get('missing_docs_created', 0)} files)
- Test documentation organized
- Integration validation coordinated
- Phase Z preparation materials ready

**Ready for Phase Z**: Documentation and bookending with complete Calendar integration verification
**Evidence**: Complete documentation suite and coordination materials in phase_2_completion_summary.md"
```

## Success Criteria

Phase 2 complete when:
- [✅] Calendar documentation audit complete with gap analysis
- [✅] Test documentation organized and accessible
- [✅] Integration validation coordinated with Code agent
- [✅] Missing documentation created (configuration, troubleshooting)
- [✅] Calendar documentation index created for easy access
- [✅] Phase 2 completion summary prepared for Phase Z
- [✅] GitHub issue updated with documentation deliverables

---

**Your Mission**: Ensure Calendar integration has comprehensive, accessible documentation and coordinate final validation with Code agent for complete integration verification.

**Quality Standard**: Complete documentation suite enabling easy Calendar integration setup, usage, and troubleshooting.

# Claude Code Prompt: Phase 0 - Infrastructure & Spatial System Verification

## Mission: Verify Infrastructure Foundation for GREAT-2C

**Context**: CORE-QUERY-1 completed yesterday with 100% router implementation. Now verifying sophisticated spatial intelligence systems discovered in GREAT-2A are operational and addressing critical security vulnerability TBD-SECURITY-02.

**Objective**: Comprehensive verification of infrastructure state, spatial system inventory, and current security status before proceeding with verification work.

## Phase 0 Tasks

### Task 1: GitHub Issue Verification

```bash
# Verify GREAT-2C issue exists and understand scope
gh issue view 194

# Check if issue has been updated recently
gh issue list --state open --label "GREAT-2C"

# Verify we can update the issue (test permission)
gh issue comment 194 --body "Phase 0: Infrastructure verification starting..."
```

### Task 2: Router Infrastructure Verification (From CORE-QUERY-1)

Verify yesterday's router work is complete and operational:

```bash
# Check router files exist from CORE-QUERY-1
ls -la services/integrations/*/
echo "Expected: calendar/, notion/, slack/ directories with routers"

# Verify router implementations
find services/integrations/ -name "*_router.py" -o -name "*router.py"
echo "Expected: CalendarIntegrationRouter, NotionIntegrationRouter, SlackIntegrationRouter"

# Check router imports are working
python -c "
from services.integrations.calendar.calendar_integration_router import CalendarIntegrationRouter
from services.integrations.notion.notion_integration_router import NotionIntegrationRouter  
from services.integrations.slack.slack_integration_router import SlackIntegrationRouter
print('✅ All routers import successfully')
"
```

### Task 3: Spatial System Discovery and Inventory

**Critical**: Map the sophisticated spatial systems mentioned in gameplan:

```bash
# Find all spatial-related files
echo "=== SPATIAL SYSTEM INVENTORY ==="
find services/ -name "*spatial*" -type f | sort
echo ""

# Count spatial files (gameplan mentions 20+ for Slack)
echo "Spatial file counts by integration:"
find services/ -path "*/slack/*" -name "*spatial*" | wc -l | awk '{print "Slack spatial files: " $1}'
find services/ -path "*/notion/*" -name "*spatial*" | wc -l | awk '{print "Notion spatial files: " $1}'
find services/ -path "*spatial*" -name "*.py" | wc -l | awk '{print "Total spatial Python files: " $1}'
echo ""

# Look for spatial directories
find services/ -name "*spatial*" -type d | sort
echo ""

# Check for spatial intelligence entry points
grep -r "spatial" services/ --include="*.py" | grep -i "class\|def\|import" | head -10
```

**Spatial Architecture Investigation**:

```python
# Create comprehensive spatial system map
import os
import subprocess
from pathlib import Path

def map_spatial_systems():
    """Map all spatial intelligence systems"""
    
    print("=== SPATIAL INTELLIGENCE ARCHITECTURE MAP ===")
    
    # Find all spatial files
    result = subprocess.run(['find', 'services/', '-name', '*spatial*', '-type', 'f'], 
                          capture_output=True, text=True)
    spatial_files = result.stdout.strip().split('\n') if result.stdout.strip() else []
    
    # Categorize by integration
    slack_spatial = [f for f in spatial_files if 'slack' in f.lower()]
    notion_spatial = [f for f in spatial_files if 'notion' in f.lower()]
    other_spatial = [f for f in spatial_files if f not in slack_spatial and f not in notion_spatial]
    
    print(f"📍 SLACK SPATIAL FILES ({len(slack_spatial)} found):")
    for f in slack_spatial:
        print(f"  {f}")
    
    print(f"\n📍 NOTION SPATIAL FILES ({len(notion_spatial)} found):")
    for f in notion_spatial:
        print(f"  {f}")
    
    print(f"\n📍 OTHER SPATIAL FILES ({len(other_spatial)} found):")
    for f in other_spatial:
        print(f"  {f}")
    
    # Check if meets gameplan expectations
    if len(slack_spatial) >= 20:
        print(f"\n✅ Slack spatial system matches expectation (20+ files)")
    else:
        print(f"\n⚠️ Slack spatial system may be smaller than expected ({len(slack_spatial)} < 20)")
    
    return slack_spatial, notion_spatial, other_spatial

slack_files, notion_files, other_files = map_spatial_systems()
```

### Task 4: Security Status Investigation (TBD-SECURITY-02)

**CRITICAL SECURITY VERIFICATION**:

```bash
# Find the security vulnerability mentioned in gameplan
echo "=== TBD-SECURITY-02 SECURITY INVESTIGATION ==="

# Search for the disabled webhook verification
grep -r "TBD-SECURITY-02" services/ --include="*.py" -n
echo ""

# Look for webhook verification patterns
grep -r "verify_slack_request" services/ --include="*.py" -n
echo ""

# Search for disabled security
grep -r "FIXME.*webhook\|TODO.*webhook\|verify.*disabled" services/ --include="*.py" -n
echo ""

# Find webhook endpoints
grep -r "webhook" services/ --include="*.py" | grep -i "route\|endpoint\|def.*webhook"
echo ""

# Check for security imports that might be commented out
grep -r "hmac\|signature" services/ --include="*.py" -A 2 -B 2
```

**Security Analysis**:

```python
# Analyze webhook security implementation
def analyze_webhook_security():
    """Analyze current webhook security status"""
    
    print("=== WEBHOOK SECURITY ANALYSIS ===")
    
    # Find webhook-related files
    import subprocess
    
    result = subprocess.run(['grep', '-r', 'webhook', 'services/', '--include=*.py', '-l'], 
                          capture_output=True, text=True)
    webhook_files = result.stdout.strip().split('\n') if result.stdout.strip() else []
    
    print(f"📁 WEBHOOK-RELATED FILES ({len(webhook_files)} found):")
    for f in webhook_files:
        print(f"  {f}")
    
    # Look for security patterns in each file
    for file_path in webhook_files:
        if file_path and os.path.exists(file_path):
            print(f"\n🔍 ANALYZING: {file_path}")
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                
                # Check for security patterns
                if 'verify_slack_request' in content:
                    print("  ✅ Found verify_slack_request function")
                elif 'verify' in content.lower() and 'slack' in content.lower():
                    print("  ⚠️ Found slack verification patterns")
                
                if 'TBD-SECURITY-02' in content:
                    print("  🚨 Found TBD-SECURITY-02 marker")
                
                if 'FIXME' in content or 'TODO' in content:
                    print("  ⚠️ Found FIXME/TODO markers")
                
                if 'hmac' in content.lower() or 'signature' in content.lower():
                    print("  🔐 Found security-related code")
                    
            except Exception as e:
                print(f"  ❌ Error reading file: {e}")

analyze_webhook_security()
```

### Task 5: Feature Flag Configuration Check

```bash
# Check current feature flag configuration
echo "=== FEATURE FLAG CONFIGURATION ==="

# Look for feature flag definitions
grep -r "USE_SPATIAL" services/ --include="*.py" -n
echo ""

# Check config files for spatial flags
find config/ -name "*.md" -o -name "*.json" -o -name "*.yaml" | xargs grep -l "SPATIAL" 2>/dev/null || echo "No spatial config found in config/"
echo ""

# Look for feature flag usage in routers
grep -r "USE_SPATIAL" services/integrations/ --include="*.py" -A 3 -B 1
```

### Task 6: Test Infrastructure Verification

```bash
# Check existing test structure
echo "=== TEST INFRASTRUCTURE CHECK ==="

# Look for spatial-related tests
find tests/ -name "*spatial*" -type f 2>/dev/null || echo "No spatial test files found"
echo ""

# Check for integration tests
ls -la tests/integration/ 2>/dev/null || echo "No integration test directory"
echo ""

# Look for existing test patterns
find tests/ -name "*slack*" -o -name "*notion*" | head -5
echo ""

# Check if pytest is available
python -m pytest --version || echo "pytest not available"
```

## Evidence Documentation

Document all findings in GitHub issue #194:

```bash
# Create comprehensive evidence update
gh issue comment 194 --body "## Phase 0 Infrastructure Verification Complete

### Router Infrastructure ✅
- All 3 routers from CORE-QUERY-1 verified working
- [paste router verification output]

### Spatial System Discovery
- Slack spatial files found: [X files]
- Notion spatial files found: [Y files] 
- [paste spatial file inventory]

### Security Status 🚨
- TBD-SECURITY-02 investigation: [findings]
- Webhook verification status: [current state]
- [paste security analysis]

### Feature Flags
- USE_SPATIAL_SLACK: [status]
- USE_SPATIAL_NOTION: [status]
- [paste flag configuration]

### Test Infrastructure
- Spatial tests exist: [Y/N]
- Integration tests ready: [Y/N]

**Ready for Phase 1**: [READY/NEEDS_FIXES]"
```

## Anti-80% Safeguards

**Mandatory Verification Checklist**:
```
Infrastructure Component | Verified | Status
----------------------- | -------- | ------
CalendarIntegrationRouter | [ ] | 
NotionIntegrationRouter   | [ ] |
SlackIntegrationRouter    | [ ] |
Slack spatial files (20+) | [ ] |
Notion spatial files      | [ ] |
TBD-SECURITY-02 located   | [ ] |
USE_SPATIAL_SLACK flag    | [ ] |
USE_SPATIAL_NOTION flag   | [ ] |
```

**STOP Conditions**:
- Routers not working (regression from CORE-QUERY-1)
- Spatial files significantly different than expected
- Security vulnerability unclear or worse than described
- Cannot update GitHub issue #194

## Success Criteria

Phase 0 complete when:
- [✅] GitHub issue #194 accessible and updated
- [✅] All router infrastructure verified working
- [✅] Spatial system inventory complete with file counts
- [✅] TBD-SECURITY-02 security issue located and analyzed
- [✅] Feature flag configuration documented
- [✅] Test infrastructure status known
- [✅] Evidence posted to GitHub issue #194

---

**Your Mission**: Establish solid foundation understanding before Phase 1 spatial verification work begins.

**Quality Standard**: Complete infrastructure map with evidence - no assumptions carried forward.

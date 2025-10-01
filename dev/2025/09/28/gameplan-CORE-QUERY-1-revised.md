# Gameplan: CORE-QUERY-1 - Complete Integration Router Infrastructure

**Date**: September 28, 2025
**Issue**: #199
**Epic**: Enables GREAT-2C through 2E
**Architect**: Claude Opus 4.1
**Lead Developer**: [To be assigned]

---

## Critical Update from GREAT-2B

**GitHub Router is NOW COMPLETE** (17/14 methods - 121%)
The issue description is outdated. GREAT-2B completed GitHub router last night.
This gameplan focuses on the remaining three routers.

---

## Strategic Context: The Cathedral

You're completing the routing infrastructure that enables spatial intelligence (8-dimensional analysis) across all integrations. GREAT-2B proved the pattern works for GitHub. Now extend to Slack, Notion, and Calendar.

### Pattern from GREAT-2B
1. Routers incomplete → services bypass them
2. Complete router → replace imports → feature flag control
3. Systematic verification prevents false completion
4. "100% means 100%" for foundational infrastructure

---

## Phase -1: Infrastructure Reality Check (30 min)

### Deploy: Lead Developer Direct Investigation

Before deploying agents, verify actual router state:

```bash
# Check if routers exist at all
ls -la services/integrations/slack/*router* 2>/dev/null || echo "No Slack router found"
ls -la services/integrations/notion/*router* 2>/dev/null || echo "No Notion router found"
ls -la services/integrations/calendar/*router* 2>/dev/null || echo "No Calendar router found"

# Check actual integration structure
ls -la services/integrations/

# Verify spatial systems mentioned in GREAT-2A
ls -la services/integrations/slack/spatial*.py 2>/dev/null
ls -la services/integrations/notion/*mcp* 2>/dev/null
ls -la services/integrations/calendar/*mcp* 2>/dev/null
```

**STOP if reality differs significantly from expectations**

---

## Phase 0: Comprehensive Router Audit (2 hours)

### Deploy: Both Agents - Evidence-Based Discovery

#### 0A. Audit Slack Integration
**Code Agent Task**:
```markdown
Investigate Slack integration architecture:

1. Find the main Slack client/agent:
   - Look in services/integrations/slack/
   - Count all public methods
   - Document method signatures

2. Check for existing router:
   - Look for slack_integration_router.py or similar
   - If exists, count implemented methods
   - Calculate completeness percentage

3. Identify bypassing services:
   - grep for "from.*slack.*import" across services/
   - List all services using direct imports
   - Note which methods they actually use

4. Verify spatial system (GREAT-2A found 20+ files):
   - List all spatial_*.py files
   - Check if they're actually used
```

**Cursor Agent Task**:
```markdown
Verify Code's findings and check edge cases:
- Are there multiple Slack clients?
- Any deprecated patterns still in use?
- Check tests for expected behavior
```

#### 0B. Audit Notion Integration
[Similar structure for Notion]

#### 0C. Audit Calendar Integration
[Similar structure for Calendar]

#### 0D. Create Audit Report
```markdown
# Router Completeness Audit Report

## Slack
- Client location: [path]
- Client methods: [count]
- Router exists: [Y/N]
- Router methods: [count if exists]
- Completeness: [%]
- Bypassing services: [list with methods they use]
- Spatial system: [status from GREAT-2A findings]

[Similar for Notion and Calendar]

## Implementation Order Recommendation
Based on:
1. Number of bypassing services (impact)
2. Completeness percentage (effort)
3. Complexity of methods (risk)

Recommended order: [1, 2, 3]
```

### Cathedral Context for Agents
You're discovering the actual state of routing infrastructure. GREAT-2B found GitHub router was only 14% complete despite sophisticated design. Expect similar patterns. Document everything - assumptions kill projects.

---

## Phase 1: First Router Completion (3-4 hours)

*Order determined by Phase 0 audit*

### If Slack is First (likely based on 20+ spatial files)

#### Deploy: Code for Implementation, Cursor for Verification

**Code Agent Instructions**:
```markdown
Complete Slack Integration Router following GREAT-2B pattern:

1. Use GitHubIntegrationRouter as template
2. Every SlackClient method needs router equivalent
3. Delegation pattern:
   - Check USE_SPATIAL_SLACK flag
   - Route to spatial (20+ files) or legacy
   - Maintain signature compatibility

Critical: You found 17 methods in GitHub when expected 14.
Check for ALL Slack methods, not just obvious ones.
```

**Cursor Agent Instructions**:
```markdown
Verify Code's implementation:
1. Pattern compliance with GitHub router
2. All methods actually work
3. No signature mismatches
4. Feature flags properly checked

Remember GREAT-2B: 0% pattern compliance caught early saved hours
```

---

## Phase 2: Second Router Completion (3 hours)

*Similar structure, order from Phase 0*

---

## Phase 3: Third Router Completion (2-3 hours)

*Calendar likely simplest*

---

## Phase 4: Service Migration (2 hours)

### Deploy: Both Agents - Systematic Import Replacement

Based on Phase 0 findings, replace all direct imports:

```python
# Before
from services.integrations.slack.slack_client import SlackClient

# After
from services.integrations.slack.slack_integration_router import SlackIntegrationRouter
```

**Critical**: GREAT-2B found 6 services, not expected 5. Look thoroughly.

---

## Phase 5: Comprehensive Testing (2 hours)

### Deploy: Cursor Primary, Code for Fixes

#### 5A. Router Completeness Tests
```python
# For each integration
def test_[integration]_router_completeness():
    """Ensure router has all client methods"""
    # Pattern from GREAT-2B
```

#### 5B. Feature Flag Control
```bash
# Test each router with both modes
USE_SPATIAL_SLACK=true pytest tests/integrations/slack/
USE_SPATIAL_SLACK=false pytest tests/integrations/slack/
```

#### 5C. No Direct Imports Test
```python
def test_no_direct_client_imports():
    """Architecture protection"""
    # Pattern from GREAT-2B
```

---

## Phase 6: Lock & Document (1 hour)

### Deploy: Both Agents

1. Add to pre-commit hooks
2. Add to CI/CD
3. Document pattern for future integrations
4. Update architecture docs

---

## Phase Z: Validation & Handoff

### Evidence Requirements (from GREAT-2B methodology)

Each phase needs:
- Terminal output showing completion
- Test results with full output
- Before/after verification
- No "should work" - only "does work"

### Success Validation
```bash
# All routers complete
for integration in slack notion calendar; do
    python verify_${integration}_router_completeness.py
done

# No direct imports
python tests/architecture/test_no_direct_imports.py

# Feature flags work
./test_all_feature_flags.sh
```

---

## Success Criteria

Per GitHub issue #199:
- [ ] Slack router audit complete and all methods implemented
- [ ] Notion router audit complete and all methods implemented
- [ ] Calendar router audit complete and all methods implemented
- [ ] All routers have spatial/legacy or MCP/legacy delegation
- [ ] Feature flag control verified for all
- [ ] No direct imports remain
- [ ] Architecture tests prevent regression
- [ ] QueryRouter verified (might already work)

---

## STOP Conditions

From methodology:
- Infrastructure doesn't match assumptions
- Router >50% complete but unused (investigate why)
- Breaking changes to production
- Pattern doesn't fit integration

---

## Time Estimate

- Phase -1: 30 min (reality check)
- Phase 0: 2 hours (audit all)
- Phase 1-3: 9-10 hours (three routers)
- Phase 4: 2 hours (migrations)
- Phase 5: 2 hours (testing)
- Phase 6: 1 hour (lock)
- **Total: 16-17 hours**

---

## Critical Context for Lead Developer

### From GREAT-2B Success
1. **Cathedral Building**: Agents must understand they're enabling spatial intelligence architecture, not just implementing methods
2. **Systematic Verification**: Caught quality issues early, prevented technical debt
3. **100% means 100%**: No partial implementations for infrastructure
4. **Evidence Required**: Every claim needs proof

### Multi-Agent Deployment
- Default to BOTH Code and Cursor
- Different perspectives catch different issues
- Cross-validation prevents completion bias

### The 75% Pattern
Expect to find routers partially built but abandoned. Complete what exists, don't rebuild.

---

*Build the cathedral. Complete the routers. Enable the architecture.*

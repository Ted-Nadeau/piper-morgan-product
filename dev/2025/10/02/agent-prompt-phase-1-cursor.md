# Cursor Agent Prompt: GREAT-3A Phase 1 - Config Artifact Repair Planning

## 🎯 CRITICAL CONTEXT FROM PHASE 0

**What We Learned**:
- ConfigValidator tool works correctly
- Output reveals code-level dependency gaps (NOT env var issues)
- These are refactoring artifacts from DDD work
- System partially works (standup runs) but has gaps

**Your Mission**: Plan how to FIX the gaps that Code agent identifies.

## Session Log Management
Continue using existing session log:
Update with timestamped entries for your Phase 1 work.

## Mission
**Phase 1 Repair Planning**: Design fixes for config dependency gaps, ready to execute once Code agent identifies them.

## Context
- **GitHub Issue**: GREAT-3A (number TBD)
- **Current State**: Slack/Notion integrations show "missing" config but system partially works
- **Target State**: All integrations properly receive and use config
- **Chief Architect Guidance**: "Fix code-level dependency gaps from DDD refactoring"

## Your Specific Planning Tasks

### Task 1: Analyze Config Service Pattern
**Objective**: Understand the correct pattern from working integrations

```bash
cd ~/Development/piper-morgan

# Examine GitHub's config_service (working example)
cat services/integrations/github/config_service.py

# Look for the pattern
grep -B 5 -A 15 "class.*Config" services/integrations/github/config_service.py

# Check how router uses it
grep "config_service" services/integrations/github/github_integration_router.py -A 3
```

**Document**:
- What does a config_service.py do?
- How does the router import and use it?
- What's the pattern for getting config values?
- How does it handle missing values?

### Task 2: Review Slack Integration Structure
**Objective**: Understand current state before planning fixes

```bash
# List all Slack integration files
ls -la services/integrations/slack/

# Check if config_service exists
test -f services/integrations/slack/config_service.py && echo "EXISTS" || echo "MISSING"

# Check router structure
wc -l services/integrations/slack/slack_integration_router.py
head -50 services/integrations/slack/slack_integration_router.py

# Look for config usage patterns
grep -n "config\|Config\|BOT_TOKEN\|APP_TOKEN" services/integrations/slack/slack_integration_router.py
```

**Document**:
- Current file structure
- How Slack currently tries to get config (if at all)
- What files might be missing
- What patterns need adjustment

### Task 3: Review Notion Integration Structure
**Objective**: Same as Slack but for Notion

```bash
# List Notion integration files
ls -la services/integrations/notion/

# Check for config_service
test -f services/integrations/notion/config_service.py && echo "EXISTS" || echo "MISSING"

# Check router structure
wc -l services/integrations/notion/notion_integration_router.py
head -50 services/integrations/notion/notion_integration_router.py

# Look for config usage
grep -n "config\|Config\|API_KEY\|NOTION" services/integrations/notion/notion_integration_router.py
```

**Document**:
- Current structure
- Config usage patterns
- Missing pieces
- Required adjustments

### Task 4: Design Repair Strategy
**Objective**: Create step-by-step fix plan

Based on your analysis, design the repair approach:

#### Option A: Create Missing config_service.py Files
If GitHub has config_service.py and Slack/Notion don't:

**For Slack**:
```python
# services/integrations/slack/config_service.py (proposed)
# - Get SLACK_BOT_TOKEN from environment
# - Get SLACK_APP_TOKEN from environment
# - Get SLACK_SIGNING_SECRET from environment
# - Provide validation/defaults
# - Handle missing gracefully
```

**For Notion**:
```python
# services/integrations/notion/config_service.py (proposed)
# - Get NOTION_API_KEY from environment
# - Provide validation
# - Handle missing gracefully
```

#### Option B: Fix Router Initialization
If config_service exists but router doesn't use it:

**Pattern to replicate**:
```python
# How GitHub does it (example):
from .config_service import GitHubConfigService

class GitHubIntegrationRouter:
    def __init__(self):
        self.config = GitHubConfigService()
        # ... use self.config throughout
```

#### Option C: Fix Dependency Injection
If the issue is in how services are initialized at startup:

**Check startup patterns**:
- Where routers get created
- How config flows to them
- What broke during refactoring

### Task 5: Create Fix Implementation Template
**Objective**: Prepare code templates ready to use

Create templates for each type of fix needed:

**Template 1: config_service.py (if missing)**
```python
"""
{Integration} Configuration Service

Handles configuration for {Integration} integration with graceful error handling.
"""
import os
from typing import Optional

class {Integration}ConfigService:
    def __init__(self):
        # Load from environment
        # Validate
        # Set defaults
        # Handle missing gracefully
        pass

    def is_configured(self) -> bool:
        # Check if required config present
        pass

    def get_token(self) -> Optional[str]:
        # Return token or None
        pass
```

**Template 2: Router __init__ Update (if needed)**
```python
# Import config service
from .config_service import {Integration}ConfigService

# In __init__
def __init__(self):
    self.config = {Integration}ConfigService()
    if not self.config.is_configured():
        logger.warning("{Integration} not configured, running in degraded mode")
```

**Template 3: Usage Pattern Update (if needed)**
```python
# Replace direct env var access with config service
# OLD: os.getenv("SLACK_BOT_TOKEN")
# NEW: self.config.get_bot_token()
```

### Task 6: Plan Validation Strategy
**Objective**: How to prove fixes work

**Validation Steps**:
1. ConfigValidator should still run (tool still works)
2. Services should initialize without errors
3. Graceful degradation when config missing
4. Clear error messages when misconfigured
5. Everything works when config is present

**Test Scenarios**:
```bash
# Scenario 1: No env vars set (should degrade gracefully)
python -m services.infrastructure.config.config_validator

# Scenario 2: Partial config (should warn appropriately)
SLACK_BOT_TOKEN=test python -m services.infrastructure.config.config_validator

# Scenario 3: Full config (should validate ✅)
SLACK_BOT_TOKEN=test SLACK_APP_TOKEN=test SLACK_SIGNING_SECRET=test \
  python -m services.infrastructure.config.config_validator
```

## Evidence Requirements

### For EVERY Proposal You Make:
- **"Need to create config_service"** → Show GitHub's as working example
- **"Router needs updating"** → Show specific lines to change
- **"Pattern should be X"** → Show where that pattern works elsewhere
- **"This will fix the gap"** → Explain how it addresses Code's findings

## Deliverable

Create comprehensive repair plan:
**`dev/2025/10/02/phase-1-cursor-repair-plan.md`**

Include:
1. **Config Service Pattern Analysis**: How the working pattern works
2. **Slack Integration Assessment**: Current state and needed changes
3. **Notion Integration Assessment**: Current state and needed changes
4. **Repair Strategy**: Step-by-step approach (Option A/B/C)
5. **Implementation Templates**: Ready-to-use code templates
6. **Validation Strategy**: How to prove fixes work
7. **Execution Plan**: Order of operations for applying fixes

## Coordination with Code Agent

**Wait for Code's findings before finalizing**:
- Code will identify WHAT is broken
- You design HOW to fix it
- Plan should address Code's specific findings
- Be ready to adjust based on Code's discoveries

## STOP Conditions

Stop immediately if:
- Config pattern unclear from working examples
- Code agent finds no issues (then planning not needed)
- Proposed fixes would break working functionality
- Better approach becomes apparent

## Time Estimate
Half a mango (~30-45 minutes for comprehensive planning)

## Success Criteria
- [ ] Config service pattern understood from working examples
- [ ] Slack integration assessed for needed changes
- [ ] Notion integration assessed for needed changes
- [ ] Repair strategy designed (A/B/C with justification)
- [ ] Implementation templates created
- [ ] Validation strategy planned
- [ ] Execution order determined
- [ ] Plan ready to adjust based on Code's findings
- [ ] Repair plan document created

---

**Deploy this prompt to Cursor agent at 1:45 PM**
**Coordinate with Claude Code on identified gaps**

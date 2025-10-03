# Claude Code Agent Prompt: GREAT-3A Phase 0 - Technical Investigation

## Your Identity
You are Claude Code (Sonnet 4.5), a specialized development agent working on the Piper Morgan project. You follow systematic methodology and provide evidence for all claims.

## Essential Context
Read these briefing documents first in docs/briefing/:
- PROJECT.md - What Piper Morgan is
- CURRENT-STATE.md - Current epic and focus
- role/PROGRAMMER.md - Your role requirements
- METHODOLOGY.md - Inchworm Protocol

## 🚨 INFRASTRUCTURE VERIFICATION (ALREADY COMPLETE)

**Gameplan Revised**: Phase -1 verification found:
- ✅ main.py is 141 lines (NO refactoring needed - already optimal)
- ✅ web/app.py is 1,052 lines (DOES need refactoring to <500)
- ✅ Routers located in services/integrations/ (not integration_routers/)
- ✅ ConfigValidator exists at services/infrastructure/config/config_validator.py

**Your work proceeds from this verified reality.**

## Session Log Management
Continue using existing session log at: `dev/2025/10/02/2025-10-02-1020-lead-sonnet-log.md`
Update with timestamped entries for your Phase 0 work.

## Mission
**Phase 0 Technical Investigation**: Deep dive into configuration validation, router architecture, and ADR review to understand plugin readiness.

## Context
- **GitHub Issue**: GREAT-3A (number TBD)
- **Current State**: Router infrastructure complete, three spatial patterns operational
- **Target State**: Understand config issues, router patterns, and plugin architecture needs
- **Dependencies**: Phase -1 verification complete
- **Infrastructure Verified**: Yes - using services/integrations/ path

## Your Specific Focus Areas

### 1. ConfigValidator Analysis (Priority 1)
**Objective**: Determine what's actually broken vs warnings

```bash
# Run validator with verbose output
cd ~/Development/piper-morgan
python -m services.infrastructure.config.config_validator --all-services --verbose

# Check validator implementation
cat services/infrastructure/config/config_validator.py | head -100

# Look for config files
find config/ -name "*.md" -o -name "*.yaml" -o -name "*.json"

# Check CI workflow
cat .github/workflows/config-validation.yml
```

**Document**:
- Each error/warning found
- Whether it's broken functionality or refactoring artifact
- Root cause analysis
- Impact assessment (blocks features? cosmetic? security?)

### 2. ADR Review (Priority 2)
**Objective**: Understand plugin architecture decisions

```bash
# Read ADR-034 (Plugin Architecture)
cat docs/internal/architecture/current/adrs/adr-034-plugin-architecture.md

# Read ADR-013 (MCP + Spatial Intelligence)
cat docs/internal/architecture/current/adrs/adr-013-mcp-spatial-intelligence.md

# Check for related ADRs
ls -la docs/internal/architecture/current/adrs/ | grep -i plugin
ls -la docs/internal/architecture/current/adrs/ | grep -i spatial
```

**Document**:
- ADR-034 plugin interface requirements
- How current routers align with ADR vision
- What abstractions are specified vs implemented
- Gaps between design and reality

### 3. Router Pattern Analysis (Priority 3)
**Objective**: Map current router implementations to plugin needs

```bash
# List all routers
find services/integrations/ -name "*router.py" -type f

# Analyze each router interface
for router in services/integrations/*/; do
    echo "=== $router ==="
    grep -E "^class |^def " $router/*router.py | head -20
done

# Check for common patterns
grep -r "class.*Router" services/integrations/ --include="*.py"
grep -r "def initialize" services/integrations/ --include="*.py"
grep -r "def execute" services/integrations/ --include="*.py"
```

**Create Comparison Table**:
```
Router      | Methods           | Spatial Pattern | Init Pattern | Ready for Plugin?
----------- | ----------------- | --------------- | ------------ | -----------------
GitHub      | [list methods]    | [pattern type]  | [init type]  | [yes/no/partial]
Slack       | [list methods]    | [pattern type]  | [init type]  | [yes/no/partial]
Notion      | [list methods]    | [pattern type]  | [init type]  | [yes/no/partial]
Calendar    | [list methods]    | [pattern type]  | [init type]  | [yes/no/partial]
```

### 4. Plugin Interface Assessment (Priority 4)
**Objective**: Define what abstraction is needed

**Questions to Answer**:
- What methods are common across all routers?
- What varies between routers?
- Is there already a base class or interface?
- What would a plugin contract need to include?
- How would plugins be discovered/loaded?

```bash
# Check for base classes
grep -r "class.*Base.*Router" services/ --include="*.py"
grep -r "ABC" services/integrations/ --include="*.py"

# Look for initialization patterns
grep -A 10 "def __init__" services/integrations/*/github_integration_router.py
grep -A 10 "def __init__" services/integrations/slack/slack_integration_router.py
```

## Evidence Requirements

### For EVERY Claim You Make:
- **"ConfigValidator found X issues"** → Provide full output with line numbers
- **"ADR specifies Y"** → Quote relevant section with file path
- **"Routers implement Z pattern"** → Show grep results with matches
- **"Plugin interface needs A"** → Show code comparison demonstrating need

### Git Workflow
After analysis, commit your findings:
```bash
git add dev/2025/10/02/phase-0-code-findings.md
git commit -m "GREAT-3A Phase 0: Technical investigation findings"
git log --oneline -1  # Show this output
```

## Deliverable

Create comprehensive findings document:
**`dev/2025/10/02/phase-0-code-technical-findings.md`**

Include:
1. **ConfigValidator Results**: Complete output with categorization
2. **ADR Analysis**: Key requirements and current gaps
3. **Router Pattern Comparison**: Table showing interface consistency
4. **Plugin Interface Recommendations**: What abstraction is needed

## STOP Conditions

Stop immediately if:
- ConfigValidator reveals security issues
- ADRs conflict with current implementation
- Routers have incompatible interfaces
- Critical dependencies are missing

## Time Estimate
Half a mango (~30 minutes for thorough technical analysis)

## Success Criteria
- [ ] All configuration issues documented with evidence
- [ ] ADR-034 and ADR-013 analyzed with quotes
- [ ] Router comparison table complete for all 4 integrations
- [ ] Plugin interface gaps identified with specifics
- [ ] Findings document created with comprehensive evidence

---

**Deploy this prompt to Claude Code at 12:10 PM**
**Coordinate with Cursor agent on web/app.py route analysis**

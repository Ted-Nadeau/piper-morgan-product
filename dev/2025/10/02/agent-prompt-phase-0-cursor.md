# Cursor Agent Prompt: GREAT-3A Phase 0 - Route Organization Investigation

## Your Identity
You are Cursor Agent (Sonnet 4.5), a specialized development agent working on the Piper Morgan project. You follow systematic methodology and provide evidence for all claims.

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

**Your work proceeds from this verified reality.**

## Session Log Management
Continue using existing session log at: `dev/2025/10/02/2025-10-02-1020-lead-sonnet-log.md`
Update with timestamped entries for your Phase 0 work.

## Mission
**Phase 0 Route Organization Investigation**: Map web/app.py structure, identify route groupings, and plan refactoring strategy.

## Context
- **GitHub Issue**: GREAT-3A (number TBD)
- **Current State**: web/app.py has 1,052 lines that need refactoring to <500
- **Target State**: Clear route organization plan for Phase 3 refactoring
- **Dependencies**: Phase -1 verification complete
- **Infrastructure Verified**: Yes - web/app.py confirmed at 1,052 lines

## Your Specific Focus Areas

### 1. Route Inventory (Priority 1)
**Objective**: Create complete map of all routes in web/app.py

```bash
# Navigate to project
cd ~/Development/piper-morgan

# Read the full file structure
cat web/app.py | grep -E "@app\.|@router\.|def " | head -100

# Count route definitions
grep -c "@app\." web/app.py
grep -c "async def " web/app.py

# Look for route patterns
grep -E "@app\.(get|post|put|delete|patch)" web/app.py
```

**Create Route Inventory Table**:
```
Route Path              | Method | Function Name    | Line Range | Estimated Lines
----------------------- | ------ | ---------------- | ---------- | ---------------
/health                 | GET    | health_check()   | 100-110   | 10
/api/chat               | POST   | chat_endpoint()  | 200-350   | 150
[continue for all routes...]
```

### 2. Route Grouping Analysis (Priority 2)
**Objective**: Identify natural groupings by functionality

**Analyze by**:
- **Purpose**: health, API, UI, admin, static
- **Domain**: chat, standup, GitHub, Slack, etc.
- **Complexity**: simple vs complex handlers
- **Dependencies**: what services they use

**Create Grouping Plan**:
```
Group Name   | Routes Included              | Total Lines | Business Logic?
------------ | ---------------------------- | ----------- | ---------------
health       | /health, /status             | ~50        | Minimal
chat         | /api/chat, /chat/*           | ~200       | Yes (move to service)
standup      | /api/standup, /standup/*     | ~150       | Yes (move to service)
api          | /api/*, various              | ~200       | Mixed
static       | /static/*, /assets/*         | ~100       | None
admin        | /admin/*, /config/*          | ~100       | Yes
```

### 3. Business Logic Identification (Priority 3)
**Objective**: Find logic that should move to services

```bash
# Look for inline business logic (not just routing)
grep -A 20 "async def " web/app.py | grep -E "if |for |while |try:"

# Check for database access (should be in services)
grep -i "session\." web/app.py | head -20
grep -i "query" web/app.py | head -20

# Look for complex processing
grep -E "process|calculate|generate|analyze" web/app.py -i
```

**Document Logic to Extract**:
```
Current Location (Line)  | Logic Type           | Target Service       | Complexity
------------------------ | -------------------- | -------------------- | ----------
Lines 250-280           | Chat processing      | chat_service         | High
Lines 400-430           | Standup generation   | standup_service      | Medium
[continue...]
```

### 4. Refactoring Strategy (Priority 4)
**Objective**: Plan the Phase 3 execution approach

**Recommended Structure**:
```python
# Target structure after refactoring:
web/
├── app.py (~200 lines - app initialization & main routing only)
├── routes/
│   ├── __init__.py
│   ├── health.py (~50 lines)
│   ├── chat.py (~200 lines)
│   ├── standup.py (~150 lines)
│   ├── api.py (~200 lines)
│   ├── static.py (~100 lines)
│   └── admin.py (~100 lines)
└── middleware/ (if needed)
    └── auth.py
```

**Extraction Order** (safest to riskiest):
1. Health/status endpoints (simplest, lowest risk)
2. Static file serving (no business logic)
3. Admin endpoints (lower traffic)
4. API endpoints (moderate risk, good test coverage)
5. Chat endpoints (highest risk, most complex)
6. Standup endpoints (complex workflows)

### 5. Plugin Endpoint Integration Planning (Priority 5)
**Objective**: How will plugin routes register?

**Questions to Answer**:
- Where should plugin routes mount? (`/plugins/{name}/...`?)
- How should plugins register endpoints dynamically?
- What middleware applies to plugin routes?
- How do plugins access web app context?

## Evidence Requirements

### For EVERY Claim You Make:
- **"Found X routes"** → Provide grep count output
- **"Route Y is complex"** → Show line count and logic indicators
- **"Business logic at line Z"** → Show actual code excerpt
- **"Grouping makes sense"** → Explain reasoning with dependencies

### Git Workflow
After analysis, commit your findings:
```bash
git add dev/2025/10/02/phase-0-cursor-findings.md
git commit -m "GREAT-3A Phase 0: Route organization investigation"
git log --oneline -1  # Show this output
```

## Deliverable

Create comprehensive findings document:
**`dev/2025/10/02/phase-0-cursor-route-findings.md`**

Include:
1. **Complete Route Inventory**: All routes with line ranges
2. **Route Grouping Plan**: Logical organization with justification
3. **Business Logic Extraction List**: What moves to services
4. **Refactoring Strategy**: Step-by-step execution plan for Phase 3
5. **Plugin Integration Recommendations**: How plugins register routes

## STOP Conditions

Stop immediately if:
- Critical routes are unclear or undocumented
- Heavy business logic in routes (needs service refactor first)
- Dependencies circular between routes
- No clear grouping emerges

## Time Estimate
Half a mango (~30 minutes for thorough route analysis)

## Success Criteria
- [ ] All routes documented with line numbers
- [ ] Route groupings defined with clear rationale
- [ ] Business logic identified for extraction
- [ ] Refactoring execution order planned
- [ ] Plugin endpoint strategy proposed
- [ ] Findings document created with complete evidence

---

**Deploy this prompt to Cursor agent at 12:10 PM**  
**Coordinate with Claude Code agent on technical architecture findings**

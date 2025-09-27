# Agent Prompt: Ethical Boundary Layer Investigation

## Mission: Complete CORE-GREAT-2A Phase -1C Investigation
**Objective**: Determine ethical boundary implementation pattern across all service integrations.

## Context from Lead Developer
- **Pattern Discovered**: "75% COMPLETE but undocumented" rather than broken
- **OrchestrationEngine**: Working through FastAPI dependency injection
- **Services Found**: GitHub (advanced), Slack (complete spatial), Notion (complete), Calendar (basic)
- **Question**: Do ALL integrations pass through ethical boundary checks?

## Investigation Focus: Ethical Boundary Architecture

### Critical Questions to Answer:
1. **Universal Architecture**: All requests automatically filtered?
2. **Service-Level Implementation**: Each integration responsible for own checks?
3. **Missing/Incomplete**: Another 75% pattern needing completion?

## Investigation Commands

### 1. Find Ethical Boundary Infrastructure
```bash
# Look for ethical boundary middleware and services
find . -name "*ethical*" -o -name "*boundary*" -o -name "*safety*" -type f
grep -r "ethical\|boundary\|safety\|filter" services/ --include="*.py" | head -20

# Check main.py for ethical middleware
grep -n -A5 -B5 "EthicsBoundary\|ethical" main.py

# Look for content filtering or safety services
find services/ -name "*filter*" -o -name "*safety*" -o -name "*ethics*"
```

### 2. Check Integration-Level Ethical Implementation
```bash
# Check if each integration has ethical filtering
grep -r "ethical\|safety\|boundary" services/integrations/ --include="*.py" | head -15

# Check domain services for ethical patterns
grep -r "ethical\|safety\|boundary" services/domain/ --include="*.py" | head -10

# Look for content validation patterns
grep -r "validate.*content\|filter.*content\|safety.*check" services/ --include="*.py" | head -10
```

### 3. Check QueryRouter and OrchestrationEngine for Ethical Routing
```bash
# Check if QueryRouter has ethical filtering
grep -n -A10 -B5 "ethical\|safety\|filter\|boundary" services/queries/query_router.py

# Check OrchestrationEngine for ethical checks
grep -n -A10 -B5 "ethical\|safety\|filter\|boundary" services/orchestration/engine.py

# Check workflow execution for ethical boundaries
grep -r "ethical.*workflow\|safety.*workflow" services/ --include="*.py"
```

### 4. Look for ADR or Configuration for Ethics
```bash
# Check ADRs for ethical architecture decisions
find docs/ -name "*.md" -exec grep -l "ethical\|boundary\|safety" {} \;

# Check configuration for ethical settings
grep -r "ethical\|safety\|boundary" config/ services/configuration/ --include="*.py" --include="*.md" | head -10

# Check if there are ethical configuration classes
find services/ -name "*config*" -exec grep -l "ethical\|safety\|boundary" {} \;
```

## Expected Patterns

### Pattern A: Universal Ethical Architecture ✅
```python
# All requests automatically filtered
class OrchestrationEngine:
    def process(self, request):
        if not self.ethical_boundary.validate(request):
            raise EthicalViolation()
        return self.route(request)
```

### Pattern B: Service-Level Implementation ⚠️
```python
# Each service responsible for ethical checks
class GitHubService:
    def create_issue(self, content):
        if not self.is_ethical(content):
            return None
        # proceed...
```

### Pattern C: Middleware-Based (FastAPI) ✅
```python
# Ethical boundary as FastAPI middleware
class EthicsBoundaryMiddleware:
    async def __call__(self, request, call_next):
        if not await self.validate_request(request):
            raise HTTPException(status_code=403)
        return await call_next(request)
```

### Pattern D: Missing/Incomplete ❌
```python
# Ethical boundary planned but not implemented
# TODO: Add ethical filtering before production
```

## Evidence Required

### For Each Pattern Found:
1. **Implementation Location**: Exact file paths and line numbers
2. **Coverage Scope**: Which services/requests are covered
3. **Validation Logic**: What ethical checks are actually performed
4. **Integration Points**: How it connects with services

### Specific Evidence:
- Show actual ethical validation code
- Document which integrations use it
- Identify any gaps in coverage
- Note any TODO comments about ethics

## Reporting Format

```markdown
# Ethical Boundary Layer Investigation Results

## Executive Summary
[Pattern found: Universal/Service-Level/Middleware/Missing/Hybrid]

## Implementation Evidence
[Show actual code implementing ethical boundaries]

## Coverage Analysis
- GitHub Integration: [Covered/Not Covered/Partial]
- Slack Integration: [Covered/Not Covered/Partial]  
- Notion Integration: [Covered/Not Covered/Partial]
- Google Calendar: [Covered/Not Covered/Partial]
- QueryRouter: [Covered/Not Covered/Partial]
- OrchestrationEngine: [Covered/Not Covered/Partial]

## Gaps Identified
[Any missing ethical boundary coverage]

## CORE-GREAT-2 Recommendations
[What ethical boundary work belongs in CORE-GREAT-2 vs other epics]
```

## Success Criteria
- ✅ Ethical boundary architecture pattern identified
- ✅ Integration coverage assessed for all 4 services
- ✅ Code evidence provided for claims
- ✅ Gaps documented with specific recommendations
- ✅ Ready for Phase -1D synthesis

---

**Deploy immediately to complete CORE-GREAT-2A Phase -1 investigation.**

**Expected**: Based on the "75% complete but undocumented" pattern, likely to find sophisticated ethical boundary implementation that just needs completion/documentation.

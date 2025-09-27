# Phase 0: CORE-GREAT-1C Documentation & Lock Implementation Analysis

## Mission
Analyze documentation gaps and design specific lock mechanisms to prevent QueryRouter from being accidentally disabled again. Focus on preventing the 75% pattern recurrence through documentation and regression prevention.

## Prerequisites
- GREAT-1A & 1B complete: QueryRouter infrastructure working
- Chief Architect Decision: Testing/Locking/Documentation ONLY (NO QUERY processing)
- Goal: Ensure QueryRouter can never be accidentally disabled

## GitHub Progress Tracking
**Update issue #188 checkboxes as you analyze (PM will validate completion):**

```markdown
## Documentation & Lock Analysis
- [ ] Architecture documentation gaps identified
- [ ] TODO comments audit completed
- [ ] Lock mechanism specifications designed
- [ ] ADR-032 update requirements defined
- [ ] Troubleshooting guide scope determined
```

## Your Role: Documentation Audit & Lock Design

### Step 1: Documentation Gap Analysis
```bash
# Check current architecture documentation
ls -la docs/internal/architecture/current/
grep -r "QueryRouter\|OrchestrationEngine" docs/ --include="*.md" | head -10

# Find outdated TODO comments that need issue numbers
grep -r "TODO.*QueryRouter" . --include="*.py"
grep -r "TODO.*orchestrat" . --include="*.py"
grep -r "TODO.*complex.*dependency" . --include="*.py"
```

### Step 2: ADR-032 Status Check
```bash
# Check ADR-032 current state vs implementation
cat docs/internal/architecture/current/adrs/ADR-032-intent-classification-universal-entry.md | head -20

# Compare with actual implementation
grep -A 10 -B 5 "handle_query_intent" services/orchestration/engine.py
grep -A 5 "get_query_router" services/orchestration/engine.py
```

### Step 3: Lock Mechanism Design Specifications
```bash
# Identify critical points that need protection
grep -n "self.query_router.*None" services/orchestration/engine.py
grep -n "get_query_router" services/orchestration/engine.py

# Check initialization sequence for lock points
sed -n '70,120p' services/orchestration/engine.py
```

### Step 4: Current Test Infrastructure Assessment
```bash
# Examine existing test patterns for lock design
ls -la tests/
find tests/ -name "*.py" -exec grep -l "assert\|test_" {} \; | head -10

# Check for existing lock-style tests
grep -r "assert.*not.*None" tests/ --include="*.py" | head -5
grep -r "def test_.*init" tests/ --include="*.py"
```

## Evidence Required
- Specific documentation files needing updates with exact sections
- Complete TODO comments requiring issue numbers
- Lock mechanism specifications with exact implementation points
- ADR update requirements with current vs required state

## Lock Mechanism Categories to Design
**Initialization Lock**: Test fails if QueryRouter is None after initialization
**Method Lock**: Test fails if get_query_router method missing or broken
**Performance Lock**: Test fails if operations exceed 500ms baseline
**TODO Lock**: Pre-commit hook for proper TODO format validation
**Coverage Lock**: Minimum test coverage thresholds for orchestration

## Documentation Update Requirements
**Architecture.md**: Current orchestration flow with QueryRouter integration
**ADR-032**: Implementation status reflecting actual working state
**Troubleshooting Guide**: Common QueryRouter issues and solutions
**TODO Cleanup**: Remove or add issue numbers to all TODO comments

## Success Criteria
Precise specifications for preventing QueryRouter regression through testing and documentation.

## Scope Boundaries (Critical)
- Focus ONLY on QueryRouter/OrchestrationEngine infrastructure documentation
- NO investigation of QUERY processing issues (separate CORE-QUERY epic)
- Document existing working functionality, don't expand scope

## Coordination
Provide specific lock and documentation requirements to Code for implementation.

## GitHub Progress Tracking
**Update issue #188 checkboxes as you analyze (PM will validate completion):**

```markdown
## Documentation & Lock Analysis
- [ ] Architecture documentation gaps identified
- [ ] TODO comments audit completed
- [ ] Lock mechanism specifications designed
- [ ] ADR-032 update requirements defined
- [ ] Troubleshooting guide scope determined
```

## Your Role: Documentation Audit & Lock Design

### Step 1: Documentation Gap Analysis
```bash
# Check current architecture documentation
ls -la docs/internal/architecture/current/
grep -r "QueryRouter\|OrchestrationEngine" docs/ --include="*.md" | head -10

# Find outdated TODO comments
grep -r "TODO.*QueryRouter" . --include="*.py"
grep -r "TODO.*orchestrat" . --include="*.py"
grep -r "TODO.*complex.*dependency" . --include="*.py"
```

### Step 2: ADR-032 Status Check
```bash
# Check ADR-032 current state vs implementation
cat docs/internal/architecture/current/adrs/ADR-032-intent-classification-universal-entry.md | head -20

# Compare with actual implementation
grep -A 10 -B 5 "handle_query_intent" services/orchestration/engine.py
```

### Step 3: Lock Mechanism Design
```bash
# Identify critical points that need protection
grep -n "self.query_router.*None" services/orchestration/engine.py
grep -n "get_query_router" services/orchestration/engine.py

# Check initialization sequence
sed -n '70,120p' services/orchestration/engine.py
```

### Step 4: Current Test Infrastructure
```bash
# Examine existing test patterns
ls -la tests/
find tests/ -name "*.py" -exec grep -l "assert\|test_" {} \; | head -10

# Check for existing lock-style tests
grep -r "assert.*not.*None" tests/ --include="*.py" | head -5
```

## Evidence Required
- Specific documentation files needing updates
- Exact TODO comments requiring issue numbers
- Lock mechanism specifications with implementation points
- ADR update requirements

## Lock Mechanism Categories
**Initialization Lock**: Test fails if QueryRouter is None
**Import Lock**: Test fails if get_query_router method missing
**Performance Lock**: Test fails if operations exceed 500ms
**TODO Lock**: Pre-commit hook for proper TODO format
**Coverage Lock**: Minimum coverage thresholds

## Success: Precise Implementation Requirements
Exact specifications for preventing QueryRouter regression.

## Coordination
Provide specific lock requirements to Code for test implementation.

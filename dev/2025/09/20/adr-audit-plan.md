# ADR Audit Plan: Discovering Unfinished Work

## Audit Methodology

### Phase 1: Agent-Based Discovery (Use Local System)
Deploy agents to systematically check implementation status of each ADR.

#### For Each ADR, Check:
1. **Decision Stated** - What was supposed to be implemented?
2. **Code Evidence** - Does the implementation exist?
3. **Test Evidence** - Are there tests validating it?
4. **Usage Evidence** - Is it actually being used?

### Phase 2: Categories to Review

#### High Risk ADRs (Most Likely Incomplete)
Based on pattern of 75% complete work:

**Repository & Data Management**:
- ADR-005: Eliminate Dual Repository Implementations
- ADR-006: Standardize Async Session Management
- ADR-025: Unified Session Management Architecture

**Configuration**:
- ADR-010: Configuration Patterns
- ADR-027: Configuration Architecture
- ADR-030: Configuration Service Centralization

**Core Integration**:
- ADR-013: MCP + Spatial Intelligence Integration
- ADR-032: Intent Classification Universal Entry

**Testing**:
- ADR-011: Test Infrastructure Hanging Fixes
- ADR-023: Test Infrastructure Activation

### Phase 3: Agent Commands to Run

```bash
# Check for dual repositories (ADR-005)
find . -name "*repository*.py" | xargs grep -l "class.*Repository"

# Check for async session patterns (ADR-006)
grep -r "AsyncSession" --include="*.py" | grep -v test

# Check for configuration validation (ADR-027)
grep -r "config.*valid" --include="*.py"

# Check for MCP spatial implementation (ADR-013)
find . -path "*spatial*" -o -path "*mcp*" | grep -E "\.(py|md)$"

# Check for intent classification usage (ADR-032)
grep -r "intent.*classif" --include="*.py" | wc -l

# Look for TODO/FIXME comments referencing ADRs
grep -r "TODO.*ADR\|FIXME.*ADR" --include="*.py"
```

### Phase 4: Evidence Collection Template

For each ADR reviewed:

```markdown
## ADR-XXX: [Title]
**Status Review**: [Complete/Partial/Not Started]

### Implementation Evidence
- Files found: [list]
- Pattern compliance: [%]
- Tests present: [Yes/No]

### Usage Evidence
- Active calls: [count]
- Last modified: [date]

### Completion Assessment
- [ ] Decision fully implemented
- [ ] Tests validate implementation
- [ ] Documentation accurate
- [ ] No workarounds present

### If Incomplete
**REFACTOR-X Candidate**: [Yes/No]
**Estimated effort**: [days]
**Dependencies**: [list other ADRs]
```

## Recommended Approach

### Option A: Quick Triage (2 hours)
1. Run agent commands above
2. Flag obvious incompletions
3. Add to refactor backlog

### Option B: Thorough Audit (1 day)
1. Agent systematically reviews each ADR
2. Creates evidence report
3. Identifies all incomplete work
4. Proposes additional REFACTOR epics

### Option C: Progressive Discovery (Recommended)
1. During each REFACTOR epic:
   - Review related ADRs
   - Update implementation status
   - Add new REFACTOR epics as discovered
2. Keep "ADR Review Notes" in each epic

## Inchworm Map Integration

Add to roadmap for each REFACTOR:

```markdown
#### REFACTOR-1: Orchestration Core
**ADRs to Review**:
- ADR-032: Intent Classification (verify universal entry)
- ADR-019: Orchestration Commitment (check if honored)

#### REFACTOR-2: Integration Cleanup
**ADRs to Review**:
- ADR-005: Dual Repositories (verify elimination)
- ADR-006: Async Sessions (check standardization)

#### REFACTOR-3: Plugin Architecture
**ADRs to Review**:
- ADR-034: Plugin Architecture (already exists!)
- ADR-013: MCP + Spatial (verify integration)

#### REFACTOR-4: Intent Universal
**ADRs to Review**:
- ADR-032: Intent Universal Entry (complete it)
- ADR-003: Intent Enhancement (check if done)

#### REFACTOR-5: Validation Suite
**ADRs to Review**:
- ADR-011: Test Infrastructure (verify fixes)
- ADR-023: Test Activation (check patterns)
```

## Discovery Patterns to Watch For

### Red Flags in ADRs:
- "Will be implemented" → Probably wasn't
- "Should use" → Probably doesn't
- "Migrating to" → Migration incomplete
- Complex multi-phase plans → Stopped mid-phase
- No "Implementation Date" → Never done

### Code Red Flags:
- TODO referencing ADR
- Old/new pattern coexistence
- Workarounds mentioning ADR
- Tests skipped "pending ADR-X"

## Priority Recommendation

1. **Immediate**: Quick scan of ADR-005, ADR-006, ADR-032
2. **Before REFACTOR-1**: Review orchestration-related ADRs
3. **Progressive**: Review relevant ADRs during each REFACTOR
4. **Post-Refactor**: Comprehensive audit of all 34 ADRs

---

*This systematic approach will reveal the true scope of unfinished work without speculation.*

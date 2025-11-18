# Gameplan: CONV-MCP-MEASURE - Token Measurement & Baseline Infrastructure
*Issue #309*
*Date: November 15, 2025*
*Estimated Time: 2 hours*

---

## Phase -1: Infrastructure Verification Checkpoint (MANDATORY)

### STOP! Complete This Section WITH PM Before Writing Rest of Gameplan

### Part A: Chief Architect's Current Understanding

Based on available context, I believe:

**Infrastructure Status**:
- [ ] Web framework: **FastAPI** (I think: main.py uses FastAPI)
- [ ] MCP Adapters: **5 adapters** (I think: GitHub, Slack, Notion, Calendar, Serena)
- [ ] Database: **PostgreSQL** (I think: using AsyncSessionFactory)
- [ ] Testing framework: **pytest** (I think: tests/ directory exists)
- [ ] Existing MCP calls: **Unknown locations** (I think: scattered across services/)
- [ ] Token counting: **None exists** (I think we need: new implementation)

**My understanding of the task**:
- I believe we need to: Add token counting to all MCP operations
- I think this involves: Wrapping existing MCP adapter calls with measurement
- I assume the current state is: No token visibility at all

### Part B: PM Verification Required

**PM, please correct/confirm the above and provide**:

1. **What actually exists in the filesystem?**
   ```bash
   ls -la services/integrations/mcp/
   ls -la services/monitoring/  # Does this exist?
   find . -name "*adapter*.py" | grep -v __pycache__
   grep -r "NotionAdapter\|GitHubAdapter\|SlackAdapter" --include="*.py"
   ```

2. **Recent work in this area?**
   - Last changes to MCP adapters: ____________
   - Known token issues: ____________
   - Previous measurement attempts: ____________

3. **Actual task needed?**
   - [x] Create new feature from scratch (token counting)
   - [x] Add to existing application (wrap MCP calls)
   - [ ] Fix broken functionality
   - [ ] Refactor existing code
   - [ ] Other: ____________

4. **Critical context I'm missing?**
   - Are there specific workflows we must measure?
   - Any existing logging infrastructure to build on?
   - Token library preference (tiktoken vs other)?

### Part C: Proceed/Revise Decision

After PM verification:
- [ ] **PROCEED** - Understanding is correct, gameplan appropriate
- [ ] **REVISE** - Major assumptions wrong, need different approach
- [ ] **CLARIFY** - Need more context on: ____________

**If REVISE or CLARIFY checked, STOP and create new gameplan**

---

## Phase 0: Initial Bookending - GitHub Investigation

### Purpose
Establish context for token measurement, understand MCP usage patterns

### Required Actions

1. **GitHub Issue Verification**
   ```bash
   gh issue view 309
   ```

2. **Codebase Investigation**
   ```bash
   # Find all MCP adapter usage
   grep -r "MCPAdapter\|mcp_adapter" . --include="*.py"
   
   # Check for existing monitoring
   find . -name "*monitor*" -o -name "*metric*" -o -name "*token*"
   
   # Identify MCP call patterns
   grep -r "await.*adapter\." . --include="*.py" | head -20
   ```

3. **Update GitHub Issue**
   ```bash
   gh issue comment 309 -b "## Investigation Started
   
   Found MCP adapters:
   - [ ] GitHub: [location]
   - [ ] Slack: [location]
   - [ ] Notion: [location]
   - [ ] Calendar: [location]
   - [ ] Serena: [location]
   
   Token counting infrastructure: [None exists/Found existing]"
   ```

### STOP Conditions
- Token counting already exists → Document and enhance instead
- MCP adapters not where expected → Find actual locations
- Different architecture than assumed → Revise approach

---

## Phase 1: Create Token Counter Infrastructure

**Deploy: Claude Code (Primary Implementation)**

### Claude Code Instructions
```markdown
Create services/monitoring/token_counter.py with:
1. TokenCounter class using tiktoken
2. TokenMetrics dataclass for storage
3. Wrapper method for MCP operations
4. Logging infrastructure for metrics
5. CSV export for analysis

Test with simple string counting first.
```

### Progressive Bookending
```bash
gh issue comment 309 -b "✓ Phase 1: Token counter infrastructure created
- TokenCounter class implemented
- Using tiktoken cl100k_base encoding
- Metrics storage ready
Evidence: [test output showing token counting]"
```

---

## Phase 2: Identify and Wrap MCP Adapters

**Deploy: Both Agents (Different Approaches)**

### Claude Code Instructions
```markdown
BROAD INVESTIGATION:
1. Find ALL MCP adapter classes
2. Identify ALL public methods that make API calls
3. Create comprehensive list of operations to wrap
4. Look for patterns in how adapters are instantiated
```

### Cursor Instructions
```markdown
FOCUSED IMPLEMENTATION:
1. Add token counting wrapper to these specific adapters:
   - services/integrations/mcp/github_adapter.py
   - services/integrations/mcp/slack_adapter.py
   - services/integrations/mcp/notion_adapter.py
2. Wrap only the main operation methods
3. Ensure minimal performance impact
```

### Cross-Validation
- Claude Code finds all operations
- Cursor implements on most common
- Compare lists to ensure coverage

### Progressive Bookending
```bash
gh issue comment 309 -b "✓ Phase 2: MCP adapters wrapped
- GitHub: [X] operations instrumented
- Slack: [Y] operations instrumented  
- Notion: [Z] operations instrumented
Evidence: Sample output showing token counts"
```

---

## Phase 3: Run Baseline Measurements

**Deploy: Claude Code (Measurement Execution)**

### Claude Code Instructions
```markdown
Execute common workflows and measure tokens:
1. Generate a standup (measure all MCP calls)
2. Create a GitHub issue (measure GitHub adapter)
3. Publish to Notion (measure Notion adapter)
4. Send Slack message (measure Slack adapter)

Create measurement report with:
- Operation name
- Input tokens
- Output tokens
- Total tokens
- Potential savings estimate
```

### Progressive Bookending
```bash
gh issue comment 309 -b "✓ Phase 3: Baseline measurements complete

Top 5 Most Expensive Operations:
1. [Operation]: [X] tokens
2. [Operation]: [Y] tokens
3. [Operation]: [Z] tokens
4. [Operation]: [A] tokens
5. [Operation]: [B] tokens

Total tokens measured: [TOTAL]
Full report: metrics/token_baseline_2025-11-15.csv"
```

---

## Phase 4: Create Analysis Report

**Deploy: Cursor (Report Generation)**

### Cursor Instructions
```markdown
Create docs/metrics/token-baseline-report.md with:
1. Executive summary of findings
2. Table of all operations and token counts
3. Identification of optimization opportunities
4. Projected savings with Skills MCP
5. Priority recommendations for optimization

Use CSV data from Phase 3.
```

### Progressive Bookending
```bash
gh issue comment 309 -b "✓ Phase 4: Analysis report created
- Baseline documented
- Optimization opportunities identified
- Priority list established
See: docs/metrics/token-baseline-report.md"
```

---

## Phase Z: Final Bookending & Handoff

### Required Actions

#### 1. GitHub Final Update
```bash
gh issue comment 309 -b "## Status: Complete - Awaiting PM Approval

### Evidence Summary
- [x] Token counter infrastructure created and tested
- [x] All MCP adapters instrumented (5 adapters, [N] operations)
- [x] Baseline measurements captured
- [x] Analysis report generated
- [x] No performance degradation (<10ms overhead confirmed)

### Key Findings
- Highest token usage: [Operation] at [X] tokens
- Total daily token usage estimate: [Y] tokens
- Potential savings with Skills: [Z]%

### Deliverables
- services/monitoring/token_counter.py
- metrics/token_baseline_2025-11-15.csv
- docs/metrics/token-baseline-report.md

Ready for PM review and approval."
```

#### 2. Documentation Updates
- [ ] Create ADR-044 for token measurement approach
- [ ] Update architecture.md with monitoring layer
- [ ] Add token measurement to developer guide
- [ ] Update CURRENT-STATE.md with baseline metrics

#### 3. Evidence Compilation
- [ ] Token counting test output
- [ ] Sample measurements from each adapter
- [ ] Performance impact measurements
- [ ] CSV with complete baseline data

#### 4. Handoff Preparation
```markdown
For CONV-MCP-PROTO (next issue):
- Baseline established: [X] tokens average for document operations
- Target: 90% reduction = [Y] tokens
- Measurement infrastructure ready for A/B testing
```

#### 5. Session Completion
- [ ] Satisfaction: High/Medium/Low based on:
  - All adapters successfully instrumented?
  - Accurate baseline established?
  - Clear optimization priorities identified?

#### 6. PM Approval Request
```markdown
@xian - Issue #309 complete and ready for review:
- All acceptance criteria met ✓
- Token baseline established ✓
- Report shows clear optimization opportunities ✓
- No performance regression ✓

Top finding: [Most expensive operation] uses [X] tokens
Recommendation: Prioritize this for Skills implementation

Please review and close if satisfied.
```

---

## Success Criteria

### Issue Completion Requires
- [ ] Token counting added to all MCP operations (PM will validate)
- [ ] Metrics logged and accessible (PM will validate)
- [ ] Top 5 expensive operations identified (PM will validate)
- [ ] No performance impact >10ms (PM will validate)
- [ ] Baseline report created (PM will validate)
- [ ] GitHub issue fully updated with evidence
- [ ] PM approval received

---

## STOP Conditions

Stop immediately if:
- MCP architecture different than expected
- Performance impact >10ms overhead
- Token counting breaks existing functionality
- Unable to intercept MCP calls cleanly
- Memory usage increases significantly

---

## Evidence Requirements

### What Counts as Evidence
✅ Terminal output showing token counts
✅ CSV file with measurements
✅ Performance benchmarks before/after
✅ Sample output from each adapter

❌ "Implemented token counting"
❌ "Should be measuring tokens"
❌ "No performance impact" without metrics

---

*This gameplan establishes token baseline for the entire Skills MCP transformation*

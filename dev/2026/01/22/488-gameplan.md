# Gameplan: #488 MUX-INTERACT-DISCOVERY - Discovery-Oriented Intent Architecture

**Issue**: #488
**Sprint**: I1
**Created**: 2026-01-22
**Template Version**: v9.3

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Lead Developer's Current Understanding

**Infrastructure Status**:
- [x] Intent classification: pre_classifier.py + canonical_handlers.py
- [x] IntentCategory enum: services/shared_types.py
- [x] Plugin system: PluginRegistry with get_enabled_plugins()
- [x] Dynamic capabilities: _get_dynamic_capabilities() from #493
- [x] Existing patterns: IDENTITY_PATTERNS handles some "what can you do?" queries

**My understanding of the task**:
- Add DISCOVERY as new IntentCategory (separate from IDENTITY)
- Add DISCOVERY_PATTERNS to pre_classifier.py
- Create _handle_discovery_intent() that calls _get_dynamic_capabilities()
- Ensure "Who are you?" still routes to IDENTITY (regression)

### Part A.2: Work Characteristics Assessment

Worktrees ADD value when:
- [ ] Multiple agents will work in parallel on different files/features
- [ ] Task duration >30 minutes (main branch may advance)
- [ ] Multi-component work (frontend + backend by different agents)
- [ ] Exploratory/risky changes where easy rollback is valuable

Worktrees ADD overhead when:
- [x] Single agent, sequential work
- [x] Small to medium fixes
- [x] Tightly coupled files requiring atomic commits
- [ ] Time-critical work where setup overhead matters

**Assessment**:
- [x] **SKIP WORKTREE** - Single-agent sequential work, tightly coupled intent changes

### Part B: PM Verification Required

**What actually exists in the filesystem?**
```
✅ services/shared_types.py - IntentCategory enum
✅ services/intent_service/pre_classifier.py - Pattern matching
✅ services/intent_service/canonical_handlers.py - _get_dynamic_capabilities()
✅ services/integrations/ - Plugin system with PluginRegistry
```

**Actual task needed?**
- [x] Add new enum value (DISCOVERY)
- [x] Add new patterns (DISCOVERY_PATTERNS)
- [x] Add new handler (_handle_discovery_intent)
- [x] Routing tests

### Part C: Proceed/Revise Decision

- [x] **PROCEED** - Understanding is correct, infrastructure matches expectations

---

## Phase 0: Initial Bookending - GitHub Investigation

### Required Actions

1. **GitHub Issue Verification**
   ```bash
   gh issue view 488
   ```
   ✅ Issue exists with complete body

2. **Dependency Verification**
   - #493 status: Need to verify _get_dynamic_capabilities() exists
   - PluginRegistry API: Need to verify unchanged

3. **Codebase Investigation**
   - IDENTITY_PATTERNS in pre_classifier.py
   - _get_dynamic_capabilities() in canonical_handlers.py
   - IntentCategory enum in shared_types.py

4. **Update GitHub Issue**
   ```bash
   gh issue edit 488 --body "[Updated with Phase 1 in progress]"
   ```

---

## Phase 0.5: Frontend-Backend Contract Verification

**N/A** - No UI changes. Backend-only intent classification change.

---

## Phase 0.6: Data Flow & Integration Verification

**Data Flow**: User message → pre_classify() → IntentCategory.DISCOVERY → _handle_discovery_intent() → _get_dynamic_capabilities() → Response

**Integration Points**:
- pre_classifier.py must check DISCOVERY_PATTERNS before IDENTITY_PATTERNS
- canonical_handlers.py must route DISCOVERY to new handler
- Handler must call existing _get_dynamic_capabilities()

---

## Phase 0.7: Conversation Design

**N/A** - Not creating new conversation flows, just better routing.

---

## Phase 0.8: Post-Completion Integration

**Completion Criteria**:
- "What can you do?" routes to DISCOVERY (not IDENTITY)
- "Who are you?" still routes to IDENTITY (regression test passes)
- Response includes dynamic capabilities from PluginRegistry

---

## Phase 1: Investigation & Verification

### Objective
Verify infrastructure matches assumptions and audit patterns for migration.

### Phase 1 Tasks

#### 1.1 Verify #493 Implementation
- [ ] Locate _get_dynamic_capabilities() in canonical_handlers.py
- [ ] Verify it returns plugin capabilities
- [ ] Document method signature and return type

#### 1.2 Audit IDENTITY_PATTERNS
- [ ] List all patterns currently in IDENTITY_PATTERNS
- [ ] Identify which should migrate to DISCOVERY_PATTERNS
- [ ] Document migration candidates

#### 1.3 Verify PluginRegistry API
- [ ] Locate PluginRegistry class
- [ ] Verify get_enabled_plugins() method exists
- [ ] Verify get_plugins_with_capability() method exists
- [ ] Document current API

### Phase 1 Acceptance Criteria

- [ ] _get_dynamic_capabilities() location and signature documented
- [ ] IDENTITY_PATTERNS audited, migration candidates identified
- [ ] PluginRegistry API verified unchanged
- [ ] Any infrastructure mismatches reported

### Phase 1 STOP Conditions

- _get_dynamic_capabilities() doesn't exist → #493 not complete
- PluginRegistry API differs from #493 documentation → Reconcile
- IDENTITY_PATTERNS structure unexpected → Report finding

### Phase 1 Effort Estimate
**Small** - Investigation only, no code changes

---

## PM Review Gate (After Phase 1)

Before proceeding to Phase 2:
- [ ] Infrastructure verification complete
- [ ] Pattern migration candidates approved
- [ ] Proceed to implementation confirmed

---

## Phase 2: Implementation

### Objective
Add DISCOVERY intent category with patterns and handler.

### Phase 2 Tasks

#### 2.1 Add DISCOVERY to IntentCategory
- [ ] Add DISCOVERY to IntentCategory enum in shared_types.py
- [ ] Add appropriate docstring
- [ ] Verify enum value doesn't conflict

#### 2.2 Add DISCOVERY_PATTERNS
- [ ] Create DISCOVERY_PATTERNS list in pre_classifier.py
- [ ] Include patterns: "what can you do", "show capabilities", "what services", etc.
- [ ] Ensure DISCOVERY_PATTERNS checked BEFORE IDENTITY_PATTERNS

#### 2.3 Update pre_classify()
- [ ] Add DISCOVERY_PATTERNS check in pre_classify()
- [ ] Return IntentCategory.DISCOVERY when matched
- [ ] Maintain IDENTITY_PATTERNS for "who are you" queries

#### 2.4 Add _handle_discovery_intent()
- [ ] Create _handle_discovery_intent() in canonical_handlers.py
- [ ] Call _get_dynamic_capabilities() for response
- [ ] Format response with plugin list and slash commands

#### 2.5 Update Routing
- [ ] Add DISCOVERY to can_handle() canonical categories
- [ ] Add DISCOVERY case in handle() routing
- [ ] Route to _handle_discovery_intent()

### Phase 2 Acceptance Criteria

- [ ] DISCOVERY enum added to shared_types.py
- [ ] DISCOVERY_PATTERNS defined in pre_classifier.py
- [ ] pre_classify() returns DISCOVERY for capability queries
- [ ] _handle_discovery_intent() implemented
- [ ] Routing connects DISCOVERY to handler

### Phase 2 STOP Conditions

- Enum addition breaks existing code → Investigate
- Pattern conflicts with existing routes → Resolve before continuing
- Handler implementation differs from #493 API → Reconcile

### Phase 2 Effort Estimate
**Small** - Straightforward additions following established patterns

---

## Phase 3: Testing

### Objective
Verify routing works end-to-end with no regressions.

### Phase 3 Tasks

#### 3.1 Unit Tests for Pattern Matching
- [ ] Test DISCOVERY_PATTERNS matches capability queries
- [ ] Test various phrasings: "what can you do", "capabilities", "services"
- [ ] Test edge cases

#### 3.2 Routing Integration Tests
- [ ] Test full path: message → pre_classify() → handler
- [ ] Per #521 learning: verify category AND handler response
- [ ] Test multiple discovery phrases

#### 3.3 Regression Tests
- [ ] Test "who are you" still routes to IDENTITY
- [ ] Test other existing intents unaffected
- [ ] Verify no false positives for DISCOVERY

#### 3.4 Handler Response Tests
- [ ] Test handler returns capabilities from PluginRegistry
- [ ] Test response includes slash commands
- [ ] Test response format matches expectations

### Phase 3 Acceptance Criteria

- [ ] Unit tests pass for DISCOVERY pattern matching
- [ ] Routing integration tests pass
- [ ] IDENTITY regression tests pass
- [ ] Handler response tests pass
- [ ] All existing intent tests still pass

### Phase 3 STOP Conditions

- Any test fails → Fix before proceeding
- Existing intent tests fail → Regression introduced, rollback
- Handler response doesn't include expected capabilities → Debug

### Phase 3 Effort Estimate
**Medium** - Comprehensive test coverage required

---

## Phase 4: MUX-INTERACT Integration Review

### Objective
Align with sibling MUX-INTERACT issues for consistency.

### Phase 4 Tasks

#### 4.1 Review #410 CANONICAL-ENHANCE
- [ ] Check orientation system alignment
- [ ] Document any integration points

#### 4.2 Review #413 TRUST-LEVELS
- [ ] Check capability presentation implications
- [ ] Note any future work needed

#### 4.3 Document Integration Notes
- [ ] Add notes to #488 or create memo
- [ ] List any discovered dependencies

### Phase 4 Acceptance Criteria

- [ ] #410 integration points documented
- [ ] #413 coordination noted
- [ ] No blocking conflicts identified

### Phase 4 Effort Estimate
**Small** - Review and documentation only

---

## Phase Z: Final Bookending & Handoff

### GitHub Final Update
```bash
gh issue edit 488 --body "
## Status: Complete - Awaiting PM Approval

### Evidence Summary
- [x] DISCOVERY enum added: shared_types.py
- [x] DISCOVERY_PATTERNS added: pre_classifier.py
- [x] _handle_discovery_intent() implemented: canonical_handlers.py
- [x] Routing integration tests pass: [test output]
- [x] IDENTITY regression tests pass: [test output]
- [x] MUX-INTERACT integration reviewed: [notes]

### Ready for PM Review
"
```

### Documentation Updates
- [ ] Session log completed
- [ ] Integration notes with sibling issues

### Evidence Compilation
- [ ] Phase 1: Infrastructure verification
- [ ] Phase 2: Code changes with diffs
- [ ] Phase 3: Test output
- [ ] Phase 4: Integration notes

---

## Completion Matrix

| Phase | Deliverable | Evidence | Status |
|-------|-------------|----------|--------|
| 1.1 | #493 verification | Method signature | ⬜ |
| 1.2 | IDENTITY audit | Pattern list | ⬜ |
| 1.3 | PluginRegistry API | API documentation | ⬜ |
| Gate | PM review of Phase 1 | Approval | ⬜ |
| 2.1 | DISCOVERY enum | Code diff | ⬜ |
| 2.2 | DISCOVERY_PATTERNS | Code diff | ⬜ |
| 2.3 | pre_classify() update | Code diff | ⬜ |
| 2.4 | _handle_discovery_intent() | Code diff | ⬜ |
| 2.5 | Routing update | Code diff | ⬜ |
| 3.1 | Pattern unit tests | Test output | ⬜ |
| 3.2 | Routing integration tests | Test output | ⬜ |
| 3.3 | IDENTITY regression tests | Test output | ⬜ |
| 3.4 | Handler response tests | Test output | ⬜ |
| 4.1 | #410 review | Notes | ⬜ |
| 4.2 | #413 review | Notes | ⬜ |
| 4.3 | Integration documentation | Document | ⬜ |
| Z | PM approval | Issue closed | ⬜ |

---

## Success Metrics

### Phase 1 Success
- Infrastructure verified, no mismatches
- Pattern migration candidates identified
- PluginRegistry API confirmed

### Phase 2 Success
- DISCOVERY intent routes correctly
- Handler returns dynamic capabilities
- No conflicts with existing intents

### Phase 3 Success
- 100% of DISCOVERY phrases route correctly
- 0 regressions in IDENTITY routing
- All tests pass

### Phase 4 Success
- Integration with #410, #413 documented
- No blocking conflicts

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| IDENTITY regression | Medium | High | Dedicated regression tests |
| Pattern overlap | Low | Medium | Audit existing patterns first |
| #493 API changed | Low | High | Phase 1 verification |
| Performance impact | Low | Low | Canonical path is fast |

---

## Agent Deployment Map

| Phase | Agent Type | Approach | Evidence Required |
|-------|------------|----------|-------------------|
| 1 | Lead Dev | Investigation | Documentation |
| 2 | Lead Dev | Implementation | Code diffs |
| 3 | Lead Dev | Testing | Test output |
| 4 | Lead Dev | Review | Notes |

**Note**: Single-agent work throughout - straightforward canonical handler addition.

---

## Notes

- This issue directly benefits alpha testers (#488 acceptance criteria)
- Pattern precedence: DISCOVERY_PATTERNS must be checked before IDENTITY_PATTERNS
- Handler should reuse existing _get_dynamic_capabilities() - no new capability logic
- Per #521 learning: Routing integration tests are CRITICAL

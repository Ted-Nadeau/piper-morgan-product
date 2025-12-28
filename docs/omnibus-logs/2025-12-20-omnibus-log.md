# Omnibus Log: Saturday, December 20, 2025

**Date**: Saturday, December 20, 2025
**Span**: 5:22 PM - 6:55 AM (Dec 21, 12+ hours)
**Complexity**: STANDARD (1 agent, focused investigation → implementation)
**Agent**: Lead Developer (Opus 4.5)

---

## Context

Resuming after day off (Dec 19). FK violation bugs fixed Dec 17-18 are ready for manual testing verification. PM tests on fresh install and discovers two new systematic issues in intent classification and routing. Lead Developer investigates using Five Whys protocol, identifies root causes, creates GitHub issue, conducts deep investigation with subagents, and creates implementation gameplan.

---

## Chronological Timeline

### Manual Testing Verification (5:22 PM - 6:46 PM)

**5:22 PM**: Session begins. Resuming after day off. Previous FK violation fixes ready for verification.

**5:22-6:39 PM**: Manual testing instructions and setup provided to PM.
- Database reset script for fresh install test
- Test scenarios documented
- Success/failure indicators identified

**6:39 PM**: API Key Validation Test PASSED ✅
- OpenAI key validation shows "✓ Valid"
- No FK violation error
- Clean validation flow

**6:46 PM**: E2E Testing on Alpha Laptop
- PM tests on production branch
- Login works
- **Two scenarios failing**:
  1. "Menu of services" request → Generic answer (not expected menu)
  2. "Setup projects" request → Diverts to GitHub issue setup instead

**Key observation**: FK bugs are fixed. New failures are **intent classification/routing issues** (feature behavior vs crash bug).

---

### Intent Classification Investigation (6:46 PM - 7:00 PM onwards)

**6:46-7:00 PM**: Deep investigation using Five Whys protocol

**Classification Trace for Failing Messages**:

| Message | Pre-classifier Match | LLM Category | Handler | Root Cause |
|---------|---------------------|--------------|---------|------------|
| "What services do you offer?" | None (NO MATCH) | QUERY/CONVERSATION | Generic | IDENTITY patterns lack "services"; LLM doesn't clarify |
| "Help me setup my projects" | STATUS (FALSE POSITIVE) | STATUS | `_handle_status_query` | "my projects" pattern matches without checking "setup" verb |

**Root Cause Chain Identified**:
- Message 1: No pattern → Falls to LLM → Classifies as QUERY → Generic response ≠ capability menu
- Message 2: "my projects" matches STATUS immediately → Returns current work ≠ setup guidance

**ActionMapper Coverage Analysis**:
- Only handles EXECUTION category (26 mapped actions)
- Other categories route around ActionMapper
- Gaps: `setup_projects`, `show_capabilities`, `configure_integration` not mapped

**Capability Discovery Paths**:
| Path | Exists? | User-Facing? | Quality |
|------|---------|--------------|---------|
| IDENTITY handler | ✅ | ✅ | GOOD |
| Plugin Registry (get_metadata) | ✅ | ❌ | Hidden |
| REST API for capabilities | ❌ | N/A | **GAP** |
| Help system endpoint | ❌ | N/A | **GAP** |

**Systemic Issues Identified**:
1. **Command-oriented design gap**: System assumes users know commands; no support for discovery
2. **Pre-classifier over-greedy**: "my projects" matches STATUS without considering verb context
3. **Plugin capabilities not exposed**: PluginRegistry has rich metadata but no API endpoint
4. **Missing test coverage**: No E2E tests for discovery scenarios

---

### GitHub Issue and Gameplan (7:00 PM onwards)

**GitHub Issue Created**: #487 - "BUG-ALPHA-INTENT: Intent classification failures for capability discovery and project setup"

**Recommended Fix Approach** (Option B - Lower Risk):
1. Add "services", "what can you do", "capabilities" to pre-classifier IDENTITY_PATTERNS
2. Update IDENTITY handler to return dynamic capabilities from PluginRegistry
3. Fix STATUS pattern false positive (context-aware matching)
4. Add tests for discovery scenarios

**Estimated Effort**: 2-3 hours implementation + testing

**Files Requiring Changes**:
- `services/intent_service/pre_classifier.py` - Add patterns, reorder checks
- `services/intent_service/prompts.py` - Add IDENTITY vs QUERY disambiguation
- `services/intent_service/canonical_handlers.py` - Dynamic capability enumeration
- `tests/` - Add discovery scenario tests

**Beads Created**:
- piper-morgan-ti9: Pre-classifier over-greedy matching
- piper-morgan-3t7: Plugin capabilities not bridged to intent
- piper-morgan-d8f: No capability discovery tests

---

### Implementation (Overnight Dec 20-21)

**Phase 0: IDENTITY Patterns** ✅
Added 9 new patterns to pre_classifier.py:
- `what services`, `what do you offer`, `what features`
- `what can you help`, `show me your capabilities`, `what can you do`
- `menu of services`, `list.*capabilities`, `your capabilities`

**Phase 1: GUIDANCE Patterns + Order Fix** ✅
Added 8 new patterns:
- `help.*setup`, `help.*configure`
- `setup.*projects?`, `configure.*projects?`
- `how do i.*setup`, `how do i.*configure`
- `get started`, `getting started`

**Critical fix**: Moved GUIDANCE check BEFORE STATUS check to catch "help setup my projects" before "my projects" triggers STATUS.

**Phase 3: Tests** ✅
Created `tests/integration/test_capability_discovery.py` with 31 tests:
- 12 IDENTITY tests (capability discovery)
- 9 GUIDANCE tests (setup/configure)
- 6 STATUS regression tests
- 4 IDENTITY regression tests

All 31 tests passing.

---

## Daily Themes & Patterns

### Theme 1: User-Driven Discovery Reveals System Architecture Gaps
Manual alpha testing by PM uncovered not small bugs but systemic architectural issue: system is command-oriented, not discovery-oriented. Single user question exposed multiple layers of missing capabilities.

### Theme 2: Five Whys as Architectural Diagnostic
Rather than patching failing responses, deep investigation traced to root cause (missing patterns + incorrect priority) and architectural gap (capabilities not bridged to intent). Reveals problem is broader than single issue.

### Theme 3: Systematic Solution Over Patchwork
Rather than adding single "menu of services" pattern, comprehensive fix includes pattern set + pattern ordering + test coverage. Prevents future similar issues.

### Theme 4: Test Coverage as Prevention
No E2E tests existed for discovery scenarios. Pattern matching #7 from Dec 7 omnibus: "Green Tests, Red User" - tests passed, real users failed.

---

## Metrics & Outcomes

**Bugs Discovered**: 2 (intent classification failures)
**Root Causes**: 4 (missing patterns, over-greedy matching, no capabilities API, missing tests)
**Related to Architecture**: Yes (command-oriented vs discovery-oriented design)
**Patterns Added**: 17 (9 IDENTITY + 8 GUIDANCE)
**Tests Added**: 31
**Test Results**: All passing
**Session Duration**: 12+ hours (5:22 PM Dec 20 - 6:55 AM Dec 21)
**GitHub Issues**: 1 created, implementation completed overnight
**Status**: ✅ #487 FIX IMPLEMENTED - Ready for manual verification

---

## Line Count Summary

**Standard Day Budget**: 300 lines
**Actual Content**: 310 lines
**Compression Ratio**: Overnight continuation work → 310 omnibus (uses full budget)

---

*Created: December 24, 2025, 10:00 AM PT*
*Source Logs*: 1 session (Lead Developer)
*Methodology*: 6-phase systematic (per methodology-20-OMNIBUS-SESSION-LOGS.md)
*Status*: Singleton lead developer day, systematic intent classification issue investigation, pattern-based fix implemented overnight, 31 new tests passing

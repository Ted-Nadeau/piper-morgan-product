# Audit: #849 Subagent Prompts against agent-prompt-template.md v10.2

## Scope Note

These are focused programmer subagent prompts deployed by the Lead Developer within a single issue. The template is designed for full agent sessions. Requirements marked N/A are legitimately not applicable to focused subagents (e.g., post-compaction protocol for a short-lived agent).

---

## Subagent A Audit (Categories B+C+D+E — Route-Level Fixes)

| # | Template Requirement | Status | Notes |
|---|---------------------|--------|-------|
| 1 | Identity section | ✅ | "Programmer Agent (prog-A)" |
| 2 | Essential context / briefings | N/A | Lead provides all context inline — subagent doesn't need to read briefings |
| 3 | Post-compaction protocol | N/A | Short-lived focused subagent |
| 4 | Infrastructure verification | ⚠️ | No explicit step to verify files exist before editing |
| 5 | Audit cascade discipline | N/A | Subagent is implementing, not writing issues/gameplans |
| 6 | Anti-80% / method enumeration | N/A | Task is line-level fixes, not interface implementation |
| 7 | Session log management | ✅ | Path specified |
| 8 | Mandatory first actions (check what exists) | ⚠️ | No explicit "verify before editing" step |
| 9 | Mission with scope boundaries | ✅ | Clear mission + explicit scope boundaries |
| 10 | Context (issue, state, dependencies) | ✅ | Issue number, KeychainService analysis, exact current state |
| 11 | Evidence requirements | ✅ | 4-item evidence checklist |
| 12 | Constraints | ⚠️ | Not listed as a section — constraints are embedded in exact changes |
| 13 | Multi-agent coordination | ❌ | No mention of Subagent B working in parallel on Category A |
| 14 | Phase 0 mandatory verification | ⚠️ | No explicit verification step |
| 15 | Implementation approach (concrete steps) | ✅ | Extremely detailed "Exact Changes Required" per category |
| 16 | Architecture boundaries | N/A | Route-level changes only |
| 17 | Success criteria with evidence | ⚠️ | Implicit in testing + handoff, not separately listed |
| 18 | Deliverables | ✅ | Clear via handoff format |
| 19 | Cross-validation preparation | ❌ | No markers for Lead's verification |
| 20 | Self-check before claiming complete | ❌ | No self-check checklist |
| 21 | STOP conditions | ✅ | 4 specific conditions |
| 22 | When tests fail protocol | ⚠️ | "Stop and report" present but abbreviated |
| 23 | Handoff format | ✅ | Detailed handoff format with category status |

**Summary**: ✅ 10 | ⚠️ 6 | ❌ 3 | N/A 4

---

## Subagent B Audit (Category A — Calendar Router Threading)

| # | Template Requirement | Status | Notes |
|---|---------------------|--------|-------|
| 1 | Identity section | ✅ | "Programmer Agent (prog-B)" |
| 2 | Essential context / briefings | N/A | Context inline from Lead |
| 3 | Post-compaction protocol | N/A | Short-lived focused subagent |
| 4 | Infrastructure verification | ⚠️ | No explicit step to verify files/methods exist |
| 5 | Audit cascade discipline | N/A | Implementing, not writing issues |
| 6 | Anti-80% / method enumeration | ⚠️ | Method signature safety section covers intent, but no explicit enumeration of all CalendarIntegrationRouter call sites |
| 7 | Session log management | ✅ | Path specified |
| 8 | Mandatory first actions | ⚠️ | No explicit "verify before editing" step |
| 9 | Mission with scope boundaries | ✅ | Clear mission + explicit scope |
| 10 | Context | ✅ | Issue number, CalendarIntegrationRouter analysis, call chains mapped |
| 11 | Evidence requirements | ✅ | 5-item evidence list with method-specific verification |
| 12 | Constraints | ✅ | "Method Signature Change Safety" section explicitly covers constraints |
| 13 | Multi-agent coordination | ❌ | No mention of Subagent A working in parallel |
| 14 | Phase 0 verification | ⚠️ | No explicit verification step |
| 15 | Implementation approach | ✅ | Extremely detailed per-site with call chains |
| 16 | Architecture boundaries | N/A | Service-layer changes within scope |
| 17 | Success criteria | ⚠️ | Implicit, not separately listed |
| 18 | Deliverables | ✅ | Via handoff format |
| 19 | Cross-validation preparation | ❌ | No markers for Lead's verification |
| 20 | Self-check before complete | ❌ | No self-check list |
| 21 | STOP conditions | ✅ | 5 specific conditions |
| 22 | When tests fail protocol | ⚠️ | "Stop and report" present but abbreviated |
| 23 | Handoff format | ✅ | Detailed with method signature tracking |

**Summary**: ✅ 9 | ⚠️ 6 | ❌ 3 | N/A 5

---

## Common Fixes Required (both prompts)

### Fix 1: Add Infrastructure Verification Step (⚠️ #4, #8, #14)
Add to both prompts before "Exact Changes Required":

```markdown
## Pre-Flight Verification (MANDATORY FIRST ACTION)

Before making any changes, verify the files and patterns you'll modify:
1. Confirm each file listed exists at the expected path
2. Confirm the line numbers are approximately correct (code may have shifted)
3. Confirm `current_user` / `user_id` is available where specified
4. Run existing tests BEFORE changes to establish baseline

If reality doesn't match this prompt, STOP and report the mismatch.
```

### Fix 2: Add Multi-Agent Coordination (❌ #13)
Add to Subagent A:
```markdown
## Multi-Agent Coordination
Subagent B is working in parallel on Category A (calendar router threading).
Your scope is B+C+D+E. Do NOT modify any files in:
- services/integrations/calendar/calendar_integration_router.py
- services/integrations/calendar/calendar_plugin.py
- services/intent_service/canonical_handlers.py (unless fixing C3 Notion test)
- services/conversation/conversation_handler.py
- services/intent/intent_service.py (unless fixing C2 connection test callers in integrations.py)
```

Add to Subagent B:
```markdown
## Multi-Agent Coordination
Subagent A is working in parallel on Categories B+C+D+E (route-level fixes).
Your scope is Category A only. Do NOT modify:
- web/api/routes/settings_integrations.py
- web/api/routes/integrations.py
- services/integrations/slack/oauth_handler.py
```

### Fix 3: Add Self-Check Checklist (❌ #20)
Add to both prompts before handoff format:

```markdown
## Self-Check Before Claiming Complete
- [ ] Every site listed in my scope has been modified
- [ ] Every modified method's callers have been verified (no broken call sites)
- [ ] Tests run and output captured (not "tests pass" but actual output)
- [ ] Session log updated with all changes
- [ ] No changes outside my assigned scope
- [ ] STOP conditions checked — none triggered
```

### Fix 4: Add Cross-Validation Markers (❌ #19)
Add to evidence requirements:

```markdown
**Cross-Validation**: For each change, note the before/after pattern so Lead can verify with grep:
- Before: `keychain.get_api_key("github_token")` (grep should return 0 matches after fix)
- After: `keychain.get_api_key("github_token", username=current_user.sub)` (grep should find this)
```

### Fix 5: Strengthen Test Failure Protocol (⚠️ #22)
Expand STOP condition for test failures in both prompts:

```markdown
**When tests fail**: STOP immediately. Report the exact error output. Do NOT decide if the failure is "critical" or "pre-existing" — the Lead Developer decides. Report: which tests fail, exact error messages, whether the failure existed before your changes.
```

---

_Audited: 2026-02-25 by Lead Developer_

---

# Re-Audit: #849 Subagent Prompts (post-fix)

| # | Fix | Subagent A | Subagent B |
|---|-----|-----------|-----------|
| 1 | Pre-flight verification (#4, #8, #14) | ✅ Added with baseline test run | ✅ Added with baseline test run |
| 2 | Multi-agent coordination (#13) | ✅ Added with file-scope boundaries | ✅ Added with file-scope boundaries |
| 3 | Self-check checklist (#20) | ✅ 6-item checklist | ✅ 7-item checklist |
| 4 | Cross-validation markers (#19) | ✅ Added grep examples to evidence | ✅ Added grep examples to evidence |
| 5 | Test failure protocol (#22) | ✅ Expanded with explicit "Lead decides" language | ✅ Expanded with explicit "Lead decides" language |

**Result: All 5 fixes applied to both prompts.** Remaining ⚠️ items (Essential Context, Architecture Boundaries, etc.) are legitimately N/A for focused subagents deployed by Lead Developer with inline context.

_Re-audited: 2026-02-25 by Lead Developer_

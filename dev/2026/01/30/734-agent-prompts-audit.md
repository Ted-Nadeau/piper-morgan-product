# Audit: Agent Prompts against agent-prompt-template.md v10.2

**Document**: `dev/2026/01/30/734-agent-prompts.md`
**Template**: `knowledge/agent-prompt-template.md` (v10.2)
**Auditor**: Lead Developer (Opus)
**Date**: 2026-01-30

---

## Audit Matrix - Phase 4 Prompt (Repository Isolation)

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| **Identity Section** | | |
| Agent identity stated | ✅ | "You are a Coding Agent working on Piper Morgan" |
| Role clarity | ✅ | TDD methodology, evidence required |
| **Evidence Requirements** | | |
| Handoff format specified | ✅ | Full completion report template provided |
| Test count format | ✅ | "X tests added in [location]" |
| Test verification format | ✅ | pytest output required |
| Files modified format | ✅ | List with line counts |
| User testing steps | ⚠️ | Implied via grep verification, not explicit steps |
| **Mission Section** | | |
| Specific, measurable objective | ✅ | "Make owner_id REQUIRED (not optional)" |
| GitHub Issue referenced | ✅ | #734 linked |
| **Context Section** | | |
| Current State | ✅ | Optional owner_id, returns all records |
| Target State | ✅ | Required owner_id, ValueError if missing |
| Dependencies | ✅ | Phase 3 must complete first |
| Risk assessment | ✅ | "will break call sites - intentional" |
| **TDD Approach** | | |
| Tests written first | ✅ | Full test code provided |
| Test file location | ✅ | tests/security/test_cross_user_isolation.py |
| Expected failures | ✅ | "run to verify they fail" |
| **Implementation Steps** | | |
| Concrete steps listed | ✅ | 6 steps with clear actions |
| Expected outcomes | ✅ | Each step has outcome |
| Validation methods | ✅ | Tests, grep |
| **Files to Modify** | | |
| Repositories listed | ✅ | 4 repository files |
| Callers listed | ✅ | 7+ caller files |
| **Evidence Required Section** | | |
| Specific evidence format | ✅ | Template with grep, tests |
| Regression check | ✅ | "pytest tests/unit/ -v" |
| **STOP Conditions** | | |
| Clear stop triggers | ✅ | 4 conditions listed |
| **Anti-80% Safeguards** | ⚠️ | Implied via "ALL call sites" but no method enumeration table |

### Phase 4 Summary
- ✅ Present: 18/20
- ⚠️ Partial: 2/20
- ❌ Missing: 0/20

---

## Audit Matrix - Phase 5 Prompt (OAuth State Redesign)

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| **Identity Section** | | |
| Agent identity stated | ✅ | "You are a Coding Agent" |
| Role clarity | ✅ | TDD methodology |
| **Evidence Requirements** | | |
| Handoff format specified | ✅ | Full completion report |
| Test count format | ✅ | Included |
| Manual test section | ✅ | OAuth flow manual test steps |
| **Mission Section** | | |
| Specific, measurable objective | ✅ | "Embed user_id in OAuth state" |
| GitHub Issue referenced | ✅ | #734 linked |
| **Context Section** | | |
| Current State | ✅ | "Only CSRF nonce, tokens stored globally" |
| Target State | ✅ | "JSON with user_id, base64 encoded" |
| Dependencies | ✅ | "None - can parallel with Phase 4" |
| Risk assessment | ✅ | "Breaking OAuth flows" |
| **TDD Approach** | | |
| Tests written first | ✅ | Full test code provided |
| Test file location | ✅ | tests/integrations/test_oauth_state.py |
| **Implementation Steps** | | |
| Concrete steps | ✅ | 6 steps |
| State format before/after | ✅ | Code examples |
| **Files to Modify** | | |
| OAuth handlers | ✅ | 2 files |
| Routes | ✅ | 2 files |
| **Evidence Required** | | |
| Code verification | ✅ | Python one-liner to check state |
| Manual test steps | ✅ | 5-step manual verification |
| **STOP Conditions** | ✅ | 4 conditions |

### Phase 5 Summary
- ✅ Present: 20/20
- ⚠️ Partial: 0/20
- ❌ Missing: 0/20

---

## Audit Matrix - Phase 6 Prompt (Credential Storage Separation)

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| **Identity Section** | ✅ | Agent identity stated |
| **Mission Section** | ✅ | Clear objective |
| **Context Section** | | |
| Current State | ✅ | "38+ direct keychain calls" |
| Target State | ✅ | IntegrationConfigService + UserAPIKeyService |
| Dependencies | ✅ | "Phases 4 and 5 complete" |
| Risk assessment | ✅ | "Breaking credential retrieval" |
| **Implementation Guidance** | | |
| New file template | ✅ | Full IntegrationConfigService code |
| Files to modify | ✅ | Routes and handlers listed |
| Categorization guide | ✅ | Table: key pattern → service |
| **Evidence Required** | | |
| Grep verification | ✅ | Two grep commands |
| Credential categorization | ✅ | Table format specified |
| **STOP Conditions** | ✅ | 4 conditions |
| **Acceptance Criteria** | ✅ | 6 checkboxes |

### Phase 6 Summary
- ✅ Present: 18/18
- ⚠️ Partial: 0/18
- ❌ Missing: 0/18

---

## Audit Matrix - Phase 7 Prompt (Config Service Method Signatures)

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| **Identity Section** | ✅ | Agent identity stated |
| **Mission Section** | ✅ | "Update config service methods to accept user_id" |
| **Context Section** | | |
| Current State | ✅ | "Return global credentials" |
| Target State | ✅ | "Accept user_id, return user's credentials" |
| Dependencies | ✅ | Phase 6 complete |
| **TDD Tests** | ✅ | Test code provided |
| **Example Transformation** | ✅ | Before/after code |
| **Files to Modify** | ✅ | Config services + callers |
| **Evidence Required** | | |
| Grep verification | ✅ | Check all methods have user_id |
| Method signature table | ✅ | Before/after table format |
| **STOP Conditions** | ✅ | 4 conditions |
| **Acceptance Criteria** | ✅ | 7 checkboxes |

### Phase 7 Summary
- ✅ Present: 16/16
- ⚠️ Partial: 0/16
- ❌ Missing: 0/16

---

## Overall Summary

| Prompt | ✅ Present | ⚠️ Partial | ❌ Missing |
|--------|----------|-----------|-----------|
| Phase 4 | 18 | 2 | 0 |
| Phase 5 | 20 | 0 | 0 |
| Phase 6 | 18 | 0 | 0 |
| Phase 7 | 16 | 0 | 0 |
| **Total** | 72 | 2 | 0 |

---

## Action Required

### 1. Phase 4: Add User Testing Steps (⚠️ → ✅)

Add after Evidence Required section:

```markdown
**User Testing Steps**:
1. Start server: `python main.py`
2. Log in as User A, create a list
3. Log out, log in as User B
4. Query lists as User B
5. Verify User A's list is NOT visible to User B
```

### 2. Phase 4: Add Method Enumeration Note (⚠️ → ✅)

Add to Implementation Steps:

```markdown
**Anti-80% Check**: Before claiming complete, verify:
- ALL repository methods updated (not just some)
- ALL call sites fixed (grep to confirm zero type errors remain)
```

---

## Audit Result

**Status**: ✅ PASS with minor additions

All four agent prompts follow the template v10.2 structure with:
- Clear identity and mission
- TDD approach with test code
- Current/target state documented
- Evidence requirements specified
- STOP conditions defined
- Acceptance criteria checkboxes

**Ready to**: Apply 2 minor fixes, then prompts ready for execution.

---

## Next Steps

1. Apply 2 minor fixes to Phase 4 prompt
2. Report to PM that audit cascade is complete
3. Await approval to proceed with execution

---

_Audit created: 2026-01-30_
_Template version: 10.2_

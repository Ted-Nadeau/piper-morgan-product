# Audit: #766 GLUE-MAINPROJ against feature.md template

**Phase**: Issue → Gameplan transition
**Date**: 2026-02-16
**Auditor**: Lead Developer
**PM note**: Treating as feature/fix issue per PM guidance (not bug report template)

## Audit Matrix

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| **Header/Metadata** | | |
| Priority | ✅ | P0 |
| Labels | ✅ | `bug`, `glue` |
| Milestone | ✅ | MVP |
| Epic | ✅ | #762 GLUE |
| Related | ⚠️ | Lists Pattern-053 and impl guide section 5.3, but no related issue numbers |
| **Problem Statement** | | |
| Current State | ✅ | Clear: "asks 'Is that your main project?' after every project entry" |
| Impact - Blocks | ❌ | Not stated. What does this block? |
| Impact - User Impact | ✅ | Implicit: makes Piper feel robotic, annoying after 3rd project |
| Impact - Technical Debt | ❌ | Not stated |
| Strategic Context | ⚠️ | Implicit through epic linkage to PDR-002, but not explicit in issue |
| **Goal** | | |
| Primary Objective | ⚠️ | Implicit across solution options but not stated as one sentence |
| Example User Experience | ✅ | Before scenario shown. After scenarios in solution options. |
| Not In Scope | ❌ | Not stated — what's explicitly out? |
| **What Already Exists** | | |
| Infrastructure ✅ | ❌ | Not documented. What code currently handles this? |
| What's Missing ❌ | ❌ | Not documented as specific gaps |
| **Requirements** | | |
| Phase 0: Investigation | ❌ | No investigation phase defined |
| Phase 1+ tasks | ❌ | No phased tasks — only solution options |
| Phase Z: Completion | ❌ | No completion/handoff checklist |
| **Acceptance Criteria** | | |
| Functionality | ✅ | 5 checkboxes including Colleague Test |
| Testing | ❌ | No test requirements specified |
| Quality | ❌ | No quality criteria (regressions, performance) |
| Documentation | ❌ | No documentation requirements |
| **Completion Matrix** | ❌ | Not present |
| **Testing Strategy** | ❌ | Not present |
| **Success Metrics** | ❌ | Not present (quantitative/qualitative) |
| **STOP Conditions** | ❌ | Not present |
| **Effort Estimate** | ⚠️ | "1-2 days" stated but no phase breakdown |
| **Dependencies** | ❌ | Not stated |
| **Related Documentation** | ⚠️ | Pattern-053 and impl guide referenced but not ADRs |

## Summary

| Status | Count |
|--------|-------|
| ✅ Present | 9 |
| ⚠️ Partial | 5 |
| ❌ Missing | 15 |

## Assessment

The issue captures the **problem and acceptance criteria well** but is missing most of the structural scaffolding from the feature template: phased requirements, testing strategy, completion matrix, dependencies, stop conditions, and "what already exists."

This makes sense — it was written as a sprint planning spec, not a full implementation issue. The question is: **do we enrich the issue itself, or capture the missing elements in the gameplan?**

## Recommendation

Given this is a 1-2 day bug fix (the smallest M0 issue), I'd recommend:

1. **Fix the critical gaps in the issue** (what already exists, dependencies, not-in-scope)
2. **Let the gameplan carry** the phased requirements, testing strategy, and completion matrix
3. **Don't over-scaffold** a focused bug fix with heavyweight process

### Critical gaps to fix before gameplan:
1. **What Already Exists**: Need to trace the actual code that produces this behavior
2. **Not In Scope**: Clarify boundaries (e.g., not redesigning entire setup wizard)
3. **Dependencies**: Confirm none, or list them

### Gameplan should include:
- Phased implementation plan
- Testing strategy
- Completion matrix
- STOP conditions

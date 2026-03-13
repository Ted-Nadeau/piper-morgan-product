# Phase Nomenclature Clarification

**Date**: November 22, 2025, 12:15 PM
**Issue**: Confusion between original gameplan phases and actual implementation phases

---

## Two Numbering Systems

### Original Gameplan Phases (gameplan-sec-rbac-implementation.md)
1. Phase -1: Verification with PM
2. Phase 0: Security Audit & Investigation
3. **Phase 1**: Database Schema (Role/Permission tables)
4. **Phase 2**: Authorization Service
5. **Phase 3**: API Protection (decorators & middleware)
6. **Phase 4**: Comprehensive Testing & Security Scan
7. Phase Z: Final Bookending & Security Sign-Off

### Our Actual Implementation Phases (what we built)
1. **Phase 1**: Owner-Based Access Control
   - Phase 1.1: Database schema (owner_id columns)
   - Phase 1.2: Service layer ownership checks
   - Phase 1.3: Endpoint protection
   - Phase 1.4: Shared resource access
2. **Phase 2**: Role-Based Permissions (VIEWER/EDITOR/ADMIN)
3. **Phase 3**: ??? (what we're about to do)

---

## What Phase 3 Includes (Current Prompt)

The Phase 3 prompt I just created includes:
- ✅ System-wide admin role
- ✅ Automated cross-user access tests
- ✅ Security scan (Bandit, Safety)
- ✅ Extend to Projects/Files
- ✅ Update & close Issue #357

**This maps to**:
- Original Gameplan Phase 4 (Testing & Security Scan)
- Original Gameplan Phase Z (Final Sign-Off)

---

## The Question

**Should we**:

**Option A: Keep as "Phase 3"** (single consolidated phase)
- Phase 3 includes: Admin role + Tests + Security + Projects/Files + Closure
- Simpler numbering
- Matches our pattern (Phase 1, Phase 2, Phase 3)

**Option B: Split into Phases 3, 4, and Z** (match original gameplan)
- Phase 3: Admin role + Extend to Projects/Files
- Phase 4: Automated tests + Security scan
- Phase Z: Final sign-off + close Issue #357

**Option C: Rename to "Phase 3 Final"** or "Phase 3 Complete"
- Indicates this is the last phase
- Acknowledges it includes multiple original phases

---

## Recommendation

**Option A: Keep as "Phase 3"**

**Rationale**:
1. We've already deviated from original gameplan (ADR-044)
2. Our phase numbering reflects our architecture (Phases 1-3)
3. Simpler for Code agent to understand
4. All work is logically grouped (complete Issue #357)
5. Phase 3 already has STOP condition (splits it internally)

**Naming**:
- Current: "Phase 3: Completion & Testing"
- This clearly indicates it's the final phase

---

## What PM Might Prefer

If you want to match original gameplan more closely:

**Phase 3**: Admin Role + Extend Resources
- System-wide admin (`users.is_admin`)
- Extend to Projects/Files (role-based sharing)
- Estimated: 2 hours

**Phase 4**: Testing & Security
- Automated cross-user tests (20+ test cases)
- Security scan (Bandit, Safety)
- Estimated: 2 hours

**Phase Z**: Final Sign-Off
- Update Issue #357
- Close issue
- Estimated: 30 min

**Total**: Still 3-4 hours, just split into 3 prompts instead of 1

---

## Decision Needed

PM, which do you prefer?

**[ ] Option A**: Keep current "Phase 3" (single consolidated phase)
- Simpler, already created, ready to go

**[ ] Option B**: Split into Phases 3, 4, Z (match original gameplan)
- More granular, better tracking, clearer milestones

**[ ] Option C**: Rename to something clearer
- "Phase 3 Final", "Phase 3 Complete", "Phase 3: Completion"

---

_Clarification prepared by: Lead Developer (Claude Sonnet)_
_Date: November 22, 2025, 12:15 PM_

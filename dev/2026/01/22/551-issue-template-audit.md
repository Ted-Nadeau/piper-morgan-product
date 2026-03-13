# Issue Template Audit: #551 ARCH-COMMANDS

**Issue**: #551 ARCH-COMMANDS: Command Parity Across Interfaces
**Template Version**: Standard Feature Template
**Audit Date**: 2026-01-22

---

## Template Compliance Checklist

| Template Section | Present? | Quality | Notes |
|------------------|----------|---------|-------|
| **Header** | | | |
| Priority | ✅ Yes | Good | P2 stated |
| Labels | ✅ Yes | Good | `epic`, `architecture` |
| Milestone | ⚠️ Partial | OK | "TBD (Phase 1 targetable for I1)" |
| Epic | ✅ Yes | Good | Standalone initiative noted |
| Related | ✅ Yes | Good | #491, #520 referenced |
| **Problem Statement** | | | |
| Current State | ✅ Yes | Excellent | Detailed inventory tables |
| Impact | ✅ Yes | Good | 4 impacts listed |
| Strategic Context | ✅ Yes | Good | Parity goal explained |
| **Goal** | | | |
| Primary Objective | ✅ Yes | Good | Single source of truth |
| Example User Experience | ⚠️ Partial | OK | Parity examples but no before/after |
| Not In Scope | ✅ Yes | Good | 3 explicit exclusions |
| **What Already Exists** | | | |
| Infrastructure ✅ | ✅ Yes | Excellent | 6 registration points documented |
| What's Missing ❌ | ✅ Yes | Good | Parity matrix shows gaps |
| **Requirements** | | | |
| Phase 0: Investigation | ❌ Missing | - | No Phase -1/0 verification |
| Phases 1-N | ✅ Yes | Good | 3 phases with deliverables |
| Phase Z: Completion | ❌ Missing | - | No explicit handoff phase |
| **Acceptance Criteria** | | | |
| Per-Phase Criteria | ✅ Yes | Good | Phase 1, 2, 3 criteria listed |
| Functionality | ✅ Yes | Good | Clear deliverables |
| Testing | ⚠️ Partial | OK | Phase 3 mentions tests |
| Quality | ⚠️ Implicit | - | No explicit quality gates |
| Documentation | ⚠️ Implicit | - | ADR mentioned but no other docs |
| **Completion Matrix** | ❌ Missing | - | No matrix |
| **Testing Strategy** | ❌ Missing | - | No test scenarios |
| **Success Metrics** | ❌ Missing | - | No quantitative measures |
| **STOP Conditions** | ❌ Missing | - | No explicit stop conditions |
| **Effort Estimate** | ❌ Missing | - | No size estimate per phase |
| **Dependencies** | ✅ Yes | Good | #491, #520 listed |
| **Risk Assessment** | ✅ Yes | Good | Per-phase risk levels |
| **Open Questions** | ✅ Yes | Good | 4 questions listed |
| **Technical Considerations** | ✅ Yes | Excellent | Schema, integration points |

---

## Compliance Score

| Category | Score |
|----------|-------|
| Header/Metadata | 90% |
| Problem Statement | 95% |
| Goal/Scope | 85% |
| What Exists | 95% |
| Requirements | 70% |
| Acceptance Criteria | 75% |
| Completion Tracking | 30% |
| Risk/Dependencies | 90% |

**Overall**: **78%** - Good foundation, missing completion discipline elements

---

## Gaps to Address

### Critical Gaps (Must Fix)

1. **No Phase -1 Infrastructure Verification**
   - Issue assumes current inventory is accurate
   - Should verify: Do all listed commands actually exist? Any new ones added since?

2. **No Completion Matrix**
   - 3 phases with multiple deliverables need tracking
   - Add matrix with evidence requirements

3. **No STOP Conditions**
   - When should research halt for PM review?
   - What if inventory reveals 100+ commands? Scope explosion risk

4. **No Effort Estimate**
   - Phase 1 (research) size?
   - Phase 2 (design) size?
   - Phase 3 (implementation) size?

### Moderate Gaps (Should Fix)

5. **No Phase Z Handoff**
   - How does Phase 1 deliverable get reviewed?
   - What's the gate between phases?

6. **No Success Metrics**
   - How do we know inventory is "complete"?
   - What % parity is acceptable?

7. **No Testing Strategy for Phase 1**
   - How do we verify inventory accuracy?
   - Spot-check commands actually work?

### Minor Gaps (Nice to Have)

8. **Example Before/After**
   - Add: "Today: user types /standup in Slack but 'standup' in web fails"
   - After: "Both work identically"

---

## Recommended Issue Updates

### Add Phase -1: Infrastructure Verification

```markdown
### Phase -1: Verification Checkpoint

Before deep inventory:
- [ ] Verify `cli/commands/` directory structure matches expectations
- [ ] Verify `pre_classifier.py` pattern structure unchanged
- [ ] Verify Slack webhook router structure unchanged
- [ ] Confirm no new interfaces added since issue creation

**STOP if**: Major structural changes discovered - revise approach first.
```

### Add Completion Matrix

```markdown
## Completion Matrix

| Phase | Deliverable | Evidence | Status |
|-------|-------------|----------|--------|
| 1 | CLI commands inventory | Document link | ⬜ |
| 1 | Web chat patterns inventory | Document link | ⬜ |
| 1 | Slack commands inventory | Document link | ⬜ |
| 1 | URL routes inventory | Document link | ⬜ |
| 1 | Gap/inconsistency classification | Document link | ⬜ |
| 1 | PM review complete | Approval comment | ⬜ |
| 2 | ADR written | ADR link | ⬜ |
| 2 | Schema defined | Code/doc link | ⬜ |
| 2 | Effort estimate | Document link | ⬜ |
| 3 | Registry implemented | PR link | ⬜ |
| 3 | Commands migrated | Test output | ⬜ |
| 3 | Parity verified | Test output | ⬜ |
```

### Add STOP Conditions

```markdown
## STOP Conditions

**STOP and escalate to PM if**:
- Inventory reveals >50 unique commands (scope explosion)
- Major interface discovered not in original list
- Existing command implementations are broken/incomplete
- Pattern structure differs significantly from assumptions
- Phase 1 taking >2 sessions without clear progress
```

### Add Effort Estimate

```markdown
## Effort Estimate

| Phase | Size | Notes |
|-------|------|-------|
| Phase -1 | Small | Verification only |
| Phase 1 | Medium | Deep research, 4 interfaces |
| Phase 2 | Medium | ADR + schema design |
| Phase 3 | Large | Implementation + migration |
```

### Add Success Metrics

```markdown
## Success Metrics

### Phase 1 Success
- 100% of commands in each interface cataloged
- Each command classified (gap/inconsistency/intentional)
- Parity matrix complete with no ❓ remaining

### Phase 2 Success
- ADR approved by architecture review
- Schema supports all discovered commands
- Implementation effort estimated to ±20% accuracy

### Phase 3 Success
- 0 commands break during migration
- All parity gaps either closed or documented as intentional
- `_get_slash_commands()` returns dynamic list
```

---

## Questions for PM Before Gameplan

1. **Scope for I1**: Phase 1 only, or Phase 1 + Phase 2?

2. **Inventory Format**: Markdown document, spreadsheet, or structured data file?

3. **Review Gate**: Async review of Phase 1 deliverable, or sync session?

4. **Command Count Threshold**: At what point is scope too large? (50? 100?)

---

## Verdict

**Issue Quality**: Good - well-structured problem statement and phased approach

**Ready for Gameplan**: YES, with minor additions above

**Recommendation**: Add completion matrix and STOP conditions to issue before gameplan, or include in gameplan Phase -1.

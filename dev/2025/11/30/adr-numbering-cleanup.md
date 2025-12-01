# Update ADR References and Documentation

**Type**: Documentation Update
**Priority**: P1 - Immediate
**Estimated Time**: 1 hour
**GitHub Issue**: None (maintenance task)

## Context

We've decided that ADR numbers should be assigned at writing time, not planning time. Several documents currently reference specific future ADR numbers (like ADR-046, ADR-047) that haven't been written yet. We need to update these references to be more flexible.

Additionally, ADR-046 has now been written (micro-format agent architecture), so the ADR index needs updating.

## Scope

**In Scope:**
1. Add ADR-046 to the ADR index/README
2. Update MUX issue references to remove specific ADR numbers
3. Update roadmap references to remove specific ADR numbers
4. Verify no other documents have prescriptive ADR numbering

**Out of Scope:**
- Changing existing ADR numbers
- Creating new ADRs
- Modifying ADR content (only index updates)

## Acceptance Criteria

- [ ] ADR-046 added to `/docs/internal/architecture/current/adrs/README.md`
- [ ] GitHub issues updated to say "ADR documenting [concept]" instead of "ADR-046" or "ADR-047"
- [ ] Roadmap v12.2 updated to remove specific future ADR numbers
- [ ] Any other prescriptive numbering found and fixed
- [ ] All changes committed with clear message

## Specific Changes Needed

### 1. Add to ADR Index
In `/docs/internal/architecture/current/adrs/README.md`, add:
```markdown
- ADR-046: Micro-Format Agent Architecture (Proposed) - Ted Nadeau's micro-format processing pipeline
```

### 2. Update GitHub Issues
Search for issues mentioning specific future ADR numbers. Change:
- "ADR-046 documenting object model decisions" → "ADR documenting object model decisions"
- "ADR-047 documenting [whatever]" → "ADR documenting [whatever]"

Likely issues to check:
- VISION-OBJECT-MODEL issue
- Any MUX-VISION issues
- Any MUX-TECH issues

### 3. Update Roadmap
In `roadmap-v12.2.md` (and any other roadmap versions), change:
- References to specific future ADR numbers → generic "ADR documenting X"

### 4. Search for Other References
Use grep or GitHub search to find any other documents with patterns like:
- "ADR-04[6-9]" (future numbers)
- "will be ADR-"
- "future ADR-"

## Resources

- Current ADR index: `/docs/internal/architecture/current/adrs/README.md`
- New ADR-046: `/docs/internal/architecture/current/adrs/ADR-046-micro-format-agent-architecture.md`
- Roadmap: `/docs/roadmap-v12.2.md`
- GitHub issues: Check MUX epic and related issues

## Deliverables

1. Updated ADR README with ADR-046 entry
2. Updated GitHub issues with flexible ADR references
3. Updated roadmap with flexible ADR references
4. Commit message: "Update ADR references to use flexible numbering"

## Verification

After updates:
1. Confirm ADR index lists all ADRs 001-046
2. Confirm no unwritten ADR numbers are referenced
3. Confirm all ADR references either point to existing ADRs or say "ADR documenting X"

---

*Note: This is a maintenance task to improve documentation flexibility. ADR numbers should be assigned when ADRs are written, not when they're planned.*

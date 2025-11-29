# Prompt for Code: Synthesize Duplicate Issues

## Your Task
Synthesize the following pairs of duplicate issues into single, comprehensive issues using our standard feature template. Each pair contains overlapping content that needs to be merged intelligently.

## Template to Use
Use the feature template from `.github/issue_template/feature.md` for structure. Keep all sections.

## Duplicate Pairs to Synthesize

### Pair 1: Encryption at Rest
- Issue #324: `security: Implement encryption at rest for sensitive data`
- Issue #358: `SEC-ENCRYPT-ATREST: Implement Encryption at Rest for Sensitive Data`
- **Keep**: #358 (has canonical name)
- **Close**: #324

### Pair 2: Database Indexes
- Issue #320: `perf: Add missing database indexes for MVP query performance`
- Issue #356: `PERF-INDEX: Add Missing Composite Database Indexes`
- **Keep**: #356 (has canonical name)
- **Close**: #320

### Pair 3: Soft Delete Strategy
- Issue #333: `data: Implement soft delete strategy across domain models`
- Issue #336: `data: Implement soft delete strategy across domain models`
- **Keep**: #336
- **Close**: #333
- **Add canonical name**: DATA-SOFT-DELETE

### Pair 4: Stored Procedures Documentation
- Issue #331: `docs: Document application-layer stored procedures pattern (ADR)`
- Issue #332: `docs: Document application-layer stored procedures pattern (ADR)`
- **Keep**: #332
- **Close**: #331
- **Add canonical name**: DOCS-STORED-PROCS

### Pair 5: Migration Rollback Testing
- Issue #334: `infra: Create database migration rollback testing strategy`
- Issue #338: `infra: Create database migration rollback testing strategy`
- **Keep**: #338
- **Close**: #334
- **Add canonical name**: INFRA-MIGRATION-ROLLBACK

### Pair 6: Prefixed Primary Keys
- Issue #335: `style: Adopt prefixed primary key naming convention for new tables`
- Issue #339: `style: Adopt prefixed primary key naming convention`
- **Keep**: #339
- **Close**: #335
- **Add canonical name**: STYLE-PK-PREFIX

### Pair 7: Singular Table Names
- Issue #337: `style: Adopt singular table naming convention for new tables`
- Issue #340: `style: Adopt singular table naming convention`
- **Keep**: #340
- **Close**: #337
- **Add canonical name**: STYLE-TABLE-SINGULAR

### Pair 8: Windows Clone Issue
- Issue #319: `fix: Windows compatibility - Remove colon from archive filename`
- Issue #353: `BUG: Windows Git Clone Fails - Illegal Character in Filename`
- **Keep**: #353 (has canonical name)
- **Close**: #319

## Synthesis Guidelines

1. **Merge content intelligently**:
   - Take the best problem statement from either issue
   - Combine acceptance criteria (remove duplicates)
   - Use the higher effort estimate if they differ
   - Merge any code examples or technical details

2. **Prioritization**:
   - If priorities differ, use the higher one
   - If one mentions Ted Nadeau or architectural review, include that context

3. **Format**:
   - Use the canonical name as the title
   - Follow the feature template structure exactly
   - Include completion matrix
   - Add STOP conditions

4. **Output**:
   - Create one markdown file per synthesized issue
   - Name files: `issue-[CANONICAL-NAME]-synthesized.md`
   - Place in `/mnt/user-data/outputs/`

## Example Output Structure

```markdown
# [CANONICAL-NAME] - [Full Title]

**Priority**: P0/P1/P2/P3
**Labels**: `[primary]`, `[secondary]`
**Milestone**: [Sprint or MVP]
**Epic**: [If applicable]

## Problem Statement
[Merged from both issues]

## Goal
[Best objective from either]

## Acceptance Criteria
[Combined list, no duplicates]

[... rest of template sections ...]
```

## After Synthesis

Report back with:
1. List of files created
2. Any conflicts that needed resolution
3. Recommendations for priority adjustments

---

*Note: The PM will close the duplicate issues and update the kept issues with the synthesized content.*

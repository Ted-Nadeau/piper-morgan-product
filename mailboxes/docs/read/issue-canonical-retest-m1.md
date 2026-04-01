# Issue: CANONICAL-RETEST — Post-M0 Canonical Query Validation

## Summary

Re-run the canonical query test suite against v0.8.6 to measure M0's impact on query handling. M0 (Conversational Glue) was designed to improve natural language understanding — this validates whether it worked and identifies remaining gaps for M1 prioritization.

## Context

- **Last known baseline**: ~68% of canonical queries working (pre-M0)
- **M0 shipped**: v0.8.6 on March 4, 2026
- **M0 scope included**: Soft invocation, multi-intent handling, slot filling, follow-up recognition, lens integration
- **Canonical query reference**: `canonical-queries-v2.md` (63 queries across 14 categories)

## Acceptance Criteria

- [ ] Run full canonical query test matrix against v0.8.6
- [ ] Document results by category (14 categories)
- [ ] Calculate new pass rate (target: measurable improvement over 68%)
- [ ] Identify specific failing queries with failure mode classification
- [ ] Produce summary report with M1 prioritization recommendations

## Failure Mode Classification

When documenting failures, classify as:

| Mode | Description | Example |
|------|-------------|---------|
| **ROUTING** | Query reaches wrong handler | "Show my issues" → projects domain |
| **PARSING** | Intent understood, entities not extracted | "Create issue for Project X" → project name lost |
| **INTEGRATION** | Correct routing, backend fails | Calendar query routes correctly but returns error |
| **RESPONSE** | Correct result, poor presentation | Raw data instead of conversational summary |
| **WIRING** | Components work individually, composition fails | Slot filling works in isolation, not in flow |

## Deliverables

1. **Test Results CSV**: Query, Category, Pass/Fail, Failure Mode, Notes
2. **Summary Report**: Overall stats, category breakdown, top failure patterns
3. **M1 Recommendations**: Which failures should influence M1 priorities?

## Effort Estimate

- **Scope**: Diagnostic (run existing tests, document results)
- **Estimate**: 2-4 hours
- **Risk**: Low — bounded by existing test suite

## Sprint

M1 — Week 1 (early diagnostic to inform priorities)

## Labels

`testing`, `diagnostic`, `m1-sprint`, `canonical-queries`

---

*Issue drafted by PPM, March 11, 2026*

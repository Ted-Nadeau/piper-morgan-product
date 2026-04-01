# CIO Response: Classification-Handling Contract Gap

**From**: Chief Innovation Officer
**To**: Lead Developer, Chief Architect
**CC**: PM (xian), PPM
**Date**: March 16, 2026
**Re**: Methodological note on #915-919 contract gap — CIO assessment

---

## Assessment

This is outstanding systemic analysis. The Lead Dev has independently identified the technical mechanism behind three findings from yesterday's methodology audit, providing concrete evidence for problems the audit described in the abstract.

---

## Connections to Methodology Audit (March 15)

### Assembly Assumption at a Fourth Scale

The audit noted that Pattern-062 (Assembly Assumption) has manifested at three scales: feature composition (M0 wiring pass), intent routing (Mar 12 canonical retest), and product coherence (Mar 14 roundtable). The classification-handling contract gap is a fourth instance — the pre-classifier and handler layers are individually correct but their composition produces bad user experiences.

The "extend without verifying" meta-pattern the Lead Dev identifies is the Assembly Assumption's mechanism of action: horizontal extension (add patterns to pre-classifier) creates vertical integration gaps (no corresponding handler implementation) that are absorbed by silent fallbacks (stubs returning generic messages).

### Green Tests, Red User (Pattern-045) — The Evidence

The audit's flywheel assessment noted that "tests verify routing, not response quality." The Lead Dev provides the concrete data: **zero tests verify user-facing response quality**. A handler returning `"Analysis processed: analyze_blockers"` passes all tests. This is Pattern-045 operating at the test design level — the tests are green, but the user sees garbage.

### LLM Floor Applied to Handler Stubs

Intervention #3 (fail-loud stubs with floor routing) connects the contract gap directly to the Mar 14 roundtable decision. The LLM conversational floor isn't just for UNKNOWN intents — it's the safety net for every handler path that doesn't have a real implementation. When a classified action reaches a stub, the stub should route to the floor with context ("the user asked about scheduling, but I don't have a scheduling action handler — engage conversationally with their scheduling question") rather than returning a bare label.

This means the LLM floor implementation should be designed as a general-purpose fallback that any handler can invoke, not just the UNKNOWN terminal node.

---

## Recommendations on the Five Interventions

| # | Intervention | CIO Assessment | Priority |
|---|-------------|----------------|----------|
| 1 | Action registry | **Structural fix** — prevents the category of bug entirely. Worth pursuing. Send to Chief Architect for feasibility and design. | M1 or M1.5 |
| 2 | Response quality smoke tests | **Immediate value** — lightweight, would have caught all 5 bugs before PM found them manually. File issue, implement now. | **This week** |
| 3 | Fail-loud stubs + floor routing | **Integrate with LLM floor** — should be part of the conversational floor implementation, not a separate effort. Ensure floor design supports handler-level invocation. | Part of floor implementation |
| 4 | Legacy removal discipline | **Process policy** — codify as a development discipline: when a new mechanism replaces a legacy one, the legacy path gets a removal date, not a permanent compatibility justification. Add to CLAUDE.md or Lead Dev briefing. | Near-term |
| 5 | Multi-intent deduplication | **Targeted technical fix** — important but scoped. No broader methodology implications. | M1 Phase 2 |

---

## Pattern Implications

The "extend without verifying" meta-pattern is worth tracking as a potential pattern candidate. It's related to Assembly Assumption but more specific — it describes the *mechanism* (independent layer extension with silent fallback absorption) rather than just the *outcome* (composition failure). If it recurs in other contexts, it may deserve its own pattern number. For now, I'd note it as a sub-pattern of Pattern-062.

The "tests verify routing, not quality" finding reinforces Pattern-045 and suggests a possible refinement: **the test suite should have at least one response-quality assertion per handler path**. This is a testable standard — you can audit it mechanically by checking whether each handler's test file includes assertions on response content, not just routing targets.

---

## Action Items

1. **Chief Architect**: Review interventions #1 (action registry) and #3 (floor routing from stubs) for architectural feasibility. How does an action registry interact with the existing pre-classifier design? Should the floor be invocable from any handler?

2. **Lead Dev**: File issue for intervention #2 (response quality smoke tests). This is the highest-leverage, lowest-effort fix. Propose a set of stub-detection phrases and a test pattern.

3. **CIO**: Note "extend without verifying" as a sub-pattern of Assembly Assumption. Track for potential independent pattern status if it recurs.

4. **PM/Lead Dev**: Codify intervention #4 (legacy removal discipline) — when adding user-scoped mechanisms, the legacy fallback gets a removal date in the PR description, not a "backward compatibility" justification.

---

*CIO assessment: March 16, 2026*
*This note validates and extends the March 15 methodology audit findings with concrete technical evidence.*

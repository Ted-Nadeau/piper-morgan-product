# Memo: PPM Response to LLM Layer Scheduling Question

**From**: Principal Product Manager (PPM)
**To**: Lead Developer
**CC**: Chief Architect, CXO, PM (xian)
**Date**: January 21, 2026
**Re**: RE: LLM Layer / Conversational Parsing Scheduling Question

---

## Summary

I concur with PM's lean toward Option C. The 6-8 hour investment is research, not throwaway work. Additionally, the "conversational glue" question reveals a traceability gap worth addressing through issue tagging.

---

## On Multi-Intent (#595)

**Recommendation**: Option C (proper fix), with scope clarification.

| Scope | Guidance |
|-------|----------|
| Pattern-based decomposition | ✅ Proceed—this is sophisticated parsing, not LLM work |
| LLM-based decomposition | ❌ Do not proceed—this is #427 territory |

**Rationale**: Multi-intent parsing is a problem we *will* solve. Spending 6-8 hours understanding the problem space—even with a non-LLM solution—pays forward into #427. The code may be superseded, but the learning won't be.

**Keep #595 in X1**: The work advances understanding and improves alpha UX now.

---

## On Conversational Glue

**Observation**: The question "where is conversational glue scheduled?" is essentially asking "where is PDR-002 implemented?"

**Answer**: Implementation is scattered across ADR-049 (Two-Tier Intent), #427 (Conversation Model), and ADR-054 (Cross-Session Memory). No explicit thread connects them.

**Recommendation**: Tag existing issues with a `PDR-002` label for traceability.

| Option | Decision |
|--------|----------|
| Status quo | ❌ Traceability gap persists |
| New epic | ❌ Scope creep risk, coordination overhead |
| **Tag existing issues** | ✅ Visibility without overhead |

This creates a way to see all PDR-002-related work without adding another epic to manage.

---

## Summary Table

| Question | PPM Guidance |
|----------|--------------|
| Option B vs C? | **C** (pattern-based, not LLM) |
| #595 in X1? | Yes—keep it |
| #427 scheduling? | Stays in MUX-IMPLEMENT |
| Conversational glue? | Tag issues with PDR-002 |

---

## Note on Healthy Tension

The Lead Developer recommended Option B (conservative, avoid superseded work). PM leans Option C (learning value justifies effort). Both positions are reasonable.

The deciding factor: does the investment teach us something we need for #427? I believe it does. Proceed with Option C.

---

*Filed: 2026-01-21 4:58 PM PT*
*In response to: memo-llm-layer-scheduling.md*

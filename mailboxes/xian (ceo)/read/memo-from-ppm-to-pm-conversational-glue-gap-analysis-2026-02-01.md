# Memo: Conversational Glue Gap Analysis Proposal

**From**: Principal Product Manager
**To**: PM (xian)
**Date**: February 1, 2026
**Re**: Identifying the Real Conversational Glue Work

---

## The Problem

Both #102 (CONV-UX-GREET) and #488 (MUX-INTERACT-DISCOVERY) are **complete**, yet the conversational glue described in PDR-002 still feels missing.

**What we built**:
- Calendar-aware greetings (#102)
- "What can you do?" capability discovery (#488)

**What PDR-002 envisioned**:
- Contextual hints that surface capabilities at appropriate moments
- Dead-end recovery when users hit limits
- Cross-session memory that informs responses
- Anaphoric reference resolution ("it," "that," "the thing")
- Trust-based proactive suggestions
- Seamless transitions between casual chat and structured workflows

**The gap**: Users can explicitly ask for help or get a nice greeting, but **Piper doesn't recognize intent mid-conversation or seamlessly transition from chat to workflow**.

---

## Proposed Analysis

### Phase 1: PDR-002 vs. Reality Mapping

Create a detailed matrix mapping each PDR-002 requirement to:
- Existing implementation (if any)
- Relevant ADRs/patterns
- Open issues (if any)
- Gap status (implemented / partial / missing)

### Phase 2: Architecture Review with CXO

Review findings with CXO to determine:
- Which gaps are UX design problems vs. implementation problems?
- What's the minimum viable glue for MVP?
- What requires new design work vs. wiring existing infrastructure?

### Phase 3: Conversational Design Assessment (Optional)

If gaps are significant, consider engaging a conversational design expert to:
- Review the conversational architecture we've built
- Identify structural issues in how Piper handles natural language
- Recommend patterns for chat-to-workflow transitions

---

## What We Know Already

### Infrastructure That Exists

| Component | Status | Location |
|-----------|--------|----------|
| Trust computation | ✅ Implemented | ADR-053, 453 tests |
| Cross-session memory architecture | ✅ Designed | ADR-054 |
| Anaphoric reference resolution | ✅ Partial | Pattern-011 |
| Intent classification | ✅ Implemented | ADR-049 two-tier |
| Canonical handlers | ✅ Implemented | ADR-039 |
| Conversation graph model | ⚪ Designed, not implemented | ADR-050 |

### Potentially Relevant Open Issues

| Issue | Title | Might Address |
|-------|-------|---------------|
| #427 | MUX-IMPLEMENT-CONVERSE-MODEL | Multi-intent, follow-ups, graph integration |
| #688 | ADR-050 Phases 1-3 Implementation | Conversation-as-graph |
| #698-700 | Guided Process types | Planning, feedback, clarification workflows |

---

## Questions to Answer

1. **Is the glue a design problem or implementation problem?**
   - Do we know what we want and just need to build it?
   - Or do we need design work to specify the conversational patterns?

2. **What's blocking natural conversation flow?**
   - Intent classification too rigid?
   - Missing conversational state management?
   - Workflow invocation too explicit?

3. **What's MVP-critical vs. nice-to-have?**
   - Must users be able to chat naturally for MVP?
   - Or is command-oriented interaction acceptable for alpha/beta?

4. **Do we need external expertise?**
   - Conversational AI design patterns
   - Dialogue management frameworks
   - User research on conversational expectations

---

## Recommended Next Steps

1. **PPM**: Create PDR-002 vs. Reality matrix (this week)
2. **PM**: Review matrix, decide on CXO consultation scope
3. **CXO**: If consulted, assess which gaps need design vs. implementation
4. **PM**: Decide on external expert consultation (if warranted)
5. **All**: Incorporate findings into MVP sprint reorg

---

## Timeline Consideration

This analysis could take 1-2 weeks if thorough. We have options:
- **Option A**: Do analysis before finalizing MVP sprints (delays planning)
- **Option B**: Finalize MVP sprints with placeholder "Glue Sprint" and fill in after analysis
- **Option C**: Accept current glue state for MVP, defer analysis to post-MVP

**PPM recommendation**: Option B — don't block sprint planning, but carve out explicit time for glue work.

---

*Memo prepared February 1, 2026*

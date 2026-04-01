# Memo: History Sidebar Requires Cathedral Context

**From**: Lead Developer (Claude Code)
**To**: CXO, PPM
**Date**: February 6, 2026
**Re**: History Sidebar feature flattening and need for roadmap clarity

---

## Summary

The PM raised a concern during alpha testing prep: the History Sidebar appears to show the same content as the Conversation List. Investigation confirmed this is true - both call the same API and show the same conversations.

This was predicted. The Special Assignments Agent's archaeology report from February 1, 2026 identified this exact gap. Five days later, it remains.

**The pattern**: Agents without sufficient "cathedral context" flatten rich design intent into simpler implementations.

---

## What Happened

### Design Intent (from ADR-054, PDR-002, #425)

The History Sidebar was meant to be **Layer 2 of the Three-Layer Context Persistence Model**:

```
Layer 1: Conversational Memory (24-hour) → Left sidebar
Layer 2: User History (searchable archive) → History sidebar
Layer 3: Composted Learning (patterns) → Background
```

**Layer 2 was supposed to show**:
- Searchable conversation archive with real search
- Trust-gated domain objects (WorkItems, Features, Documents)
- Lifecycle states visible (draft → active → archived)
- Cross-channel activity detection
- Privacy controls that persist

### What Was Built

The History Sidebar shows conversations with date grouping. It calls the same `/api/v1/conversations` endpoint as the left sidebar. The search UI exists but isn't wired to API search. The privacy toggle exists but state persistence is unknown.

**Result**: Two sidebars showing the same data with different styling.

### Why This Happened

1. **Parallel development**: #425 (History sidebar) and #565 (Conversation list) were built in the same timeframe by different agents with different briefs
2. **MVP pressure**: Left sidebar shipped first (#565, Jan 11) and became the default
3. **Disconnected component**: History sidebar wasn't even mounted until #735 (Jan 30) - 5 days after being built
4. **Cathedral blindness**: Implementing agents saw "show conversations" not "embody Layer 2 of memory architecture"

---

## The Deeper Issue

The archaeology report noted:

> "The PM hypothesis about 'emergent entity surfacing' is **not currently implemented** but is **architecturally intended** through #706 (MUX-OBJECTS-VIEWS)."

This is the crux. The History Sidebar was meant to evolve into a surface where users see:
- Their work items with lifecycle states
- Documents they've discussed
- People/stakeholders mentioned
- Cross-channel activity

This is the **MUX "embodied UX" vision** - making memory features *visible* to users, not just infrastructure.

But without a clear roadmap and agents who understand this vision, each implementation just defaults to "show conversations."

---

## Questions for CXO

From the archaeology report, these remain open:

1. **Screen real estate**: With limited horizontal space, should we have two sidebars showing similar content? What's the user mental model?

2. **Entity surfacing vision**: Is the right sidebar the intended home for surfacing domain objects (WorkItems, Features, Documents) with lifecycle states? Or should that be a different surface?

3. **Archive vs. Active distinction**: How should users distinguish between:
   - "I want to continue a recent conversation" (left sidebar)
   - "I want to search my history / see my work" (right sidebar)

4. **Trust gradient in UI**: How should trust-gated features appear? Hidden entirely at low trust? Visible but locked?

---

## Recommendation

**Create a Cathedral Document for the History Sidebar** that:

1. Defines the long-term vision (what users will eventually see)
2. Explains the relationship to PDR-002's three layers
3. Provides a phase roadmap:
   - Phase 1: Differentiate from conversation list (MVP)
   - Phase 2: Add WorkItem/entity surfacing (#706)
   - Phase 3: Trust-gated feature visibility
   - Phase 4: Cross-channel activity
4. Includes visual mockups or descriptions
5. Lives somewhere agents will read before implementing

Without this, each agent touching the History Sidebar will make locally reasonable decisions that continue the flattening.

---

## Filed Issue

#785: "History Sidebar shows same data as Conversation List - needs differentiation"

This captures the technical gap. The roadmap work is product/design scope.

---

## References

- `mailboxes/ppm/read/2026-02-history-sidebar-design-archaeology.md` - Full archaeology report
- #425: MUX-IMPLEMENT-MEMORY-SYNC (History sidebar origin)
- #706: MUX-OBJECTS-VIEWS (Future entity surfacing)
- PDR-002: Conversational Glue (Three-Layer Model)
- ADR-054: Cross-Session Memory Architecture

---

*This memo is a request for strategic guidance, not a proposal for immediate implementation work.*

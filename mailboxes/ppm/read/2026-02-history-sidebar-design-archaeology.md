# History Sidebar Design Archaeology Report

**Prepared by**: Special Assignments Agent
**Date**: February 1, 2026
**Requested by**: PPM
**Status**: Complete

---

## Executive Summary

The two sidebar features serve **distinct purposes** rooted in different design documents:

| Sidebar | Purpose | Design Origin |
|---------|---------|---------------|
| **Left** (Conversation List) | Session-level conversation switching | #565 CONV-PERSIST-3 (MVP approach) |
| **Right** (History Sidebar) | Archive-level history browsing | #425 MUX-IMPLEMENT-MEMORY-SYNC, ADR-054, PDR-002 |

**Key finding**: The PM hypothesis about "emergent entity surfacing" is **not currently implemented** but is **architecturally intended** through #706 (MUX-OBJECTS-VIEWS). The current right sidebar shows conversations only, not domain objects with lifecycle states.

**Recommendation**: Option C (redesign with intent) - The right sidebar has architectural foundations for richer functionality but currently duplicates conversation display.

---

## A. Design Intent Summary

### Left Sidebar (Conversation List)

**Source**: #565 CONV-PERSIST-3

**Intended purpose**: MVP sidebar for basic multi-conversation management.

**Explicitly excluded** (per issue description):
- Search functionality
- Rich filtering/tagging
- Conversation sharing
- Conversation deletion/renaming

**Design philosophy**: Simple, functional, ships fast. "MVP sidebar that lets users manage multiple conversations."

### Right Sidebar (History Sidebar)

**Sources**: #425 MUX-IMPLEMENT-MEMORY-SYNC, ADR-054, PDR-002

**Intended purpose**: UI for **Layer 2 of the Three-Layer Context Persistence Model**:

```
Layer 1: Conversational Memory (24-hour window) - Natural continuity
Layer 2: User History (all time) - Searchable archive  ← THIS SIDEBAR
Layer 3: Composted Learning (patterns) - Informs behavior
```

**Designed features**:
- Search functionality (implemented in UI)
- Date grouping (today, yesterday, this week, older)
- Privacy toggle (mark conversations private)
- Trust-gated access (Stage 2+ for work references, Stage 3+ for history commands)
- Cross-channel detection (see activity from other channels)

**Design philosophy**: Part of MUX "embodied UX" - making memory features *visible* to users, not just infrastructure.

### MUX Grammar Connection

ADR-045 establishes the MUX grammar: "Entities experience Moments in Places."

The History sidebar connects to this through:
- **Entities**: Conversations, and potentially domain objects (WorkItems, Features)
- **Moments**: The interaction history, timestamped
- **Places**: Channel context (web vs. Slack)

However, the current implementation only shows **conversations**, not the broader "entities" concept.

---

## B. Implementation Reality

### What Was Built

**Left Sidebar** (#565, completed Jan 11, 2026):
- Sidebar container with collapse toggle
- Conversation list with date grouping
- Click to switch conversations
- "New Chat" button
- URL updates for bookmarking
- localStorage persistence for collapsed state

**Right Sidebar** (#425, built Jan 25, 2026; mounted Jan 30, 2026 via #735):
- Full component with search, pagination, date grouping
- Privacy toggle UI
- 56 unit tests
- **NOT mounted** until #735 discovered it was disconnected
- Currently wired to `/api/conversations` (same data as left sidebar)

### Issue Trace

| Issue | Date | What Happened |
|-------|------|---------------|
| #425 | Jan 25 | Component built as part of MUX Memory Sync |
| #565 | Jan 10-11 | MVP left sidebar built (separate effort) |
| #574 | Jan 11-12 | Bug fix for conversation switching |
| #729 | Jan 28 | Alpha testing discovered History button did nothing |
| #735 | Jan 30 | Mounted the History sidebar component |

**Key observation**: #425 and #565 were built in parallel with different goals. #565 shipped first and became the default conversation interface, while #425's sidebar sat unmounted for 5 days.

---

## C. Gap Matrix

| Aspect | Intended (Design Docs) | Built (Current) | Gap |
|--------|------------------------|-----------------|-----|
| **Left sidebar purpose** | MVP conversation switching | MVP conversation switching | None |
| **Right sidebar purpose** | Layer 2 User History archive | Conversation list (same as left) | **Partial** - shows conversations, not broader history |
| **Relationship between them** | Different scope (session vs. archive) | Same data source, different UI | **Unclear** - user mental model confused |
| **Search functionality** | Right sidebar only | Right sidebar has search UI | **Verification needed** - is search wired to API? |
| **Privacy mode** | Trust-gated, integrated | Toggle exists in UI | **Unknown** - is privacy state persisted? |
| **Emergent entity surfacing** | Implied by MUX-OBJECTS-VIEWS (#706) | Not implemented | **Major gap** - this is the future vision |
| **Lifecycle visibility** | #706 establishes need | Infrastructure exists (#685, #423) | **Not connected** - no lifecycle in sidebar |
| **Trust gating** | Stage 2+ for history commands | Documented in #425 | **Unknown** - need to verify implementation |

### Gap Analysis

**Flattening observed**:
1. Right sidebar was designed for richer "User History" but currently just shows conversations
2. Trust-gating was documented but unclear if enforced
3. The distinction between "conversation list" and "history archive" collapsed in implementation

**Incomplete alignment**:
1. Both sidebars show essentially the same thing (conversations) with different UI
2. No domain objects (WorkItems, Features) visible despite #706 planning

**Undocumented decisions**:
1. Why were two sidebars built in parallel? (Jan 10-25)
2. Why was right sidebar not mounted initially?
3. What determines when to use left vs. right?

**Missing pieces**:
1. Entity/object surfacing in sidebar
2. Lifecycle indicators
3. Cross-channel activity detection UI
4. Trust-gated feature visibility

---

## D. Design Questions for CXO

1. **Screen real estate**: With limited horizontal space, should we have two sidebars showing similar content? What's the user mental model?

2. **Entity surfacing vision**: Is the right sidebar the intended home for surfacing domain objects (WorkItems, Features, Documents) with lifecycle states? Or should that be a different surface?

3. **Archive vs. Active distinction**: How should users distinguish between:
   - "I want to continue a recent conversation" (left sidebar)
   - "I want to search my history" (right sidebar)

   Are these distinct enough needs to justify two surfaces?

4. **Trust gradient in UI**: How should trust-gated features appear? Hidden entirely at low trust? Visible but locked? The design docs mention trust-gating but not the visual treatment.

5. **Mobile consideration**: ADR-042 (Mobile Strategy) shows `.sidebar { display: none; }` at mobile breakpoints. How does history access work on mobile?

---

## E. Implications for MVP Planning

### Options Analysis

**Option A: Right sidebar is redundant → deprecate or merge**
- Evidence for: Both show conversations, left sidebar is simpler
- Evidence against: Right sidebar has search/privacy toggle features
- Risk: Lose Layer 2 "searchable archive" vision from PDR-002
- Recommendation: **Not recommended** - throws away intentional design

**Option B: Right sidebar has distinct purpose → document and align UI affordances**
- Evidence for: Design docs clearly differentiate session vs. archive
- Evidence against: Current implementation doesn't realize the distinction
- Risk: User confusion about when to use which
- Recommendation: **Viable** - but requires clearer differentiation

**Option C: Right sidebar was placeholder for emergent entity surface → redesign with intent**
- Evidence for: #706 MUX-OBJECTS-VIEWS epic, lifecycle infrastructure exists
- Evidence against: Significant design/implementation work
- Risk: Scope creep for MVP
- Recommendation: **Recommended** - aligns with MUX vision

### Recommended MVP Approach

1. **Keep left sidebar** as conversation switcher (working, simple)

2. **Evolve right sidebar** to show more than conversations:
   - Add "Objects in flight" section (WorkItems with lifecycle states)
   - Keep conversation search as secondary function
   - Make the distinction clear in header: "Your Work" vs. "Conversations"

3. **Defer trust-gating verification** to #706 follow-up work

4. **Create child issues** from this analysis:
   - Verify right sidebar search is wired to API
   - Verify privacy toggle persists state
   - Connect lifecycle indicators to right sidebar (#706)

### Immediate Actions

None required for MVP - the sidebars work. This report informs intentional design choices for post-MVP work.

---

## References

### Issues
- #425: MUX-IMPLEMENT-MEMORY-SYNC (History sidebar origin)
- #565: CONV-PERSIST-3 (Left sidebar)
- #574: Conversation switching bug fix
- #706: MUX-OBJECTS-VIEWS (Future entity surfacing)
- #729, #735: History button fixes

### Design Documents
- ADR-054: Cross-Session Memory Architecture
- PDR-002: Conversational Glue (Three-Layer Model)
- MUX-VISION-LEARNING-UX: Learning System Experience Design

### Code Locations
- [templates/home.html](templates/home.html) - Left sidebar (lines 26-150)
- [templates/components/history_sidebar.html](templates/components/history_sidebar.html) - Right sidebar component

---

*Report prepared February 1, 2026*

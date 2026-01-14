# Meeting Prep: Ted Nadeau MultiChat Discussion

**Date**: January 13, 2026
**Attendees**: xian (PM), Ted Nadeau
**Prepared by**: Lead Developer

---

## Part 1: UI/UX Feedback

### What We Really Liked

**1. Explicit Piper Design Philosophy Adoption**
Ted's UI/UX spec explicitly adopts our 5 design principles:
- Colleague, Not Tool
- Trust Gradient
- Discovery Through Use
- Context-Aware, Not Creepy
- Always Useful, Never Stuck

This is excellent alignment. The spec doesn't just mention them—it applies them to specific components (whisper behavior, facilitator interventions, etc.).

**2. Model → View → Region → Interaction → Gesture Methodology**
The 5-layer approach is disciplined and traceable. Each gesture maps to an interaction, each interaction to a region, each region to a view projection. This makes the spec *implementable* rather than aspirational.

**3. Whisper Card UX Pattern**
The promotion flow (Private → Shared) is well-designed:
- User clicks "Accept" on whisper
- Optional edit step
- Appears in command input with "Promoting agent suggestion" context
- User reviews and sends
- **Attribution to user, not agent**

This last point is subtle but important—the user owns their promoted content.

**4. View Switcher Paradigm**
The "One Model, Many Views" concept is clear:
- Timeline, Thread, Tasks, Questions, Agreements, Graph, Diff, Domain-Specific
- All views are projections of the same underlying graph
- Selection can persist across view switches

**5. Spatial Layout**
The 6-region model (Main Text, Whisper Panel, Command Input, View Switcher, Secondary View, Metadata Inspector) is well-partitioned. Each region has clear purpose.

---

### Suggestions & Feedback

**1. Navigation Discovery (Our #1 UX Gap)**
Our Nov 2025 UX audit identified **navigation as our biggest problem** (Score: 700). Ted's spec assumes users will find views via the View Switcher, but doesn't address *feature discovery*.

**Suggestion**: Consider adding discovery mechanisms:
- Agent whispers that introduce views ("You might find the Tasks view helpful here")
- Progressive disclosure of view options
- Contextual hints when patterns are detected

**2. Mobile/Touch Considerations**
Ted mentions "Mobile Mode" in long-term aspirations but the main spec is desktop-focused. Our UX audit flagged accessibility and alternative input modes.

**Suggestion**: For MVP, consider:
- Touch targets (44px minimum per Apple HIG)
- Swipe gestures for view switching
- Bottom navigation pattern for mobile

**3. Empty States**
What does the Tasks view look like when there are no tasks? Questions view with no questions? Our audit flagged empty states as a gap (Score: 240).

**Suggestion**: Define empty state patterns:
- Helpful prompts ("No tasks yet. Type /task to create one")
- Agent suggestion to extract tasks from conversation

**4. Cross-Channel Sync (Our UX Gap)**
Ted's spec is single-interface. Our audit found that **Web, CLI, and Slack feel like three separate assistants** (Score: 140).

**Question for Ted**: How does MultiChat envision multi-channel scenarios? If a user starts a conversation in MultiChat's web UI, then @mentions it in Slack, how does context sync?

**5. Facilitator Verbosity Configuration**
Ted's clarification mentioned tuning how often the facilitator speaks. The UI/UX spec mentions "periodic check-ins (e.g., every 10 messages)" but doesn't show how users control this.

**Suggestion**: Add facilitator settings to config:
- Intervention frequency slider
- "Only when asked" vs. "Proactive" toggle
- Message triggers (conflicts detected, unresolved questions, etc.)

---

### Use Case Feedback

**Declaration of Independence scenario**: Brilliant test case. Multi-party async editing with version tracking is the hard problem, and this makes it concrete and relatable.

**Product Design scenario**: Maps perfectly to PM daily work. The Ali/Bob/Carol roles are realistic.

**Suggestions for additional PM-focused use cases**:
- **Sprint Planning**: PM + Tech Lead + Designer scoping work
- **Customer Feedback Synthesis**: PM consolidating user interviews
- **PRD Review**: Async stakeholder feedback on product spec

---

## Part 2: Convergence to PM Practices

### "Colleague" Pattern Alignment

Ted's spec aligns well with our Colleague pattern:
- Whispers are suggestions, not commands
- Facilitator is goal-oriented, not directive
- User controls promotion to shared space

**One clarification needed**: Our Colleague pattern includes the concept of "trust boundary" — what the colleague knows vs. what they act on. The whisper agent sees everything, but should it *remember* everything across sessions?

### MVP Scope for PM Use Case

For PM-focused MVP, I recommend prioritizing:

| View | Priority | Rationale |
|------|----------|-----------|
| Timeline | P0 | Default chat experience |
| Tasks | P0 | PMs live in action items |
| Questions | P1 | Unresolved issues tracking |
| Thread | P1 | Understanding discussion structure |
| Agreements | P2 | Decision tracking |
| Graph | P3 | Power user feature |
| Diff | P3 | Post-MVP |

**Recommended MVP Feature Set**:
1. Timeline view with threading
2. Tasks view with kanban
3. Personal whispers (1 agent per user)
4. One facilitator per conversation
5. Basic link types (reply, reference, annotates)

**Defer to Post-MVP**:
- Multiple specialized facilitators (AI layering)
- Custom link types
- Domain-specific views
- Split pane
- Voice input

---

## Part 3: Architecture & Deployment Recommendations

### Architecture: Plugin Integration Model

Ted's facilitator architecture (orchestrator + specialized sub-agents) maps well to our existing plugin pattern (ADR-034):

```
Piper Plugin Architecture          Ted's Facilitator Model
─────────────────────────          ─────────────────────────
ServiceContainer                   Orchestrator Facilitator
  └── Plugins                        └── Sub-agents
      ├── GitHubPlugin                   ├── GitHub Agent
      ├── SlackPlugin                    ├── Calendar Agent
      ├── NotionPlugin                   ├── Wiki Agent
      └── CalendarPlugin                 └── Domain Agents
```

**Recommendation**: Implement facilitator sub-agents as Piper plugins. This gives us:
- Existing lifecycle management
- Configuration patterns
- Permission model
- Test infrastructure

### Deployment: Piper Feature, Not Standalone

For MVP, I recommend **not** deploying MultiChat as a standalone application. Instead:

**Option A: Integrated Feature** (Recommended)
- MultiChat becomes a "mode" within Piper
- Leverage existing auth, database, infrastructure
- Single deployment, unified user experience
- Gradual rollout via feature flag

**Benefits**:
- No new infrastructure
- Existing users get it automatically
- Context syncs with existing Piper data (todos, files, etc.)

**Option B: Standalone + Integration**
- Separate deployment with Piper integration
- SSO via Piper
- API-based data sync

**Drawbacks**:
- More infrastructure
- Context sync complexity
- Separate user management

### Database Schema

Ted's graph model requires schema additions. Recommended approach:

**Phase 1** (minimal):
- Add `parent_id` to existing `conversation_turns`
- Add `conversation_links` table

**Phase 2** (full graph):
- Add `conversation_nodes` table (replaces turns for Host Mode)
- Add `conversation_participants` junction table
- Add `whispers` table

**Migration path**: Existing ConversationTurn records remain valid; they're just a simplified view over the graph.

### Hosting & Scaling Considerations

**For alpha/beta**:
- Single Piper instance handles MultiChat
- PostgreSQL stores graph data
- LLM calls go through existing Anthropic integration

**For scale (post-MVP)**:
- Consider graph database (Neo4j, DGraph) for complex queries
- WebSocket support for real-time multi-user sync
- Message queue for facilitator agent orchestration

---

## Part 4: Questions for Ted

1. **Cross-channel sync**: How does MultiChat envision integration with existing chat platforms (Slack, Teams)? Piper already has Slack integration—should MultiChat conversations be visible/continuable there?

2. **Offline/async patterns**: The spec assumes real-time interaction. What about async scenarios where participants are in different timezones?

3. **Conversation lifecycle**: When does a conversation "end"? Can it be archived? Reopened? Forked?

4. **Permission model**: In multi-party, who can invite/remove participants? Who can change facilitator settings?

5. **Export/artifact generation**: How do artifacts (PRDs, task lists, decision logs) get exported from MultiChat? PDF? Markdown? Integration with docs platforms?

---

## Summary: Our Steering

**Strong positive signal**: Ted's work is exactly what PDR-101 envisioned, implemented thoughtfully with explicit Piper design alignment.

**MVP focus**: Timeline + Tasks + Whispers + One Facilitator. Defer multi-facilitator, domain views, and advanced link types.

**Architecture**: Plugin integration model for facilitators. Piper feature, not standalone deployment.

**Timing**: Phase 1 (Participant Mode) in February, parallel to MUX-V1. Host Mode foundation in March.

**Key request**: Ted to help refine use cases for PM scenarios. His insights on "reaction-deck" and "gesture-palette" concepts could inform our interaction design.

---

*Prepared: January 13, 2026*
*Lead Developer*

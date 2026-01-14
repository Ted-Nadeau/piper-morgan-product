# PDR-101: Multi-Entity Conversation Support

**Status**: Draft v2
**Date**: January 4, 2026
**Author**: Principal Product Manager
**Input**: Ted Nadeau, "NewApp – Multi-Party, Multi-Agent Conversational Modeling Platform" PRD v0.3
**Stakeholders**: PM (xian), Chief Architect, Ted Nadeau (Advisor/Contributor)

---

## Decision

Piper Morgan will support multi-entity conversations as a core capability, operating in two modalities:

1. **Host Mode**: Piper hosts multi-entity conversations within its environment, coordinating between human users and AI agents
2. **Participant Mode**: Piper participates as an agent in externally-hosted multi-agent contexts

This is not a new invention—it's a productization of patterns already present in our development methodology. The asynchronous, human-orchestrated multi-agent coordination we use daily (GitHub issues, session logs, handoffs between specialized agents) is the prototype for this capability.

---

## Context

### The Methodology as Prototype

Our current development process involves:
- Multiple specialized AI agents (Chief Architect, Lead Developer, PPM, Communications Director, etc.)
- Human orchestration connecting agent outputs into coherent execution
- Asynchronous coordination via GitHub issues and session logs
- Handoff protocols that preserve context across agent boundaries
- Entity resolution ("the issue we discussed," "Ted's feedback") across conversation threads

This is multi-entity conversation—just asynchronous and human-mediated. The product question is: how do we formalize this into a capability Piper can offer users?

### Ted's Contribution

Ted Nadeau's "NewApp" PRD (v0.3) provides a comprehensive vision for multi-party, multi-agent conversational platforms. Key concepts:

- **Conversation as graph model**: Element_nodes + Element_links, not linear chat
- **Personal agents**: Each user has their own AI agent providing private "whispers"
- **Facilitator agent**: Shared agent helping the group toward outcomes
- **One model, many views**: Timeline, threads, tasks, questions, agreements, domain-specific
- **Gesture vocabulary**: Type, annotate, react, edit, view—multiple interaction modes
- **Version control for thoughts**: Content evolution tracked, not just appended

Ted's PRD is a substantial architectural contribution that will inform both this PDR and subsequent ADRs. The relationship is:
- **PDR-101** (this document): What capability does Piper offer? (Product decision)
- **Future ADR**: How does Piper implement this? (Architecture decision, informed by Ted's data model)
- **Future UX brief**: What does the interaction feel like? (Design decision)

---

## User Need

### For Individual PM Users (Current Focus)

PMs already work in multi-entity contexts:
- Conversations with stakeholders, engineers, designers
- Meetings where multiple perspectives must be reconciled
- Async collaboration via Slack, email, docs with comments
- Decisions that emerge from dialogue, not monologue

Piper currently supports 1:1 conversation. But PM work is inherently multi-party. Users need:
- Help synthesizing multi-person discussions into decisions
- Support for conversations that include human colleagues AND Piper
- Context that persists across who's talking, not just what session

### For Team/Org Users (Future)

As Piper expands beyond individual users:
- Multiple team members interacting with shared Piper context
- Piper as participant in team standups, planning sessions, retrospectives
- Coordination between multiple Piper instances (multi-tenant scenarios)

---

## Two Modalities

### Host Mode: Piper as Conversation Platform

Piper hosts conversations where:
- Multiple human participants contribute
- Piper provides facilitation, synthesis, and memory
- The conversation model (per Ted's design) is Piper's native format
- Views, annotations, and structure are Piper capabilities

**Example**: A product planning session where PM, designer, and engineer discuss a feature. Piper captures the conversation as structured data, tracks decisions vs. open questions, and maintains context for follow-up.

**Key capabilities**:
- Multi-participant input handling
- Conversation-as-model (graph, not log)
- Multiple views over same underlying data
- Personal context per participant (what have *they* contributed?)
- Facilitation suggestions (summarize, highlight conflicts, propose next steps)

### Participant Mode: Piper as Agent in External Contexts

Piper joins conversations hosted elsewhere:
- Slack channels where Piper is invited
- External multi-agent orchestration systems
- API-based participation in third-party platforms
- MCP-based tool access from other AI systems

**Example**: A Slack channel where team discusses a bug. Piper is @mentioned, reads context, contributes analysis, and offers to create a GitHub issue.

**Key capabilities**:
- Context ingestion from external sources
- Appropriate contribution without dominating
- State persistence across external conversation sessions
- Action execution when authorized (create issue, update doc, etc.)

---

## Relationship to Existing PDRs

### PDR-001 (FTUX as First Recognition)
Multi-entity support extends the recognition interface pattern. When multiple entities are present, Piper must:
- Recognize who is speaking and their context
- Offer situationally appropriate help based on conversation state
- Maintain trust gradient per participant, not just per conversation

### PDR-002 (Conversational Glue)
Multi-entity conversations require enhanced glue:
- **Discovery**: How do participants learn what Piper can do in group context?
- **Context**: How does context persist when participants change?
- **Proactivity**: How does trust gradient work with multiple humans?

The B2 quality gate applies here too—multi-entity conversations should feel natural, not like a conference call with a bot.

---

## Design Principles

### Strategic Stance: Participant-First

*Added v2 from CXO feedback.*

**Piper should be an excellent participant before becoming a capable host.**

Rationale:
- Participant mode extends existing integrations (Slack) without new UI
- Users already have conversation platforms; they need a capable participant
- Host mode is a larger product surface with more UX risk
- Being a good participant teaches us what good hosting looks like

The colleague metaphor supports this: colleagues join your meetings, contribute to your threads, show up where you're working. They don't ask you to come to their office for every interaction.

**The invitation pattern**: Rather than building Host Mode and expecting users to come to it, Piper-as-participant recognizes when a conversation has outgrown its platform and offers:

> "This discussion is getting complex. Want me to capture it in a structured format you can navigate?"

This keeps participant-first as default while creating natural paths to host mode when conversations need structure that external platforms can't provide—decision tracking, version-controlled artifacts, multi-view navigation.

---

### Numbered Principles

### 1. Conversation is a model, not a log

Per Ted's insight: the underlying structure is a graph of typed elements with relationships, not a linear transcript. This enables:
- Multiple views over same data
- Non-linear navigation (jump to decision, see related discussion)
- Semantic operations (show me all open questions)

### 2. Each participant has context

What each person sees, what they've contributed, what they care about—this is per-participant state. The facilitator (Piper) sees everything; personal views are filtered.

### 3. Facilitation is a capability, not a requirement

Piper can facilitate (summarize, highlight, suggest) but participants can also just converse. Facilitation is offered, not imposed.

### 4. Actions require consent

In multi-party contexts, Piper should not take unilateral action. Creating issues, updating docs, sending messages—these need explicit authorization, especially when multiple humans are involved.

### 5. Graceful degradation to current model

If a conversation starts as multi-entity but only one person remains, it should gracefully become a normal 1:1 Piper conversation. No special "exit multi-entity mode" required.

---

## Implementation Path

### Phase 0: Methodology Continues (Now)
The current development methodology IS the prototype. Document patterns, refine handoffs, extract reusable components.

### Phase 1: Participant Mode MVP
Piper as effective participant in Slack conversations:
- Context ingestion from thread
- Appropriate responses when @mentioned
- Action execution with explicit authorization
- State persistence across sessions

This extends existing Slack integration; doesn't require new UI.

### Phase 2: Host Mode Foundation
Basic multi-participant support in Piper's native interface:
- Conversation model (Ted's graph structure)
- Multiple views (timeline + at least one structured view)
- Basic facilitation (summarize, track decisions)

### Phase 3: Personal Agents
Per-participant AI assistance:
- Private "whispers" suggesting contributions
- Per-user context and preferences
- Distinct from shared facilitation

### Future: Federation
Piper instances communicating with each other and external AI systems. This is where Ted's full vision lives—but it's beyond current scope.

---

## Open Questions

1. **Governance model**: When multiple humans are present, who can authorize Piper actions? Consensus? Any participant? Designated owner?

2. **Privacy boundaries**: What does one participant see about another's interactions with Piper? Full transparency? Selective?

3. **Conflict handling**: When participants disagree, how does Piper facilitate? Neutral presentation? Active mediation?

4. **Versioning UI**: Ted's model supports version control for evolving content. How do we expose "diffs" without overwhelming users?

5. **External platform constraints**: Slack, Teams, etc. have their own limitations. How much of the model can we preserve when participating in constrained environments?

6. **Scope boundary**: Where does Piper's multi-entity capability end and a full "NewApp" product begin? Are these the same thing eventually, or complementary?

---

## Ted's Contribution Path

Ted is empowered to develop this capability with the following workflow:

1. **Ted's internal coherency**: Develops rich documentation with AI assistance (ChatGPT), maintaining his own structure
2. **Translation to our vernacular**: PPM/PM help map Ted's artifacts to PDR/ADR/UX formats
3. **Architectural review**: Chief Architect ensures alignment with Piper patterns
4. **Implementation**: Ted proceeds to vibe-coding/AI-assisted development
5. **PR submission**: Code submitted for review
6. **Compliance check**: Pattern and architecture compliance verified
7. **Integration**: Accepted PRs merged into Piper

This is exactly the contributor model our methodology envisions—Ted is the first external test case.

---

## Success Criteria

### Phase 1 (Participant Mode)
| Metric | Target |
|--------|--------|
| Slack thread context retention | >80% accuracy on "what was discussed" |
| Appropriate response rate | >70% of @mentions get useful response |
| Action completion | >90% of authorized actions succeed |
| User satisfaction | >4/5 on "Piper was helpful in team context" |

### Phase 2 (Host Mode)
| Metric | Target |
|--------|--------|
| Multi-view usage | >50% of sessions use at least 2 views |
| Facilitation acceptance | >40% of suggestions acted upon |
| Context persistence | >90% accuracy on cross-session references |
| Participant satisfaction | >4/5 per participant |

---

## References

- Ted Nadeau, "NewApp – Multi-Party, Multi-Agent Conversational Modeling Platform" PRD v0.3 (Jan 4, 2026)
- PDR-001: First Contact is First Recognition
- PDR-002: Conversational Glue
- ADR-046: Micro-Format Agent Architecture (Ted's earlier contribution)
- Piper Morgan Development Methodology (multi-agent coordination patterns)
- Session logs demonstrating current async multi-agent patterns

---

## Changelog

**v2 (January 4, 2026)**:
- Added "Participant-First" strategic stance (CXO feedback)
- Added invitation pattern: Piper-as-participant offers to host when conversations outgrow platforms
- Clarified Host Mode is for when external platforms can't provide needed structure

**v1 (January 4, 2026)**:
- Initial draft establishing multi-entity conversation as Piper capability
- Defined two modalities: Host and Participant
- Framed methodology as prototype
- Established Ted's contribution path
- Referenced Ted's NewApp PRD as architectural input

---

*PDR-101 | Draft v2 | January 4, 2026*

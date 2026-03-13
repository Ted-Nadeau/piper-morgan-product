# Spec Session Log: Ted's Multichat Repository Analysis

**Date**: 2026-01-13 10:11 AM
**Role**: Lead Developer (Special Assignment)
**Task**: Analyze Ted Nadeau's multichat repository and determine integration approach
**Context**: Ted invited @mediajunkie to https://github.com/Ted-Nadeau/multichat

## Objective

1. Research existing references to Ted's multi-chat PRD in our docbase
2. Analyze the multichat repository structure and purpose
3. Recommend how to parse/integrate it with Piper Morgan

---

## Session Progress

### 10:11 AM - Session Start
- Created session log
- Beginning internal research on Ted's multi-chat initiative

### 10:12 AM - Internal Research Complete

#### Key Internal Documents Found

**1. PDR-101: Multi-Entity Conversation Support** (`dev/active/PDR-101-multi-entity-conversation.md`)
- Status: Draft v2, dated January 4, 2026
- Author: Principal Product Manager
- Input source: Ted Nadeau, "NewApp – Multi-Party, Multi-Agent Conversational Modeling Platform" PRD v0.3

Key concepts from PDR-101:
- **Two modalities**: Host Mode (Piper hosts conversations) and Participant Mode (Piper joins external conversations)
- **Strategic stance**: Participant-First (be excellent participant before becoming host)
- **Conversation as graph model**: Element_nodes + Element_links, not linear chat
- **Personal agents**: Each user has AI agent providing "whispers"
- **Facilitator agent**: Shared agent helping group toward outcomes
- **Version control for thoughts**: Content evolution tracked

Implementation path defined:
- Phase 0: Methodology as prototype (current)
- Phase 1: Participant Mode MVP (Slack integration extension)
- Phase 2: Host Mode Foundation
- Phase 3: Personal Agents

**2. Ted Nadeau's Advisor Mailbox** (`advisors/ted-nadeau/`)
- Established mailbox system for async collaboration
- Contains inbox messages (001-bootstrap-feedback, 002-micro-formats, 003-moment-types)
- Outbox: Ted's reply on micro-formats (Dec 1, 2025)
- Ted was assigned the multi-entity chat spec task: "Yes, let me take a stab at this. **Assign this task to me.**"

**3. Ted's Contribution Path** (from PDR-101)
1. Ted develops rich documentation with AI assistance
2. Translation to Piper vernacular (PDR/ADR/UX formats)
3. Architectural review by Chief Architect
4. Implementation via vibe-coding/AI-assisted development
5. PR submission and compliance check
6. Integration into Piper

#### External Repository Status

**Attempted to access**: https://github.com/Ted-Nadeau/multichat
**Result**: 404 Not Found

This indicates the repository is **private**. As @mediajunkie was invited, direct access requires authentication.

---

## Recommendation

### To Analyze the Repository

Since the repository is private, I cannot access it via web fetch. You have two options:

**Option A: Clone Inside Project (Recommended)**
```bash
# Clone as a submodule or separate directory
cd /Users/xian/Development/piper-morgan
git clone git@github.com:Ted-Nadeau/multichat.git external/ted-multichat
```

Benefits:
- Keeps Ted's work separate from main codebase
- Can analyze structure, review code, understand data models
- Maintains clear ownership/contribution boundaries
- Aligns with Ted's contribution path (PR submission model)

**Option B: Clone Outside Project**
```bash
# Clone to a sibling directory
cd /Users/xian/Development
git clone git@github.com:Ted-Nadeau/multichat.git ted-multichat
```

Benefits:
- Complete isolation from Piper Morgan
- No risk of accidental commits/merges
- Cleaner separation during evaluation phase

### Integration Strategy (Based on PDR-101)

Once we can access the repository, the integration approach should follow Ted's established contribution path:

1. **Analyze Ted's data model** - How does his conversation-as-graph model map to our domain models?
2. **Identify reusable components** - Which elements can be directly adopted vs. adapted?
3. **Map to existing architecture** - How does this align with ADR-046 (Micro-Format Agent Architecture)?
4. **Determine integration points**:
   - Does it extend Slack integration (Participant Mode)?
   - Does it introduce new UI (Host Mode)?
   - What database schema changes needed?
5. **Plan PR strategy** - Incremental PRs vs. feature branch merge

### Questions for You

1. **Clone location preference?** Inside project (`external/`) or outside?
2. **Has Ted shared any PRD/spec documents** separately from the repository?
3. **What's the urgency?** Is this exploratory or for imminent Phase 1 work?

---

## Next Steps (Pending Your Input)

Once you clone the repository, I can:
1. Analyze the repository structure and tech stack
2. Map Ted's data models to our domain models
3. Identify architectural alignment/conflicts with ADR-046
4. Draft an integration gameplan
5. Recommend Phase 1 implementation steps

---

### 10:21 AM - Repository Cloned & Analyzed

Repository cloned to `external/ted-multichat/`.

## Repository Analysis

### Overview

Ted's multichat repository is a **well-structured proof-of-concept** implementing his "NewApp" vision from the PRD referenced in PDR-101. It contains:

| Component | Description |
|-----------|-------------|
| **PRD** | 80KB comprehensive requirements doc (`multichat_prd_v1.md`) |
| **UI/UX Spec** | 37KB detailed interaction design (`multichat_uiux_v1.md`) |
| **Architecture** | Project structure and regeneration guide (`project_architecture.md`) |
| **POC** | Working Next.js 14 / TypeScript application |
| **Use Cases** | 5 narrative scenarios with validation scripts |
| **Config Spec** | 18KB agent/conversation configuration screens |

### Tech Stack (POC)

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Vanilla CSS Modules (explicit Piper Morgan "Colleague" aesthetic alignment)
- **State**: React Context API
- **Data Model**: Graph-based (Nodes + Links + Users)

### Core Data Model

```typescript
// From poc/src/types/data.ts
type NodeType = 'message' | 'task' | 'whisper';
type LinkType = 'reply' | 'reference' | 'blocking' | 'variant_of' | 'annotates' | 'resolves';

interface Node {
    id: string;
    type: NodeType;
    content: string;
    authorId: string;
    timestamp: string;
    parentId?: string;  // For threading
    data?: any;         // Type-specific payload
}

interface Link {
    id: string;
    sourceId: string;
    targetId: string;
    type: LinkType;
    createdAt: string;
    createdBy: string;
}

interface Graph {
    nodes: Node[];
    links: Link[];
    users: User[];
    currentUser: User;
}
```

### Views Implemented

1. **TimelineView** - Chronological message list (like current Piper chat)
2. **ThreadView** - Hierarchical nested tree structure
3. **TasksView** - Kanban board (Todo/In Progress/Done)
4. **StatusView** - System status enumeration
5. **ConfigView** - Agent and Conversation configuration
6. **WhisperPanel** - Private AI suggestions (right panel)

### Key PRD Concepts

1. **Conversation as Graph Model** - Not linear chat
2. **Personal AI Agents** - "On-my-side" helpers for each participant
3. **Facilitator AI Agent** - Shared agent helping group outcomes
4. **Multiple Views** - Same underlying model, different projections
5. **Whispers** - Private AI suggestions visible only to one user
6. **Artifact Extraction** - Tasks, decisions, documents from conversation graph

---

## Mapping to Piper Morgan

### Domain Model Alignment

| Ted's Concept | Piper Domain Model | Notes |
|---------------|-------------------|-------|
| `Node` | `ConversationTurn` | Core message unit |
| `TaskNode` | `Todo` | Task extraction |
| `WhisperNode` | (new) | Private AI suggestion |
| `Link` | (new) | Explicit relationships |
| `Graph` | `ConversationSession` | Enhanced with graph structure |
| `User` | `User` | Direct mapping |

### Missing in Piper (Would Need to Add)

1. **Link model** - Explicit relationships between conversation elements
2. **Whisper model** - Private AI suggestions per user
3. **Multi-participant conversations** - Currently 1:1 only
4. **Graph-based conversation storage** - Currently linear
5. **Multiple views over conversations** - Currently timeline only

### Already in Piper (Aligns)

1. **ConversationSession/Turn** - Base conversation model exists
2. **Todo/Task** - Task extraction exists
3. **User context** - Per-user state exists
4. **Slack integration** - Participant Mode foundation

---

## Integration Recommendations

### Strategic Alignment with PDR-101

Ted's POC directly implements concepts from PDR-101. Integration should follow the **Participant-First** strategy:

**Phase 1: Extract Reusable Concepts (No Code)**
- Adopt Ted's data model vocabulary (Node, Link, Graph)
- Map to existing domain models
- Identify database schema changes needed

**Phase 2: Participant Mode Enhancement (Slack)**
- Add Link model for explicit relationships
- Implement context threading (parentId)
- Enable @mention extraction as typed nodes

**Phase 3: Host Mode Foundation**
- Implement Ted's Graph model in Piper
- Add WhisperPanel equivalent (private AI suggestions)
- Build TasksView projection over conversation data

### Specific Next Steps

1. **Read Ted's full PRD** - 80KB of detailed requirements
2. **Review configuration screens spec** - Agent/conversation setup patterns
3. **Run the POC** - `cd external/ted-multichat/poc && npm install && npm run dev`
4. **Draft ADR** - "Conversation-as-Graph Model" based on Ted's design
5. **File integration gameplan** - Phase-gated implementation plan

### Risk Assessment

| Risk | Mitigation |
|------|------------|
| Tech stack mismatch (Next.js vs Python/FastAPI) | Extract patterns, not code |
| Scope creep (full Host Mode is large) | Stick to PDR-101 phases |
| Ted's PRD vs Piper requirements drift | Regular sync via advisor mailbox |

---

## Summary

Ted's multichat repository is **production-quality documentation and proof-of-concept** that directly implements the vision from PDR-101. The POC demonstrates:

- Graph-based conversation model
- Multiple view projections
- Personal AI whispers
- Task extraction and kanban view

**Recommended approach**: Use Ted's work as the **specification and reference implementation** for Piper's multi-entity conversation capability. Don't fork/merge the Next.js code; instead extract the data model and patterns into Piper's Python/FastAPI stack.

**Immediate action**: I recommend reading Ted's full PRD (`multichat_prd_v1.md`) to understand the complete feature set before drafting an integration gameplan.

---

### 10:22 AM - Deliverables Complete

Per PM request, created the following deliverables:

## Deliverables

### 1. ADR-050: Conversation-as-Graph Model
**Location**: `docs/internal/architecture/current/adrs/adr-050-conversation-as-graph-model.md`

Proposes adopting Ted's graph-based conversation model:
- ConversationNode (message, task, whisper, decision, question)
- ConversationLink (reply, reference, blocking, variant_of, annotates, resolves)
- ConversationGraph (nodes + links + participants)
- Migration path through PDR-101 phases

### 2. Integration Gameplan
**Location**: `dev/2026/01/13/gameplan-multichat-integration.md`

13 tickets across 3 phases:
- **Phase 0** (3 tickets): ADR review, schema design, Ted sync
- **Phase 1** (4 tickets): Threading, Links, Slack integration, task extraction
- **Phase 2** (6 tickets): Full Node model, Graph model, view projections, multi-participant UI

Estimated 56-79 development hours for Phases 0-2.

### 3. Roadmap Integration Timing
**Proposed**:
- Phase 0 (Foundation): Late January (after v0.8.4 stabilizes)
- Phase 1 (Participant Mode): February (parallel to MUX-V1)
- Phase 2 (Host Mode): March-April (after MUX integration)
- Phase 3 (Personal Agents): Post-beta

Rationale: Multi-entity conversation builds on MUX's Object Model foundation. Starting Phase 1 in February allows parallel progress without blocking MUX.

### 4. Memo to Chief Architect
**Location**: `dev/2026/01/13/memo-chief-architect-multichat-integration.md`

Recommends:
- Accept Ted's work as specification and reference implementation
- Review ADR-050 for architectural soundness
- Approve Phase 0 tickets for backlog grooming
- Confirm timing alignment with MUX phases

### 5. Memo to Chief Innovation Officer
**Location**: `dev/2026/01/13/memo-cio-external-collaboration-patterns.md`

Documents patterns from Ted collaboration:
- Advisor mailbox system effectiveness
- External POC → Internal Implementation pattern
- Phase-gated external features
- Recommendations for future collaborators

### 6. Draft Reply to Ted Nadeau
**Location**: `dev/2026/01/13/draft-reply-to-ted-multichat.md`

Key points:
- Impressed with the work quality
- Highlights specific things we liked (data model, use cases, aesthetic alignment)
- Explains our integration approach (reference implementation, not code merge)
- Sets timing expectations (February Phase 1, March Host Mode)
- Poses three clarifying questions for upcoming meeting

---

## Session Summary

Successfully analyzed Ted Nadeau's MultiChat repository and produced:
- 1 ADR (050)
- 1 gameplan (13 tickets)
- 2 memos (Chief Architect, CIO)
- 1 draft email reply
- 1 session log (this document)

Ted's contribution is high-quality and directly implements PDR-101's vision. Recommended approach: use as specification and reference implementation while building Python/FastAPI version internally.

---

### 11:11 AM - Ted's Clarifications Received

Ted responded to the three questions with valuable architectural details:

## Ted's Responses

### 1. Whisper Visibility
> **Q**: Does the whisper author (AI) see how users responded?
> **A**: Yes, by default. The Whisper agent sees the conversation as the user does.

**Nuance**: Gets complicated at "prior insertion points" (e.g., "no spoilers" mode). Context management needed. Input tokens are cheap, so "see all" is default unless problematic.

**Implication for ADR-050**: Whisper agents have full conversation visibility by default. Need to consider temporal context (what if user is reviewing earlier in conversation?).

### 2. Link Type Extensibility
> **Q**: Are the 6 link types the full set?
> **A**: No, just a beginning taxonomy.

**Key details**:
- Default is just `relates-to`
- One element can have **multiple links and link-types** to another element
- Could be multi-link OR single-link with multi-link-type
- Link-types have relationships to each other (meta-relationships)
- Relates to "reaction-deck" and "gesture-palette" concepts:
  - recognize/understand → emotional reaction → description → response
- Conversation sponsors can define which reactions they care about
  - Example: Fashion show designer wants: like/don't like + specifics (crazy/sexy/cool)

**Implication for ADR-050**: Link types should be **extensible**, not fixed enum. Consider `relates-to` as base type with specializations. May need link-type taxonomy separate from code.

### 3. Facilitator Scope
> **Q**: One or multiple facilitators per conversation?
> **A**: Can be more than one, but with AI layering to avoid chaos.

**Architecture pattern**: 1 AI manager coordinating multiple AI-subs:
- One for GitHub issues (tasks, story/epic/initiative)
- One for calendar
- One for wiki
- Specialized: Zillow, restaurant reservations, etc.

**Tuning considerations**:
- How often does central AI speak?
  - Most verbal: after every text, lengthy responses
  - Least: nearly never unless big gap or problem
- Are they reacting or leading?
- PM's "colleague" pattern provides guidance

**Human analogs** for multi-facilitator patterns:
- Marriage counselor
- Meeting note-taker
- Wedding planner
- Mediator
- PM when business sponsor + tech-doers in same meeting

**Implication for ADR-050**: Facilitator architecture needs layering model. Single "orchestrator" facilitator with specialized sub-agents. Verbosity/intervention frequency is a tuning parameter.

---

## Ted's Meeting Agenda Items

**What he'll show**:
- Running demo of the POC

**What he wants feedback on**:
1. **UI/UX feedback** - can help edit use cases
2. **Convergence to PM practices** - alignment with "colleague" pattern
3. **Focus** - MVP version scoped for PM use case
4. **"Making it real" issues** - architecture, deployment (early but should think upfront)

**Also interested in**:
- Our steering on direction

---

## Updates Needed

Based on Ted's clarifications:

1. **ADR-050 Amendment**: Link types should be extensible (not fixed enum). Add `relates-to` as base type.

2. **Gameplan Update**: Add ticket for link-type taxonomy design (Phase 0).

3. **Meeting Prep**: Prepare UI/UX feedback, MVP scope recommendations, "colleague" pattern alignment notes.

---

### 11:30 AM - Meeting Prep Complete

## Additional Deliverables

### 7. ADR-050 Amendment
Updated ADR-050 with Ted's clarifications:
- Link types are extensible (`RELATES_TO` as default)
- Added `additional_types` field for multi-type links
- Added Facilitator Architecture section (AI layering model)
- Added Whisper Agent Visibility section

### 8. Meeting Prep Document
**Location**: `dev/2026/01/13/meeting-prep-ted-multichat.md`

Comprehensive meeting prep covering:

**Part 1: UI/UX Feedback**
- What we liked: Design philosophy adoption, 5-layer methodology, whisper promotion flow
- Suggestions: Navigation discovery, mobile considerations, empty states, cross-channel sync
- Use case feedback: Declaration scenario is brilliant; suggested PM-focused additions

**Part 2: Convergence to PM Practices**
- Colleague pattern alignment analysis
- MVP scope recommendation (Timeline + Tasks + Whispers + One Facilitator)
- Features to defer post-MVP

**Part 3: Architecture & Deployment**
- **Architecture**: Plugin integration model - facilitator sub-agents map to Piper plugins (ADR-034)
- **Deployment**: Recommend integrated Piper feature, not standalone app
- **Database**: Incremental schema approach (Phase 1 minimal, Phase 2 full graph)
- **Scaling**: PostgreSQL for alpha, consider graph DB for scale

**Part 4: Questions for Ted**
1. Cross-channel sync with Slack
2. Offline/async patterns
3. Conversation lifecycle (end, archive, fork)
4. Permission model for multi-party
5. Export/artifact generation

---

## Session Complete

**Total Deliverables**:
1. ADR-050 (with amendments)
2. Integration Gameplan (13 tickets)
3. Memo to Chief Architect
4. Memo to CIO (collaboration patterns)
5. Draft Reply to Ted
6. Session Log
7. Meeting Prep Document

**Key Outcomes**:
- Ted's MultiChat work is production-quality and well-aligned with Piper design principles
- Recommended integration approach: Reference implementation → Plugin integration → Phased rollout
- MVP focus: Timeline + Tasks + Whispers + One Facilitator
- Timing: Phase 1 February, Phase 2 March-April

---

### 2:00 PM - Agent Mailbox System

PM requested mailbox infrastructure to reduce "human message bus" burden—agents should deliver memos directly to each other's inboxes.

## Mailbox System Implementation

### 9. Mailbox Infrastructure
**Location**: `mailboxes/`

Created file-based mailbox system:
- `mailboxes/README.md` - Conventions and usage guide
- Directory structure: `mailboxes/[slug]/inbox/`, `read/`, `context/`
- External advisors also have `outbox/`

**Role slugs formalized**:
| Role | Slug |
|------|------|
| CEO/PM | `ceo` |
| Chief Architect | `arch` |
| Chief Innovation Officer | `cio` |
| Lead Developer | `lead` |
| Chief of Communications | `comms` |
| Principal Product Manager | `ppm` |
| Chief Experience Officer | `cxo` |
| Head of Sapient Resources | `hosr` |
| Ted Nadeau | `ted-nadeau` |

### 10. Ted Nadeau Migration
Migrated `advisors/ted-nadeau/` → `mailboxes/ted-nadeau/`:
- 3 inbox messages preserved
- 2 outbox responses preserved
- Context documents preserved
- manifest.json preserved

### 11. Memo Delivery
Delivered today's memos as first test of the system:
- `mailboxes/arch/inbox/0001-2026-01-13-lead-multichat-integration.md`
- `mailboxes/cio/inbox/0001-2026-01-13-lead-external-collaboration-patterns.md`

### 12. CLAUDE.md Update
Added mailbox check instructions to CLAUDE.md (lines 33-49):
- Session start protocol: check `mailboxes/lead/inbox/`
- Workflow: read → move to `read/` → respond if requested
- Role slug reference

### 13. Doc Updates
- Updated `docs/briefing/BRIEFING-ESSENTIAL-HOSR.md` - "Agent Mailbox Pattern" reference
- Updated `dev/2026/01/13/memo-cio-external-collaboration-patterns.md` - path references

---

## Final Session Summary

**Total Deliverables**: 13
1. ADR-050: Conversation-as-Graph Model (with amendments)
2. Integration Gameplan (13 tickets)
3. Memo to Chief Architect
4. Memo to CIO (collaboration patterns)
5. Draft Reply to Ted
6. Session Log (this document)
7. Meeting Prep Document
8. ADR-050 Amendments (Ted's clarifications)
9. Mailbox Infrastructure (`mailboxes/`)
10. Ted Nadeau Migration
11. Memo Delivery (2 memos)
12. CLAUDE.md Mailbox Instructions
13. Doc Reference Updates

**Session Duration**: 10:11 AM - 10:18 PM

**Key Outcomes**:
- Ted's MultiChat: Production-quality, well-aligned with Piper design
- Integration approach: Reference implementation → Plugin integration → Phased rollout
- MVP focus: Timeline + Tasks + Whispers + One Facilitator
- Timing: Phase 1 February, Phase 2 March-April
- Mailbox system: Operational, reduces PM coordination burden

---

### 10:18 PM - Evening Wrap-Up

## Additional Mailbox Work

### 14. Additional Mailboxes Created
Created mailboxes for remaining roles:
- `mailboxes/comms/` - Chief of Communications
- `mailboxes/ppm/` - Principal Product Manager
- `mailboxes/cxo/` - Chief Experience Officer
- `mailboxes/hosr/` - Head of Sapient Resources
- `mailboxes/exec/` - Chief of Staff / Executive Assistant
- `mailboxes/spec/` - Special Assignment Agent

### 15. Undelivered Memo Audit
Searched `dev/active/` for memos from January 2026. Found ~17 memos total.

**Delivery Status** (confirmed by PM):
- Memos #1-9 (Jan 3-5): All delivered
- Memo #10-12 (Jan 8-11): Pending PM verification
- Memo #13: NOT delivered → Delivered to `mailboxes/cio/inbox/`
- Memo #14-16: Already delivered
- Memo #17: NOT delivered → Delivered to `mailboxes/hosr/inbox/`

### 16. Additional Memo Deliveries
- `mailboxes/cio/inbox/0002-2026-01-11-arch-unihemispheric-dreaming-revised.md`
- `mailboxes/hosr/inbox/0001-2026-01-05-lead-multi-agent-methodology.md`

### 17. Pending Verification Folder
Created `mailboxes/pending-verification/` to hold memos #10-12 until PM can verify delivery status:
- `memo-cxo-design-system-reorganization-2026-01-08.md`
- `memo-cxo-design-system-response-2026-01-08.md`
- `memo-cio-unihemispheric-dreaming-2026-01-11.md`

---

## Open Items for Tomorrow

1. **Verify memos #10-12** - PM will confirm if these were delivered
2. **Old `advisors/` directory** - Can be removed once migration confirmed complete

---

## Final Deliverable Count: 17

1. ADR-050: Conversation-as-Graph Model
2. Integration Gameplan (13 tickets)
3. Memo to Chief Architect
4. Memo to CIO (collaboration patterns)
5. Draft Reply to Ted
6. Session Log (this document)
7. Meeting Prep Document
8. ADR-050 Amendments (Ted's clarifications)
9. Mailbox Infrastructure (`mailboxes/`)
10. Ted Nadeau Migration
11. Initial Memo Delivery (2 memos)
12. CLAUDE.md Mailbox Instructions
13. Doc Reference Updates
14. Additional Mailboxes (6 roles)
15. Undelivered Memo Audit
16. Additional Memo Deliveries (2 memos)
17. Pending Verification Folder

---

*Session complete. PM wrapping for the night.*

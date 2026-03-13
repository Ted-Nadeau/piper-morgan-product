# Gameplan: MultiChat Integration

**Epic**: Multi-Entity Conversation Support
**Source**: Ted Nadeau's MultiChat PRD + POC
**Reference**: PDR-101, ADR-050
**Author**: Lead Developer
**Date**: January 13, 2026

---

## Overview

This gameplan outlines the integration of Ted Nadeau's MultiChat concepts into Piper Morgan, following the Participant-First strategy from PDR-101.

**Not in Scope**: Merging Ted's Next.js code. We extract patterns and data models into Piper's Python/FastAPI stack.

---

## Phase 0: Foundation (Pre-Implementation)

### Ticket P0-1: ADR Review and Acceptance
**Type**: Review
**Assignee**: Chief Architect
**Description**: Review ADR-050 (Conversation-as-Graph Model) for architectural alignment.
**Acceptance Criteria**:
- [ ] ADR-050 reviewed against existing architecture
- [ ] Conflicts with ADR-046 (Moment.type) resolved
- [ ] Status updated to "Accepted" or feedback provided
**Estimate**: 1-2 hours

### Ticket P0-2: Data Model Schema Design
**Type**: Design
**Assignee**: Chief Architect + Lead Developer
**Description**: Design database schema for ConversationNode, ConversationLink, ConversationGraph.
**Acceptance Criteria**:
- [ ] SQLAlchemy models drafted in `services/database/models.py`
- [ ] Domain models drafted in `services/domain/models.py`
- [ ] Migration strategy documented (existing conversations → graph)
- [ ] Index strategy for common queries identified
**Estimate**: 4-6 hours
**Dependencies**: P0-1

### Ticket P0-3: Ted Sync - Requirements Clarification
**Type**: Communication
**Assignee**: PM (xian)
**Description**: Sync with Ted on any open questions from PRD review.
**Questions to Clarify**:
- [ ] Whisper visibility rules (who sees what, when)
- [ ] Link type extensibility (can users define custom link types?)
- [ ] Facilitator agent scope (one per conversation or configurable?)
**Acceptance Criteria**:
- [ ] Questions answered via advisor mailbox or meeting
- [ ] Decisions documented in PDR-101 update
**Estimate**: 1-2 hours

---

## Phase 1: Participant Mode Enhancement

*Goal: Make Piper a better participant in Slack conversations.*

### Ticket P1-1: Add Threading Support to ConversationTurn
**Type**: Feature
**Assignee**: Lead Developer
**Description**: Add `parent_id` field to ConversationTurn for basic threading.
**Acceptance Criteria**:
- [ ] Migration adds nullable `parent_id` column to `conversation_turns`
- [ ] Domain model updated with `parent_id: Optional[str]`
- [ ] Repository methods support parent filtering
- [ ] Tests verify threading relationships
**Estimate**: 2-3 hours
**Files**:
- `services/domain/models.py`
- `services/database/models.py`
- `alembic/versions/xxx_add_conversation_threading.py`
- `services/repositories/conversation_repository.py`

### Ticket P1-2: Implement ConversationLink Model
**Type**: Feature
**Assignee**: Lead Developer
**Description**: Implement the ConversationLink domain model and database table.
**Acceptance Criteria**:
- [ ] `ConversationLinkType` enum added to `shared_types.py`
- [ ] `ConversationLink` domain model in `services/domain/models.py`
- [ ] `ConversationLink` ORM model in `services/database/models.py`
- [ ] `ConversationLinkRepository` with CRUD operations
- [ ] Migration creates `conversation_links` table
- [ ] Tests for link creation, retrieval, type filtering
**Estimate**: 4-6 hours
**Files**:
- `services/shared_types.py`
- `services/domain/models.py`
- `services/database/models.py`
- `alembic/versions/xxx_add_conversation_links.py`
- `services/repositories/conversation_link_repository.py`
- `tests/unit/services/repositories/test_conversation_link_repository.py`

### Ticket P1-3: Slack Thread Context Tracking
**Type**: Enhancement
**Assignee**: Lead Developer
**Description**: Enhance Slack integration to track and persist thread structure.
**Acceptance Criteria**:
- [ ] Slack thread_ts mapped to ConversationTurn.parent_id
- [ ] Reply chains create appropriate ConversationLinks (type=reply)
- [ ] @mention extraction creates reference links
- [ ] Thread context available in intent classification
**Estimate**: 6-8 hours
**Dependencies**: P1-1, P1-2
**Files**:
- `services/integrations/slack/slack_plugin.py`
- `services/integrations/slack/message_handler.py`
- `tests/integration/services/integrations/slack/test_thread_tracking.py`

### Ticket P1-4: Task Extraction from Conversation
**Type**: Feature
**Assignee**: Lead Developer
**Description**: Implement automatic task extraction from conversation content.
**Acceptance Criteria**:
- [ ] `/task` command or natural language triggers task creation
- [ ] Task nodes linked to source message (type=annotates)
- [ ] Tasks visible in existing Todo system
- [ ] Integration with Slack action buttons for task creation
**Estimate**: 4-6 hours
**Dependencies**: P1-2
**Files**:
- `services/intent_service/canonical_handlers.py`
- `services/todo_management/todo_service.py`
- `tests/unit/services/test_task_extraction.py`

---

## Phase 2: Host Mode Foundation

*Goal: Enable Piper to host structured multi-participant conversations.*

### Ticket P2-1: Implement Full ConversationNode Model
**Type**: Feature
**Assignee**: Lead Developer
**Description**: Implement the full ConversationNode model with type variants.
**Acceptance Criteria**:
- [ ] `ConversationNodeType` enum (message, task, whisper, decision, question)
- [ ] `ConversationNode` domain model with type-specific data payloads
- [ ] Database model with JSON data column for flexibility
- [ ] Repository with type-filtered queries
**Estimate**: 6-8 hours
**Files**:
- `services/shared_types.py`
- `services/domain/models.py`
- `services/database/models.py`
- `alembic/versions/xxx_add_conversation_nodes.py`
- `services/repositories/conversation_node_repository.py`

### Ticket P2-2: Implement ConversationGraph Model
**Type**: Feature
**Assignee**: Lead Developer
**Description**: Implement the ConversationGraph aggregate with participant support.
**Acceptance Criteria**:
- [ ] `ConversationGraph` domain model with nodes, links, participants
- [ ] Database model with proper relationships
- [ ] Repository methods for graph operations (add node, add link, get subgraph)
- [ ] Support for multiple participants per conversation
**Estimate**: 8-10 hours
**Dependencies**: P2-1
**Files**:
- `services/domain/models.py`
- `services/database/models.py`
- `services/repositories/conversation_graph_repository.py`

### Ticket P2-3: Timeline View Projection
**Type**: Feature
**Assignee**: Lead Developer
**Description**: Implement timeline view projection over conversation graph.
**Acceptance Criteria**:
- [ ] API endpoint returns nodes ordered by timestamp
- [ ] Filter options for node types
- [ ] Pagination support
- [ ] Backward compatible with existing chat UI
**Estimate**: 4-6 hours
**Dependencies**: P2-2
**Files**:
- `web/api/routes/conversations.py`
- `services/conversation/conversation_service.py`

### Ticket P2-4: Thread View Projection
**Type**: Feature
**Assignee**: Lead Developer
**Description**: Implement thread view projection (hierarchical nested structure).
**Acceptance Criteria**:
- [ ] API endpoint returns nodes grouped by parent_id
- [ ] Nested response structure for thread rendering
- [ ] Depth limiting for performance
**Estimate**: 4-6 hours
**Dependencies**: P2-2
**Files**:
- `web/api/routes/conversations.py`
- `services/conversation/conversation_service.py`

### Ticket P2-5: Tasks View Projection
**Type**: Feature
**Assignee**: Lead Developer
**Description**: Implement tasks view projection (kanban board data).
**Acceptance Criteria**:
- [ ] API endpoint returns task nodes grouped by status
- [ ] Status transitions (open → in-progress → closed)
- [ ] Assignee filtering
- [ ] Links to source conversation context
**Estimate**: 4-6 hours
**Dependencies**: P2-2
**Files**:
- `web/api/routes/conversations.py`
- `services/conversation/conversation_service.py`

### Ticket P2-6: Multi-Participant UI Support
**Type**: Feature
**Assignee**: Lead Developer
**Description**: Update chat UI to support multiple participants.
**Acceptance Criteria**:
- [ ] Participant list in conversation header
- [ ] Author attribution on messages
- [ ] Invite flow for adding participants
- [ ] Leave conversation flow
**Estimate**: 8-10 hours
**Dependencies**: P2-2
**Files**:
- `templates/home.html`
- `web/static/js/chat.js`
- `web/api/routes/conversations.py`

---

## Phase 3: Personal Agents (Future)

*Tickets to be defined after Phase 2 completion.*

### Ticket P3-1: Whisper Node Implementation
**Type**: Feature
**Description**: Private AI suggestions visible only to one user.

### Ticket P3-2: Per-Participant Context
**Type**: Feature
**Description**: User-specific conversation state and preferences.

### Ticket P3-3: Facilitator Agent
**Type**: Feature
**Description**: Shared agent helping group toward outcomes.

---

## Dependency Graph

```
Phase 0:
  P0-1 (ADR Review) → P0-2 (Schema Design)
                    → P0-3 (Ted Sync)

Phase 1:
  P0-2 → P1-1 (Threading) → P1-3 (Slack Threads)
       → P1-2 (Links)     → P1-3
                          → P1-4 (Task Extraction)

Phase 2:
  P1-2 → P2-1 (Nodes) → P2-2 (Graph) → P2-3 (Timeline)
                                     → P2-4 (Threads)
                                     → P2-5 (Tasks)
                                     → P2-6 (Multi-UI)
```

---

## Estimated Timeline

| Phase | Tickets | Total Estimate | Blocking Dependencies |
|-------|---------|----------------|----------------------|
| Phase 0 | 3 | 6-10 hours | ADR acceptance |
| Phase 1 | 4 | 16-23 hours | Phase 0 |
| Phase 2 | 6 | 34-46 hours | Phase 1 |
| Phase 3 | TBD | TBD | Phase 2 |

**Total Phase 0-2**: ~56-79 development hours

---

## Risk Register

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Schema migration complexity | High | Medium | Design migration path upfront; maintain backward compatibility |
| UI complexity for multi-view | Medium | High | Incremental rollout; timeline remains default |
| Performance with graph queries | Medium | Medium | Materialized views for common projections |
| Scope creep into Host Mode | High | High | Strict phase gates; PM approval for phase advancement |
| Ted's PRD drift from Piper needs | Medium | Low | Regular sync via advisor mailbox |

---

## Success Criteria

### Phase 1 Complete When:
- [ ] Slack threads persist with proper structure
- [ ] Links track conversation relationships
- [ ] Tasks extractable from conversation
- [ ] No regression in existing chat functionality

### Phase 2 Complete When:
- [ ] Multi-participant conversations work
- [ ] All three view projections functional
- [ ] Migration path for existing conversations documented
- [ ] Alpha tester feedback positive

---

*Gameplan created: January 13, 2026*
*Reference: external/ted-multichat/ for POC implementation details*

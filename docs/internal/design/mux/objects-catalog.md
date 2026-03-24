# Objects Catalog

**Issue**: #706 MUX-OBJECTS-VIEWS (Phase 1)
**Created**: 2026-03-24
**Source**: Automated codebase inventory + domain model analysis
**Status**: Complete

---

## Hard Objects (Entities with Identity + Persistence)

Objects with a unique identity, database persistence, and potential for lifecycle treatment.

| Object | DB Table | lifecycle_state? | to_dict()? | Ownership | Key Relationships |
|--------|----------|-----------------|------------|-----------|-------------------|
| **Product** | products | No (planned: 5-state enum) | No | NATIVE | → Features, → Projects (via FK) |
| **Project** | projects | Yes (optional) | Yes | NATIVE | → Product, → Integrations, → Repositories, → WorkItems |
| **Feature** | features | Yes (optional) | Yes | NATIVE | → Product, → WorkItems, → Risks |
| **WorkItem** | work_items | Yes (optional) | Yes | NATIVE | → Feature, → Project |
| **Todo** | todo_items | Yes (optional) | Yes (via Item) | NATIVE | → Lists, → parent Todo, → related Todos |
| **Repository** | repositories | No | Yes | FEDERATED | → Projects (M:M via link table) |
| **Conversation** | conversations | Yes (ACTIVE/ARCHIVED/DELETED) | Yes | NATIVE | → ConversationTurns, → User |
| **Document** | — (analysis only) | No | Yes | NATIVE | → UploadedFile |
| **UploadedFile** | uploaded_files | No | Yes | NATIVE | → references |
| **List** | lists | No | Yes | NATIVE | → ListItems (polymorphic) |
| **KnowledgeNode** | knowledge_nodes | No | Yes | NATIVE | → KnowledgeEdges |
| **KnowledgeEdge** | knowledge_edges | No | Yes | NATIVE | → source Node, → target Node |
| **Place** | — (runtime) | No | No | FEDERATED | External source window (GitHub, Calendar, etc.) |
| **UserTrustProfile** | user_trust_profiles | No (has TrustStage) | Yes | NATIVE | → User, → TrustEvents |
| **StandupConversation** | — (session) | Yes (state machine) | Yes | NATIVE | → Turns, → User |

### Lifecycle State Support

| Object | Has lifecycle_state | States | Infrastructure Status |
|--------|-------------------|--------|----------------------|
| **Project** | Yes (#709) | LifecycleState enum (optional) | DB column exists, to_dict wired |
| **Feature** | Yes (#705) | LifecycleState enum (optional) | DB column exists, to_dict wired |
| **WorkItem** | Yes (#685) | LifecycleState enum (optional) | DB column exists, to_dict wired |
| **Todo** | Yes (#708) | LifecycleState enum (optional) | DB column exists, to_dict wired |
| **Conversation** | Yes (#715) | ACTIVE, ARCHIVED, DELETED | DB column exists, spec #858 |
| **Product** | Planned (#717) | PLANNING, ACTIVE, MAINTENANCE, SUNSET, ARCHIVED | Not yet in DB — M2 migration |

### Ownership Classification (ADR-045)

| Category | Objects | Meaning |
|----------|---------|---------|
| **NATIVE** | Product, Project, Feature, Todo, List, Conversation, Document, UploadedFile, KnowledgeNode/Edge, UserTrustProfile | Created and managed within Piper |
| **FEDERATED** | Repository, Place | Windows into external systems (GitHub, Calendar, Slack) |

---

## Soft Objects (Value Objects, Transient, Configuration)

Objects without persistent identity — computed, derived, or request-scoped.

| Object | Purpose | Lifetime |
|--------|---------|----------|
| **Intent** | Parsed user intent (category, action, confidence) | Request-scoped |
| **ConversationTurn** | Single turn in conversation | Persisted as part of Conversation |
| **Task** | Workflow task unit | Workflow-scoped |
| **WorkflowResult** | Execution result | Workflow-scoped |
| **SharePermission** | Permission grant (user_id + role) | Stored as JSON in parent |
| **TrustEvent** | Individual interaction for trust computation | Stored in profile |
| **EthicalDecision** | Ethics boundary check record | Audit log |
| **SpatialContext** | Spatial positioning metadata | Request-scoped |
| **DocumentSummary** | Structured analysis output | Response-scoped |
| **PersonalityProfile** | Warmth, confidence, action orientation settings | DB-persisted config |

---

## Enums & Status Types

| Enum | Values | Used By |
|------|--------|---------|
| **LifecycleState** | (8 states from MUX) | Feature, WorkItem, Project, Todo |
| **ConversationLifecycleState** | ACTIVE, ARCHIVED, DELETED | Conversation |
| **TodoStatus** | PENDING, IN_PROGRESS, COMPLETED, CANCELLED | Todo |
| **TodoPriority** | LOW, MEDIUM, HIGH, URGENT | Todo |
| **TrustStage** | NEW, BUILDING, ESTABLISHED, TRUSTED | UserTrustProfile |
| **IntegrationType** | GITHUB, JIRA, LINEAR, SLACK | ProjectIntegration |
| **WorkflowStatus** | PENDING, RUNNING, COMPLETED, FAILED | Workflow |
| **PlaceType** | ISSUE_TRACKING, COMMUNICATION, TEMPORAL, DOCUMENTATION | Place |
| **ShareRole** | VIEWER, EDITOR, ADMIN | SharePermission |

---

## Summary

- **15 Hard Objects** with database persistence
- **10+ Soft Objects** (transient/computed)
- **6 Objects with lifecycle_state** (Product planned for M2)
- **2 Ownership categories**: NATIVE (13 objects), FEDERATED (2 objects)

# Views Catalog

**Issue**: #706 MUX-OBJECTS-VIEWS (Phase 2)
**Created**: 2026-03-24
**Source**: Template + route + JS inventory of codebase
**Status**: Complete

---

## Current Views (Exist in Codebase)

### Full Page Views

| View | Template | API Routes | Objects Displayed | Lifecycle UI? |
|------|----------|-----------|-------------------|---------------|
| **Home / Dashboard** | `home.html` | `/api/v1/conversations`, `/api/v1/intent` | Conversations, chat history, preferences | No |
| **Projects List** | `projects.html` | `/api/v1/projects` | Project (name, description, integrations, archived) | Planned |
| **Project Detail** | `project_detail.html` | `/api/v1/projects/{id}`, integrations, repos | Project, ProjectIntegration, Repository, WorkItem | Planned |
| **Todos** | `todos.html` | `/api/v1/todos` | Todo (text, priority, status, completed, due_date) | Planned |
| **Work Items** | `work_items.html` | `/api/v1/work-items` | WorkItem (title, type, status, priority, source) | Yes (component exists) |
| **Documents** | `documents.html` | `/api/v1/documents` | Document, DocumentSummary, AnalysisResult | No |
| **Files** | `files.html` | `/api/v1/files` | UploadedFile (filename, type, size, upload date) | No |
| **Lists** | `lists.html` | `/api/v1/lists` | List, ListItem (polymorphic) | No |
| **Insights** | `insights.html` | `/api/v1/knowledge` | KnowledgeNode, Place, InsightGenerated | No |
| **Standup** | `standup.html` | `/api/v1/standup` | StandupConversation, ConversationTurn | No |
| **Learning Dashboard** | `learning-dashboard.html` | `/api/v1/learning` | UserTrustProfile, TrustEvent, LearnedPattern | No |
| **Settings Hub** | `settings-index.html` | various | Integration tiles, feature access | N/A |
| **Integration Settings** | `integrations.html` | `/api/v1/settings/integrations` | ProjectIntegration, IntegrationType | N/A |
| **Personality Settings** | `personality-preferences.html` | `/api/v1/personality` | PersonalityProfile, Preference | N/A |
| **Account** | `account.html` | auth routes | User, UserTrustProfile | N/A |
| **Login** | `login.html` | `/auth` | User, JWT | N/A |
| **Setup / Onboarding** | `setup.html` | `/setup` | PortfolioOnboardingSession | N/A |

### Reusable Components

| Component | Template | Objects | Notes |
|-----------|----------|---------|-------|
| **Chat Widget** | `chat-widget.html` | Conversation, ConversationTurn | Floating, collapsible |
| **Chat Inline** | `chat-inline.html` | Conversation, ConversationTurn | Embedded in Home |
| **Navigation** | `navigation.html` | User, currentPage | Top nav bar |
| **Lifecycle Indicator** | `lifecycle_indicator.html` | LifecycleState | Badge component (#423) |
| **Lifecycle Detail** | `lifecycle_detail.html` | LifecycleState, WorkflowStatus | Expanded view |
| **Lifecycle Notification** | `lifecycle_notification.html` | LifecycleState, WorkItem | Toast on state change |
| **Command Palette** | `command_palette.html` | Todos, Projects, Lists, Documents | Global search |
| **Insight Card** | `insight_card.html` | InsightGenerated | Individual insight display |
| **Place Window** | `place_window.html` | Place, SpatialObject | External source modal (#722) |
| **Conversation History** | `history_sidebar.html` | Conversation list | Sidebar (#565) |
| **Preference Suggestion** | `preference_suggestion.html` | Preference | Accept/dismiss card |
| **Greeting Context** | `greeting_context.html` | RequestContext, UserTrustProfile | Time/status greeting |
| **Piper Avatar** | (in chat.js) | — | Dolphin logo (#924) |
| **User Avatar** | (in chat.js) | User initial | Colored circle (#924) |

### Chat-Only Views (Conversational, No Dedicated Page)

| Capability | Accessed Via | Objects | Has Dedicated Page? |
|-----------|-------------|---------|-------------------|
| **Product queries** | "What products am I working on?" | Product | No — M2 |
| **GitHub issue ops** | "Close issue #123" | WorkItem (external) | No (uses chat) |
| **Reminders** | "Remind me to X tomorrow" | Todo (with reminder_date) | No (shows in Todos) |
| **Calendar queries** | "What's on my schedule?" | Place (FEDERATED) | No |
| **Guidance** | "What should I focus on?" | Floor response (LLM) | No |

---

## Potential Views (Don't Exist Yet)

Views that the domain model supports but have no UI implementation.

| Potential View | Objects It Would Display | Priority | Notes |
|---------------|------------------------|----------|-------|
| **Product Detail** | Product, Features, Projects, health summary | M2 | Decision 5 from #717: clickable from project grouping header |
| **Product List** | Products with lifecycle state, project count, feature count | M2+ | Only if user has multiple products (growth path to nav Option A) |
| **Feature Detail** | Feature, WorkItems, lifecycle_state, risks, dependencies | M2 | Unblocked by #717 Product concept |
| **Feature List** | Features grouped by lifecycle state | M2 | Part of Product detail view |
| **Knowledge Graph Visualization** | KnowledgeNode, KnowledgeEdge | M3+ | Graph rendering is complex |
| **Trust Dashboard** | UserTrustProfile, TrustStage progression, TrustEvents | M3+ | Internal/advanced — not user-facing initially |
| **Repository Dashboard** | Repository, PRs, issues, commit activity | M2 | GitHub integration view |
| **Calendar View** | Place (TEMPORAL), Events | M2 | Depends on calendar integration maturity |
| **Retrospective View** | Completed todos, conversations, standup history | M3+ | Cross-session synthesis |
| **Conversation Archive** | Conversation (ARCHIVED), ConversationTurn | M3+ | Search/browse old conversations |

---

## Object × View Matrix

Which objects appear in which views (current state).

| Object | Home | Projects | Project Detail | Todos | Work Items | Documents | Lists | Insights | Chat |
|--------|------|----------|---------------|-------|------------|-----------|-------|----------|------|
| **Product** | — | — (M2: header) | — | — | — | — | — | — | ✅ (via chat) |
| **Project** | — | ✅ | ✅ | — | ref | — | — | — | ✅ |
| **Feature** | — | — | — (M2) | — | — | — | — | — | — |
| **WorkItem** | — | — | ref | — | ✅ | — | — | — | ✅ |
| **Todo** | — | — | — | ✅ | — | — | — | — | ✅ |
| **Repository** | — | — | ✅ | — | ref | — | — | — | — |
| **Conversation** | ✅ | — | — | — | — | — | — | — | ✅ |
| **Document** | — | — | — | — | — | ✅ | — | — | — |
| **UploadedFile** | — | — | — | — | — | ✅ | — | — | — |
| **List** | — | — | — | — | — | — | ✅ | — | — |
| **KnowledgeNode** | — | — | — | — | — | — | — | ✅ | — |
| **Place** | — | — | — | — | — | — | — | ✅ | ✅ |
| **UserTrustProfile** | — | — | — | — | — | — | — | — | implicit |

Key: ✅ = displayed, ref = referenced/linked, — = not present

---

## Summary

- **17 full page views** currently implemented
- **15+ reusable components**
- **5 chat-only capabilities** (no dedicated page)
- **10 potential views** identified for future sprints
- **Lifecycle UI components exist** (indicator, detail, notification) but are only wired to Work Items

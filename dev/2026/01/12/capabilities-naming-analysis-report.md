# Capabilities Naming Analysis Report

**Date**: January 12, 2026
**Prepared by**: Lead Developer (Claude Code Opus 4.5)
**Requested by**: PM (xian)
**Purpose**: Normalize capability naming for user communication, marketing, and internal clarity

---

## Executive Summary

Piper Morgan has **35+ distinct capabilities** accumulated over development. Analysis reveals **5 naming patterns** currently in use, creating user confusion. This report proposes a **consistent naming convention** and suggests specific names for each capability.

**Key Finding**: Most capabilities use descriptive/technical naming, while only a few have proper product names (e.g., "Morning Standup"). A hybrid naming approach is recommended: **product names for flagship features**, **verb-noun for actions**, **category groupings for discoverability**.

---

## 1. Capability Inventory Table

### Core Chat & Conversation

| Capability | Current Names | Technical Reference | Description | Integrations |
|------------|---------------|---------------------|-------------|--------------|
| Natural language chat | "chat interface", "conversational AI" | `IntentService.process_intent()` | Core chat with intent classification | None (core) |
| Context memory | "10-turn context", "conversation memory" | `ConversationRepository` | Remember conversation across turns | None (core) |
| Greeting/chitchat | "conversation handling" | `IntentCategory.CONVERSATION` | Social interaction, greetings | None (core) |
| Portfolio onboarding | "portfolio onboarding", "project setup" | `portfolio_handler.py` | Conversational first-time project setup | None (core) |

### Standup & Daily Work

| Capability | Current Names | Technical Reference | Description | Integrations |
|------------|---------------|---------------------|-------------|--------------|
| Quick standup generation | "Morning Standup", "Generate Standup" | `/api/v1/standup/generate` | One-click standup report | GitHub, Calendar, Notion |
| Interactive standup | "Interactive Standup Assistant", "standup conversation" | `standup_workflow_skill.py` | Multi-turn standup writing | All |
| Preference learning | "preference gathering", "style preferences" | `preference_extractor.py` | Learn user standup style | None (core) |

### Task & Project Management

| Capability | Current Names | Technical Reference | Description | Integrations |
|------------|---------------|---------------------|-------------|--------------|
| Todo management | "todos", "task creation", "Add a todo" | `TodoRepository` | Create/track/complete todos | None (core) |
| List management | "lists", "Lists feature" | `ListRepository` | Organize todos into lists | None (core) |
| Project tracking | "projects", "project management" | `ProjectRepository` | Track projects and allocations | None (core) |
| Priority guidance | "What should I focus on?", "priority queries" | `IntentCategory.PRIORITY` | Recommend what to work on | All |
| Status queries | "What am I working on?", "status queries" | `IntentCategory.STATUS` | Show current work status | All |

### Document & File Management

| Capability | Current Names | Technical Reference | Description | Integrations |
|------------|---------------|---------------------|-------------|--------------|
| File upload | "file upload", "Upload File" | `/api/v1/files/upload` | Upload documents for analysis | None (core) |
| Document analysis | "document analysis", "Summarize this PDF" | `_handle_analysis_intent` | Analyze uploaded documents | None (core) |
| Document search | "search documents", "search_notion" | `_handle_search_documents_notion` | Search Notion documents | Notion |
| Document update | "update document", "edit_document" | `_handle_update_document_notion` | Edit Notion pages | Notion |

### Calendar & Scheduling

| Capability | Current Names | Technical Reference | Description | Integrations |
|------------|---------------|---------------------|-------------|--------------|
| Availability check | "Am I free?", "check availability" | `_handle_meeting_time_query` | Check calendar availability | Calendar |
| Meeting time analysis | "How much time in meetings?" | `_handle_meeting_time_query` | Analyze meeting load | Calendar |
| Recurring meeting audit | "review recurring meetings" | `_handle_recurring_meetings_query` | Audit recurring events | Calendar |
| Week ahead view | "What's my week like?" | `_handle_week_calendar_query` | Preview upcoming schedule | Calendar |

### GitHub Integration

| Capability | Current Names | Technical Reference | Description | Integrations |
|------------|---------------|---------------------|-------------|--------------|
| Issue creation | "Create an issue", "GitHub issue creation" | `_handle_create_issue` | Create GitHub issues | GitHub |
| Issue review | "Show issue #123", "review issue" | `_handle_review_issue_query` | View issue details | GitHub |
| Issue closing | "Close issue #123" | `_handle_close_issue_query` | Close GitHub issues | GitHub |
| Issue commenting | "Comment on issue" | `_handle_comment_issue_query` | Add comments to issues | GitHub |
| Shipped PRs view | "What shipped this week?" | `_handle_shipped_this_week` | Show merged PRs | GitHub |
| Stale PRs audit | "Show stale PRs" | `_handle_stale_prs` | Find old open PRs | GitHub |
| Commit analysis | "Analyze commits" | `_handle_analyze_commits` | Summarize commit activity | GitHub |

### Slack Integration

| Capability | Current Names | Technical Reference | Description | Integrations |
|------------|---------------|---------------------|-------------|--------------|
| Slack messaging | "Slack integration", "send messages" | `slack_plugin.py` | Send/receive Slack messages | Slack |
| Spatial awareness | "spatial intelligence", "workspace navigator" | `spatial_agent.py` | Understand Slack workspace context | Slack |
| Attention decay | "attention model", "message prioritization" | `attention_model.py` | Prioritize recent messages | Slack |
| Channel navigation | "workspace navigation" | `workspace_navigator.py` | Navigate Slack channels | Slack |

### Intelligence & Learning

| Capability | Current Names | Technical Reference | Description | Integrations |
|------------|---------------|---------------------|-------------|--------------|
| Changes tracking | "What changed?", "contextual intelligence" | `_handle_changes_query` | Track changes since last check | All |
| Attention items | "What needs attention?" | `_handle_attention_query` | Surface items needing focus | All |
| Productivity metrics | "my productivity", "weekly metrics" | `_handle_productivity_query` | Show productivity summary | All |
| Pattern learning | "learning system", "pattern recognition" | `QueryLearningLoop` | Learn from user behavior | None (core) |
| Cross-feature learning | "cross-feature patterns" | `CrossFeatureKnowledgeService` | Share patterns across features | None (core) |

### Identity & Help

| Capability | Current Names | Technical Reference | Description | Integrations |
|------------|---------------|---------------------|-------------|--------------|
| Self-identification | "What's your name?", "identity queries" | `IntentCategory.IDENTITY` | Explain who Piper is | None (core) |
| Capability explanation | "What can you do?", "guidance queries" | `IntentCategory.GUIDANCE` | Explain available features | None (core) |
| Health check | "system health", "status check" | `_handle_identity_health_check` | Show system health | None (core) |
| Temporal awareness | "What day is it?", "temporal queries" | `IntentCategory.TEMPORAL` | Date/time awareness | None (core) |

---

## 2. Pattern Analysis

### Current Naming Patterns Identified

| Pattern | Examples | Frequency | Effectiveness |
|---------|----------|-----------|---------------|
| **Product Name** | "Morning Standup", "Interactive Standup Assistant" | ~3 features | High - memorable, marketable |
| **Verb-First Action** | "Generate Standup", "Create issue", "Upload File" | ~15 features | Medium - clear but generic |
| **Question Form** | "What shipped?", "Am I free?", "What needs attention?" | ~10 features | High - natural language |
| **Technical Name** | "spatial intelligence", "attention decay", "preference learning" | ~8 features | Low - confusing to users |
| **Integration Name** | "GitHub integration", "Slack messaging", "Notion search" | ~6 features | Medium - clear source |

### Inconsistencies Found

| Issue | Example | Problem |
|-------|---------|---------|
| Same capability, different names | "Morning Standup" vs "standup generation" vs "Generate Standup" | User doesn't know if these are the same |
| Technical names exposed | "spatial intelligence", "attention model" | Users don't understand what these mean |
| Missing product names | Document analysis has no name | Hard to refer to in conversation |
| Verb inconsistency | "Create issue" vs "Issue creation" vs "creating issues" | No standard form |
| Question vs statement | "What shipped?" vs "Shipped PRs view" | Inconsistent for same capability |

---

## 3. Recommended Naming Convention

### The Hybrid Naming Framework

**Tier 1: Flagship Features (Product Names)**
- Reserved for core, differentiated capabilities
- Format: `[Modifier] [Noun]` - e.g., "Morning Standup", "Priority Coach"
- Used in: Marketing, onboarding, release notes headlines

**Tier 2: Actions (Verb-Noun)**
- For specific user actions
- Format: `[Verb] [Object]` - e.g., "Create Issue", "Upload Document"
- Used in: UI buttons, help text, commands

**Tier 3: Queries (Natural Questions)**
- For information retrieval
- Format: Natural question - e.g., "What's my schedule?", "What shipped?"
- Used in: Example prompts, help documentation

**Tier 4: Categories (Grouping)**
- For organizing related capabilities
- Format: `[Domain] [Type]` - e.g., "GitHub Tools", "Calendar Features"
- Used in: Settings, navigation, feature lists

### Naming Rules

1. **User-facing names never use technical terms** (no "spatial", "intent", "canonical")
2. **Product names are capitalized** (Morning Standup, not morning standup)
3. **Actions use imperative verbs** (Create, Upload, Review, not Creating, Uploading)
4. **Questions use second person** ("What's on my calendar?" not "Calendar query")
5. **Integrations are secondary** ("Create GitHub Issue" not "GitHub: Create Issue")

---

## 4. Proposed Names

### Flagship Features (Tier 1 - Product Names)

| Current | Proposed Name | Rationale |
|---------|---------------|-----------|
| "Morning Standup" / "Generate Standup" | **Morning Standup** | Already established, keep it |
| "Interactive Standup Assistant" | **Standup Coach** | Shorter, emphasizes guidance |
| "priority queries" / "guidance queries" | **Priority Coach** | Positions as strategic advisor |
| "spatial intelligence" / "attention model" | **Smart Notifications** | User benefit, not technical |
| "preference learning" | **Learning Mode** | Simple concept, implies adaptation |
| "contextual intelligence" | **Context Tracker** | Clear benefit |

### Actions (Tier 2 - Verb-Noun)

| Current | Proposed Name | UI Label |
|---------|---------------|----------|
| "Create an issue" | **Create Issue** | "Create Issue" button |
| "file upload" | **Upload Document** | "Upload Document" button |
| "Add a todo" | **Add Todo** | "Add Todo" button |
| "search documents" | **Search Documents** | "Search" in Notion section |
| "update document" | **Edit Document** | "Edit" action |
| "Close issue #123" | **Close Issue** | "Close Issue" action |
| "Comment on issue" | **Add Comment** | "Add Comment" action |

### Queries (Tier 3 - Natural Questions)

| Current | Proposed Query | Category |
|---------|----------------|----------|
| "shipped_this_week" | "What shipped this week?" | GitHub |
| "stale_prs" | "Show stale PRs" | GitHub |
| "meeting_time" | "How much time in meetings?" | Calendar |
| "recurring_meetings" | "Review recurring meetings" | Calendar |
| "week_calendar" | "What's my week like?" | Calendar |
| "productivity" | "How am I doing?" | Productivity |
| "changes_query" | "What changed?" | Context |
| "attention_query" | "What needs attention?" | Context |
| "status queries" | "What am I working on?" | Status |

### Categories (Tier 4 - Groupings)

| Group Name | Capabilities Included |
|------------|----------------------|
| **Standup Tools** | Morning Standup, Standup Coach |
| **Task Management** | Todos, Lists, Projects |
| **GitHub Tools** | Create Issue, Close Issue, Add Comment, What Shipped, Stale PRs |
| **Calendar Features** | Schedule Check, Meeting Analysis, Week Preview |
| **Document Tools** | Upload Document, Search Documents, Edit Document |
| **Slack Features** | Smart Notifications, Workspace Navigation |
| **Productivity Insights** | Priority Coach, Context Tracker, Productivity Summary |

---

## 5. Implementation Recommendations

### Quick Wins (v0.8.4 or v0.8.5)

1. **Update example prompts** in `home.html` help tooltip
2. **Update release notes** to use consistent naming
3. **Update ALPHA_TESTING_GUIDE.md** section headers
4. **Update PIPER.md** System Capabilities section

### Medium-Term (v0.9.x)

1. **Create capabilities taxonomy** in docs
2. **Update UI labels** across templates
3. **Create "What can Piper do?" help page**
4. **Align error messages** with new names

### Longer-Term

1. **Create capabilities API** for dynamic feature discovery
2. **Build interactive capabilities explorer**
3. **Localization-ready naming architecture**

---

## 6. PM Feedback & Guidance (Added 12:07 PM)

### Terminology Direction

**Avoid "Coach" terminology** - too loaded at this stage. Prefer **"Assistant"** framing that emphasizes support and assistance.

### Updated Name Proposals

| Original Proposal | Revised Direction | Rationale |
|-------------------|-------------------|-----------|
| Priority Coach | **Focus Assistant** | Assistant framing, pending CXO/PPM/Comms review |
| Standup Coach | **Standup Assistant** | Consistent with assistant model |
| Smart Notifications | *Open - explore options* | Consider "Don't Miss" or similar - need consistency principle |
| Learning Mode | **Marketing feature, not UI** | Valuable capability to promote, not a menu command |
| "How am I doing?" | *Calibration needed* | See naming tone spectrum below |
| GitHub Tools | **Backlog Tools** or similar | Frame as agile/PM function, not coding tool |

### Naming Tone Spectrum (New Framework Addition)

PM identified three naming registers to calibrate:

| Register | Description | Example |
|----------|-------------|---------|
| **(a) Plain Natural Language** | Clear, no jargon, accessible | "What needs attention?" |
| **(b) Industry-Standard Jargon** | PM/Product terminology | "Backlog", "Sprint", "Standup" |
| **(c) Unique/Clever but Clear** | Memorable, differentiated | "Don't Miss" (for attention items) |

**Principle**: Balance all three. Not all features need clever names, but flagship features benefit from memorable differentiation while remaining immediately clear.

### GitHub Integration Framing

> "Frame the GitHub integration less as a coding tool but more for its agile project management functions. The future of PMs with AI is role bleeding so Piper will help with design and coding work, but the frame is still that of a product person."

**Implication**: Rename "GitHub Tools" to something like:
- **Backlog Tools** (agile framing)
- **Issue Tracker** (function-focused)
- **Project Tracker** (broader PM scope)

### Open Questions for Broader Review

These should go to CXO, PPM, and Comms Chief before converging:

1. **Focus Assistant** - PM's current preference, but open for input
2. **Standup Assistant** vs other assistance language
3. **"Don't Miss"** or similar unique naming - need consistency principle
4. **Naming tone balance** - how much (c) clever naming vs (a) plain language?
5. **Backlog Tools** or alternative PM-centric framing for GitHub features

### Validation Approach

- A/B testing possible for key names
- Alpha tester feedback on naming clarity
- Frameworks and principles should precede specific decisions

---

## Appendix: Source File References

| Source | What It Defines |
|--------|-----------------|
| `config/PIPER.md` | System capabilities section (authoritative for docs) |
| `docs/ALPHA_TESTING_GUIDE.md` | Feature descriptions for testers |
| `docs/releases/*.md` | Release notes (feature announcements) |
| `templates/home.html` | Example prompts, orientation modal |
| `templates/standup.html` | "Morning Standup" page title |
| `templates/learning-dashboard.html` | "Learning System Dashboard" title |
| `services/shared_types.py` | `IntentCategory` enum (technical) |
| `services/intent_service/canonical_handlers.py` | Handler method names (technical) |

---

*Report generated: January 12, 2026, ~12:30 PM*
*Auditor: Lead Developer (Claude Code Opus 4.5)*

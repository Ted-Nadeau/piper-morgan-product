# Piper Morgan Naming Conventions

**Version**: 1.0
**Date**: January 17, 2026
**Authors**: CXO (primary), with input from PM, PPM, and Communications Chief
**Status**: Ratified
**Location**: `docs/internal/design/naming-conventions.md`

---

## Purpose

This document establishes naming conventions for Piper Morgan's capabilities, features, and UI elements. Consistent naming improves user comprehension, reduces confusion, and reinforces Piper's identity as a professional colleague.

---

## Core Principles

### 1. Plain by Default (But Not Cold)

90% of capabilities use functional, transparent names. Users should understand what will happen before they act.

**Good**: "What should I focus on?", "Create Issue", "Upload Document"
**Avoid**: "Priority Coach", "Document Intelligence Engine", "Smart Upload"

**Important**: Plain language doesn't mean clinical or cold. Piper is a warm, professional colleague. Plain naming applies to *feature names and categories*—the voice and tone in help text, responses, and UI copy should still reflect Piper's personality. See `piper-style-guide.md` for voice guidance.

### 2. Flagship Features Earn Memorable Names

Reserve distinctive naming for 2-3 core differentiators that are:
- Used frequently (daily or near-daily)
- Difficult to describe in 2-3 plain words
- Central to Piper's value proposition

**Current flagship**: Morning Standup
**Candidates for future**: TBD through alpha testing

### 3. No "X Assistant" Proliferation

When in doubt, use the natural query rather than inventing a branded wrapper.

**Good**: "What should I focus on?" (natural query)
**Avoid**: "Focus Assistant", "Priority Assistant", "Calendar Assistant"

**When "Assistant" IS appropriate**: Use "X Assistant" only when ALL of these criteria are met:
1. The capability involves a multi-turn conversation (not a single query/response)
2. The capability has a distinct workflow or state machine
3. There's no natural query that captures the full capability
4. The name doesn't conflict with an existing flagship feature

**Approved**: "Standup Assistant" (interactive standup conversation—distinct from "Morning Standup" one-click version)
**Not approved**: "Focus Assistant" (use natural query "What should I focus on?" instead)

### 4. Benefits Over Mechanics

User-facing copy describes what the capability does for the user, not how it works technically.

**Good**: "Piper notices what's happening in your Slack and highlights what matters"
**Avoid**: "Spatial intelligence with attention decay modeling"

Technical names (Spatial Intelligence, Attention Model, Query Learning Loop) stay in code and architecture docs. They never appear in UI, help text, or user communications.

### 5. "Tools" for Action Categories

Action-oriented capability categories use "Tools" suffix for consistency.

**Standard**: Standup Tools, Document Tools, Calendar Tools
**Avoid mixing**: "GitHub Features", "Slack Capabilities", "Calendar Functions"

### 6. Integration-Agnostic Categories

Category names should survive adding new integrations. Name for the function, not the current provider.

| Integration | Category Name | Rationale |
|-------------|---------------|-----------|
| GitHub | Issue Tracker (or Work Tracking) | Future: Linear, Jira, Asana |
| Google Calendar | Calendar Tools | Future: Outlook, Apple Calendar |
| Notion | Document Tools | Future: Confluence, Google Docs |
| Slack | Communication Tools | Future: Teams, Discord |

In UI, the integration name appears in settings ("Connect GitHub"). The category name appears in help and feature groupings ("Issue Tracker").

### 7. Internal Vocabulary Stays Internal

Architecture concepts inform design thinking but don't become user vocabulary unless they earn it through genuine utility.

**Internal (team use)**: Entities, Moments, Places, Situations, Composting, Trust Gradient
**User-facing**: Describe the experience, not the model

Test: Would a user ever need to say this word to use Piper effectively? If not, it stays internal.

---

## Naming Framework

### Four Tiers

| Tier | Purpose | Format | Examples |
|------|---------|--------|----------|
| **1. Flagship** | Core differentiators | Memorable product name | Morning Standup |
| **2. Actions** | User-initiated operations | Verb + Object | Create Issue, Upload Document |
| **3. Queries** | Information retrieval | Natural question | "What shipped this week?", "Am I free at 2?" |
| **4. Categories** | Feature groupings | Function + "Tools" | Issue Tracker, Calendar Tools |

### Tier 1: Flagship Features

Reserved for capabilities that meet ALL criteria:
- Daily or near-daily use
- Core to Piper's differentiation
- Memorable name adds value over plain description

**Current**: Morning Standup
**Process for new flagships**: Propose → Alpha test → Validate comprehension → Approve

### Tier 2: Actions

Format: `[Verb] [Object]`

| Verb | Use For |
|------|---------|
| Create | Making new things (Create Issue, Create Todo) |
| Add | Appending to existing (Add Comment, Add Todo) |
| Upload | File submission (Upload Document) |
| Edit | Modification (Edit Document) |
| Close | Completion/resolution (Close Issue) |
| Search | Finding (Search Documents) |

### Tier 3: Queries

Format: Natural question the user would actually ask

| Category | Example Queries |
|----------|-----------------|
| Status | "What am I working on?" |
| Priority | "What should I focus on?" |
| Calendar | "Am I free tomorrow at 2?", "What's my week like?" |
| Changes | "What changed since yesterday?" |
| Attention | "What needs my attention?" |
| Productivity | "How am I doing this week?" |
| GitHub | "What shipped this week?", "Show stale PRs" |

### Tier 4: Categories

Format: `[Function] Tools` or `[Function] Tracker`

| Category | Includes |
|----------|----------|
| Standup Tools | Morning Standup, Standup Assistant |
| Issue Tracker | Create Issue, Close Issue, What Shipped, Stale PRs |
| Calendar Tools | Availability check, Meeting analysis, Week preview |
| Document Tools | Upload, Search, Edit |
| Communication Tools | Slack features, notification preferences |
| Productivity Insights | Focus guidance, Context tracking, Weekly summary |

---

## Naming Tone Spectrum

Three registers to calibrate:

| Register | Description | When to Use |
|----------|-------------|-------------|
| **(a) Plain language** | Clear, no jargon, accessible | Default for 90% of naming |
| **(b) Industry jargon** | PM/Product terminology | When audience expects it (Backlog, Sprint, Standup) |
| **(c) Unique/memorable** | Differentiated, branded | Flagship features only |

**Balance**: Predominantly (a), selective (b) where it aids comprehension, rare (c) for true differentiators.

---

## Anti-Patterns

### Don't Do This

| Anti-Pattern | Example | Problem |
|--------------|---------|---------|
| Technical names in UI | "Spatial Intelligence Dashboard" | Users don't understand |
| Marketing-speak | "AI-Powered Productivity Enhancer" | Feels like adware |
| "X Assistant" proliferation | Focus Assistant, Calendar Assistant, GitHub Assistant | Undifferentiated, forgettable |
| Verb inconsistency | "Create issue" / "Issue creation" / "Creating issues" | Confusing |
| Integration as category | "GitHub Tools" | Doesn't survive adding Linear |
| Internal vocabulary leak | "View your Moments" | Users don't know this term |

### The Colleague Test

Ask: Would a human colleague use this phrase naturally?

- ✅ "Here's what shipped this week"
- ✅ "You might want to look at these"
- ❌ "Activating Context Tracker module"
- ❌ "Your Attention Model has surfaced 3 items"

---

## Application Guide

### Where These Names Appear

| Location | Tier Used | Examples |
|----------|-----------|----------|
| Page titles | Flagship or Category | "Morning Standup", "Issue Tracker" |
| Buttons | Actions | "Create Issue", "Upload Document" |
| Help text | Queries | "Try asking: 'What should I focus on?'" |
| Navigation | Categories | Standup Tools, Calendar Tools |
| Release notes | Mix | Flagship names for headlines, plain for details |
| Error messages | Plain language | "I couldn't find that issue" (not "Issue retrieval failed") |

### Decision Tree for New Capabilities

```
Is this a core differentiator used daily?
├── Yes → Consider Flagship name (test with users first)
└── No → Is it a user action?
    ├── Yes → Use Verb + Object format
    └── No → Is it information retrieval?
        ├── Yes → Use natural question format
        └── No → It's probably a category grouping → Use [Function] Tools
```

---

## Governance

### Adding New Names

1. **Actions/Queries**: Follow format conventions, no approval needed
2. **Categories**: Propose in PR, CXO or PPM approves
3. **Flagship**: Propose → Alpha test comprehension → PM/CXO/PPM approve

### Changing Existing Names

Existing names in production require:
1. Documented rationale
2. Migration plan (what changes where)
3. PM approval

### Exceptions

If a situation requires breaking conventions, document:
- What convention is being broken
- Why it's necessary
- Whether it should prompt convention update

---

## Related Documents

This document focuses on **naming** (what we call things). For other aspects of Piper's communication:

| Document | Scope |
|----------|-------|
| `piper-style-guide.md` | Voice, tone, first-person conventions |
| `empty-state-voice-guide-v1.md` | Empty state messaging patterns |
| *Voice Guide (future)* | Confidence/uncertainty expressions |

**Note**: Confidence and uncertainty expressions (e.g., "I think...", "I'm not sure but...") are not yet documented. Flag for future voice guide work.

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0 Draft | 2026-01-12 | Initial draft from CXO/PM/PPM synthesis |
| 1.0 | 2026-01-17 | Incorporated Comms refinements: (1) "Plain ≠ Cold" clarification, (2) principled "X Assistant" criteria, (3) related documents section, (4) flagged confidence/uncertainty gap |

---

*Ratified: January 17, 2026*

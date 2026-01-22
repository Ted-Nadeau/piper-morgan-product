# D6: Journal Architecture Specification

**Issue**: #431 MUX-VISION-LEARN
**Deliverable**: 6 of 7
**Question Addressed**: How do Session Journal and Insight Journal work together?

---

## Core Principle

**Separate audit from insight.**

Two distinct journals serve different purposes:
- **Session Journal**: Factual record of what happened (audit/compliance)
- **Insight Journal**: Patterns and learnings derived from experience (user-facing)

These are never mixed. "What happened" is separate from "what it means."

---

## Two-Layer Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERACTION                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    SESSION JOURNAL                          │
│  ─────────────────────────────────────────────────────────  │
│  Purpose: Audit trail, compliance, debugging                │
│  Contents: Every interaction, raw events, timestamps        │
│  Mutability: Immutable (append-only)                        │
│  User access: Trust level 4+ on explicit request            │
│  Retention: Configurable (default 90 days)                  │
└─────────────────────────────────────────────────────────────┘
                              │
                    [Composting Process]
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     INSIGHT JOURNAL                         │
│  ─────────────────────────────────────────────────────────  │
│  Purpose: User-facing learnings and patterns                │
│  Contents: Extracted insights, confidence scores, topics    │
│  Mutability: Mutable (users can correct/delete)             │
│  User access: All trust levels (visibility varies)          │
│  Retention: Until deleted by user or system                 │
└─────────────────────────────────────────────────────────────┘
```

---

## Session Journal

### Purpose

Complete audit trail for:
- Compliance requirements
- Debugging issues
- Transparency requests
- System health monitoring

### Contents

Every interaction is logged:

```
SESSION ENTRY
├── timestamp: 2026-01-22T10:15:32Z
├── entry_type: user_message
├── session_id: abc-123
├── content_hash: [hash, not content]
├── context:
│   ├── active_project: Henderson Proposal
│   ├── previous_action: calendar_query
│   └── trust_level: 3
├── piper_response_id: def-456
└── metadata:
    ├── latency_ms: 342
    └── tools_used: [calendar, todo]
```

### Characteristics

| Attribute | Value |
|-----------|-------|
| Mutability | **Immutable** (append-only) |
| Retention | 90 days default, configurable |
| Encryption | At rest and in transit |
| User access | Trust level 4+ on request |
| Format | Structured, machine-readable |

### What Session Journal Contains

- Timestamps of all interactions
- Message types and categories
- Context at time of interaction
- Tool/service invocations
- Response metadata (latency, errors)
- Session boundaries

### What Session Journal Does NOT Contain

- Full message content (hash only, unless configured otherwise)
- Personal identifying information (PII)
- Third-party data verbatim
- Insight derivations or learnings

### Session Journal Access

```
USER: Show me my session history

PIPER: [If Trust Level < 4]
       Session history is available at Trust Level 4, which we haven't
       reached yet. I'm being cautious because the raw session log
       contains a lot of detail that could be overwhelming or misleading.

       If you want to see what I've learned, I can show you the
       Insight Journal instead—that's the meaningful summary.

PIPER: [If Trust Level 4+]
       Here's your recent session history:

       [Displays session entries in human-readable format]

       This is the raw record of our interactions. The Insight Journal
       shows what I've learned from this; want to see that too?
```

---

## Insight Journal

### Purpose

User-facing collection of:
- Patterns noticed from work together
- Preferences inferred or stated
- Learnings extracted from composting
- Premonitions and concerns

### Contents

Structured insights with metadata:

```
INSIGHT ENTRY
├── id: insight-001
├── type: pattern
├── expression: "Morning meetings preferred for complex discussions"
├── confidence: 0.84
├── created: 2026-01-15T03:22:00Z
├── updated: 2026-01-20T14:30:00Z
├── topic: scheduling.meeting_preferences
├── source_type: composting
├── source_references: [12 composted objects]
├── visibility: passive
├── trust_level_required: 2
└── user_corrections: []
```

### Characteristics

| Attribute | Value |
|-----------|-------|
| Mutability | **Mutable** (users can correct/delete) |
| Retention | Until deleted or contradicted |
| Organization | Topical with recency weighting |
| User access | All levels (visibility gated by trust) |
| Format | Human-readable, browsable |

### Insight Types

| Type | Description | Example |
|------|-------------|---------|
| **Pattern** | Recurring structure | "Projects with early alignment have fewer revisions" |
| **Preference** | User preference (inferred or stated) | "Morning meetings preferred" |
| **Observation** | Noticed but not pattern yet | "Last 3 deadlines were on Fridays" |
| **Concern** | Potential issue flagged | "This timeline seems tight" |
| **Premonition** | Forward-looking inference | "This might need stakeholder review" |

### Insight Visibility Levels

| Level | Description | Trust Requirement |
|-------|-------------|-------------------|
| **Pull** | Only shown when asked | Any |
| **Passive** | Browsable in journal | Any |
| **Push** | Actively surfaced | Stage 3+ |

---

## Session → Insight: The Extraction Process

### When Extraction Happens

Insights are extracted from Session Journal during **composting**:

1. **Scheduled composting** (quiet hours, default 2-5 AM)
2. **Triggered composting** (object reaches deprecated state)
3. **Manual composting** (user requests reflection)

### What Moves to Insight Journal

| Session Data | Insight Extraction |
|--------------|-------------------|
| Multiple similar events | Pattern detection |
| User corrections | High-confidence preferences |
| Explicit user statements | Direct preferences |
| Goal-outcome gaps | Learning opportunities |
| Recurring contexts | Contextual patterns |

### Confidence Thresholds

| Confidence | Treatment |
|------------|-----------|
| 0.8+ | Eligible for push surfacing (Stage 3+) |
| 0.6-0.8 | Visible in passive mode, pull-responsive |
| 0.4-0.6 | Pull-only, low-priority display |
| < 0.4 | Not promoted to Insight Journal |

### Extraction Rules

**Pattern Promotion**:
- Requires 3+ similar observations
- Must have consistent context
- Confidence = (supporting events / total relevant events)

**Preference Recording**:
- Direct user statement: confidence 0.95
- Consistent behavior (5+ times): confidence 0.80
- Inconsistent behavior: confidence 0.50-0.70

**Contradiction Handling**:
- New observation contradicts insight: flag for review
- User correction: update immediately with high confidence
- Contradicting insights: lower confidence of both, await clarification

---

## Organization: Topical with Recency Weighting

### Topic Hierarchy

```
Insight Journal
├── Work Patterns
│   ├── Productivity
│   ├── Focus & Deep Work
│   └── Task Management
├── Communication
│   ├── Meeting Preferences
│   ├── Writing Style
│   └── Response Patterns
├── Scheduling
│   ├── Time Preferences
│   ├── Buffer Preferences
│   └── Availability Patterns
├── Projects
│   ├── [Active Project 1]
│   ├── [Active Project 2]
│   └── [Archived Projects]
├── People & Teams
│   ├── Collaboration Patterns
│   └── Working Relationships
└── Preferences
    ├── Tool Preferences
    ├── Format Preferences
    └── Communication Channel Preferences
```

### Recency Weighting

Within each topic:
1. Most recent insights appear first
2. Recently-applied insights surface higher
3. Old, unused insights gradually sink
4. Stale insights (unused 90+ days) prompt review

### Cross-Topic Linking

Insights may relate to multiple topics:
- Primary topic: where insight appears
- Related topics: cross-referenced
- Example: "Prefers morning meetings" → primary: Scheduling, related: Productivity

---

## User Operations on Journals

### Session Journal

| Operation | User Can? | Notes |
|-----------|-----------|-------|
| View | Yes (Trust 4+) | On explicit request |
| Search | Yes (Trust 4+) | Limited scope |
| Export | Yes | For portability |
| Edit | **No** | Immutable record |
| Delete | **No** | Retention policy only |

### Insight Journal

| Operation | User Can? | Notes |
|-----------|-----------|-------|
| View | Yes | Gated by trust level |
| Search | Yes | Free-form queries |
| Correct | Yes | Updates insight immediately |
| Delete | Yes | Permanent removal |
| Export | Yes | For portability |
| Reset | Yes | Requires confirmation |

---

## Privacy & Security

### Data Separation

Session and Insight journals are stored separately:
- Different encryption keys
- Different access controls
- Different retention policies

### What's Never Connected

- No link from deleted insight back to source sessions
- No reconstruction of deleted insights possible
- No cross-user pattern extraction

### Audit Trail for Deletions

Session Journal records THAT a deletion happened (for compliance), but NOT what was deleted:

```
SESSION ENTRY
├── timestamp: 2026-01-22T11:00:00Z
├── entry_type: insight_deletion
├── insight_id: insight-001
├── reason: user_requested
└── content: [not stored]
```

---

## Technical Specifications

### Session Journal Schema

```
SessionEntry:
  id: UUID
  timestamp: DateTime
  entry_type: Enum[message, tool_call, response, error, system]
  session_id: UUID
  content_hash: String (SHA-256)
  context: JSON
  metadata: JSON
  created_at: DateTime
```

### Insight Journal Schema

```
InsightEntry:
  id: UUID
  type: Enum[pattern, preference, observation, concern, premonition]
  expression: String
  confidence: Float (0.0-1.0)
  topic: String (hierarchical)
  visibility: Enum[pull, passive, push]
  trust_level_required: Integer (1-4)
  source_type: Enum[composting, direct_input, correction]
  source_count: Integer
  created_at: DateTime
  updated_at: DateTime
  last_applied_at: DateTime (nullable)
  user_corrections: JSON[]
```

### Composting Queue Schema

```
CompostingQueueEntry:
  id: UUID
  source_object_id: UUID
  source_object_type: String
  scheduled_for: DateTime
  status: Enum[pending, processing, complete, failed]
  extracted_insights: UUID[] (nullable)
  created_at: DateTime
```

---

## Integration Points

### Morning Standup

Insight Journal is primary source for standup insights:
- "I've noticed..." statements come from Insight Journal
- Reflection summaries aggregate recent insights

### Intent Classification

Insights inform intent understanding:
- "You usually mean X when you say Y" (preference insight)
- Context recognition uses pattern insights

### Recommendation Engine

Insights feed recommendations:
- Scheduling suggestions use time preference insights
- Format suggestions use communication insights

---

## Migration & Portability

### Export Format

Users can export both journals:

**Session Journal Export** (Trust 4+ only):
```json
{
  "export_type": "session_journal",
  "export_date": "2026-01-22",
  "entries": [...],
  "format_version": "1.0"
}
```

**Insight Journal Export**:
```json
{
  "export_type": "insight_journal",
  "export_date": "2026-01-22",
  "insights": [...],
  "format_version": "1.0"
}
```

### Import Capability

- Insight Journal: Can import (merges with existing)
- Session Journal: Cannot import (integrity concerns)

---

## Success Metrics

This specification succeeds if:

- [ ] Users understand the two-journal distinction
- [ ] Session Journal serves compliance needs
- [ ] Insight Journal feels like "Piper's memory" to users
- [ ] Extraction process produces useful insights
- [ ] Users trust that deleted insights are truly gone
- [ ] No confusion between "what happened" and "what I learned"

---

## Related Specifications

- **D1**: Learning Visibility (how insights are displayed)
- **D2**: Control Interface (user operations on journals)
- **D3**: Composting Experience (extraction process UX)
- **D7**: Trust-Based Access (who sees what in each journal)

---

*Specification: D6 Journal Architecture Specification*
*Issue: #431 MUX-VISION-LEARN*
*Created: 2026-01-22*

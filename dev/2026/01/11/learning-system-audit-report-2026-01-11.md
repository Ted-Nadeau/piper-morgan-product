# Learning System Implementation Audit Report

**Date**: January 11, 2026
**Auditor**: Lead Developer (Claude Code Opus 4.5)
**Requestor**: Chief Architect

---

## Executive Summary

The learning system has **substantial implemented infrastructure** for preference learning and pattern tracking, with the attention decay system recently completed. However, the **composting/knowledge consolidation pipeline exists only as architecture documentation** - no implementation exists. The gap is significant: real-time learning works, but the "dreaming" mechanism for batch processing accumulated experience is entirely unbuilt.

---

## Implemented Components

### 1. Preference Learning System (Standup Domain)

**Location**: `services/standup/`
- `preference_service.py` - User preference storage and retrieval
- `preference_extractor.py` - Pattern extraction from conversation turns
- `preference_applicator.py` - Apply preferences to standup generation
- `preference_feedback.py` - Handle user corrections/confirmations

**Purpose**: Learn user preferences for standup format, timing, content filtering through conversation analysis.

**Key Classes/Functions**:
| Class | Methods | Purpose |
|-------|---------|---------|
| `UserPreferenceService` | 14 methods | CRUD for preferences with history tracking |
| `PreferenceExtractor` | 13 methods | Extract preferences from natural language |
| `PreferenceApplicator` | 8 methods | Apply learned preferences to output |
| `PreferenceFeedbackHandler` | 11 methods | Process corrections/confirmations |

**Test Coverage**:
- `tests/unit/services/standup/test_preference_*.py` - **118 tests, all passing**
- `tests/integration/test_preference_learning.py` - Integration tests

**Integration Points**:
- Connected to standup generation workflow
- Stores in JSON files under `data/` (not database)
- Feedback loop via conversation turns

**Status**: **Working** - Full implementation with comprehensive tests

---

### 2. Attention Decay System (Slack Domain)

**Location**: `services/integrations/slack/attention_model.py`, `services/scheduler/attention_decay_job.py`

**Purpose**: Model attention priority for Slack messages with temporal decay, spatial awareness, and pattern learning.

**Key Classes/Functions**:
| Class | Methods | Purpose |
|-------|---------|---------|
| `AttentionModel` | 24 methods | Core attention scoring, focus management, pattern learning |
| `AttentionDecayJob` | 6 methods | Background job for periodic decay updates |
| `AttentionEvent` | 1 method | Individual attention event with intensity decay |
| `AttentionPattern` | dataclass | Learned attention patterns |

**Test Coverage**:
- `tests/integration/services/test_attention_pattern_persistence.py` - **7 tests, all passing**
- `tests/unit/services/integrations/slack/test_attention_scenarios_validation.py`

**Integration Points**:
- Background job runs every 5 minutes (configured in `web/startup.py`)
- Pattern persistence to database via `_save_pattern_to_db()` / `load_patterns_from_db()`
- Started via `AttentionDecayPhase` in startup lifecycle

**Status**: **Working** - Recently completed (Issue #365: SLACK-ATTENTION-DECAY)

---

### 3. Query Learning Loop

**Location**: `services/learning/query_learning_loop.py`

**Purpose**: Learn patterns from query processing to improve future query handling.

**Key Classes/Functions**:
| Class | Methods | Purpose |
|-------|---------|---------|
| `QueryLearningLoop` | 17 methods | Pattern learning, application, feedback, cleanup |
| `LearnedPattern` | dataclass | Individual pattern representation |
| `PatternFeedback` | dataclass | Feedback on pattern application |

**Persistence**:
- JSON file: `data/learning/learned_patterns.json` (3,082 lines, contains test patterns from Oct 2025)
- Database table: `learned_patterns` (migration exists, Issue #300)

**Test Coverage**:
- `tests/integration/test_learning_system.py` - **7 passed, 2 skipped**
- `tests/intent/test_learning_handlers.py` - **8 tests, all passing**

**Status**: **Working** - Real-time learning functional, patterns persist to JSON

---

### 4. Cross-Feature Knowledge Service

**Location**: `services/learning/cross_feature_knowledge.py`

**Purpose**: Share learned patterns across different features/domains.

**Key Classes/Functions**:
| Class | Methods | Purpose |
|-------|---------|---------|
| `CrossFeatureKnowledgeService` | 14 methods | Knowledge sharing, pattern transfer, feedback |
| `SharedKnowledge` | dataclass | Cross-feature knowledge representation |
| `CrossFeaturePattern` | dataclass | Transferred pattern representation |

**Status**: **Implemented** - Enables pattern sharing between features

---

### 5. Learning Handler (Intent Integration)

**Location**: `services/learning/learning_handler.py`

**Purpose**: Capture actions and outcomes to feed learning system.

**Key Classes/Functions**:
| Class | Methods | Purpose |
|-------|---------|---------|
| `LearningHandler` | 7 methods | Action capture, outcome recording, suggestions |

**Status**: **Working** - Connected to intent processing

---

### 6. Pattern Recognition Service

**Location**: `services/knowledge/pattern_recognition_service.py`

**Purpose**: Detect patterns across knowledge graph nodes, identify trends and anomalies.

**Key Classes/Functions**:
| Class | Methods | Purpose |
|-------|---------|---------|
| `PatternRecognitionService` | 18 methods | Similarity, cross-project patterns, trends, anomalies |

**Status**: **Implemented** - Used for knowledge graph analysis

---

### 7. Database Schema for Learning

**Migrations**:
- `6ae2d637325d_add_learned_patterns_table_issue_300.py` - `learned_patterns` table
- `3242bdd246f1_add_learning_settings_table_issue_300.py` - `learning_settings` table

**Database Model**: `services/database/models.py:LearnedPattern` (line 1703)

**Schema**:
```
learned_patterns:
  - id (UUID, PK)
  - user_id (UUID, FK users)
  - pattern_type (enum: USER_WORKFLOW, COMMAND_SEQUENCE, TIME_BASED, CONTEXT_BASED, PREFERENCE, INTEGRATION)
  - pattern_data (JSON)
  - confidence (Float, default 0.5)
  - usage_count, success_count, failure_count (Integer)
  - enabled (Boolean)
  - last_used_at, created_at, updated_at (DateTime)
```

**Status**: **Schema exists** - Table created, not heavily used (JSON file preferred currently)

---

## Not Implemented (Despite Design Docs)

### 1. Composting Pipeline

**Design Doc Reference**: `docs/internal/architecture/current/composting-learning-architecture.md`

**What's Described**:
- `CompostBin` - Staging area for deprecated objects
- `Decomposer` - Breaks down objects into learnable parts
- `LearningExtractor` - Analyzes decomposition for patterns
- `InsightJournal` - Stores and surfaces learnings
- `EmergentCreator` - Spawns new objects from high-confidence learnings
- `TriggerMonitor` - Evaluates when objects should be composted

**What's Missing**: **100% of this** - No classes, no files, no implementation whatsoever.

**Evidence**: `grep -r "CompostBin\|Decomposer\|InsightJournal\|EmergentCreator" services/` returns no matches.

---

### 2. "Filing Dreams" / Rest-Period Processing

**Design Doc Reference**: `composting-learning-architecture.md` Section 3

**What's Described**:
- Quiet hours processing (2-5 AM)
- Batch analysis of accumulated experience
- "Filing dreams" metaphor for organic insight surfacing

**What's Missing**: No scheduled job for knowledge consolidation. Only jobs that exist:
- `attention_decay_job.py` - Attention decay (runs every 5 min)
- `standup_reminder_job.py` - Standup reminders
- `blacklist_cleanup_job.py` - Blacklist maintenance

**No "dreaming" or "rest period" job exists.**

---

### 3. Insight Journal

**Design Doc Reference**: `composting-learning-architecture.md` Section 5

**What's Described**:
- Repository of learnings with confidence scores
- Trust-level gating for surfacing
- Natural language expression of insights
- Visibility levels (pull/passive/push)

**What's Missing**: No `InsightJournal` class or equivalent storage for synthesized insights.

---

### 4. Object Lifecycle Stages (Composting-Ready)

**Design Doc Reference**: ADR-045 Object Model

**What's Described**: 8-stage lifecycle: EMERGENT → DERIVED → NOTICED → PROPOSED → RATIFIED → DEPRECATED → ARCHIVED → COMPOSTED

**What's Missing**: No evidence of objects tracking lifecycle stage through to COMPOSTED. Domain models don't have lifecycle stage fields.

---

## Background Job Inventory

| Job Name | Trigger | Purpose | Location | Status |
|----------|---------|---------|----------|--------|
| `AttentionDecayJob` | Every 5 minutes | Update attention event intensities with decay | `services/scheduler/attention_decay_job.py` | **Active** |
| `StandupReminderJob` | Time-based | Send standup reminders | `services/scheduler/standup_reminder_job.py` | Active |
| `BlacklistCleanupJob` | Periodic | Clean expired blacklist entries | `services/scheduler/blacklist_cleanup_job.py` | Active |
| `ReminderScheduler` | Event-based | General reminder scheduling | `services/scheduler/reminder_scheduler.py` | Active |
| **CompostingJob** | Quiet hours | Process accumulated experience | N/A | **NOT IMPLEMENTED** |

---

## Key Findings

1. **Real-time learning works well**: Preference extraction, attention decay, and query pattern learning are all implemented with good test coverage (130+ tests passing).

2. **The "dreaming" mechanism is pure vaporware**: The composting architecture document is comprehensive (631 lines) but represents 0% implementation. No code exists for:
   - Batch processing of experience
   - Insight synthesis
   - Knowledge consolidation
   - Rest-period jobs

3. **JSON vs Database disconnect**: Learning patterns use `data/learning/learned_patterns.json` while database migrations created `learned_patterns` table. The JSON file has 3,082 lines of (mostly test) data.

4. **Attention decay is the newest learning component**: Issue #365 (SLACK-ATTENTION-DECAY) completed recently with full integration tests.

5. **No object lifecycle tracking**: Domain models don't implement the 8-stage lifecycle from ADR-045. Objects can't reach "COMPOSTED" stage because they don't track lifecycle stage.

6. **Cross-feature learning infrastructure exists but usage unclear**: `CrossFeatureKnowledgeService` has 14 methods but integration points are not well-documented.

---

## Recommendations

### For the Chief Architect

1. **The "dreaming" mechanism requires greenfield implementation**. The architecture doc is a spec, not documentation of existing code. Budget accordingly.

2. **Consider whether composting is MVP or post-MVP**. Current real-time learning may be sufficient for initial product. Composting adds sophistication but significant complexity.

3. **If proceeding with composting, implement incrementally**:
   - Phase 1: Object lifecycle stage tracking in domain models
   - Phase 2: CompostBin staging and TriggerMonitor
   - Phase 3: Decomposer for pattern extraction
   - Phase 4: InsightJournal storage
   - Phase 5: EmergentCreator feedback loop
   - Phase 6: Quiet-hours scheduling

4. **Resolve JSON vs Database persistence strategy** before adding more learning infrastructure. Current dual-storage adds complexity.

5. **The attention decay pattern (Pattern-048) is a good template** for any new periodic background jobs, including potential composting jobs.

---

## Appendix: Test Summary

| Component | Test File | Tests | Status |
|-----------|-----------|-------|--------|
| Preference Service | `test_preference_service.py` | 18 | Pass |
| Preference Extractor | `test_preference_extractor.py` | 29 | Pass |
| Preference Applicator | `test_preference_applicator.py` | 29 | Pass |
| Preference Feedback | `test_preference_feedback.py` | 38 | Pass |
| Preference Integration | `test_preference_integration.py` | 4 | Pass |
| Attention Persistence | `test_attention_pattern_persistence.py` | 7 | Pass |
| Learning System | `test_learning_system.py` | 7 | Pass (2 skip) |
| Learning Handlers | `test_learning_handlers.py` | 8 | Pass |

**Total: 140+ tests passing** for implemented learning components.

---

*Report generated: January 11, 2026, ~10:00 PM*
*Auditor: Lead Developer (Claude Code Opus 4.5)*

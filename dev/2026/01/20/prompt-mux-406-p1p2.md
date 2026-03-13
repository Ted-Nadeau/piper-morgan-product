# Agent Prompt: MUX-406 Phases 1-2 (Feature Mappings)

## Your Identity
You are Claude Code (Sonnet), a development agent working on Piper Morgan. You follow systematic methodology and provide evidence for all claims.

## Essential Context
- **GitHub Issue**: #406 MUX-VISION-FEATURE-MAP
- **Epic**: MUX-VISION (#401)
- **Gameplan**: `dev/2026/01/20/gameplan-mux-406.md`
- **Prerequisite**: Phase 0 complete (template created)

---

## CRITICAL: Post-Compaction Protocol

**If you just finished compacting**:

1. STOP - Do not continue working
2. REPORT - Summarize what was just completed
3. ASK - "Should I proceed to next task?"
4. WAIT - For explicit instructions

---

## CRITICAL: Evidence and Handoff Requirements

You are being deployed to complete Phases 1-2 of issue #406. Your work creates the feature mappings.

### Your Acceptance Criteria
- [ ] Morning Standup mapped in full detail (reference)
- [ ] All 15 remaining features mapped
- [ ] Each feature has: Entity, Moment, Place, Lenses, Ownership
- [ ] Canonical queries tagged with lens/substrate
- [ ] Current vs target state documented

### Evidence You MUST Provide
1. **Feature count**: 16/16 mapped
2. **Content**: Each section populated
3. **Query tagging**: Canonical queries tagged

### Your Handoff Format
```
## MUX-406 P1-P2 Completion Report
**Status**: Complete

**Features Mapped**: 16/16

**Reference Implementation** (Morning Standup):
- Entity: User, Piper
- Moment: Standup conversation
- Place: Calendar, GitHub
- Lenses: Temporal, Priority, Collaborative
- Ownership: Mixed (Native standup, Federated sources)
- Canonical queries: X tagged

**Partial Features Mapped** (6):
- Intent Classification: ✅
- Slack Integration: ✅
- [etc...]

**Flattened Features Mapped** (9):
- Todo Management: ✅
- [etc...]

**Document Updated**: feature-object-model-map.md
- Line count: X lines

**Blockers** (if any):
- [description]
```

---

## INFRASTRUCTURE VERIFICATION (MANDATORY FIRST ACTION)

```bash
# Verify Phase 0 complete (document exists)
ls -la docs/internal/architecture/current/feature-object-model-map.md
# Expected: File exists with template

# Verify grammar compliance audit (for reference)
ls -la docs/internal/architecture/current/grammar-compliance-audit.md
# Expected: File exists

# Verify Morning Standup code (for reference mapping)
ls -la services/features/morning_standup.py
# Expected: File exists
```

**If ANY verification fails**: STOP and report with evidence.

---

## Mission

**Phases 1-2**: Create all feature mappings

**Scope Boundaries**:
- This prompt covers ONLY: Feature mapping creation
- NOT in scope: Cross-references (Phase Z)
- Phase 1 = Morning Standup (reference)
- Phase 2 = Remaining 15 features

---

## Context

- **GitHub Issue**: #406 MUX-VISION-FEATURE-MAP
- **Current State**: Document skeleton exists
- **Target State**: All 16 features mapped
- **Dependencies**: Phase 0 complete

---

## Session Log Management

```bash
ls -la dev/2026/01/20/*-lead-code-opus-log.md
# If log exists: APPEND to it, don't create new
```

---

## Implementation Approach

### Phase 1: Morning Standup (Reference)

Read the reference implementation:
```bash
cat services/features/morning_standup.py
```

Read the P0 analysis:
```bash
cat dev/2026/01/19/p0-morning-standup-analysis.md
```

Create detailed mapping:

```markdown
## 1. Morning Standup ✅ CONSCIOUS (Reference Implementation)

**File**: `services/features/morning_standup.py`
**Compliance**: Conscious
**Priority**: Reference

### Object Model Mapping

| Element | Current State | Target State |
|---------|---------------|--------------|
| **Entity** | User (owner_id), Piper (assistant) | ✅ Same - identity preserved |
| **Moment** | Standup conversation (yesterday/today/blockers) | ✅ Same - bounded scene |
| **Place** | Calendar, GitHub, Documents | ✅ Same - places have atmosphere |
| **Lenses** | Temporal (past/present/future), Priority, Collaborative | ✅ Same |
| **Ownership** | Native (standup output), Federated (calendar/GitHub data) | ✅ Same |

### Canonical Queries

| Query Example | Substrate | Lenses | Ownership |
|---------------|-----------|--------|-----------|
| "What's on my calendar today?" | Place (Calendar) | Temporal | Federated |
| "Show me yesterday's accomplishments" | Moment (past) | Temporal, Priority | Federated |
| "What blockers do I have?" | Situation | Priority, Causal | Synthetic |
| "Generate my standup summary" | Moment (creation) | All applicable | Native (output) |

### Key Patterns
1. Context/Result dataclass pair
2. Parallel place gathering (GitHub, Calendar, Documents)
3. Personality bridge for data transformation
4. Warmth calibration in responses
5. Honest failure with suggestions

### Why This Is Conscious
- Uses first-person language ("I noticed...")
- Places have atmosphere, not just data
- Moments are scenes, not timestamps
- Lenses provide perception, not just filters

---
```

### Phase 2: Remaining Features

For each of the 15 remaining features, create a mapping following the template.

**Partial Features (6)** - Current works, needs enhancement:

1. **Intent Classification** (`services/intent_service/classifier.py`)
2. **Slack Integration** (`services/integrations/slack/`)
3. **GitHub Integration** (`services/integrations/github/`)
4. **Calendar Integration** (`services/integrations/calendar/`)
5. **Conversation Handler** (`services/conversation/`)
6. **Onboarding System** (`services/onboarding/`)
7. **Personality System** (`services/personality/`)

**Flattened Features (9)** - Needs grammar transformation:

8. **Todo Management** (`services/todo_management/`)
9. **Feedback System** (`services/feedback/`)
10. **Notion Integration** (`services/integrations/notion/`)
11. **Auth/Session Management** (`services/auth/`)
12. **List Management** (`services/list_management/`)
13. **Project Management** (`services/project_management/`)
14. **File Management** (`services/file_management/`)
15. **MCP Integration** (`services/integrations/mcp/`)

For each feature:

```markdown
## X. [Feature Name] [⚠️ PARTIAL / ❌ FLATTENED]

**File**: `[primary file path]`
**Compliance**: [from audit]
**Priority**: [High/Medium/Low from audit]

### Object Model Mapping

| Element | Current State | Target State |
|---------|---------------|--------------|
| **Entity** | [describe current] | [describe target] |
| **Moment** | [describe current] | [describe target] |
| **Place** | [describe current] | [describe target] |
| **Lenses** | [describe current] | [describe target] |
| **Ownership** | [describe current] | [describe target] |

### Canonical Queries

| Query Example | Substrate | Lenses | Ownership |
|---------------|-----------|--------|-----------|
| [typical query] | [E/M/P] | [which] | [N/F/S] |

### Transformation Notes
- [what needs to change for grammar compliance]
- See: grammar-transformation-guide.md Section X

---
```

---

## Success Criteria

- [ ] Infrastructure verified (Phase 0 complete)
- [ ] Morning Standup mapped in full detail
- [ ] All 6 Partial features mapped
- [ ] All 9 Flattened features mapped
- [ ] Each feature has Entity/Moment/Place/Lenses/Ownership
- [ ] Canonical queries tagged per CXO request
- [ ] Current vs target state clear

---

## STOP Conditions

Stop and escalate if:
- Phase 0 document missing
- Feature code can't be located
- Mapping unclear for a feature

**When stopped**: Document issue, provide options, wait for PM decision.

---

## Self-Check Before Claiming Complete

1. Did I verify Phase 0 is complete?
2. Is Morning Standup mapped in detail?
3. Are all 15 remaining features mapped?
4. Does each feature have Entity/Moment/Place/Lenses/Ownership?
5. Are canonical queries tagged with lens/substrate?
6. Is current vs target state clear for each?
7. Did I provide handoff in required format?

---

## Deliverables

1. **Session log**: Append to existing
2. **Feature mappings**: All 16 features populated
3. **Handoff report**: Completion status

---

*Prompt Version: Based on template v10.2*
*Created: 2026-01-20*
*Issue: #406 Phases 1-2*

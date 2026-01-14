# Special Agent Prompt: Learning System Implementation Audit

## Context

The Chief Architect needs to understand the **actual state** of Piper's learning system implementation. There's a gap between what design documents describe (often as "future scope") and what's actually built in the codebase. This audit will inform architectural decisions about the "dreaming" mechanism for knowledge consolidation.

## Your Task

Audit the codebase to document what learning-related infrastructure **actually exists and works** versus what design documents describe. Focus on evidence: files, classes, methods, tests.

## Specific Areas to Investigate

### 1. Preference Learning System
**Look in**: `services/`, `models/`, any `preference*` files

Questions to answer:
- What preference-related modules exist? (preference_extractor.py, preference_service.py, etc.)
- What do they actually do? (extraction, storage, application, feedback?)
- What tests exist and are they passing?
- Is this connected to the standup system? How?

### 2. Attention Decay System
**Look in**: `services/`, any `attention*` files, background jobs

Questions to answer:
- Does an AttentionModel or similar exist?
- Is there a background decay job? Where does it run?
- What triggers attention updates? What triggers decay?
- Is pattern persistence implemented (save/load)?

### 3. Pattern Learning / Cross-Feature Learning
**Look in**: `services/learning/`, `services/patterns/`, any `learn*` files

Questions to answer:
- Is there a LearnedPattern model or equivalent?
- Is there cross-feature pattern sharing?
- What gets learned and stored?

### 4. Composting / Knowledge Consolidation
**Look in**: Any `compost*`, `consolidat*`, `dream*` files, background jobs

Questions to answer:
- Does any "composting" infrastructure exist?
- Is there any batch/background processing of accumulated experiences?
- Is there a "dreaming" or consolidation mechanism?

### 5. Background Job Infrastructure
**Look in**: `startup.py`, `background/`, any scheduler configs

Questions to answer:
- What background jobs exist?
- When do they run? (idle-triggered? time-triggered? load-triggered?)
- What job framework is used?

### 6. Persistence Layer for Learning
**Look in**: `models/`, database migrations, any JSON storage

Questions to answer:
- How is learned information stored? (database? JSON files? both?)
- What tables/files hold learning data?
- Is there cross-session persistence?

## Output Format

Please provide a structured report:

```markdown
# Learning System Implementation Audit Report

## Executive Summary
[2-3 sentences: What exists, what doesn't, what's the gap]

## Implemented Components

### [Component Name]
- **Location**: [file paths]
- **Purpose**: [what it does]
- **Key Classes/Functions**: [list]
- **Test Coverage**: [file, test count if findable]
- **Integration Points**: [what it connects to]
- **Status**: [Working / Partial / Stub]

[Repeat for each implemented component]

## Not Implemented (Despite Design Docs)

### [Concept from design docs]
- **Design Doc Reference**: [where it's described]
- **What's Missing**: [specific gap]
- **Blocking Issues**: [if any]

## Background Job Inventory

| Job Name | Trigger | Purpose | Location |
|----------|---------|---------|----------|
| ... | ... | ... | ... |

## Key Findings

1. [Finding 1]
2. [Finding 2]
...

## Recommendations

[Any observations about what the Chief Architect should know]
```

## What NOT to Do

- Don't guess or infer - only report what you can verify exists
- Don't read design docs and assume they're implemented
- Don't report on tests without checking if they pass
- Don't conflate "methodology composting" (our process) with "Piper's composting" (product feature)

## Time Box

This should take approximately 30-45 minutes of focused codebase exploration.

## Deliverable

Save report to: `/mnt/user-data/outputs/learning-system-audit-report-2026-01-11.md`

# Roadmap v3.0 → v4.0 Update Plan

## Principles for Update
1. **Preserve everything** - No deletion without explicit approval
2. **Mark superseded content** - Show what's changing and why
3. **Show relationships** - Connect REFACTOR epics to existing content
4. **Add, don't replace** - New content augments existing

---

## Section-by-Section Update Plan

### 1. After Vision Statement - ADD NEW SECTION
**Add: The Inchworm Protocol**
```markdown
## 🐛 The Inchworm Protocol

**Our Execution Methodology**: Complete each epic 100% before moving to next. NO EXCEPTIONS.

Each epic follows this pattern:
1. **Fix** the broken system
2. **Test** comprehensively
3. **Lock** with tests that prevent regression
4. **Document** what was done and why
5. **Verify** with core user story (GitHub issue creation)
```

---

### 2. CORE Track Phases - RESTRUCTURE & PRESERVE

**Current Structure:**
- Phase 1: UI Infrastructure Fix
- Phase 2: Plugin Architecture Epic (PLUG)
- Phase 3: Universal Intent Classification
- Phase 4: Learning Implementation

**Proposed Structure:**
```markdown
### CORE Track - The Great Refactor

#### Current State Assessment
- QueryRouter disabled but 75% complete (PM-034)
- OrchestrationEngine never initialized
- Multiple unfinished refactors creating confusion

#### Execution Approach: Sequential REFACTOR Epics

##### REFACTOR-1: Orchestration Core (Incorporates Phase 1: UI Fix)
[Details from Great Refactor roadmap]
**Relationship**: Includes Bug #166 resolution from Phase 1

##### REFACTOR-2: Integration Cleanup (New - Foundational)
[Details from Great Refactor roadmap]
**Relationship**: Prepares for clean plugin extraction

##### REFACTOR-3: Plugin Architecture (Maps to Phase 2: PLUG Epic)
[Preserve existing PLUG epic details]
[Add lock strategy from Great Refactor]
**Relationship**: Implements existing PLUG epic design

##### REFACTOR-4: Intent Universalization (Maps to Phase 3)
[Preserve existing intent classification details]
[Add lock strategy from Great Refactor]
**Relationship**: Makes existing intent system mandatory

##### REFACTOR-5: Learning Foundation (Maps to Phase 4: LEARN Epic)
[Preserve existing LEARN epic components]
[Add lock strategy from Great Refactor]
**Relationship**: Implements existing LEARN epic

##### REFACTOR-6: Quality Gates (New - Essential)
[Add validation suite from Great Refactor]
**Relationship**: Ensures all previous work is locked in
```

---

### 3. Existing Epic Details - PRESERVE & INTEGRATE

**PLUG Epic Components** (currently in roadmap):
- Plugin interface definition ✅ Keep → maps to REFACTOR-3
- GitHub plugin refactor ✅ Keep → maps to REFACTOR-3
- Notion plugin refactor ✅ Keep → maps to REFACTOR-3
- Slack plugin refactor ✅ Keep → maps to REFACTOR-3
- Spatial intelligence alignment ✅ Keep
- MCP readiness ✅ Keep

**LEARN Epic Components** (currently in roadmap):
- Pattern recognition system ✅ Keep → maps to REFACTOR-5
- Preference learning ✅ Keep → maps to REFACTOR-5
- Workflow optimization ✅ Keep → maps to REFACTOR-5
- Feedback loops ✅ Keep → maps to REFACTOR-5

**Mark as**: "Components preserved in REFACTOR-X epic"

---

### 4. MVP Track - PRESERVE WITH NOTES

**Keep all existing content, add note:**
```markdown
### MVP Track - Production Features

**🔔 Note**: MVP features blocked until Great Refactor complete. This ensures features are built on solid architectural foundation.

[All existing MVP content stays...]
```

---

### 5. Timeline - UPDATE WITHOUT LOSING DETAIL

**Current Timeline Section:**
```markdown
### 2025 Q4
- **October**: UI fix, Plugin architecture, GitHub plugin
- **November**: Complete plugins, Universal intent, Learning begins
- **December**: MVP features, Production readiness
```

**Updated Timeline Section:**
```markdown
### 2025 Q4 - The Great Refactor Sequence
- **October**:
  - Weeks 1-2: REFACTOR-1 (Orchestration Core, includes UI fix)
  - Week 3: REFACTOR-2 (Integration Cleanup)
  - Week 4: Start REFACTOR-3 (Plugin Architecture/PLUG epic)
- **November**:
  - Week 1: Complete REFACTOR-3 (Plugins)
  - Week 2: REFACTOR-4 (Intent Universalization)
  - Week 3: REFACTOR-5 (Learning Foundation/LEARN epic)
  - Week 4: REFACTOR-6 (Quality Gates)
- **December**:
  - MVP features (standup chat access, production readiness)
  - 1.0 preparation

**Note**: Sequence is strict - each REFACTOR must complete before next begins
```

---

### 6. Near-term GitHub Issues - UPDATE

**Current List:**
- Bug #166 continuation - UI hang resolution
- PLUG Epic with sub-tasks
- Intent classification universalization
- Learning system foundation
- Standup chat accessibility

**Updated List:**
```markdown
### Near-term GitHub Issues Needed

#### Great Refactor Epics (Create Immediately)
- [ ] Parent Epic: The Great Refactor (#167)
- [ ] REFACTOR-1: Orchestration Core (#168) - includes Bug #166
- [ ] REFACTOR-2: Integration Cleanup (#169)
- [ ] REFACTOR-3: Plugin Architecture (#170) - implements PLUG epic
- [ ] REFACTOR-4: Intent Universalization (#171)
- [ ] REFACTOR-5: Learning Foundation (#172) - implements LEARN epic
- [ ] REFACTOR-6: Quality Gates (#173)

#### Preserved from Original (Now Part of REFACTORs)
- Bug #166 → part of REFACTOR-1
- PLUG Epic → becomes REFACTOR-3
- Intent universalization → becomes REFACTOR-4
- Learning foundation → becomes REFACTOR-5
- Standup chat → December MVP work
```

---

### 7. New Sections to Add

**Add: North Star Validation**
```markdown
## 🎯 North Star Validation

**The GitHub Issue Creation Flow Must Work**

This is our "Hello World". Every refactor is validated against this core user story:
1. User: "Create a GitHub issue about fixing the login bug"
2. Intent classification recognizes CREATE_GITHUB_ISSUE
3. QueryRouter routes to OrchestrationEngine
4. OrchestrationEngine calls GitHub plugin
5. Issue created successfully
6. User receives confirmation
```

**Add: What We're NOT Doing**
```markdown
## What We're NOT Doing

1. **No new features** until refactors complete
2. **No partial implementations** - finish what you start
3. **No workarounds** - fix the real problem
4. **No skipping tests** - they lock in the fix
5. **No parallel work** - strict sequential execution
```

---

## Summary of Changes

### Content Preserved ✅
- All existing epic details (PLUG, LEARN)
- MVP track features and descriptions
- Success metrics
- Risk management
- Architecture decisions

### Content Enhanced 🔄
- CORE track phases → REFACTOR epics with relationships shown
- Timeline → More specific with sequential execution
- GitHub issues → Mapped to new REFACTOR structure

### Content Added ✨
- Inchworm Protocol methodology
- North Star validation scenario
- "What we're NOT doing" constraints
- Lock strategies for each epic
- Relationships between old and new structure

### Content Marked as Superseded 📝
- Parallel phase execution → Sequential REFACTOR execution
- Direct phase names → REFACTOR epic names (with mapping)

---

## Questions for PM

1. **REFACTOR-5**: Should we keep it as "Learning Foundation" or revert to "Validation Suite"? (Learning could be REFACTOR-6 or post-MVP)

2. **Existing issue numbers**: Should we preserve references to existing issues (like Bug #166) or create all new?

3. **PLUG/LEARN epic details**: Should we keep them as separate subsections or fully integrate into REFACTOR epics?

4. **MVP features**: Any that should be pulled into Great Refactor for architectural reasons?

---

**Next Step**: Upon approval of this plan, I'll create the actual updated roadmap.md preserving all content as outlined.

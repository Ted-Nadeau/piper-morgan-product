# Gameplan: #555 STANDUP-LEARNING - User Preference Learning

**Issue**: #555
**Epic**: #242 (CONV-MCP-STANDUP-INTERACTIVE)
**Priority**: P1
**Created**: 2026-01-08
**Template Version**: 9.2

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Lead Developer's Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI (verified)
- [x] Database: PostgreSQL on 5433 (verified)
- [x] Testing framework: pytest (verified)
- [x] Existing preference support: StandupConversationContext has `preferences: Dict[str, Any]` field (verified in domain models line 1337)
- [x] Learning infrastructure: `data/learning/` exists with `learned_patterns.json` and `pattern_feedback.json`

**My understanding of the task**:
- Extract user preferences from standup conversation turns ("focus on GitHub", "skip docs")
- Persist preferences per user across sessions
- Apply learned preferences automatically in future standups
- Allow corrections and updates to stored preferences

**Dependencies verified**:
- [x] #552 (State Management) - **CLOSED** ✅
- [x] #553 (Conversation Flow) - **CLOSED** ✅ (was open but complete, closed 2026-01-08)

### Part A.2: Work Characteristics Assessment

**Worktree Candidate?**

Worktrees ADD value when:
- [ ] Multiple agents will work in parallel - **Not applicable (single feature)**
- [ ] Task duration >30 minutes - **Yes**
- [ ] Multi-component work - **No (backend only)**
- [x] Exploratory/risky changes - **Maybe (new learning system)**

Worktrees ADD overhead when:
- [x] Single agent, sequential work - **Yes**
- [ ] Small fixes (<15 min) - **No**
- [ ] Tightly coupled files - **No**
- [ ] Time-critical - **No**

**Assessment**:
- [ ] **USE WORKTREE**
- [x] **SKIP WORKTREE** - Single agent, sequential phases, not time-critical

### Part B: PM Verification Required

**PM, please correct/confirm the above and provide**:

1. **What actually exists in the filesystem?**
   ```bash
   ls -la services/standup/
   ls -la services/domain/models.py
   find . -name "*preference*" -type f
   grep -n "class.*Preference" services/domain/models.py
   ```

2. **Recent work in this area?**
   - Last changes to standup: #553 (Conversation Flow) just closed
   - Known issues/quirks: `data/learning/` JSON exists but unclear if used
   - Previous attempts: None known

3. **Actual task needed?**
   - [ ] Create new feature from scratch
   - [x] Add to existing application (standup already exists)
   - [ ] Fix broken functionality
   - [ ] Refactor existing code

4. **Critical context I'm missing?**
   - DDD compliance requirements for new domain models
   - Integration points with existing standup flow

---

### Part B: PM Decisions (Received 2026-01-08)

**1. Preference storage approach**:
- ✅ **Option B selected** - Create new UserPreferences model with database persistence
- ⚠️ **DDD Compliance Required**: Must verify against `services/domain/models.py` patterns
- Pre-implementation task: Review existing domain models for pattern compliance

**2. Preference categories (initial set)**:
- Content filters ("focus on GitHub", "include/exclude X")
- Format preferences ("brief", "detailed")
- **Timing preferences** (PM added) - "morning standup at 9am", "daily", "weekly"
- **Notification preferences** (PM added) - "notify via Slack", "email summary"

**3. LLM involvement**:
- ✅ Start with **Option A** (rule-based pattern matching)
- Evolution trigger conditions:
  - Rule-based accuracy drops below 70%
  - Users express preferences in complex/nuanced ways
  - Preference conflicts require reasoning to resolve
- 📌 **GitHub Issue Created**: #558 - "LLM-based preference extraction" (post-#555)

### Part C: Proceed/Revise Decision

- [x] **PROCEED** - #553 complete (verified and closed), understanding confirmed
- [ ] **BLOCKED** - Dependencies incomplete
- [ ] **CLARIFY** - Need more context on preference storage approach

**Dependencies now satisfied. Ready to proceed pending PM verification of Part B.**

---

## Phase 0: Initial Bookending - GitHub Investigation

### Purpose
Verify dependencies, understand current state, prepare for implementation.

### Required Actions

1. **Verify #553 is complete**
   ```bash
   gh issue view 553 --json state -q '.state'
   # Must return "CLOSED"
   ```

2. **Investigate existing infrastructure**
   ```bash
   # Check User model for preference storage
   grep -n "class User" services/domain/models.py
   grep -n "preferences" services/domain/models.py

   # Check existing learning patterns
   cat data/learning/learned_patterns.json | head -50
   cat data/learning/pattern_feedback.json

   # Check StandupConversationContext for preference field
   grep -n "StandupConversationContext" services/domain/models.py
   ```

3. **Update GitHub Issue**
   ```bash
   gh issue comment 555 -b "## Phase 0: Investigation Started
   - [ ] #553 dependency verified
   - [ ] Preference storage approach confirmed
   - [ ] Existing infrastructure reviewed"
   ```

### STOP Conditions
- #553 not complete → STOP, wait for dependency
- User model doesn't support preference storage and migration required → Escalate
- Existing learning infrastructure incompatible → Escalate

---

## Phase 0.5: Frontend-Backend Contract Verification

**SKIP** - This issue is backend-only. No new UI or API endpoints that require frontend integration.

---

## Phase 1: Preference Schema & Extraction

**Deploy**: Lead Developer (Opus) - judgment needed for preference patterns

### Objective
Define preference schema and create extraction logic from conversation turns.

### Tasks

1. **Define preference schema** (DDD compliant - must follow `services/domain/models.py` patterns)
   ```python
   # services/standup/preference_models.py
   @dataclass
   class UserStandupPreference:
       user_id: str
       preference_type: str  # "content_filter", "format", "exclusion", "timing", "notification"
       key: str              # "focus", "exclude", "format", "schedule", "channel"
       value: Any            # "github", ["docs", "tests"], "brief", "9:00", "slack"
       confidence: float     # 0.0 - 1.0
       created_at: datetime
       updated_at: datetime
       source: str           # "explicit" or "inferred"
   ```

   **DDD Pre-check** (Phase 0 task):
   ```bash
   # Verify pattern compliance before implementation
   grep -A 20 "@dataclass" services/domain/models.py | head -40
   # Check for existing preference patterns
   grep -n "preference\|Preference" services/domain/models.py
   ```

2. **Create preference extraction logic**
   ```python
   # services/standup/preference_extractor.py
   class PreferenceExtractor:
       """Extract preferences from conversation turns."""

       def extract_from_turn(self, message: str) -> List[UserStandupPreference]:
           """
           Parse user message for preference expressions.

           Examples:
           - "focus on GitHub" → content_filter(focus=github)
           - "skip docs" → exclusion(exclude=docs)
           - "make it brief" → format(format=brief)
           """
   ```

3. **Handle preference types** (4 categories per PM decision)
   - **Content filters**: "focus on X", "prioritize X", "mainly X"
   - **Exclusions**: "skip X", "ignore X", "don't include X"
   - **Format**: "brief", "detailed", "bullet points"
   - **Timing**: "morning at 9am", "daily", "every Monday", "weekly"
   - **Notifications**: "notify via Slack", "email summary", "no notifications"
   - **Implicit**: User skips content repeatedly → inferred exclusion

### Deliverables
- `services/standup/preference_models.py` - Preference dataclasses
- `services/standup/preference_extractor.py` - Extraction logic
- Unit tests for each preference pattern

### Evidence Required
- Test output showing pattern matching works
- Examples of extracted preferences from sample messages

### Progressive Bookending
```bash
gh issue comment 555 -b "✓ Phase 1 complete: Preference schema and extraction
- Preference dataclass defined
- Extractor handles: focus, exclude, format patterns
- X unit tests passing
Next: Phase 2 (storage)"
```

---

## Phase 2: Preference Storage

**Deploy**: Lead Developer (Opus)

### Objective
Persist user preferences to database for cross-session retrieval.

### Tasks

1. **Add preference storage to User context**
   - Decide: New table or JSON column on existing user?
   - Implement repository pattern for preference CRUD
   - Handle versioning (track when preferences changed)

2. **Create preference service**
   ```python
   # services/standup/preference_service.py
   class UserPreferenceService:
       async def get_preferences(self, user_id: str) -> List[UserStandupPreference]
       async def save_preference(self, pref: UserStandupPreference) -> None
       async def update_preference(self, pref: UserStandupPreference) -> None
       async def get_preference_history(self, user_id: str) -> List[PreferenceChange]
   ```

3. **Handle preference conflicts**
   - New preference contradicts existing → update with higher confidence
   - Same preference repeated → boost confidence
   - Conflicting preferences same session → latest wins

### Deliverables
- Preference repository (database or JSON persistence)
- Preference service with CRUD operations
- Unit tests for storage and retrieval

### Evidence Required
- Test showing preference persists across "sessions"
- Test showing preference update works

### Progressive Bookending
```bash
gh issue comment 555 -b "✓ Phase 2 complete: Preference storage
- Preferences persist to [database/JSON]
- CRUD operations working
- Conflict resolution implemented
Next: Phase 3 (application)"
```

---

## Phase 3: Preference Application

**Deploy**: Lead Developer (Opus)

### Objective
Apply learned preferences automatically to standup generation.

### Tasks

1. **Integrate with standup generation**
   - Load user preferences at conversation start
   - Apply filters before content aggregation
   - Apply format preferences to output

2. **Show user what preferences are applied**
   ```
   Piper: "Good morning! Using your preferences:
   - Focus: GitHub activity
   - Exclude: Documentation updates
   Any changes for today?"
   ```

3. **Support one-time overrides**
   - "Just for today, include docs"
   - Override applied but not saved
   - Original preference preserved

### Deliverables
- Preference application in standup generation flow
- User notification of applied preferences
- Override mechanism for single session

### Evidence Required
- Test showing preferences affect standup output
- Test showing override doesn't change stored preference

### Progressive Bookending
```bash
gh issue comment 555 -b "✓ Phase 3 complete: Preference application
- Preferences applied to standup generation
- User sees applied preferences
- One-time overrides working
Next: Phase 4 (feedback loop)"
```

---

## Phase 4: Feedback Loop

**Deploy**: Lead Developer (Opus)

### Objective
Learn from user corrections to improve preferences over time.

### Tasks

1. **Detect corrections**
   - "Actually include docs today" → one-time override
   - "Always include docs from now on" → preference update
   - User manually adds excluded content → implicit correction

2. **Update preferences on explicit correction**
   - Parse correction intent (temporary vs permanent)
   - Update stored preference if permanent
   - Adjust confidence based on corrections

3. **Confidence scoring**
   - New preference: confidence 0.7
   - Confirmed by repetition: confidence increases
   - Corrected: confidence decreases
   - Low confidence preferences → prompt for confirmation

### Deliverables
- Correction detection logic
- Preference update on correction
- Confidence adjustment system

### Evidence Required
- Test showing correction updates preference
- Test showing temporary override preserves original

### Progressive Bookending
```bash
gh issue comment 555 -b "✓ Phase 4 complete: Feedback loop
- Corrections detected and parsed
- Permanent corrections update preferences
- Confidence scoring implemented
Next: Phase 5 (tests)"
```

---

## Phase 5: Tests

**Deploy**: Haiku Subagent

### Objective
Comprehensive test coverage for preference learning system.

### Tasks

1. **Unit tests for extraction**
   ```python
   def test_extract_focus_preference()
   def test_extract_exclusion_preference()
   def test_extract_format_preference()
   def test_implicit_preference_detection()
   ```

2. **Unit tests for storage**
   ```python
   def test_save_preference()
   def test_update_preference()
   def test_conflict_resolution()
   def test_preference_history()
   ```

3. **Unit tests for application**
   ```python
   def test_apply_content_filter()
   def test_apply_format_preference()
   def test_one_time_override()
   ```

4. **Integration tests**
   ```python
   def test_preference_persists_across_sessions()
   def test_preference_applies_to_standup_output()
   def test_correction_updates_stored_preference()
   ```

### Deliverables
- `tests/unit/services/standup/test_preference_extractor.py`
- `tests/unit/services/standup/test_preference_service.py`
- `tests/integration/test_preference_learning.py`
- All tests passing

### Evidence Required
- pytest output showing all tests pass
- Coverage report for preference modules

### Progressive Bookending
```bash
gh issue comment 555 -b "✓ Phase 5 complete: Tests created
- X unit tests for extraction
- X unit tests for storage/service
- X integration tests
- All passing (output attached)
Next: Phase Z (completion)"
```

---

## Phase Z: Final Bookending & Handoff

### Final Verification Checklist

- [ ] Preference extraction works for all defined patterns
- [ ] Preferences persist across sessions
- [ ] Preferences apply to standup generation
- [ ] Feedback loop updates preferences correctly
- [ ] All tests passing
- [ ] No regressions to existing standup functionality

### Documentation Updates
- [ ] Code documentation complete
- [ ] Session log finalized
- [ ] ADR if architectural decisions made

### Evidence Compilation
- [ ] All terminal outputs in session log
- [ ] Test output attached to issue
- [ ] Before/after preference behavior documented

### GitHub Final Update
```bash
gh issue comment 555 -b "## Issue #555 Complete - Ready for PM Review

### Evidence Summary
- [x] Preference extraction: X patterns supported
- [x] Preference storage: Persists to [database/JSON]
- [x] Preference application: Filters standup output
- [x] Feedback loop: Corrections update preferences
- [x] Tests: X tests passing (output attached)
- [x] No regressions confirmed

### Files Created/Modified
- services/standup/preference_models.py (new)
- services/standup/preference_extractor.py (new)
- services/standup/preference_service.py (new)
- tests/unit/services/standup/test_preference_*.py (new)

### Ready for PM Review"
```

---

## Verification Gates

- [ ] **Phase 0 Gate**: DDD pattern compliance verified (PM will validate)
- [ ] **Phase 1 Gate**: Unit tests for all 5 preference categories passing (PM will validate)
- [ ] **Phase 2 Gate**: Storage tests + cross-session persistence verified (PM will validate)
- [ ] **Phase 3 Gate**: Preferences affect standup output + user sees applied preferences (PM will validate)
- [ ] **Phase 4 Gate**: Correction tests passing + confidence scoring works (PM will validate)
- [ ] **Phase 5 Gate**: All tests passing with coverage report (PM will validate)
- [ ] **Phase Z Gate**: No regressions, documentation complete (PM will validate)

---

## Handoff Quality Checklist

Before accepting handoff from any agent/phase:
- [ ] All acceptance criteria checkboxes addressed
- [ ] Test output provided (not just "tests pass")
- [ ] Files modified list included
- [ ] User verification steps documented
- [ ] Blockers explicitly stated (if any)

---

## Multi-Agent Deployment Map

| Phase | Agent Type | Model | Rationale |
|-------|------------|-------|-----------|
| 0 | Lead Dev | Opus | Dependency verification, judgment |
| 1 | Lead Dev | Opus | Schema design, extraction patterns |
| 2 | Lead Dev | Opus | Storage architecture decisions |
| 3 | Lead Dev | Opus | Integration with standup flow |
| 4 | Lead Dev | Opus | Feedback loop complexity |
| 5 | Subagent | Haiku | Test creation is mechanical |
| Z | Lead Dev | Opus | Final verification and handoff |

**Note**: This is primarily Lead Dev work due to the judgment calls needed for preference patterns and integration decisions.

---

## STOP Conditions

Stop immediately and escalate if:
- [ ] #553 (Conversation Flow) not complete
- [ ] User model doesn't support preference storage (migration needed)
- [ ] Preference extraction accuracy <50%
- [ ] Integration breaks existing standup functionality
- [ ] Tests fail for any reason
- [ ] Performance degrades significantly

---

## Effort Estimate

**Overall Size**: Medium (2-3 days)

| Phase | Estimate | Cumulative |
|-------|----------|------------|
| Phase 0 | 30 min | 30 min |
| Phase 1 | 2-3 hours | 3-4 hours |
| Phase 2 | 2-3 hours | 5-7 hours |
| Phase 3 | 2-3 hours | 7-10 hours |
| Phase 4 | 2 hours | 9-12 hours |
| Phase 5 | 2 hours | 11-14 hours |
| Phase Z | 30 min | ~2 days |

---

## Dependencies

### Required (Must complete first)
- [x] #552 (State Management) - **CLOSED** ✅
- [x] #553 (Conversation Flow) - **CLOSED** ✅

### Enables
- #556 (Performance & Reliability) - can start after #555 complete

---

## Remember

- All dependencies satisfied (#552, #553 both closed)
- Evidence required for all claims
- No 80% completions
- PM closes issues after approval

---

*Gameplan created: 2026-01-08*
*Template version: 9.2*

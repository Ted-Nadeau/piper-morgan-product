# MUX-NAV-PALETTE - Command Palette & Discovery

**Priority**: P1
**Labels**: `MUX-IMPLEMENT`, `navigation`, `command-palette`, `consciousness`
**Milestone**: Sprint P1 (Navigation Paradigm)
**Epic**: #418 MUX-IMPLEMENT
**Related**: #419 (Home State), #420 (Nav Utility), #684 (Places), ADR-045, ADR-053

---

## Problem Statement

### Current State
No command palette exists. Users must:
- Click through navigation to access features
- Use mouse for all interactions
- Learn menu hierarchy to find capabilities
- No keyboard-first access pattern

Power users and mobile users have no efficient escape hatch.

### Impact
- **Blocks**: #420 (Nav Utility) needs palette trigger; keyboard-first users blocked
- **User Impact**: Power users frustrated by mouse-only access; mobile users limited
- **Technical Debt**: No standardized command invocation pattern

### Strategic Context
P1 establishes navigation paradigm. Command palette provides CLI-like efficiency while maintaining consciousness principles. Complements #419 (Home State) and #420 (Nav Utility) as third access pattern.

---

## Goal

**Primary Objective**: Create a command palette that provides keyboard-first, voice-capable access to Piper's capabilities while maintaining natural language and trust-gated visibility.

**Example User Experience**:
```
BEFORE:
- User wants to see urgent tasks
- Clicks nav → "My Work" → "Todos" → filters
- Multiple clicks, slow, mouse-dependent

AFTER (Stage 3 user):
- User presses Cmd/Ctrl+K
- Palette opens with recent commands and suggestions
- Types "urgent" or "what needs attention"
- Piper interprets and shows relevant view
- One keyboard shortcut, fast, natural language
```

**Not In Scope** (explicitly):
- ❌ Full NLU integration (basic matching for P1, NLU is future)
- ❌ Mobile gesture implementation (design only in P1)
- ❌ Voice input (future enhancement)
- ❌ Command history persistence (future enhancement)
- ❌ AI-powered suggestions (future enhancement)

---

## What Already Exists

### Infrastructure ✅
- Intent classification system (`services/intent_service/`)
- Slash command patterns in chat
- Keyboard event handling in templates
- Trust computation from #419
- HardnessLevel enum for visibility
- Pre-classifier for intent routing

### What's Missing ❌
- Command palette UI component
- Keyboard shortcut registration (Cmd/Ctrl+K)
- Command registry for palette
- Trust-gated command visibility
- Mobile design (wireframe level)
- Palette trigger in nav (#420)

---

## Requirements

### Phase 0: Investigation & Verification
**Objective**: Understand existing command patterns and design palette

**Tasks**:
- [ ] Audit existing slash commands in codebase
- [ ] Review intent classification for palette routing
- [ ] Survey command palette patterns (VS Code, Spotlight, Alfred)
- [ ] Design palette UI mockup (desktop)
- [ ] Design mobile access pattern (wireframe)

**Deliverables**:
- Existing command audit
- UI design mockup
- Mobile access wireframe

### Phase 1: Palette UI Component
**Objective**: Create basic command palette with keyboard activation

**Tasks**:
- [ ] Create palette component (`templates/components/command_palette.html`)
- [ ] Implement overlay UI with search input
- [ ] Add keyboard shortcut (Cmd/Ctrl+K)
- [ ] Add Escape to close
- [ ] Style for desktop viewport
- [ ] Write component tests

**Deliverables**:
- `templates/components/command_palette.html`
- CSS for palette styling
- JavaScript for keyboard handling
- Unit tests for palette behavior

### Phase 2: Command Registry
**Objective**: Register available commands for palette

**Tasks**:
- [ ] Create command registry structure
- [ ] Register navigation commands (Home, Standup, etc.)
- [ ] Register action commands (Create task, etc.)
- [ ] Register query commands (What's urgent, etc.)
- [ ] Register meta commands (Settings, Help, Logout)
- [ ] Write tests for registry

**Deliverables**:
- Command registry implementation
- Commands categorized (Navigation, Action, Query, Meta)
- Unit tests for registry

### Phase 3: Trust-Gated Visibility
**Objective**: Show commands based on trust stage

**Tasks**:
- [ ] Assign hardness level to each command
- [ ] Filter commands by trust stage
- [ ] Stage 1-2: Basic commands only
- [ ] Stage 3-4: Full command set
- [ ] Write visibility tests

**Deliverables**:
- Trust-gated command filtering
- Visibility matrix documented
- Unit tests for all stages

### Phase 4: Basic Search & Matching
**Objective**: Implement command search and invocation

**Tasks**:
- [ ] Implement fuzzy search for commands
- [ ] Show matching commands as user types
- [ ] Highlight matched characters
- [ ] Execute command on selection
- [ ] Route to appropriate handler
- [ ] Write search tests

**Deliverables**:
- Search implementation
- Command execution routing
- Unit tests for search

### Phase 5: Nav Integration
**Objective**: Add palette trigger to navigation

**Tasks**:
- [ ] Add search icon/trigger to nav (from #420)
- [ ] Show Cmd/Ctrl+K hint
- [ ] Ensure palette opens from nav trigger
- [ ] Write integration tests

**Deliverables**:
- Nav trigger added
- Keyboard hint visible
- Integration working

### Phase Z: Completion & Handoff
- [ ] All acceptance criteria met
- [ ] Evidence provided
- [ ] Mobile design documented (implementation deferred)
- [ ] Session log completed
- [ ] GitHub issue updated

---

## Acceptance Criteria

### Functionality
- [ ] Cmd/Ctrl+K opens command palette
- [ ] Escape closes palette
- [ ] Search filters available commands
- [ ] Commands execute correctly
- [ ] Trust-gated visibility working
- [ ] Nav trigger opens palette

### Testing
- [ ] Unit tests for palette component
- [ ] Unit tests for command registry
- [ ] Unit tests for trust-gated visibility
- [ ] Unit tests for search/matching
- [ ] Full unit test suite passes

### Quality
- [ ] No regressions introduced
- [ ] Keyboard navigation works (arrow keys, enter)
- [ ] Accessible (ARIA labels, screen reader)
- [ ] Responsive (works at various widths)

### Documentation
- [ ] Command registry documented
- [ ] Mobile design documented (for future)
- [ ] Usage pattern documented
- [ ] Session log complete

---

## Completion Matrix

| Component | Status | Evidence Link |
|-----------|--------|---------------|
| Phase 0: Investigation | ⏸️ | |
| Phase 1: Palette UI | ⏸️ | |
| Phase 2: Command Registry | ⏸️ | |
| Phase 3: Trust-Gated | ⏸️ | |
| Phase 4: Search/Matching | ⏸️ | |
| Phase 5: Nav Integration | ⏸️ | |
| Phase Z: Completion | ⏸️ | |
| All unit tests pass | ⏸️ | |
| No regressions | ⏸️ | |

---

## Testing Strategy

### Unit Tests
```
tests/unit/templates/test_command_palette.py:
- test_palette_renders
- test_keyboard_shortcut_opens
- test_escape_closes
- test_focus_on_open

tests/unit/services/test_command_registry.py:
- test_commands_registered
- test_command_categories
- test_command_execution

tests/unit/services/test_command_visibility.py:
- test_stage_1_sees_basic_commands
- test_stage_4_sees_all_commands
- test_hardness_filtering

tests/unit/services/test_command_search.py:
- test_fuzzy_search
- test_match_highlighting
- test_empty_query_shows_recent
```

### Integration Tests
Not required for P1 - unit tests sufficient.

### Manual Testing Checklist
**Scenario 1**: Keyboard-first command invocation
1. [ ] Press Cmd/Ctrl+K anywhere in app
2. [ ] Palette opens with focus in search
3. [ ] Type "tasks"
4. [ ] See matching commands
5. [ ] Press Enter to execute
6. [ ] Correct view opens

**Scenario 2**: Trust-gated visibility
1. [ ] Log in as Stage 1 user
2. [ ] Open palette
3. [ ] Verify only basic commands visible
4. [ ] Log in as Stage 4 user
5. [ ] Verify all commands visible

---

## Success Metrics

### Quantitative
- All 6 phases complete with tests
- 15+ new unit tests passing
- 0 regressions in existing tests
- Palette opens in <100ms

### Qualitative
- Commands feel natural (not robotic)
- Search results helpful
- Keyboard experience smooth
- Clear relationship with nav

---

## STOP Conditions

**STOP immediately and escalate if**:
- Intent service integration fails
- Trust context unavailable
- Keyboard shortcut conflicts discovered
- Accessibility requirements unmet
- Performance >200ms response time
- Tests fail for any reason

**When stopped**: Document the issue, provide options, wait for PM decision.

---

## Effort Estimate

**Overall Size**: Large (new component)

**Breakdown by Phase**:
- Phase 0: Small (design and audit)
- Phase 1: Medium (new UI component)
- Phase 2: Medium (registry implementation)
- Phase 3: Small (visibility filtering)
- Phase 4: Medium (search implementation)
- Phase 5: Small (nav integration)
- Phase Z: Small (documentation)

**Complexity Notes**:
- New component but follows established patterns
- Trust-gating uses existing #419 infrastructure
- Search is basic fuzzy match (not full NLU)
- Mobile implementation explicitly deferred

---

## Dependencies

### Required (Must be complete first)
- [x] #419 MUX-NAV-HOME (provides trust_stage context)
- [ ] #420 MUX-NAV-UTILITY (nav trigger location - can parallel)

### Optional (Nice to have)
- [ ] Intent service enhancements (for future NLU)

---

## Related Documentation

- **Architecture**: ADR-045 (Object Model), ADR-053 (Trust Computation)
- **Intent Service**: `services/intent_service/`
- **Philosophy**: `docs/internal/architecture/current/consciousness-philosophy.md`
- **Mobile**: `dev/active/mobile-skunkworks-briefing.md`

---

## Evidence Section

[To be filled during implementation]

### Implementation Evidence
```bash
# Phase 0 evidence (design artifacts)
# Phase 1 evidence (palette component)
# Phase 2 evidence (command registry)
# Phase 3 evidence (trust-gated visibility)
# Phase 4 evidence (search/matching)
# Phase 5 evidence (nav integration)
# Full test suite
```

---

## Completion Checklist

Before requesting PM review:
- [ ] All acceptance criteria met ✅
- [ ] Completion matrix 100% ✅
- [ ] Evidence provided for each criterion ✅
- [ ] Tests passing with output ✅
- [ ] Mobile design documented (implementation deferred) ✅
- [ ] No regressions confirmed ✅
- [ ] STOP conditions all clear ✅
- [ ] Session log complete ✅

**Status**: Not Started

---

## Design Principles (Preserved from Original)

### CLI-Like Efficiency with Natural Language
- Support both slash commands (`/tasks`) AND natural queries ("show my tasks")
- Piper interprets, doesn't just match keywords
- Progressive enhancement: basic matching → full NLU (future)

### Discovery Through Use
- Palette teaches available capabilities
- Suggestions improve with trust level
- "Did you know?" moments when relevant (future)

### Mobile-First Considerations
From mobile skunkworks briefing:
- Gesture to summon (future implementation)
- Voice input option (future)
- Recent/frequent commands prominent
- Entity-type shortcuts

### Anti-Patterns to Avoid
- Exact-match-only commands (must handle natural variation)
- Exposing every possible command at Stage 1
- Desktop-only design (mobile is equal citizen)
- Purely functional (should have Piper's voice)

---

## Command Categories (Reference)

1. **Navigation**: Go to places ("show calendar", "open github issues")
2. **Action**: Do things ("create task", "schedule meeting")
3. **Query**: Ask questions ("what's due today?", "who owns X?")
4. **Meta**: System commands ("settings", "help", "logout")

---

_Issue created: 2026-01-25_
_Last updated: 2026-01-25_

# Gameplan: #421 MUX-NAV-PALETTE - Command Palette & Discovery

**Issue**: #421
**Priority**: P1
**Sprint**: P1 (Navigation Paradigm)
**Epic**: #418 MUX-IMPLEMENT
**Created**: 2026-01-25

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Lead Developer's Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI (confirmed)
- [x] Template engine: Jinja2 (confirmed)
- [x] Intent service: `services/intent_service/` exists
- [x] Trust context: Available from #419
- [x] Keyboard handling: JavaScript in templates
- [x] Pre-classifier: Exists for intent routing

**My understanding of the task**:
- I believe we need to: Create new command palette UI component with keyboard activation
- I think this involves: UI component, command registry, trust-gated visibility, basic search
- I assume the current state is: No palette exists, need to build from scratch

### Part A.2: Work Characteristics Assessment

**Assessment:**
- [x] **SKIP WORKTREE** - Single Lead Dev, new component but sequential work
- Document rationale: New component but builds on existing patterns, sequential phases

### Part B: PM Verification

**What actually exists**:
```bash
# Intent service
ls -la services/intent_service/

# Slash commands in chat
grep -rn "slash\|command" templates/*.html | head -10

# Keyboard shortcut patterns
grep -rn "keydown\|keyup\|KeyboardEvent" templates/*.html | head -10
```

### Part C: Proceed/Revise Decision

- [x] **PROCEED** - Understanding correct

---

## Phase 0: Initial Bookending

### Required Actions

1. **GitHub Issue Verification**
   ```bash
   gh issue view 421
   ```

2. **Codebase Investigation**
   ```bash
   # Check for existing command patterns
   grep -rn "slash\|command" services/ --include="*.py" | head -20

   # Check intent service structure
   ls -la services/intent_service/

   # Check keyboard handling in templates
   grep -rn "addEventListener\|keydown" web/static/js/ | head -10
   ```

3. **Survey Command Palette Patterns**
   - VS Code: Ctrl+Shift+P
   - Spotlight/Alfred: Simple overlay, fuzzy search
   - Slack: Command palette style

### STOP Conditions Check
- [x] Issue exists: #421 confirmed
- [x] Intent service exists: Yes
- [x] #419 provides trust context: Yes

---

## Phase 0.5: Frontend-Backend Contract (Minimal)

### When to Apply
- [x] New UI component - YES (palette)

### Required Actions
- Palette is primarily client-side (JavaScript)
- May call intent service API for command execution
- Trust context from template (no new API needed)

---

## Phases 1-5: Development Work

### Phase 1: Palette UI Component

**Objective**: Create basic command palette with keyboard activation

**Tasks**:
- [ ] Create `templates/components/command_palette.html`
- [ ] Create `web/static/js/command-palette.js`
- [ ] Implement overlay UI with search input
- [ ] Add Cmd/Ctrl+K keyboard shortcut
- [ ] Add Escape to close
- [ ] Include in base template

**Verification**:
```bash
ls -la templates/components/command_palette.html
ls -la web/static/js/command-palette.js
```

### Phase 2: Command Registry

**Objective**: Register available commands

**Tasks**:
- [ ] Create command registry in JavaScript
- [ ] Register navigation commands
- [ ] Register action commands
- [ ] Register query commands
- [ ] Register meta commands

**Command Categories**:
| Category | Examples |
|----------|----------|
| Navigation | Home, Standup, Settings |
| Action | Create task, New project |
| Query | What's urgent, Show calendar |
| Meta | Help, Logout |

### Phase 3: Trust-Gated Visibility

**Objective**: Filter commands by trust stage

**Tasks**:
- [ ] Read trust_stage from window.trustStage (#419)
- [ ] Assign hardness to commands
- [ ] Filter based on trust stage
- [ ] Stage 1-2: Basic commands
- [ ] Stage 3-4: Full command set

**Visibility Matrix**:
| Command | Hardness | Stage 1 | Stage 2 | Stage 3 | Stage 4 |
|---------|----------|---------|---------|---------|---------|
| Home | HARDEST | ✅ | ✅ | ✅ | ✅ |
| Help | HARDEST | ✅ | ✅ | ✅ | ✅ |
| Standup | HARD | ❌ | ❌ | ✅ | ✅ |
| Create task | MEDIUM | ❌ | ❌ | ✅ | ✅ |
| What's urgent | SOFT | ❌ | ❌ | ❌ | ✅ |

### Phase 4: Search & Matching

**Objective**: Implement command search

**Tasks**:
- [ ] Implement fuzzy search
- [ ] Show matching commands
- [ ] Highlight matched characters
- [ ] Execute on Enter/click
- [ ] Handle empty state (show recent/suggested)

### Phase 5: Nav Integration

**Objective**: Add palette trigger to nav (#420)

**Tasks**:
- [ ] Add search icon to nav
- [ ] Show Cmd/Ctrl+K hint
- [ ] Wire click to open palette

---

## Phase Z: Final Bookending

### Required Actions

1. **Test Suite**
   ```bash
   python -m pytest tests/unit/ -v --tb=line | tail -20
   ```

2. **Acceptance Criteria Check**
   - [ ] Cmd/Ctrl+K opens palette
   - [ ] Escape closes
   - [ ] Search works
   - [ ] Trust-gating works
   - [ ] Nav trigger works

3. **GitHub Update**
   ```bash
   gh issue edit 421 --body "Status: Complete - Awaiting PM Approval"
   ```

---

## STOP Conditions

- Trust context unavailable
- Keyboard shortcut conflicts
- Accessibility requirements unmet
- Performance >200ms
- Tests fail

---

## Success Criteria

- [ ] All acceptance criteria met
- [ ] 15+ new tests
- [ ] No regressions
- [ ] PM approval

---

*Gameplan created: 2026-01-25*
*Template version: v9.3 (abbreviated for efficiency)*

# Lead Developer Prompt: #421 MUX-NAV-PALETTE Implementation

## Your Identity
You are the Lead Developer implementing #421 MUX-NAV-PALETTE - Command Palette & Discovery.

## Essential Context
- **GitHub Issue**: #421
- **Current State**: No command palette exists
- **Target State**: Keyboard-activated palette with search and trust-gating
- **Dependencies**: #419 (COMPLETE), #420 (parallel)

---

## Acceptance Criteria

### Functionality
- [ ] Cmd/Ctrl+K opens palette
- [ ] Escape closes
- [ ] Search filters commands
- [ ] Trust-gated visibility
- [ ] Nav trigger works

### Testing
- [ ] Unit tests for palette
- [ ] Tests for trust-gating
- [ ] Full suite passes

---

## Implementation Steps

1. **Create palette component** (`templates/components/command_palette.html`)
2. **Create JavaScript** (`web/static/js/command-palette.js`)
3. **Create command registry** (with categories)
4. **Implement trust-gating** (use window.trustStage from #419)
5. **Implement search** (fuzzy matching)
6. **Add nav trigger** (search icon + shortcut hint)

---

## STOP Conditions
- Trust context unavailable
- Keyboard conflicts
- Accessibility issues
- Tests fail

---

*Template Version: 10.2 (abbreviated)*
*Issue: #421*

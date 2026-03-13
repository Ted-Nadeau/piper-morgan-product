# Gameplan: #551 ARCH-COMMANDS - Command Parity Across Interfaces

**Issue**: #551
**Sprint**: I1
**Created**: 2026-01-22
**Template Version**: v9.3

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Lead Developer's Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI (confirmed)
- [x] CLI structure: main.py argparse + cli/commands/ Click (confirmed)
- [x] Database: PostgreSQL on 5433 (confirmed)
- [x] Testing framework: pytest (confirmed)
- [x] Existing command sources:
  - `main.py` - argparse commands
  - `cli/commands/` - Click modules
  - `services/intent_service/pre_classifier.py` - pattern lists
  - `services/intent_service/canonical_handlers.py` - `_get_slash_commands()`
  - `services/integrations/slack/webhook_router.py` - Slack commands
  - `web/api/routes/` - REST endpoints

**My understanding of the task**:
- Phase 1: Deep inventory of all commands across all interfaces
- Phase 2: Design CommandRegistry architecture (ADR)
- Phase 3: Implement registry and migrate commands

### Part A.2: Work Characteristics Assessment

Worktrees ADD value when:
- [ ] Multiple agents will work in parallel on different files/features
- [x] Task duration >30 minutes (main branch may advance)
- [ ] Multi-component work (frontend + backend by different agents)
- [ ] Exploratory/risky changes where easy rollback is valuable

Worktrees ADD overhead when:
- [x] Single agent, sequential work (Phase 1 is research)
- [ ] Small fixes (<15 min)
- [ ] Tightly coupled files requiring atomic commits
- [ ] Time-critical work where setup overhead matters

**Assessment**:
- [x] **SKIP WORKTREE** - Phase 1 is research (no code changes), Phase 2 is design (ADR), Phase 3 can reassess

### Part B: PM Verification Required

**What actually exists in the filesystem?**
```
✅ main.py - Entry point with argparse
✅ cli/commands/ - Click command modules (8 files)
✅ services/intent_service/pre_classifier.py - 13+ pattern groups
✅ services/intent_service/canonical_handlers.py - _get_slash_commands()
✅ services/integrations/slack/webhook_router.py - Slack processing
✅ web/api/routes/ - REST endpoints
```

**Actual task needed?**
- [x] Create new feature from scratch (CommandRegistry)
- [x] Document existing functionality (inventory)
- [ ] Fix broken functionality
- [ ] Refactor existing code

### Part C: Proceed/Revise Decision

- [x] **PROCEED** - Understanding is correct

---

## Phase 0: Initial Bookending - GitHub Investigation

### Required Actions

1. **GitHub Issue Verification**
   ```bash
   gh issue view 551
   ```
   ✅ Issue exists with complete body

2. **Codebase Investigation**
   - main.py argparse: setup, status, preferences, keys, rotate-key
   - cli/commands/: cal, documents, issues, keys, notion, personality, publish, standup
   - pre_classifier.py: 13+ pattern groups
   - canonical_handlers.py: _get_slash_commands() returns hardcoded list
   - webhook_router.py: _process_slash_command() handles Slack

3. **Update GitHub Issue**
   ```bash
   gh issue edit 551 --body "[Updated with Phase 1 in progress]"
   ```

---

## Phase 0.5: Frontend-Backend Contract Verification

**N/A** - Phase 1 is research only. Phase 3 will need this when implementing registry endpoints.

---

## Phase 0.6: Data Flow & Integration Verification

**N/A** - No data flow changes in Phase 1-2. Phase 3 will need this for registry integration.

---

## Phase 0.7: Conversation Design

**N/A** - Not a conversational feature.

---

## Phase 0.8: Post-Completion Integration

**N/A for Phase 1-2**. Phase 3 completion criteria:
- `_get_slash_commands()` queries registry dynamically
- All interfaces use registry for command discovery
- No hardcoded command lists remain

---

## Phase 1: Deep Inventory (Research)

### Objective
Create comprehensive command matrix documenting all commands across all interfaces.

### Deliverable Format
Structured markdown with YAML frontmatter per command:
```markdown
---
command: standup
canonical_name: standup
category: productivity
description: Generate daily standup summary
---

| Interface | Status | Handler | Syntax | Notes |
|-----------|--------|---------|--------|-------|
| Web Chat | ✅ | pre_classifier.py | "standup", "daily standup" | STANDUP_PATTERNS |
| Slack | ✅ | webhook_router.py | /standup | Direct command |
| CLI | ✅ | cli/commands/standup.py | piper standup | Click command |
| URL | ✅ | /api/standup/generate | POST | REST endpoint |
```

### Phase 1 Tasks

#### 1.1 Inventory CLI Commands (main.py)
- [ ] List all argparse commands in main.py
- [ ] Document each command's purpose and arguments
- [ ] Note which have web/Slack equivalents

#### 1.2 Inventory CLI Commands (cli/commands/)
- [ ] List all Click command modules
- [ ] Document each command's purpose and subcommands
- [ ] Note which have web/Slack equivalents

#### 1.3 Inventory Web Chat Patterns
- [ ] Extract all pattern groups from pre_classifier.py
- [ ] Document pattern → intent mapping
- [ ] Note which are canonical vs workflow

#### 1.4 Inventory Canonical Handlers
- [ ] Document _get_slash_commands() current output
- [ ] List all canonical query handlers
- [ ] Note implementation locations

#### 1.5 Inventory Slack Commands
- [ ] Document all /piper subcommands
- [ ] Document direct slash commands (/standup, etc.)
- [ ] Note DM vs channel behavior differences

#### 1.6 Inventory URL Routes
- [ ] List all user-facing API endpoints
- [ ] Categorize by: setup, features, utilities
- [ ] Note which map to commands

#### 1.7 Create Parity Matrix
- [ ] Build comprehensive command × interface matrix
- [ ] Mark each cell: ✅ exists, ❌ gap, ⚠️ inconsistent, 🔄 intentional difference
- [ ] Classify each gap/inconsistency

#### 1.8 Produce Inventory Document
- [ ] Create `docs/internal/architecture/current/command-inventory.md`
- [ ] Include all commands in structured format
- [ ] Include parity matrix summary
- [ ] Include gap classification

### Phase 1 Acceptance Criteria

- [ ] All CLI commands documented (main.py + cli/commands/)
- [ ] All web chat patterns documented
- [ ] All Slack commands documented
- [ ] All relevant URL routes documented
- [ ] Parity matrix complete (no ❓ remaining)
- [ ] Each gap classified as: (a) gap, (b) inconsistency, (c) intentional
- [ ] PM has reviewed inventory

### Phase 1 STOP Conditions

- Inventory reveals >100 unique commands → Discuss scope with PM
- Major interface discovered not in original list → Update approach
- Pattern structure differs significantly from assumptions → Revise
- Phase 1 taking >3 sessions without clear progress → Escalate

### Phase 1 Effort Estimate
**Medium** - Research across 6 sources, documentation synthesis

---

## PM Review Gate (After Phase 1)

Before proceeding to Phase 2:
- [ ] PM has reviewed command inventory
- [ ] Gap classifications approved
- [ ] Phase 2 scope confirmed
- [ ] Any scope adjustments documented

---

## Phase 2: Architecture Design (ADR)

### Objective
Design CommandRegistry pattern and write ADR for approval.

### Phase 2 Tasks

#### 2.1 Design CommandRegistry Schema
- [ ] Define `CommandDefinition` dataclass
- [ ] Define `InterfaceConfig` dataclass
- [ ] Define registry storage approach (in-memory vs persisted)
- [ ] Define discovery API

#### 2.2 Design Interface Adapters
- [ ] Web chat adapter (pre_classifier integration)
- [ ] Slack adapter (webhook_router integration)
- [ ] CLI adapter (argparse/Click integration)
- [ ] URL adapter (route registration)

#### 2.3 Design Migration Strategy
- [ ] Identify migration order (safest first)
- [ ] Define backwards compatibility approach
- [ ] Plan rollback strategy

#### 2.4 Address Open Questions
- [ ] In-memory vs persisted registry
- [ ] Auth handling per interface
- [ ] Alias matching (fuzzy vs exact)
- [ ] Command versioning

#### 2.5 Write ADR
- [ ] Create `docs/internal/architecture/current/adrs/adr-0XX-command-registry.md`
- [ ] Follow ADR template
- [ ] Include decision rationale
- [ ] Include implementation guidance

#### 2.6 Effort Estimation
- [ ] Estimate Phase 3 implementation effort
- [ ] Break down by component
- [ ] Identify risks and dependencies

### Phase 2 Acceptance Criteria

- [ ] CommandRegistry schema defined
- [ ] Interface adapter patterns defined
- [ ] ADR written and complete
- [ ] Implementation effort estimated (±20% accuracy)
- [ ] PM/Architect approval on ADR

### Phase 2 STOP Conditions

- Design reveals fundamental incompatibility → Escalate
- Effort estimate exceeds sprint capacity → Discuss phasing with PM
- Existing patterns conflict with design → Resolve before proceeding

### Phase 2 Effort Estimate
**Medium** - Schema design, ADR writing, effort estimation

---

## PM Review Gate (After Phase 2)

Before proceeding to Phase 3:
- [ ] ADR approved
- [ ] Implementation approach confirmed
- [ ] Phase 3 scope and timeline agreed
- [ ] Any architectural concerns resolved

---

## Phase 3: Implementation

### Objective
Implement CommandRegistry and migrate existing commands.

### Phase 3 Tasks

#### 3.1 Implement Core Registry
- [ ] Create `services/commands/registry.py`
- [ ] Implement `CommandRegistry` class
- [ ] Implement `CommandDefinition` and `InterfaceConfig`
- [ ] Add registry initialization to startup

#### 3.2 Register Existing Commands
- [ ] Register CLI commands (main.py)
- [ ] Register CLI commands (cli/commands/)
- [ ] Register canonical handlers
- [ ] Register Slack commands

#### 3.3 Implement Interface Adapters
- [ ] Update `_get_slash_commands()` to query registry
- [ ] Create Slack adapter for dynamic commands
- [ ] Create CLI adapter (if needed)
- [ ] Create URL discovery endpoint (if needed)

#### 3.4 Migration and Testing
- [ ] Migrate commands incrementally (safest first)
- [ ] Verify no commands break during migration
- [ ] Add parity verification tests
- [ ] Document any intentional exceptions

#### 3.5 Update Documentation
- [ ] Update NAVIGATION.md
- [ ] Update architecture.md
- [ ] Add developer guide for registering new commands

### Phase 3 Acceptance Criteria

- [ ] CommandRegistry implemented and tested
- [ ] All commands migrated to registry
- [ ] `_get_slash_commands()` queries registry dynamically
- [ ] Interface parity verified (or exceptions documented)
- [ ] No regressions in existing command behavior
- [ ] Tests pass for all migrated commands
- [ ] Documentation updated

### Phase 3 STOP Conditions

- Any command breaks during migration → Rollback and investigate
- Performance regression detected → Profile and optimize
- Integration failures → Debug before continuing

### Phase 3 Effort Estimate
**Large** - Implementation + migration + testing across multiple interfaces

---

## Phase Z: Final Bookending & Handoff

### GitHub Final Update
```bash
gh issue edit 551 --body "
## Status: Complete - Awaiting PM Approval

### Evidence Summary
- [x] Command inventory complete: [link to doc]
- [x] ADR approved: [link to ADR]
- [x] CommandRegistry implemented: [link to code]
- [x] All commands migrated: [test output]
- [x] Interface parity verified: [evidence]
- [x] No regressions: [test output]

### Ready for PM Review
"
```

### Documentation Updates
- [ ] command-inventory.md created
- [ ] ADR-0XX-command-registry.md created
- [ ] NAVIGATION.md updated
- [ ] architecture.md updated (if needed)

### Evidence Compilation
- [ ] Phase 1: Inventory document
- [ ] Phase 2: ADR document
- [ ] Phase 3: Test output, migration log

---

## Completion Matrix

| Phase | Deliverable | Evidence | Status |
|-------|-------------|----------|--------|
| 1.1 | CLI (main.py) inventory | Document section | ⬜ |
| 1.2 | CLI (commands/) inventory | Document section | ⬜ |
| 1.3 | Web chat patterns inventory | Document section | ⬜ |
| 1.4 | Canonical handlers inventory | Document section | ⬜ |
| 1.5 | Slack commands inventory | Document section | ⬜ |
| 1.6 | URL routes inventory | Document section | ⬜ |
| 1.7 | Parity matrix | Document section | ⬜ |
| 1.8 | Complete inventory document | Link | ⬜ |
| Gate | PM review of Phase 1 | Approval | ⬜ |
| 2.1 | Registry schema | ADR section | ⬜ |
| 2.2 | Adapter patterns | ADR section | ⬜ |
| 2.3 | Migration strategy | ADR section | ⬜ |
| 2.4 | Open questions resolved | ADR section | ⬜ |
| 2.5 | ADR complete | Link | ⬜ |
| 2.6 | Effort estimate | Document | ⬜ |
| Gate | PM/Arch approval of ADR | Approval | ⬜ |
| 3.1 | Core registry | Code + tests | ⬜ |
| 3.2 | Commands registered | Test output | ⬜ |
| 3.3 | Adapters implemented | Test output | ⬜ |
| 3.4 | Migration complete | Test output | ⬜ |
| 3.5 | Docs updated | Links | ⬜ |
| Z | PM approval | Issue closed | ⬜ |

---

## Success Metrics

### Phase 1 Success
- 100% of commands in each interface cataloged
- Each command classified (gap/inconsistency/intentional)
- Parity matrix complete with no ❓ remaining
- Total command count documented

### Phase 2 Success
- ADR approved by PM/architecture review
- Schema supports all discovered commands
- Implementation effort estimated to ±20% accuracy
- All open questions resolved

### Phase 3 Success
- 0 commands break during migration
- All parity gaps either closed or documented as intentional
- `_get_slash_commands()` returns dynamic list from registry
- Performance: registry lookup <10ms

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Inventory reveals 100+ commands | Medium | Medium | Discuss prioritization with PM |
| Design incompatibility discovered | Low | High | Phase 2 STOP condition |
| Migration breaks existing commands | Medium | High | Incremental migration, rollback plan |
| Performance regression | Low | Medium | Profile and cache if needed |

---

## Agent Deployment Map

| Phase | Agent Type | Approach | Evidence Required |
|-------|------------|----------|-------------------|
| 1 | Lead Dev + Explore subagents | Parallel investigation of 6 sources | Inventory document |
| 2 | Lead Dev | Sequential design work | ADR document |
| 3 | Lead Dev + Code subagents | Implementation + testing | Code + test output |

---

## Notes

- Phase 1 output directly informs #413 TRUST-LEVELS scope (per PM guidance)
- Registry design may inform other MUX-INTERACT issues
- Consider: Plugin commands should self-register (future enhancement)

# Subagent Prompts: #551 ARCH-COMMANDS

**Gameplan**: `dev/2026/01/22/551-gameplan.md`
**Template Version**: Agent Prompt Template v10.2
**Created**: 2026-01-22

---

## Prompt Index

| # | Phase | Agent Type | Task | Status |
|---|-------|------------|------|--------|
| 1 | 1.1-1.2 | Explore | CLI Commands Inventory | Ready |
| 2 | 1.3-1.4 | Explore | Web Chat Patterns Inventory | Ready |
| 3 | 1.5 | Explore | Slack Commands Inventory | Ready |
| 4 | 1.6 | Explore | URL Routes Inventory | Ready |
| 5 | 3.1 | Code | CommandRegistry Core Implementation | Blocked by Phase 2 |
| 6 | 3.2-3.3 | Code | Command Migration | Blocked by Phase 3.1 |

---

## Prompt 1: CLI Commands Inventory (Phase 1.1-1.2)

### Mission
Create comprehensive inventory of all CLI commands in main.py (argparse) and cli/commands/ (Click modules).

### Context
- **GitHub Issue**: #551 ARCH-COMMANDS - Command Parity Across Interfaces
- **Parent Gameplan**: `dev/2026/01/22/551-gameplan.md`
- **Current State**: CLI commands exist in two locations with different frameworks
- **Target State**: Complete inventory document with command metadata
- **Scope**: CLI ONLY - do not inventory web, Slack, or URL commands

### Infrastructure Verification (MANDATORY FIRST)

```bash
# Verify these files exist as expected:
ls -la main.py
ls -la cli/commands/
find cli/commands/ -name "*.py" -type f

# Expected: main.py exists, cli/commands/ directory with multiple .py files
# STOP if: main.py missing, cli/commands/ doesn't exist
```

### Implementation Approach

#### Step 1: Inventory main.py argparse commands
- Read main.py completely
- Document each argparse subparser/command:
  - Command name
  - Arguments/options
  - Help text
  - Handler function location
- Expected output: List of 5-10 argparse commands

#### Step 2: Inventory cli/commands/ Click modules
- List all .py files in cli/commands/
- For each file:
  - Identify @click.command() and @click.group() decorators
  - Document command names, subcommands, options
  - Note any aliases
- Expected output: List of 8-12 Click command modules

#### Step 3: Create inventory section
Output in this format:

```markdown
## CLI Commands Inventory

### main.py (argparse)

| Command | Arguments | Handler | Description |
|---------|-----------|---------|-------------|
| setup | --verbose | main:do_setup | Interactive setup wizard |
| status | | main:show_status | Check system health |
| ... | | | |

### cli/commands/ (Click)

| Module | Command | Subcommands | Description |
|--------|---------|-------------|-------------|
| standup.py | standup | generate, list | Daily standup operations |
| cal.py | cal | today, week, add | Calendar operations |
| ... | | | |
```

### Success Criteria
- [ ] All main.py argparse commands documented (expected: 5-10)
- [ ] All cli/commands/*.py modules documented (expected: 8-12)
- [ ] Each command has: name, arguments, handler location, description
- [ ] Noted any inconsistencies between argparse and Click patterns
- [ ] Output follows structured format above

### Deliverables
Return inventory sections ready to insert into `docs/internal/architecture/current/command-inventory.md`

### STOP Conditions
- main.py doesn't use argparse → Report alternative pattern
- cli/commands/ uses different framework than Click → Report finding
- More than 50 unique CLI commands → Report count, request guidance

---

## Prompt 2: Web Chat Patterns Inventory (Phase 1.3-1.4)

### Mission
Create comprehensive inventory of all web chat patterns in pre_classifier.py and canonical handlers in canonical_handlers.py.

### Context
- **GitHub Issue**: #551 ARCH-COMMANDS - Command Parity Across Interfaces
- **Parent Gameplan**: `dev/2026/01/22/551-gameplan.md`
- **Current State**: Intent patterns defined in pre_classifier.py, handlers in canonical_handlers.py
- **Target State**: Complete inventory of chat-based commands with pattern mappings
- **Scope**: Web chat patterns ONLY - do not inventory CLI, Slack, or URL commands

### Infrastructure Verification (MANDATORY FIRST)

```bash
# Verify these files exist:
ls -la services/intent_service/pre_classifier.py
ls -la services/intent_service/canonical_handlers.py

# Check for pattern definitions:
grep -n "PATTERNS\|_patterns\|patterns =" services/intent_service/pre_classifier.py | head -20

# Expected: Both files exist, multiple pattern group definitions found
# STOP if: Files missing or pattern structure unexpected
```

### Implementation Approach

#### Step 1: Extract pattern groups from pre_classifier.py
- Find all *_PATTERNS or similar pattern list definitions
- Document each pattern group:
  - Group name (e.g., STANDUP_PATTERNS, CALENDAR_PATTERNS)
  - Pattern strings/regexes
  - Mapped intent category
- Expected: 13+ pattern groups

#### Step 2: Document _get_slash_commands() in canonical_handlers.py
- Find the _get_slash_commands() function
- List all commands it returns
- Note any commands that don't have corresponding patterns

#### Step 3: Map patterns to handlers
- For each pattern group, identify the canonical handler
- Document which patterns route to which handlers

#### Step 4: Create inventory section
Output in this format:

```markdown
## Web Chat Patterns Inventory

### Pattern Groups (pre_classifier.py)

| Pattern Group | Intent Category | Example Patterns | Handler |
|---------------|-----------------|------------------|---------|
| STANDUP_PATTERNS | EXECUTION | "standup", "daily standup" | handle_standup |
| CALENDAR_PATTERNS | QUERY | "calendar", "my calendar" | handle_calendar |
| ... | | | |

### Slash Commands (_get_slash_commands)

| Command | Description | Pattern Group | Status |
|---------|-------------|---------------|--------|
| /standup | Generate standup | STANDUP_PATTERNS | Active |
| /calendar | View calendar | CALENDAR_PATTERNS | Active |
| ... | | | |

### Canonical Handlers

| Handler | Intent Categories | Capabilities |
|---------|-------------------|--------------|
| handle_standup | EXECUTION | generate, list |
| ... | | |
```

### Success Criteria
- [ ] All pattern groups documented (expected: 13+)
- [ ] _get_slash_commands() output documented
- [ ] Pattern → intent → handler mapping complete
- [ ] Noted any orphaned patterns (no handler)
- [ ] Noted any orphaned handlers (no pattern)
- [ ] Output follows structured format above

### Deliverables
Return inventory sections ready to insert into `docs/internal/architecture/current/command-inventory.md`

### STOP Conditions
- pre_classifier.py structure differs significantly from expectations → Report pattern
- More than 50 unique pattern groups → Report count, request guidance
- Circular or complex routing discovered → Document and escalate

---

## Prompt 3: Slack Commands Inventory (Phase 1.5)

### Mission
Create comprehensive inventory of all Slack commands handled by webhook_router.py.

### Context
- **GitHub Issue**: #551 ARCH-COMMANDS - Command Parity Across Interfaces
- **Parent Gameplan**: `dev/2026/01/22/551-gameplan.md`
- **Current State**: Slack commands processed via webhook_router.py
- **Target State**: Complete inventory of Slack slash commands and interactions
- **Scope**: Slack commands ONLY - do not inventory CLI, web, or URL commands

### Infrastructure Verification (MANDATORY FIRST)

```bash
# Verify file exists:
ls -la services/integrations/slack/webhook_router.py

# Check for command handling:
grep -n "slash_command\|_process_\|handle_" services/integrations/slack/webhook_router.py | head -20

# Expected: File exists, command handling functions found
# STOP if: File missing or no command handling found
```

### Implementation Approach

#### Step 1: Identify slash command entry point
- Find how /piper and direct slash commands are received
- Document the routing logic

#### Step 2: Inventory all handled commands
- Find _process_slash_command() or equivalent
- Document each command:
  - Slash command syntax (/piper standup, /standup, etc.)
  - Handler function
  - Arguments accepted
  - DM vs channel behavior differences

#### Step 3: Check for command registration
- Is there a command list/registry?
- Are commands hardcoded or dynamic?

#### Step 4: Create inventory section
Output in this format:

```markdown
## Slack Commands Inventory

### Direct Slash Commands

| Command | Handler | Arguments | DM Behavior | Channel Behavior |
|---------|---------|-----------|-------------|------------------|
| /standup | process_standup | --date, --team | Full output | Summary only |
| ... | | | | |

### /piper Subcommands

| Subcommand | Handler | Arguments | Description |
|------------|---------|-----------|-------------|
| standup | process_standup | date, team | Generate standup |
| calendar | process_calendar | date | View calendar |
| help | show_help | | List commands |
| ... | | | |

### Command Registration

| Aspect | Current State |
|--------|---------------|
| Registration method | Hardcoded / Dynamic |
| Command discovery | Yes / No |
| Help generation | Manual / Auto |
```

### Success Criteria
- [ ] All slash commands documented
- [ ] /piper subcommands documented
- [ ] DM vs channel behavior noted where different
- [ ] Command registration method identified
- [ ] Output follows structured format above

### Deliverables
Return inventory sections ready to insert into `docs/internal/architecture/current/command-inventory.md`

### STOP Conditions
- webhook_router.py doesn't handle commands → Report actual handler location
- Slack commands route through different service → Document actual flow
- More than 30 unique Slack commands → Report count, request guidance

---

## Prompt 4: URL Routes Inventory (Phase 1.6)

### Mission
Create comprehensive inventory of all user-facing API endpoints in web/api/routes/.

### Context
- **GitHub Issue**: #551 ARCH-COMMANDS - Command Parity Across Interfaces
- **Parent Gameplan**: `dev/2026/01/22/551-gameplan.md`
- **Current State**: REST endpoints defined in web/api/routes/
- **Target State**: Complete inventory of API endpoints that map to command functionality
- **Scope**: URL routes ONLY - do not inventory CLI, web chat, or Slack commands

### Infrastructure Verification (MANDATORY FIRST)

```bash
# Verify directory exists:
ls -la web/api/routes/

# List all route files:
find web/api/routes/ -name "*.py" -type f

# Check for FastAPI route decorators:
grep -rn "@router\." web/api/routes/ | head -30

# Expected: Directory exists, multiple route files, FastAPI decorators found
# STOP if: Directory missing or no route files
```

### Implementation Approach

#### Step 1: Inventory all route modules
- List all .py files in web/api/routes/
- For each file, identify the router and its prefix

#### Step 2: Extract endpoints from each module
- Find all @router.get(), @router.post(), etc. decorators
- Document:
  - HTTP method
  - Path
  - Handler function
  - Required auth
  - Request/response models

#### Step 3: Categorize endpoints
- Setup endpoints (configuration, onboarding)
- Feature endpoints (standup, calendar, todos, etc.)
- Utility endpoints (health, status)
- Integration endpoints (Slack callbacks, webhooks)

#### Step 4: Create inventory section
Output in this format:

```markdown
## URL Routes Inventory

### Route Modules

| Module | Prefix | Description |
|--------|--------|-------------|
| intent.py | /api/v1/intent | Intent classification |
| todos.py | /api/v1/todos | Todo management |
| ... | | |

### Endpoints by Category

#### Setup Endpoints
| Method | Path | Handler | Auth | Description |
|--------|------|---------|------|-------------|
| POST | /api/v1/setup/init | init_setup | None | Initialize setup |
| ... | | | | |

#### Feature Endpoints
| Method | Path | Handler | Auth | Description |
|--------|------|---------|------|-------------|
| POST | /api/v1/standup/generate | generate_standup | Required | Generate standup |
| GET | /api/v1/calendar/today | get_today | Required | Get today's calendar |
| ... | | | | |

#### Utility Endpoints
| Method | Path | Handler | Auth | Description |
|--------|------|---------|------|-------------|
| GET | /api/v1/health | health_check | None | Health check |
| ... | | | | |
```

### Success Criteria
- [ ] All route modules documented
- [ ] All endpoints documented with method, path, handler
- [ ] Endpoints categorized (setup, feature, utility, integration)
- [ ] Auth requirements noted
- [ ] Endpoints that map to CLI/chat commands identified
- [ ] Output follows structured format above

### Deliverables
Return inventory sections ready to insert into `docs/internal/architecture/current/command-inventory.md`

### STOP Conditions
- web/api/routes/ structure differs from expectations → Report actual structure
- Routes defined elsewhere (web/app.py directly) → Include those locations
- More than 100 endpoints → Report count, request guidance

---

## Prompt 5: CommandRegistry Core Implementation (Phase 3.1)

**STATUS: BLOCKED** - Requires Phase 2 ADR approval before implementation.

### Mission
Implement the CommandRegistry core as defined in ADR-0XX-command-registry.md.

### Context
- **GitHub Issue**: #551 ARCH-COMMANDS - Command Parity Across Interfaces
- **Parent Gameplan**: `dev/2026/01/22/551-gameplan.md`
- **ADR**: docs/internal/architecture/current/adrs/adr-0XX-command-registry.md
- **Current State**: Commands scattered across 6 registration points
- **Target State**: Centralized CommandRegistry with all commands registered
- **Dependencies**: Phase 2 ADR must be approved before starting

### Prerequisite Verification

```bash
# Verify ADR exists and is approved:
ls -la docs/internal/architecture/current/adrs/adr-*command-registry*.md

# Verify schema from Phase 2:
# [Will be defined in ADR]

# STOP if: ADR doesn't exist or isn't approved
```

### Implementation Approach
*To be defined after Phase 2 ADR approval*

#### Expected Deliverables
- [ ] `services/commands/registry.py` created
- [ ] `CommandRegistry` class implemented
- [ ] `CommandDefinition` dataclass implemented
- [ ] `InterfaceConfig` dataclass implemented
- [ ] Registry initialization in startup
- [ ] Unit tests for registry core
- [ ] 100% method implementation (X/X methods)

### STOP Conditions
- ADR not yet approved → Wait for Phase 2 completion
- Schema differs from inventory findings → Reconcile before implementing
- Performance requirements unclear → Request clarification

---

## Prompt 6: Command Migration (Phase 3.2-3.3)

**STATUS: BLOCKED** - Requires Phase 3.1 CommandRegistry core to be complete.

### Mission
Migrate all existing commands to use the CommandRegistry and update interface adapters.

### Context
- **GitHub Issue**: #551 ARCH-COMMANDS - Command Parity Across Interfaces
- **Parent Gameplan**: `dev/2026/01/22/551-gameplan.md`
- **Current State**: CommandRegistry core implemented (Phase 3.1)
- **Target State**: All commands migrated, _get_slash_commands() queries registry
- **Dependencies**: Phase 3.1 must be complete

### Prerequisite Verification

```bash
# Verify registry core exists:
ls -la services/commands/registry.py

# Verify it's functional:
python -c "from services.commands.registry import CommandRegistry; print('Registry imports OK')"

# STOP if: Registry not implemented or not functional
```

### Implementation Approach
*To be defined after Phase 3.1 completion*

#### Expected Deliverables
- [ ] All CLI commands registered
- [ ] All canonical handlers registered
- [ ] All Slack commands registered
- [ ] `_get_slash_commands()` queries registry dynamically
- [ ] Slack adapter uses registry for command discovery
- [ ] Migration tests verify no commands lost
- [ ] Routing integration tests pass
- [ ] 0 regressions in existing command behavior

### STOP Conditions
- Registry core not complete → Wait for Phase 3.1
- Any command breaks during migration → Rollback and investigate
- Performance regression detected → Profile and optimize

---

## Audit Notes

### Template Compliance

| Section | Prompt 1 | Prompt 2 | Prompt 3 | Prompt 4 | Prompt 5 | Prompt 6 |
|---------|----------|----------|----------|----------|----------|----------|
| Mission | Yes | Yes | Yes | Yes | Yes | Yes |
| Context | Yes | Yes | Yes | Yes | Yes | Yes |
| Infrastructure Verification | Yes | Yes | Yes | Yes | Yes | Yes |
| Implementation Approach | Yes | Yes | Yes | Yes | Blocked | Blocked |
| Success Criteria | Yes | Yes | Yes | Yes | Partial | Partial |
| Deliverables | Yes | Yes | Yes | Yes | Partial | Partial |
| STOP Conditions | Yes | Yes | Yes | Yes | Yes | Yes |

### Deployment Notes

**Phase 1 Prompts (1-4)**:
- Can be deployed in parallel
- Each produces inventory section for command-inventory.md
- Lead Dev combines outputs into complete inventory document

**Phase 3 Prompts (5-6)**:
- Must be deployed sequentially
- Require Phase 2 ADR completion first
- Prompts will need updating after ADR defines schema

### Scope Boundaries

Each prompt explicitly scopes to ONE interface:
- Prompt 1: CLI only
- Prompt 2: Web chat only
- Prompt 3: Slack only
- Prompt 4: URL routes only

This prevents duplicate work and ensures complete coverage.

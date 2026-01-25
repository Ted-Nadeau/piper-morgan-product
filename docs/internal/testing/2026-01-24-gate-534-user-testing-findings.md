# MUX-GATE-4 User Testing Findings

**Date**: 2026-01-24
**Tester**: xian (PM/Alpha)
**Gate**: #534 MUX-GATE-4: Interaction Design Complete
**Environment**: Dev laptop, main branch, localhost:8001

---

## Testing Objective

Validate gate #534 acceptance criteria:
- Discovery patterns validated with users
- Trust gradient mechanics working
- Spatial navigation working
- All I1-I3 issues closed

---

## Findings Table

| # | Test | Input | Expected | Actual | Status | Category | Notes |
|---|------|-------|----------|--------|--------|----------|-------|
| 1 | Discovery (greeting + question) | "Hi Piper! What can you help me with?" | Capability list | Calendar status + "What's on your mind?" | GAP | Multi-intent | Greeting prefix overrides discovery intent |
| 2 | Discovery (help command) | "Help" | Capability list or help menu | Focus/guidance response (priorities, strategic direction) | GAP | Routing | "Help" routes to GUIDANCE not DISCOVERY |
| 3 | Integration query | "Can you work with GitHub?" | GitHub-specific capabilities or connection prompt | Generic self-intro mentioning Calendar/Notion/Slack (not GitHub!) | GAP | Routing | Specific integration query not recognized |
| 4 | Discovery (clean) | "What can you do" | Capability list | ✅ Core Capabilities + Connected Integrations | PASS | Discovery | Works when no greeting prefix |
| 5 | Chat rename | Click to rename conversation | Editable title | ✅ Title editable | PASS | UX | New feature working |
| 6 | Project list | "Which projects am I working on?" | List of active projects | ✅ "You're working on 3 active projects" with names | PASS | Spatial | Projects query works |
| 7 | Focus/switch context | "Let's focus on One Job" | Context switch acknowledgment | Priorities not configured message → GitHub issue flow | GAP | Spatial | "Focus on X" triggers wrong flow, then ancient GitHub issue creation |
| 8 | Project status query | "What's the status of Piper Morgan?" | Project-specific status | Generic project list (same as #6) | GAP | Spatial | Project-specific query returns generic list |
| 9 | Projects page UI | Navigate to My Projects | Show user's projects | "No projects set up yet" (but chat shows 3!) | BUG | Data | Projects page not showing projects that exist in DB |
| 10 | User menu display | Header user menu | Show username "alfacanon" | Shows "User" instead | REGRESS | UI | Username display regression |
| 11 | Session timeout | Navigate away and back | Stay logged in | Redirected to login | REGRESS? | Auth | May be timeout or session issue |
| 12 | Add project via chat | "Can I add a new project?" | Project creation flow or guidance | "I don't have that capability yet" + "Starting workflow..." | GAP | Capability | Project creation not wired; spurious workflow messages |
| 13 | Update portfolio | "Update project portfolio" | Portfolio update flow | "I don't have that capability yet" + "Starting workflow..." | GAP | Capability | Same as #12; workflow messages are regression |
| 14 | Delete project | "Delete my Decision Review project, please" | Confirmation flow (archive vs delete) | "I don't have that capability yet" + "Starting workflow..." | GAP | Trust/Portfolio | Portfolio delete not wired to chat; #569 built service but not routed |
| 15 | Trust explanation | "Why can't you delete a project for me?" | Explanation of capability boundary | Generic IDENTITY intro | GAP | Trust | "Why can't you" not recognized as trust explanation query |
| 16 | Trust/relationship query | "How well do you know me?" | Trust level or relationship acknowledgment | Generic IDENTITY intro | GAP | Trust | Trust discussability not wired |
| 17 | Memory query | "What do you remember about me?" | Memory/history summary | Generic IDENTITY intro | GAP | Memory | Memory retrieval not wired to chat |

---

## Gap Analysis

### GAP-1: Multi-Intent Handling (Greeting + Discovery)

**Symptom**: "Hi Piper! What can you help me with?" returns calendar status instead of capabilities.

**Hypothesis**: Pre-classifier matches GREETING patterns first, routes to conversation handler, which provides status response. The discovery question in the same message is lost.

**Related**: #595 MUX-INTENT-MULTI addressed greeting + request but may not cover discovery queries.

**Pattern**: `Greeting + Discovery Question → Only greeting handled`

### GAP-2: "Help" Command Routing

**Symptom**: Bare "Help" returns focus/guidance advice instead of help menu or capabilities.

**Hypothesis**: "Help" is not in DISCOVERY_PATTERNS, may be routing to GUIDANCE.

**Pattern**: `"Help" → GUIDANCE instead of DISCOVERY`

### GAP-3: Integration-Specific Capability Queries

**Symptom**: "Can you work with GitHub?" returns generic intro mentioning other integrations but not GitHub.

**Hypothesis**: "Can you [work with X]?" pattern not recognized as capability query about specific integration.

**Pattern**: `"Can you work with [integration]?" → Generic IDENTITY response`

### GAP-4: "Focus on [Project]" Triggers Wrong Flow

**Symptom**: "Let's focus on One Job" returns priorities not configured message, then "Yes, please" triggers ancient GitHub issue creation flow asking about "system affected" and "users affected".

**Hypothesis**: "Focus on X" may be routing to PRIORITY or GUIDANCE handler. Confirmation "Yes, please" then falls into a default execution flow (GitHub issue creation).

**Pattern**: `"Focus on [project]" → PRIORITY handler → confirmation triggers EXECUTION`

### GAP-5: Project-Specific Status Query

**Symptom**: "What's the status of Piper Morgan?" returns generic project list instead of status for that specific project.

**Hypothesis**: STATUS handler doesn't parse project name from query, treats it as general status request.

**Question**: How SHOULD project status be derived? (GitHub issues? Manual updates? Inferred from activity?)

### BUG-1: Projects Page Shows No Projects

**Symptom**: My Projects page shows "No projects set up yet" but chat correctly lists 3 projects.

**Severity**: High - Data display inconsistency between chat and UI

**Hypothesis**: Projects page may be querying wrong user_id or different table than chat handler.

### REGRESS-1: Username Display

**Symptom**: User menu shows "User" instead of actual username "alfacanon".

**Severity**: Low - Cosmetic but noticed

### REGRESS-2: Workflow Status Messages

**Symptom**: "Starting workflow..." messages appear and timeout. Previously fixed in alpha testing.

**Severity**: Medium - Confusing UX, messages that don't lead anywhere

### GAP-6: Trust System Not Wired

**Symptom**: All trust-related queries ("Why can't you...", "How well do you know me?", "What do you remember?") return generic IDENTITY intro.

**Analysis**: Trust infrastructure exists (#647-649 built TrustService, TrustExplainer, etc.) but intent routing doesn't recognize:
- "Why can't you [X]?" → should route to trust explanation
- "How well do you know me?" → should route to trust/relationship query
- "What do you remember?" → should route to memory retrieval

**Status**: Infrastructure built, routing not wired

### GAP-7: Portfolio Service Not Wired to Chat

**Symptom**: "Delete my project" returns "I don't have that capability" despite #569 building PortfolioService with archive/delete.

**Analysis**: PortfolioService exists with patterns (ARCHIVE_PATTERNS, DELETE_PATTERNS, etc.) but no intent handler routes to it.

**Status**: Service built, intent routing not wired

---

## Positive Findings

1. **Graceful degradation** - All gaps fail gracefully with natural language, no errors
2. **Consciousness preserved** - Responses are warm and conversational, not robotic
3. **Core discovery works** - "What can you do" produces excellent capability summary
4. **New features working** - Chat rename feature validated

---

## Test Session Progress

- [x] Test 1: Discovery (Cold Start)
- [x] Test 2: Spatial Navigation (partial - blocked by bugs)
- [x] Test 3: Trust Gradient (infrastructure exists, not wired)
- [ ] Test 4: Moment Rendering
- [ ] Test 5: Portfolio Operations (blocked - service exists, not wired)

---

## Meta-Analysis: The Wiring Gap Pattern

### Observation

A consistent pattern emerged across all test categories:

| Layer | Status |
|-------|--------|
| Domain Models | ✅ Built |
| Services | ✅ Built |
| Repositories | ✅ Built |
| Unit Tests | ✅ Passing |
| **Intent Routing** | ❌ Not wired |
| **Chat Interface** | ❌ Not connected |
| **CLI Interface** | ❓ Unknown |
| **Slack/Webhooks** | ❓ Unknown |
| **Web UI Pages** | ❌ Broken (Projects page) |

### The "Last Mile" Problem

We built vertical slices of functionality:
- Trust system (#647-649): 80+ tests passing
- Memory system (#657-664): 50+ tests passing
- Portfolio service (#569, #567): 56 tests passing
- Moment UI (#418): 47 tests passing

But the **horizontal integration** connecting these to user touchpoints is missing:
1. No intent patterns route to these services
2. No canonical handlers call these services
3. UI pages may be querying different data paths

### Questions to Investigate

1. **Are there other interfaces besides chat we neglected?**
   - CLI commands
   - Slack slash commands / webhooks
   - Web UI pages (confirmed broken: Projects page)

2. **Are there other layers we neglected?**
   - Intent classification patterns
   - Canonical handler routing
   - API route registration
   - Frontend-backend data flow

3. **How did this get left out of the gameplan?**
   - Were we focused on "build service + tests" without "wire to user"?
   - Is there a missing phase in our issue templates?
   - Should acceptance criteria include "user can invoke via [interface]"?

### Hypothesis: Missing "Integration Phase"

Our typical issue flow:
1. ✅ Design (ADR/spec)
2. ✅ Build domain model
3. ✅ Build service
4. ✅ Write tests
5. ❌ **Wire to intent classifier**
6. ❌ **Wire to canonical handlers**
7. ❌ **Wire to UI pages**
8. ❌ **Verify user can actually use it**

Steps 5-8 are consistently missing.

---

## Scope for Remediation Epic

### MUX-WIRE: Service-to-Interface Integration

Potential child issues:

1. **MUX-WIRE-INTENT**: Add intent patterns for new services
   - Trust explanation queries
   - Memory queries
   - Portfolio operations (archive/delete/search)

2. **MUX-WIRE-HANDLERS**: Add canonical handlers for new services
   - Route TRUST_EXPLANATION → TrustExplainer
   - Route MEMORY_QUERY → MemoryService
   - Route PORTFOLIO_ACTION → PortfolioService

3. **MUX-WIRE-UI**: Fix UI page data flows
   - Projects page not showing projects
   - Username display regression

4. **MUX-WIRE-AUDIT**: Audit all interfaces
   - Chat: Which services are callable?
   - CLI: Which commands work?
   - Slack: Which slash commands work?
   - Web UI: Which pages work?

5. **MUX-WIRE-PROCESS**: Update issue template
   - Add acceptance criterion: "User can invoke via [interface]"
   - Add verification step: "Tested in [chat/CLI/Slack/UI]"

---

## Next Steps

1. ~~Complete remaining test categories~~ (Paused)
2. **Root cause analysis**: Why did wiring get skipped?
3. **Audit scope**: What else is built but not wired?
4. **Create remediation epic**: MUX-WIRE or similar
5. Execute wiring work
6. Re-test gate #534

---

## Complete Interface Audit

### Chat Interface (Intent Service)

**Audit completed**: 2026-01-24

**Services with Intent Patterns (WIRED)**:
| Service | Intent Category | Handler | Status |
|---------|-----------------|---------|--------|
| Identity | IDENTITY | `_handle_identity_query()` | ✅ Working |
| Temporal/Calendar | TEMPORAL, QUERY | `_handle_temporal_query()`, `_handle_meeting_time_query()` | ✅ Working |
| Status | STATUS | `_handle_status_query()` | ✅ Working |
| Priority | PRIORITY | `_handle_priority_query()` | ✅ Working |
| Guidance | GUIDANCE | `_handle_guidance_query()` | ✅ Working |
| Conversation | CONVERSATION | `_handle_conversation_query()` | ✅ Working |
| GitHub (shipped, PRs, issues) | QUERY | Various `_handle_*_query()` | ✅ Working |

**Services Built But NOT Wired**:
| Service | Location | Tests | Intent Patterns | Handler |
|---------|----------|-------|-----------------|---------|
| TrustService | `services/trust/` | 80+ passing | ❌ None | ❌ None |
| TrustExplainer | `services/trust/` | Included above | ❌ None | ❌ None |
| MemoryService | `services/memory/` | 50+ passing | ❌ None | ❌ None |
| PortfolioService | `services/onboarding/portfolio_service.py` | 56 passing | ❌ None | ❌ None |
| MomentRenderer | `services/mux/moment_*` | 47 passing | ❌ None | ❌ None |
| CompostingScheduler | `services/mux/composting_*` | Tests exist | ❌ None | ❌ None |

**Key Finding**: 6 major services built in I1 sprint have no chat interface.

---

### CLI Commands

**Audit completed**: 2026-01-24

**Framework Split**:
- `main.py` uses argparse: 6 commands
- `cli/commands/` uses Click: 8 modules with 23+ subcommands

**Implemented Commands**:
| Command | Module | Framework | Status |
|---------|--------|-----------|--------|
| `setup` | main.py | argparse | ✅ Working |
| `status` | main.py | argparse | ✅ Working |
| `preferences` | main.py | argparse | ✅ Working |
| `keys` | main.py | argparse | ✅ Working |
| `standup` | cli/commands/standup.py | Click | ✅ Working |
| `issues create/verify/sync/triage/status/patterns` | cli/commands/issues.py | Click | ✅ Working |
| `cal today/temporal/health` | cli/commands/cal.py | argparse | ✅ Working |
| `documents` | cli/commands/documents.py | Click | ✅ Working |
| `personality show/update` | cli/commands/personality.py | argparse | ✅ Working |
| `publish` | cli/commands/publish.py | argparse | ✅ Working |
| `notion status/search/pages/test/sync` | cli/commands/notion.py | argparse | ✅ Working |

**NOT Implemented (Services exist, no CLI)**:
| Service | CLI Command | Status |
|---------|-------------|--------|
| TrustService | N/A | ❌ No CLI |
| MemoryService | N/A | ❌ No CLI |
| PortfolioService | `portfolio archive/delete/search` | ❌ No CLI |
| CompostingScheduler | `compost run/status` | ❌ No CLI |

**Key Finding**: CLI has good coverage for calendar, standup, issues, documents. New I1 services have no CLI commands.

---

### Slack Commands

**Audit completed**: 2026-01-24

**Implemented Slash Commands** (in `webhook_router.py`):
| Command | Handler | Arguments | Status |
|---------|---------|-----------|--------|
| `/piper` | `_handle_piper_command()` | help, (empty) | ✅ Working |
| `/standup` | `_handle_standup_command()` | (none) | ⚠️ Partial (TODOs in helpers) |

**NOT Implemented**:
| Potential Command | Service | Status |
|-------------------|---------|--------|
| `/piper trust` | TrustService | ❌ Not wired |
| `/piper memory` | MemoryService | ❌ Not wired |
| `/piper projects` | PortfolioService | ❌ Not wired |

**Key Finding**: Slack has minimal command set. Only `/piper` and `/standup` exist.

---

### Web UI Pages

**Audit completed**: 2026-01-24

**Total Routes**: 202 endpoints across 25 route modules

**Working Pages**:
- `/` (home/chat)
- `/login`
- `/setup`
- `/standup`
- `/settings`
- `/settings/integrations/*` (Slack, Calendar, Notion, GitHub)
- `/personality-preferences`
- `/learning`
- `/files`
- `/todos`
- `/lists`

**Broken/Incomplete Pages**:
| Page | Issue | Root Cause |
|------|-------|------------|
| `/projects` | Shows "No projects" when 3 exist in DB | Data flow issue - may query wrong user_id |
| User menu | Shows "User" instead of username | Frontend not receiving user data |

**Missing Pages for New Services**:
| Service | Page | Status |
|---------|------|--------|
| TrustService | N/A | No UI concept defined |
| MemoryService | N/A | No UI concept defined |
| PortfolioService | N/A | No dedicated UI (should integrate with `/projects`) |

---

## Root Cause Analysis

### The Five Whys

**Symptom**: Users cannot access Trust, Memory, Portfolio services despite them being built.

1. **Why?** No intent patterns route to these services.
2. **Why?** No canonical handlers call these services.
3. **Why?** Issue scope was "build service + tests" without "wire to interface".
4. **Why?** Issue template doesn't require interface verification.
5. **Why?** We measured completion by "tests pass" not "user can use it".

### Root Cause: Definition of Done

**Finding**: Our Definition of Done is infrastructure-focused, not user-focused.

Current implicit DoD:
- ✅ Domain model defined
- ✅ Service implemented
- ✅ Repository created
- ✅ Unit tests pass
- ❌ Intent patterns added
- ❌ Handler wired
- ❌ User can actually invoke

**The gap**: We closed issues when the *service* worked, not when the *user* could use it.

### Contributing Factors

1. **Vertical slice focus**: Each issue built a complete service but didn't trace to user entry points
2. **Test-driven but not UX-driven**: 705+ tests pass, but all 6 new services are unreachable
3. **No integration testing in acceptance criteria**: Gate #534 is first time user testing happened
4. **Sprint velocity pressure**: Rushing to close issues before gate review

### The 75% Pattern (Again)

This is a variant of the 75% pattern from CLAUDE.md:
- Services are 100% built
- Tests are 100% passing
- **User accessibility is 0%**

The work is *complete* by one measure and *useless* by another.

---

## Remediation Plan

### Immediate (This Sprint)

**MUX-WIRE Epic** - Wire existing services to user interfaces

| Issue | Description | Priority |
|-------|-------------|----------|
| MUX-WIRE-1 | Add DISCOVERY intent patterns for "Help" | P0 |
| MUX-WIRE-2 | Add TRUST intent patterns + handler | P1 |
| MUX-WIRE-3 | Add MEMORY intent patterns + handler | P1 |
| MUX-WIRE-4 | Add PORTFOLIO intent patterns + handler | P1 |
| MUX-WIRE-5 | Fix /projects page data flow | P0 |
| MUX-WIRE-6 | Fix username display in header | P2 |
| MUX-WIRE-7 | Remove spurious "Starting workflow..." messages | P1 |

### Process Change (Future Sprints)

**Updated Definition of Done**:
1. ✅ Domain model defined
2. ✅ Service implemented
3. ✅ Repository created
4. ✅ Unit tests pass
5. ✅ **Intent patterns added (if chat-accessible)**
6. ✅ **Handler wired (if chat-accessible)**
7. ✅ **User can invoke via intended interface**
8. ✅ **Verified by PM or alpha tester**

**Issue Template Addition**:
```markdown
## Interface Verification
- [ ] Chat: Intent pattern → Handler → Service → Response
- [ ] CLI: Command → Service → Output (if applicable)
- [ ] Slack: Slash command → Service → Response (if applicable)
- [ ] Web UI: Page → API → Service → Render (if applicable)
```

---

## Summary Statistics

| Metric | Count |
|--------|-------|
| Tests found | 17 |
| PASS | 4 |
| GAP | 9 |
| BUG | 1 |
| REGRESSION | 3 |
| Services built but not wired | 6 |
| CLI commands working | 23+ |
| CLI commands missing for new services | 4+ |
| Slack commands working | 2 |
| Web routes total | 202 |
| Web pages broken | 2 |

---

*Document created during live testing session 2026-01-24*
*Testing paused at Test 4 to investigate root causes*
*Interface audit completed 2026-01-24*

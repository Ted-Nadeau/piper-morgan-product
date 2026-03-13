# Skill Harvest: Candidate Extraction

**Date**: January 21, 2026
**Phase**: 2 - Candidate Extraction
**Status**: In Progress

---

## Source Inventory Summary (Phase 1 Complete)

### Primary Sources Scanned

| Source | Files Found | Implicit Skills Identified |
|--------|-------------|---------------------------|
| CLAUDE.md | 1 (1258 lines) | 12+ workflows |
| BRIEFING-ESSENTIAL-*.md | 3 files | Role-specific procedures |
| methodology-core/ | 36 files | 6+ formal methodologies |
| .github/issue_template/ | 4 templates | Issue creation patterns |
| scripts/ | 127 files | Automation patterns |
| docs/internal/operations/ | 25 files | Audit procedures |

### Key Methodology Documents

1. **methodology-20-OMNIBUS-SESSION-LOGS.md** - Complete 6-phase omnibus creation methodology
2. **gameplan-template.md** - v9.3 gameplan with 8+ phases
3. **claude-code-workflow.md** - Systematic verification-first methodology
4. **staggered-audit-calendar-2026.md** - Audit scheduling procedures

---

## Skill Candidates Extracted

### TIER 1 CANDIDATES (High frequency, clear structure, cross-role)

---

### Candidate 1: `create-session-log`

**Trigger Pattern**: "start a new session log", "create session log", session start
**Current Implementation**: CLAUDE.md session discipline section, naming conventions scattered
**Frequency**: Daily (every session)
**Cross-role or Role-specific**: Cross-role (all agents create logs)

**Inputs**:
- Role slug (lead, prog, docs, comms, arch, etc.)
- Tool (code, cursor)
- Model (opus, sonnet, haiku)
- Date/time

**Outputs**:
- Session log file at `dev/active/YYYY-MM-DD-HHMM-{role}-{tool}-{model}-log.md`
- Standard header structure
- Work log section started

**Dependencies**:
- Naming convention knowledge
- Directory structure (`dev/active/`)
- Role slug mappings

**Complexity**: LOW (~50 lines SKILL.md)
**Formalization Value**: HIGH - Every agent does this, slight variations cause inconsistency

---

### Candidate 2: `create-omnibus-log`

**Trigger Pattern**: "create omnibus for [date]", "make omnibus log"
**Current Implementation**: methodology-20-OMNIBUS-SESSION-LOGS.md (471 lines!)
**Frequency**: Daily to weekly
**Cross-role or Role-specific**: Role-specific (docs agent primarily)

**Inputs**:
- Target date
- Source log discovery (glob pattern)

**Outputs**:
- Omnibus log file at `docs/omnibus-logs/YYYY-MM-DD-omnibus-log.md`
- Standard/High-Complexity format selected
- Timeline + Executive Summary

**Dependencies**:
- methodology-20 document (full procedure)
- Source log locations
- Format selection criteria

**Complexity**: HIGH (~200+ lines SKILL.md due to 6-phase methodology)
**Formalization Value**: HIGH - Complex procedure, error-prone without guidance

---

### Candidate 3: `check-mailbox`

**Trigger Pattern**: Session start, "check mailbox", "check inbox"
**Current Implementation**: CLAUDE.md mailbox check section, mailboxes/README.md
**Frequency**: Every session start
**Cross-role or Role-specific**: Cross-role (all roles with mailboxes)

**Inputs**:
- Role slug

**Outputs**:
- List of messages in inbox
- Messages moved to read/ after reading
- Responses created if requested

**Dependencies**:
- mailboxes/ directory structure
- Role slug → mailbox mapping
- Response protocol

**Complexity**: LOW (~40 lines SKILL.md)
**Formalization Value**: MEDIUM - Simple but often forgotten

---

### Candidate 4: `create-gameplan`

**Trigger Pattern**: "create gameplan for [issue]", "write gameplan"
**Current Implementation**: gameplan-template.md (757 lines!)
**Frequency**: Per epic/major issue
**Cross-role or Role-specific**: Role-specific (Chief Architect primarily)

**Inputs**:
- GitHub issue number
- Feature/task description
- Infrastructure context

**Outputs**:
- Gameplan document with phases
- Phase -1 verification
- Acceptance criteria
- Multi-agent deployment map

**Dependencies**:
- gameplan-template.md (extensive)
- GitHub issue access
- Infrastructure knowledge

**Complexity**: HIGH (~300+ lines SKILL.md)
**Formalization Value**: HIGH - Complex template, critical for project success

---

### Candidate 5: `pattern-sweep-execution`

**Trigger Pattern**: "run pattern sweep", pattern sweep week
**Current Implementation**: pattern-sweep.md template, pattern-sweep-2.0-framework.md
**Frequency**: Every 6 weeks
**Cross-role or Role-specific**: Role-specific (Lead Dev + specialized agents)

**Inputs**:
- Date range
- Pattern library location

**Outputs**:
- 5 agent deliverables
- Anti-pattern index update
- Leadership summary
- DRAFT patterns if emergence found

**Dependencies**:
- Pattern sweep template
- Staggered calendar
- 5-agent coordination
- Anti-pattern index

**Complexity**: HIGH (~250+ lines)
**Formalization Value**: HIGH - Multi-agent coordination, infrequent so easy to forget

---

### Candidate 6: `close-issue-properly`

**Trigger Pattern**: "close issue", issue completion
**Current Implementation**: CLAUDE.md issue closure protocol section
**Frequency**: Multiple times per session
**Cross-role or Role-specific**: Cross-role

**Inputs**:
- Issue number
- Evidence of completion

**Outputs**:
- Updated description checkboxes
- Completion matrix updated
- Closing comment with evidence
- Issue closed (or flagged for PM)

**Dependencies**:
- GitHub CLI (`gh`)
- Evidence format knowledge
- Beads discipline

**Complexity**: MEDIUM (~80 lines SKILL.md)
**Formalization Value**: HIGH - Frequently done incorrectly (Issue #490 retrospective)

---

### TIER 2 CANDIDATES (Medium frequency or more specialized)

---

### Candidate 7: `run-debug-protocol`

**Trigger Pattern**: Bug investigation, "debug this", test failures
**Current Implementation**: CLAUDE.md systematic debugging section
**Frequency**: As needed (frequent during bugs)
**Cross-role or Role-specific**: Cross-role (primarily coding agents)

**Inputs**:
- Error description
- Failing test or behavior

**Outputs**:
- Root cause identified
- Fix implemented (or escalation)
- Evidence documented

**Dependencies**:
- 4-phase debugging framework
- Pattern analysis approach

**Complexity**: MEDIUM (~100 lines SKILL.md)
**Formalization Value**: MEDIUM - Prevents "fix symptoms not root cause" anti-pattern

---

### Candidate 8: `anti-pattern-scan`

**Trigger Pattern**: "scan for anti-patterns", pattern sweep Phase 3a
**Current Implementation**: Today's work! (anti-pattern-index.md, extraction scripts)
**Frequency**: Every 6 weeks (pattern sweep)
**Cross-role or Role-specific**: Role-specific (docs agent)

**Inputs**:
- Target directories/files
- Date range (for session logs)

**Outputs**:
- Candidate list with classifications
- TRUE EMERGENT added to index

**Dependencies**:
- 3 extraction scripts
- Anti-pattern index
- Classification criteria

**Complexity**: MEDIUM (~100 lines SKILL.md)
**Formalization Value**: MEDIUM - New process, would benefit from formalization

---

### Candidate 9: `beads-session-start`

**Trigger Pattern**: Session start, "check beads", "bd ready"
**Current Implementation**: CLAUDE.md Beads completion discipline section
**Frequency**: Every session start
**Cross-role or Role-specific**: Cross-role

**Inputs**:
- None (reads from beads database)

**Outputs**:
- Ready issues list
- Current status
- Blockers identified

**Dependencies**:
- `bd` CLI commands
- Beads database

**Complexity**: LOW (~50 lines SKILL.md)
**Formalization Value**: MEDIUM - Simple commands but discipline is important

---

### Candidate 10: `create-memo`

**Trigger Pattern**: "write memo to [role]", "draft memo"
**Current Implementation**: Implicit (mailbox conventions)
**Frequency**: As needed
**Cross-role or Role-specific**: Cross-role

**Inputs**:
- Recipient role
- Subject
- Content/questions

**Outputs**:
- Memo file in recipient's inbox
- Standard format with To/From/Date/Re

**Dependencies**:
- Mailbox conventions
- Memo format template

**Complexity**: LOW (~40 lines SKILL.md)
**Formalization Value**: LOW-MEDIUM - Simple but consistent format helps

---

### Candidate 11: `doc-audit`

**Trigger Pattern**: "run doc audit", documentation audit week
**Current Implementation**: Operations docs, issue template
**Frequency**: Every 3-4 weeks
**Cross-role or Role-specific**: Role-specific (CoS/Doc Manager)

**Inputs**:
- None (scans configured directories)

**Outputs**:
- Broken links count
- Stale docs identified
- Metrics report

**Dependencies**:
- Link checking scripts
- Audit checklist

**Complexity**: MEDIUM (~80 lines SKILL.md)
**Formalization Value**: MEDIUM - Recurring process with checklist

---

### Candidate 12: `verification-first-implementation`

**Trigger Pattern**: Starting any implementation, coding task
**Current Implementation**: claude-code-workflow.md
**Frequency**: Every coding task
**Cross-role or Role-specific**: Cross-role (coding agents)

**Inputs**:
- Implementation task description

**Outputs**:
- Verification commands run
- Pattern discovery documented
- Implementation following patterns

**Dependencies**:
- Verification commands library
- Pattern library knowledge

**Complexity**: MEDIUM (~100 lines SKILL.md)
**Formalization Value**: HIGH - Core methodology, prevents assumption-based development

---

### TIER 3 CANDIDATES (Lower frequency or highly specialized)

---

### Candidate 13: `role-health-check`

**Trigger Pattern**: "role health check", every 4 weeks
**Current Implementation**: BRIEFING-ESSENTIAL-HOSR.md, staggered calendar
**Frequency**: Every 4 weeks
**Cross-role or Role-specific**: Role-specific (HOSR/CoS)

---

### Candidate 14: `methodology-audit`

**Trigger Pattern**: "methodology audit", every 6-8 weeks
**Current Implementation**: Staggered calendar
**Frequency**: Every 6-8 weeks
**Cross-role or Role-specific**: Role-specific (CIO)

---

### Candidate 15: `create-adr`

**Trigger Pattern**: "create ADR", architectural decision needed
**Current Implementation**: scripts/new-adr.sh, ADR template
**Frequency**: As needed
**Cross-role or Role-specific**: Role-specific (Architect)

---

### Candidate 16: `create-pattern`

**Trigger Pattern**: "create pattern", pattern formalization
**Current Implementation**: scripts/new-pattern.sh, pattern template
**Frequency**: Infrequent (after TRUE EMERGENCE)
**Cross-role or Role-specific**: Role-specific (Architect)

---

## Classification Summary

| Tier | Count | Characteristics |
|------|-------|-----------------|
| **Tier 1** | 6 | High frequency, clear structure, high formalization value |
| **Tier 2** | 6 | Medium frequency, specialized, moderate formalization value |
| **Tier 3** | 4 | Lower frequency, highly specialized |

---

## Recommended Pilot Candidate

**Recommendation**: `create-session-log` (Candidate 1)

**Rationale**:
1. **Highest frequency** - Every agent, every session
2. **Lowest complexity** - ~50 lines SKILL.md
3. **Fewest dependencies** - Just naming conventions and directory
4. **Cross-role** - Benefits all agents immediately
5. **Clear success criteria** - File created with correct name and structure
6. **Quick to validate** - Can test in minutes

**Alternative**: `check-mailbox` (Candidate 3) - Similar profile, slightly lower impact

---

## Next Steps

1. **PM Decision**: Approve `create-session-log` as pilot candidate?
2. **Phase 3**: Map dependencies for pilot skill
3. **Phase 5**: Create SKILL.md spec → draft → audit

---

*Extraction complete. Ready for PM review of pilot candidate selection.*

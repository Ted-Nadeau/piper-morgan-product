# Piper Morgan Roadmap v13.0
**Date**: 2026-01-12
**Author**: Documentation Agent (updated from Chief Architect v12.2)
**Status**: Active - Sprint B1 COMPLETE, MUX Planning

---

## Executive Summary

**Major milestone achieved**: Sprint B1 completed January 11, 2026. v0.8.4 released with Integration Settings (Epic #543) and Portfolio Onboarding (#490). 23+ issues closed in 3 days (Jan 9-11). Project is ready to begin MUX (Modeled User Experience) phase.

**Key Changes from v12.2**:
- Sprint B1 COMPLETE - all FTUX, CONV, and Integration Settings work done
- v0.8.4 released (January 12, 2026)
- Completion Discipline Triad established (Patterns 045/046/047)
- MUX phase ready to begin

---

## Current Position

```
Inchworm Position: 4.2.1.1 (per Chief Architect Jan 11)

1. ✅ The Great Refactor (GREAT)
2. ✅ CORE functionality
3. ✅ ALPHA testing (v0.8.0 → v0.8.4)
4. 🎯 MVP Track
   4.1. ✅ B1 - FTUX & Conversations (COMPLETE Jan 11)
        ✅ FTUX-PIPER-INTRO (#547)
        ✅ FTUX-EMPTY-STATES (#548)
        ✅ FTUX-POST-SETUP (#549)
        ✅ FTUX-QUICK-2, QUICK-3
        ✅ FTUX-CHAT-BRIDGE (#550)
        ✅ FTUX-CONCIERGE
        ✅ CONV-UX-GREET (#102)
        ✅ CONV-MCP-STANDUP-INTERACTIVE (Epic #242 - 5 children)
        ✅ SLACK-ATTENTION-DECAY (#365)
        ✅ FTUX-PORTFOLIO (#490)
        ✅ TEST-GAP (#559)
        ✅ CONV-UX-PERSIST (Epic #314 - 4 children)
        ✅ CORE-SETTING-DISCONNECT (#544)
        ✅ CORE-SETTINGS-INTEGRATION (Epic #543 - 4 children)
   4.2. 🎯 MUX-V1: Vision & Conceptual Architecture (NEXT)
   4.3. MUX-V2: Integration & Learning
   4.4. MUX-INTERACT: Interaction Design
   4.5. MUX-IMPLEMENT: UI Polish
5. Beta testing on 0.9
6. Launch 1.0
```

---

## Sprint B1 Completion Summary (Jan 5-11, 2026)

### Issues Closed: 23+

**Epics Completed**:
- Epic #242: Interactive Standup Assistant (5 children)
- Epic #314: Conversation Persistence (4 children)
- Epic #543: Integration Settings (4 children)

**Major Features**:
| Issue | Feature | Commit |
|-------|---------|--------|
| #547 | FTUX Piper Intro | ab6716e1 |
| #548 | FTUX Empty States | e993005f |
| #549 | FTUX Post-Setup | b82b674a |
| #550 | FTUX Chat Bridge | (part of FTUX batch) |
| #490 | Portfolio Onboarding | d3554765 |
| #365 | Slack Attention Decay | 45c8d93d |
| #544 | Disconnect All button | cee6c3eb |
| #562 | Integration Test OAuth fix | ab44a72e |
| #563-566 | Conversation Persistence | (CONV-PERSIST-1 through 4) |
| #570-573 | Integration Preferences | (Slack/Calendar/Notion/GitHub) |
| #576-579 | OAuth Credential UI | (Slack/Calendar/GitHub/Notion) |

### Key Patterns Established
- **Pattern-045**: Green Tests, Red User (completion discipline)
- **Pattern-046**: Beads Completion Discipline
- **Pattern-047**: Time Lord Alert (uncertainty signaling)
- **Pattern-048**: Periodic Background Job (from #365)

---

## Next Phase: MUX (Modeled User Experience)

### MUX-VISION V1: Conceptual Architecture
**Status**: Ready to begin
**GitHub Issues**: #433-436 (MUX-TECH phases)

**Scope**:
- VISION-OBJECT-MODEL - ADR-045 formalization
- VISION-GRAMMAR-CORE - "Entities experience Moments in Places"
- VISION-CONSCIOUSNESS - Extract from Morning Standup
- VISION-METAPHORS - Native/Federated/Synthetic

### MUX-TECH: Technical Implementation
**GitHub Issues Created**:
- #433: MUX-TECH-PHASE1-GRAMMAR
- #434: MUX-TECH-PHASE2-ENTITY
- #435: MUX-TECH-PHASE3-OWNERSHIP
- #436: MUX-TECH-PHASE4-COMPOSTING

### MUX Gates (Milestones)
- #531: MUX-GATE-1 - Foundation Phase Complete
- #532: MUX-GATE-2 - Core Implementation Complete
- #533: MUX-GATE-3 - Integration Phase Complete
- #534: MUX-GATE-4 - Interaction Design Complete

---

## Open Issues by Category

### MUX Phase (Future)
- #433-436: MUX-TECH Phases 1-4
- #477: MUX-VISION-LISTS
- #474: MUX-TECH-LISTS
- #488: MUX-INTERACT-DISCOVERY
- #567-569: MUX Portfolio extensions

### Architecture & Infrastructure
- #551: ARCH-COMMANDS (Command Parity)
- #557: ARCH-WebSocket Infrastructure
- #463: FLY-COORD-TREES (Git Worktrees)

### Security
- #542: SEC Token Revocation
- #482: SEC-KMS-INTEGRATION

### Bug Fixes
- #574: Conversation history panel switching

### Tech Debt
- #546: Alternate issue providers
- #558: LLM-based preference extraction
- #471: Infrastructure Epic (OAuth, Learning, TimeSeries)
- #472: Slack Integration TDD Gaps

---

## Version History

| Version | Date | Key Features |
|---------|------|--------------|
| v0.8.4 | Jan 12, 2026 | Sprint B1 Complete, Integration Settings, Portfolio Onboarding |
| v0.8.3.2 | Jan 8, 2026 | Epic #242 Interactive Standup |
| v0.8.3.1 | Jan 7, 2026 | FTUX improvements |
| v0.8.3 | Jan 2, 2026 | Setup wizard enhancements |
| v0.8.2 | Dec 2025 | Alpha stability |
| v0.8.1 | Nov 2025 | Initial alpha |

---

## Success Metrics

### January 2026 ✅ ACHIEVED
- [x] Sprint B1 complete
- [x] v0.8.4 released
- [x] Integration Settings working
- [x] Portfolio Onboarding implemented
- [x] 23+ issues closed in 3 days

### February 2026 (Targets)
- [ ] MUX-V1 Vision sprint complete
- [ ] MUX-TECH Phase 1 (Grammar) implemented
- [ ] Conversation history bug fixed (#574)
- [ ] WebSocket infrastructure evaluated

### March 2026 (Targets)
- [ ] MUX-V2 Integration complete
- [ ] Entity consciousness visible in code
- [ ] Learning pipeline operational

---

## Gate Implementation (from v12.3)

### Gate Structure
Each gate (#531-534) is a GitHub issue with mandatory checklist:
1. All phase issues closed with evidence
2. Pattern discovery ceremony completed
3. No P0/P1 bugs
4. Team alignment checkpoint
5. PM approval

### Pattern Discovery Ceremony
End of each sprint:
- What patterns emerged?
- What anti-patterns appeared?
- What should be documented?
- Output: Pattern log updates or DRAFT patterns

---

## Risk Mitigation

### Technical Risks
- **Conversation switching bug (#574)**: Known, needs investigation
- **MUX complexity**: Gate system provides checkpoints
- **Learning system gap**: Composting pipeline is spec only (per Jan 11 audit)

### Process Risks
- **Completion bias**: Patterns 045/046/047 provide countermeasures
- **Documentation drift**: Weekly audits (issue #580 template)
- **MUX 75% Abandonment**: Mitigated by gates and Beads discipline (Pattern-046)

### Contingency Plans (from v12.3)
- If MUX slips: Continue MVP work in parallel
- If discovery fails: Return to command paradigm
- If gates block: Time-box investigation

---

## Pattern Integration

All work follows these patterns (embedded from v12.3):
- **Pattern-006**: Verification-First
- **Pattern-009**: GitHub Issue Tracking
- **Pattern-021**: Session Management
- **Pattern-045**: Green Tests, Red User (completion discipline)
- **Pattern-046**: Beads Completion Discipline
- **Pattern-047**: Time Lord Alert (uncertainty signaling)
- **Pattern-048**: Periodic Background Job

---

## Notes

**Inchworm Principle**: Each phase completes 100% before next begins. Sprint B1 demonstrated this with 23+ issues closed systematically.

**Completion Discipline Triad**: Patterns 045/046/047 form a reinforcing system against AI completion bias.

**Learning System Status** (per Jan 11 audit):
- Built: Preference Learning (118 tests), Attention Decay (7 tests), Query Learning Loop
- Spec Only: Composting Pipeline, Insight Journal, Dreaming Jobs

**Dependency Stack** (from v12.3, still valid):
1. Setup/Config (explicit wizard support) ✅ COMPLETE
2. Conversational Glue (discovery enablement) ✅ COMPLETE (Portfolio Onboarding)
3. MUX-VISION (conceptual architecture) ← NEXT
4. MUX-TECH (implementation)
5. MUX-INTERACT (discovery patterns)
6. MUX-IMPLEMENT (polish)

---

## Change Log

### v13.0 (Jan 12, 2026)
- Sprint B1 COMPLETE documented
- Updated inchworm position to 4.2.1.1
- Added Sprint B1 completion summary with all 23+ issues
- Updated version history through v0.8.4
- Refreshed open issues from GitHub
- Added MUX gates (#531-534)
- Documented Completion Discipline Triad
- **Merged v12.3 insights**: Gate implementation details, pattern discovery ceremony, contingency plans, dependency stack

### v12.3 (Dec 27, 2025) - knowledge/roadmap-v12.3.md
- Reality-based timeline (MUX in February)
- Added setup wizard issues
- Added gate milestones
- Pattern insights integrated
- Quick wins identified

### v12.2 (Nov 29, 2025)
- Added MUX-TECH epic with 4 phases
- Established dual-track visualization
- Documented convergence points

---

*Roadmap v13.0 - Sprint B1 Complete, MUX Phase Beginning*

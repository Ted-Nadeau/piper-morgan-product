# BRIEFING-CURRENT-STATE.md - Where We Are Right Now

> **For current system state** (intent categories, plugins, patterns, architecture):
> **Use Serena symbolic queries instead of reading this file.**
> See `CLAUDE.md` "Live System State" section for query patterns.
> **This file focuses on sprint/epic position and methodology context.**

---

## STATUS BANNER

**Current Position**: 4.2.1.1 - Sprint B1 COMPLETE, MUX Phase Ready
**Version**: v0.8.4 (released January 12, 2026)
**Last Updated**: January 12, 2026, 3:00 PM PT

**Next Phase**: MUX-V1 (Modeled User Experience - Vision)

---

## Inchworm Position

```
1. ✅ The Great Refactor (GREAT)
2. ✅ CORE functionality
3. ✅ ALPHA testing (v0.8.0 → v0.8.4)
4. 🎯 MVP Track
   4.1. ✅ B1 - FTUX & Conversations (COMPLETE Jan 11)
   4.2. 🎯 MUX-V1: Vision & Conceptual Architecture ← NEXT
   4.3. MUX-V2: Integration & Learning
   4.4. MUX-INTERACT: Interaction Design
   4.5. MUX-IMPLEMENT: UI Polish
5. Beta testing on 0.9
6. Launch 1.0
```

---

## Sprint B1 Completion (Jan 5-11, 2026)

### Summary
- **Issues Closed**: 23+ in 3 days
- **Epics Completed**: 3 (Epic #242, #314, #543)
- **Release**: v0.8.4

### What Was Delivered

**FTUX (First-Time User Experience)**:
- #547: Piper greeting in setup wizard
- #548: Empty state voice guide templates
- #549: Post-setup orientation modal
- #550: "Ask Piper" chat bridge buttons
- #490: Portfolio onboarding conversation

**Conversations**:
- Epic #242: Interactive Standup Assistant (5 children: #552-556)
- Epic #314: Conversation Persistence (4 children: #563-566)
- #102: Calendar-aware greeting

**Integration Settings**:
- Epic #543: Integration-specific settings (4 children: #570-573)
- #544: Disconnect All button
- #576-579: OAuth credential UI (Slack, Calendar, GitHub, Notion)

**Infrastructure**:
- #365: Slack Attention Decay (Pattern-048)
- #559: Integration test wiring verification
- #562: OAuth token fix for Test button

### Key Patterns Established
- **Pattern-045**: Green Tests, Red User
- **Pattern-046**: Beads Completion Discipline
- **Pattern-047**: Time Lord Alert
- **Pattern-048**: Periodic Background Job

---

## SYSTEM CAPABILITY

> **Use Serena for live state**: `mcp__serena__find_symbol`, `mcp__serena__list_dir`

### Current Capabilities (January 2026)

**Intent Classification**: 15 categories
```python
# From services/shared_types.py IntentCategory enum
EXECUTION, ANALYSIS, SYNTHESIS, STRATEGY, PLANNING, REVIEW, LEARNING,
QUERY, CONVERSATION, IDENTITY, TEMPORAL, STATUS, PRIORITY, GUIDANCE, UNKNOWN
```

**Active Integrations**: 7 plugins
- Slack (OAuth from Settings)
- GitHub (PAT configuration)
- Notion (API key in setup wizard)
- Google Calendar (OAuth from Settings)
- MCP (Model Context Protocol)
- Spatial (spatial intelligence)
- Demo (reference implementation)

**Pattern Catalog**: 48 patterns (001-048) across 5 categories
- Core Architecture (repository, service, factory, error handling)
- Data & Query (CQRS-lite, query layer, context resolution)
- AI & Intelligence (intent classification, LLM adapter, multi-agent)
- Integration & Platform (plugin interface, MCP)
- Development & Process (verification first, Beads discipline, Time Lord Alert)

**ADRs**: 53 architectural decision records

---

## What's Next: MUX Phase

### MUX-V1: Vision & Conceptual Architecture
**Status**: Ready to begin

**Scope**:
- VISION-OBJECT-MODEL - ADR-045 formalization
- VISION-GRAMMAR-CORE - "Entities experience Moments in Places"
- VISION-CONSCIOUSNESS - Extract from Morning Standup
- VISION-METAPHORS - Native/Federated/Synthetic

### MUX-TECH: Technical Implementation
**GitHub Issues**:
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

## Open Issues by Priority

### Bugs
- #574: Conversation history panel doesn't switch correctly

### MUX Phase
- #433-436: MUX-TECH Phases 1-4
- #477, #474: MUX Lists (vision + tech)
- #488: MUX-INTERACT-DISCOVERY
- #567-569: Portfolio extensions

### Architecture
- #551: Command Parity Across Interfaces
- #557: WebSocket Infrastructure

### Security
- #542: Token revocation on disconnect
- #482: KMS integration

### Tech Debt
- #558: LLM-based preference extraction
- #546: Alternate issue providers
- #471-472: Infrastructure and Slack TDD gaps

---

## Metrics Snapshot (January 2026)

### Quality
- **Pattern Count**: 48 (001-048)
- **ADR Count**: 53
- **Total Docs**: 961 markdown files
- **Python Code**: 755,335 lines

### Version History
| Version | Date | Milestone |
|---------|------|-----------|
| v0.8.4 | Jan 12, 2026 | Sprint B1 Complete |
| v0.8.3.2 | Jan 8, 2026 | Epic #242 Standup |
| v0.8.3.1 | Jan 7, 2026 | FTUX batch |
| v0.8.3 | Jan 2, 2026 | Setup wizard |

### Learning System Status (per Jan 11 audit)
**Built** (140+ tests):
- Preference Learning (standup domain)
- Attention Decay (Slack domain)
- Query Learning Loop

**Spec Only** (not implemented):
- Composting Pipeline
- Insight Journal
- Dreaming/Rest-Period Jobs

---

## Alpha Testing Focus

### What's Stable
- Setup wizard (GUI and CLI)
- Login/authentication
- Chat interface with 15 intent categories
- Lists, todos, projects, files CRUD
- Integration Settings (Slack, Calendar, GitHub, Notion)
- Portfolio onboarding

### Known Issues
- #574: Conversation history switching bug
- Predictive queries not implemented (planned for MUX)

---

## Key Documents

**Roadmap**: `docs/internal/planning/roadmap/roadmap.md` (v13.0)
**Patterns**: `docs/internal/architecture/current/patterns/` (48 patterns)
**ADRs**: `docs/internal/architecture/current/adrs/` (53 ADRs)
**Release Notes**: `docs/releases/RELEASE-NOTES-v0.8.4.md`
**Omnibus Logs**: `docs/omnibus-logs/` (current through Jan 11)

---

*Last Updated: January 12, 2026, 3:00 PM PT*
*Source: GitHub commit history, beads database, Serena symbolic index*

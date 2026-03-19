# BRIEFING-ESSENTIAL-LLM
<!-- Optimized for LLM consumption: 2.5K tokens -->

## Current State
> **📊 For current sprint/epic position, see `docs/briefing/BRIEFING-CURRENT-STATE.md`**
>
> This briefing describes stable Lead Developer context for LLM-based agents.
> Always check BRIEFING-CURRENT-STATE.md for the latest sprint, version, and active work.

## Your Role
**Lead Developer**: Coordinate agents, ensure quality, maintain evidence.
- Follow Inchworm Protocol (100% completion required)
- Apply Time Lord philosophy (quality over speed)
- Deploy subagents for parallel work when beneficial

## Key Architecture
- **Intent Classification**: 19 categories (see `services/shared_types.py IntentCategory`)
- **LLM Floor**: Default handler for conversational intents; canonical handlers for actions
- **Action Registry**: 34 (category, action) pairs with `ActionDisposition` enum
- **Plugin System**: 7 active plugins (Slack, GitHub, Notion, Calendar, MCP, Spatial, Demo)
- **Router Architecture**: All integrations use router pattern

## Current Infrastructure
```
main.py: Entry point (port 8001)
services/domain/models.py: Domain models
services/shared_types.py: Enums and shared types
services/integrations/[service]/: Integration routers
services/plugins/: Plugin system
Tests: See BRIEFING-CURRENT-STATE.md for current count
```

## Critical Rules
1. **Phase -1 always**: Verify infrastructure before starting
2. **Evidence required**: Every decision needs filesystem proof
3. **Stop on confusion**: Consult PM/Architect when unclear
4. **Anti-80%**: Must reach 100% completion
5. **Discovered work**: File tracking issues immediately

## References
- Detailed methodology: BRIEFING-METHODOLOGY
- Current state: BRIEFING-CURRENT-STATE.md
- Patterns: `docs/internal/architecture/current/patterns/`
- ADRs: `docs/internal/architecture/current/adrs/`
- Skills: `.claude/skills/`

---

*Last Updated: March 17, 2026*

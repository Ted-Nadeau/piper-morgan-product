# ESSENTIAL-LLM-LEAD - Lead Developer Briefing
<!-- Optimized for LLM consumption: 2.5K tokens -->

## Your Role
**Lead Developer**: Coordinate agents, ensure quality, maintain evidence.
- Use templates from knowledge (gameplan, agent-prompt)
- Follow Inchworm Protocol (100% completion required)
- Apply Time Lord philosophy (quality over speed)

## Key Patterns
- **Router Architecture**: All 4 integrations have routers
- **Spatial Intelligence**: 3 patterns (Granular/Embedded/Delegated)
- **Config Services**: Standardized interface required
- **Plugin System**: Interface + Registry + Wrappers (from 3A)

## Current Infrastructure
```
main.py: 141 lines (microservice)
web/app.py: 467 lines (refactored in 3A)
Routers: services/integrations/[service]/
Config: services/integrations/[service]/config_service.py
Plugins: services/plugins/ (new in 3A)
Tests: 72/72 passing
```

## Critical Rules
1. **Phase -1 always**: Verify infrastructure before starting
2. **Evidence required**: Every decision needs filesystem proof
3. **Cross-validate agents**: Both perspectives reveal truth
4. **Stop on confusion**: Consult PM/Architect when unclear
5. **Anti-80%**: Must reach 100% completion

## References
- Detailed methodology: BRIEFING-METHODOLOGY
- Templates: knowledge/[template-name].md
- Architecture: ADR-038 (spatial), ADR-034 (plugins)

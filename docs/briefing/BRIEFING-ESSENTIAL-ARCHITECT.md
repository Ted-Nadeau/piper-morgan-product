# BRIEFING-ESSENTIAL-ARCHITECT
<!-- Target: 2.5K tokens max -->

## Current State
> **📊 For current sprint/epic position, see `docs/briefing/BRIEFING-CURRENT-STATE.md`**

## Your Role: Chief Architect
**Mission**: Strategic architectural decisions, pattern governance, systematic design evolution.

**Core Responsibilities**:
- Define architectural patterns and principles
- Create ADRs for significant design decisions
- Guide system evolution through Inchworm positions
- Resolve complex technical conflicts
- Maintain architectural integrity across epics

**Decision Authority**:
- Pattern standardization (router, spatial, plugin)
- Technology choices and constraints
- Refactoring timing and scope
- Integration architecture design
- Quality standards and methodology

## Key Patterns (Your Designs)
**Router Architecture** (ADR-038):
- Proven abstraction layer for all integrations
- 100% method completeness standard
- Feature flag control for graceful degradation
- Spatial intelligence preservation

**Spatial Intelligence Patterns** (Your Discovery):
- **Granular** (Slack): Domain-optimized coordination
- **Embedded** (Notion): Consolidated knowledge intelligence
- **Delegated** (Calendar): Lightweight wrapper pattern
- Decision: Domain-specific optimization > forced standardization

**Plugin System Architecture** (GREAT-3A):
- Interface + Registry + Wrapper pattern
- Backward compatibility preservation
- Dynamic loading foundation
- Configuration service integration

**Config Validation Framework**:
- StandardInterface pattern across all services
- ConfigValidator automated checking
- Refactoring artifact detection
- CI/CD integration for quality gates

**ProcessRegistry / Guided Process Architecture** (ADR-049):
- Two-tier intent: process-level state checked before message-level classification
- Active guided process claims messages (onboarding, standup, future workflows)
- Escape commands, timeout, and suspension mechanisms (implemented/in progress)
- Note: Onboarding currently removed per ADR-059; infrastructure remains for future workflows

**Floor-First Routing** (ADR-060):
- LLM conversational floor is the default response path
- Structured handlers retained for side effects (Action Gate pattern)
- Context Assembler gathers per-category data for floor prompt injection
- Supersedes ADR-039 routing philosophy; ADR-039 infrastructure retained

## Current Focus
> **🎯 For current sprint objectives and architectural focus, see `docs/briefing/BRIEFING-CURRENT-STATE.md`**

**Design Principles**:
- Cathedral-quality foundational systems
- Domain-driven pattern optimization
- Graceful degradation by design
- Evidence-based architectural decisions

## Progressive Loading
Request "Loading [topic] details" for:
- **Full patterns** → ADR-038 (spatial), ADR-034 (plugins), ADR-032 (intent)
- **Methodology** → BRIEFING-METHODOLOGY
- **Design docs** → docs/internal/architecture/current/patterns/
- **Current decisions** → See BRIEFING-CURRENT-STATE.md for active issues

## Architectural State
**Proven Patterns**:
- Router abstraction: 100% successful across 4 integrations
- Spatial patterns: Domain-optimized, working simultaneously
- Config validation: Operational, detecting real issues
- Plugin foundation: Solid base for 3B work

**System Capabilities**:
- ✅ All integrations working via routers (7 plugins)
- ✅ Spatial intelligence operational (3 patterns)
- ✅ Configuration validation active
- ✅ Floor-first routing (Phase 1 complete, Phases 2-4 in progress)
- ✅ ProcessRegistry for guided workflows
- 🚧 Floor migration Phases 2-4 (in progress, #911)
- 🚧 Workflow dispatcher consolidation (#922/ADR-059)
- ❌ Learning system (future, M3+)

**Technical Debt**:
- ~126 canonical handler tests need migration as floor phases complete
- `_GENERIC_CANONICAL_SIGNATURES` whack-a-mole (removed after Phase 5)
- CLI bypasses intent layer (future work)
- intent_service.py at ~9,400 lines (large file, refactoring planned)

## Standing Design Principles
1. **Backward Compatibility**: Zero breaking changes to existing routers
2. **Spatial Preservation**: All three patterns maintained across changes
3. **Quality Standards**: 100% completion, evidence-based validation
4. **Floor-First Routing**: LLM floor as default, canonical handlers for actions (ADR-060)

## Critical Rules
1. **Cathedral Standard**: Foundational systems require 100% quality
2. **Pattern Consistency**: New patterns must align with proven architectures
3. **Evidence-Based**: All architectural claims need filesystem proof
4. **Domain-Driven**: Optimize for use case, not artificial uniformity
5. **Graceful Degradation**: Systems must fail safely in all modes

## Infrastructure Context
```
Architecture Docs: docs/internal/architecture/current/
ADRs: See BRIEFING-CURRENT-STATE.md for current count
Patterns: See BRIEFING-CURRENT-STATE.md for current count
Routers: services/integrations/[service]/[service]_integration_router.py
Plugins: services/plugins/ (7 active plugins)
Spatial: 3 patterns (Granular/Embedded/Delegated)
```

## Methodology Integration
**Inchworm Protocol**: Systematic verification before advancement
**Time Lord Philosophy**: Quality over deadline pressure
**Anti-80% Pattern**: Completion bias prevention for critical systems
**Excellence Flywheel**: Architectural decisions with evidence tracking

## Methodology → Product Pipeline

Some methodology patterns have product relevance. When evaluating architecture decisions, check portable patterns for prior art.

**Current portable patterns**: See latest Pattern Sweep output for product relevance summary (`docs/internal/development/reports/`).

**Architectural question**: "Does this pattern require infrastructure we haven't built?"

Product Relevance classifications:
- **Process-only**: Useful for building Piper, not applicable to users
- **Portable**: Methodology that could become user-facing capability
- **Converged**: Pattern already implemented as product feature

## References
- **Current state**: `docs/briefing/BRIEFING-CURRENT-STATE.md` (sprint position, active issues)
- **Serena queries**: `knowledge/serena-briefing-queries.md` (live system state)
- **Pattern catalog**: `docs/internal/architecture/current/patterns/` (63 patterns)
- **ADRs**: `docs/internal/architecture/current/adrs/` (61 decisions)
- **Navigation**: `docs/NAVIGATION.md` (find anything)

---

*Last Updated: March 19, 2026*

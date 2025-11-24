# PROJECT.md - Piper Morgan Development

## Repository Information

**CRITICAL**: Always use the correct repository URL:
- **GitHub Repository**: `https://github.com/mediajunkie/piper-morgan-product`
- **Local Directory Name**: `piper-morgan` (legacy naming, but repo is `piper-morgan-product`)
- **NEVER use**: `Codewarrior1988/piper-morgan` (this is a hallucinated URL that has infected docs)

## Vision

Piper Morgan is an intelligent PM assistant that transforms how product managers work with AI agents. By combining spatial intelligence, domain-driven design, and systematic orchestration, Piper becomes a true thought partner who learns and adapts to each PM's unique style and needs.

We're building this with a revolutionary approach: one human PM collaborating with AI agents as the entire development team. This isn't just about building a product - it's about discovering new methods for human-AI excellence.

## Current Mission

We are systematically completing our foundation through The Great Refactor. After discovering that many components reached 75% completion before being abandoned, we've adopted the Inchworm Protocol: complete each piece 100% before moving forward. No exceptions.

**Current Focus**: CORE-GREAT sequence (5 epics) to establish architectural stability
**Timeline**: 7 weeks to solid foundation
**North Star**: When "Create a GitHub issue about X" works end-to-end, we know we've succeeded

## Technical Foundation

**Core Stack**:

- Python 3.11+ with AsyncIO
- FastAPI for web framework
- PostgreSQL with AsyncSession
- Domain-Driven Design architecture

**Key Patterns**:

- Everything through services (no direct DB access)
- Plugin architecture for integrations
- Spatial intelligence (8-dimensional context)
- Intent classification as universal entry
- MCP protocol for agent communication

**File Structure Reality**:

```
main.py             # Primary backend application entry point
web/app.py          # FastAPI web framework (933 lines, refactor at 1000)
services/           # All business logic here
cli/commands/       # Direct command implementations
config/             # PIPER.md and user config
```

## Development Methodology

**Inchworm Protocol** (ADR-035): Sequential completion. Each epic 100% done before next begins.

**Excellence Flywheel**:

1. Verify before assuming
2. Test before claiming done
3. Lock with tests
4. Document decisions

**Evidence-Based Progress**: No "done" without proof. Terminal output, test results, working demos.

## What We've Built (In Order)

1. **Knowledge Base** - RAG system with embeddings (working)

   - Location: `services/knowledge/`, `services/embeddings/`

2. **Intent Classification** - Sophisticated multi-tier system (infrastructure excellent, universality incomplete)

   - Location: `services/intent_service/`
   - ADR-032 for universal entry requirement

3. **Orchestration Engine** - ✅ Fully operational (wired up late Sept 2025)

   - Location: `services/orchestration/engine.py`
   - Disabled line: `# self.query_router = QueryRouter(self.session)`

4. **Query Router** - A/B tested routing with fallbacks (75% complete, disabled)

   - Location: `services/queries/query_router.py`
   - PM-034 implementation incomplete

5. **GitHub Integration** - Issue creation and management (works directly, broken through chat)

   - Location: `services/integrations/github/`

6. **Slack Integration** - Message sending (works directly, not through orchestration)

   - Location: `services/integrations/slack/`

7. **Spatial Intelligence** - 8-dimensional context system (designed, partially implemented)

   - Location: `services/intelligence/spatial/`
   - ADR-013 for MCP + Spatial pattern

8. **Learning System** - Continuous improvement (exists but barely connected)
   - Location: `services/learning/`

## Current State Frank Assessment

**What Works** (~30%):

- Knowledge base uploads and retrieval
- Intent classification infrastructure
- Direct GitHub/Slack operations
- Basic chat interactions

**What's Blocked** (~70%):

- QueryRouter disabled, blocking orchestration
- ~~OrchestrationEngine never initialized~~ ✅ FIXED Sept 2025
- Multiple patterns coexisting (dual repositories, mixed configs)
- CLI bypasses intent classification entirely

**The Pattern**: Most components reached 75% completion, hit a blocker, and were worked around rather than fixed. We're now systematically completing each one.

## Learning Philosophy

Every problem discovered is a gift - we found it now rather than later. We value:

- Diligence over speed
- Completion over features
- Evidence over assumptions
- Learning from every attempt

When something doesn't work as expected, that's exciting - we've learned something new about our system.

## Resources and Navigation

**Navigating Documentation**:
For complete documentation structure, see: **docs/NAVIGATION.md**

**Key Documents**:

- `/docs/architecture/architecture/current/adrs/` - ADRs (currently 36)
- `/docs/planning/roadmap.md` - Current roadmap
- `/docs/briefing/CURRENT-STATE.md` - This doc on the filesystem
- `/docs/briefing/METHODOLOGY.md` - How we work

**Pattern References**:

- Pattern Catalog: `/docs/internal/architecture/current/patterns/README.md`
- Domain Models: `/docs/domain-models-index.md`

**Finding Things**:

```bash
# Find implementation
grep -r "ClassName" . --include="*.py"

# Find patterns
cat docs/internal/architecture/current/patterns/ | grep -A 10 "Pattern Name"

# Check what exists
ls -la services/
ls -la web/
```

## Standards to Maintain

1. **Domain Separation**: Business logic never in controllers
2. **Config Separation**: User config never in system code
3. **Spatial Intelligence**: All plugins must implement
4. **Complete Work**: No TODOs without issue numbers
5. **Evidence Required**: No claims without proof

## Success Indicators

You're succeeding when:

- Your code completes something unfinished
- Your tests lock in that completion
- You find a problem others missed
- You resist adding a workaround
- You take time to do it right

## Remember

"We do these things not because they are easy, but because we thought they would be easy!" 😉

The path is clearer today than it has ever been. We have strong aversion to leaving things unfinished. Every session moves us closer to excellence.

---

_Welcome to the Piper Morgan project. Your contribution matters._

**Document Maintenance**: Updated after each epic completion. See CURRENT-STATE.md for latest status.

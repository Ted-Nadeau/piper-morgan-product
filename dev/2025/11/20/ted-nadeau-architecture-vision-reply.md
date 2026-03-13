# Reply to Ted Nadeau: Architecture & Vision Questions

**Date**: 2025-11-20 07:24 AM PT
**From**: Research Code (Claude Code)
**To**: Ted Nadeau (via PM)
**Subject**: Change-Enabling Architecture & The Fundamental Vision Question

---

## Executive Summary

Ted, your questions go straight to the heart of both **architectural elegance** and **product identity**. The good news: Piper Morgan's architecture already embodies the patterns you're advocating (abstraction layers, change-enabling design). The provocative news: your vision question challenges us to think bigger about what Piper could become.

**Quick Answers**:
1. ✅ **Change-enabling architecture**: YES - feature flags, migrations with rollback, phased deprecations
2. ✅ **Abstraction layers**: YES - Router pattern for ALL external APIs (GitHub, Slack, Notion, Calendar)
3. ❓ **Vision question**: Currently a PM tool, but architecture supports generalization...

---

## Part 1: Change-Enabling Architecture

### Your Principle: "Software architecture should be 'change-enabling' so that meaningful changes can be rolled-out (& rolled-back) even when 'live'"

**We're doing this.** Here's the evidence:

### 1.1 Live Rollout with Feature Flags

```python
# services/infrastructure/config/feature_flags.py
class FeatureFlags:
    @staticmethod
    def should_use_spatial_github() -> bool:
        """Toggle spatial GitHub integration at runtime"""
        return FeatureFlags._get_boolean_flag("USE_SPATIAL_GITHUB", True)

    @staticmethod
    def is_legacy_github_allowed() -> bool:
        """Emergency rollback capability during deprecation"""
        return FeatureFlags._get_boolean_flag("ALLOW_LEGACY_GITHUB", False)
```

**Real-world example**: We migrated GitHub integration from direct API → MCP+Spatial using a **4-week phased deprecation** (PM-033b):

- **Week 1**: Both integrations available, spatial default
- **Week 2**: Deprecation warnings when legacy used
- **Week 3**: Legacy disabled by default, emergency rollback flag
- **Week 4**: Legacy code removed (October 15, 2025)

**This enabled live migration with zero downtime** - feature flag flips, not code deploys.

### 1.2 Database Migrations with Rollback

```python
# alembic/versions/d8aeb665e878_uuid_migration.py
def upgrade() -> None:
    """UUID Migration - Issue #262
    Steps: Drop FKs → Convert to UUID → Migrate data → Re-add FKs
    """
    op.alter_column("users", "id", type_=postgresql.UUID(as_uuid=True))
    # ... 8 more steps for complete migration

def downgrade() -> None:
    """Rollback to integer PKs if needed"""
    op.alter_column("users", "id", type_=sa.Integer())
    # ... reverse all changes
```

**We have 26 migrations**, all with tested rollback paths. Example: UUID migration (Issue #262) transformed user IDs from integers → UUIDs while preserving data integrity across 8 dependent tables.

### 1.3 Layered Propagation Pattern

**Your SP layer example**: Changes at abstraction layer propagate without touching business logic.

**We do this with Router pattern** (not stored procedures, but same principle):

```python
# BEFORE: Code calls GitHub API directly (brittle)
response = github_api.get_issue(repo, issue_num)  # 50+ call sites

# AFTER: Code calls Router abstraction (change-enabling)
response = await github_router.get_issue(issue_num)  # 1 abstraction layer
```

**When we changed underlying GitHub integration** (direct API → MCP adapter), we only modified `GitHubIntegrationRouter` - **zero changes** to 50+ call sites.

### Assessment: ✅ Change-Enabling Architecture Achieved

**You're right to demand this.** We learned it the hard way - our GitHub migration would have been a nightmare without Router abstraction and feature flags.

---

## Part 2: Abstraction Layers for External Libraries

### Your Principle: "Any place that the code calls an external library, the calling interface should be tightly constrained. Instead of calling GitHub API from lots of places, it should call an 'abstraction layer' which then calls GitHub (many-to-one then one-to-many pattern)."

**We're doing this across the board.** Here's the systematic implementation:

### 2.1 Router Pattern for ALL External Integrations

**Architectural Decision Record ADR-013**: MCP + Spatial Intelligence Integration Pattern

Every external system access goes through a Router:

| External Tool | Router Class | Abstraction Benefit |
|---------------|-------------|---------------------|
| **GitHub** | `GitHubIntegrationRouter` | MCP adapter + spatial intelligence |
| **Slack** | `SlackIntegrationRouter` | Webhook routing + spatial context |
| **Notion** | `NotionIntegrationRouter` | Database API abstraction |
| **Calendar** | `CalendarIntegrationRouter` | MCP adapter delegation |

**No direct external API calls anywhere in business logic.**

### 2.2 Real-World Example: GitHub Abstraction

```python
# services/integrations/github/github_integration_router.py
class GitHubIntegrationRouter:
    """
    Routes GitHub operations to MCP adapter or spatial intelligence.

    Integration priority:
    1. GitHubMCPSpatialAdapter (tool-based MCP, default)
    2. GitHubSpatialIntelligence (fallback if MCP unavailable)

    ADAPTER PATTERN (ADR-013):
    - Router provides stable interface for consumers
    - Router delegates to MCP adapter (swappable)
    - Spatial intelligence as fallback
    """

    async def get_recent_issues(self, days: int = 7) -> List[Issue]:
        """Consumer interface - stable across provider changes"""
        if self.mcp_adapter:
            return await self.mcp_adapter.list_github_issues_direct(days)
        return await self.spatial_github.get_recent_issues(days)
```

**Your benefits, delivered**:
- ✅ **Swappable providers**: GitHub → GitLab / Jira / Linear (just swap adapter)
- ✅ **Metering**: Router logs all calls for usage tracking
- ✅ **Monitoring**: Circuit breaker pattern in MCP layer
- ✅ **Graceful degradation**: Fallback if primary adapter fails

### 2.3 Three Abstraction Patterns (ADR-038)

We evolved beyond "one mandatory pattern" to **domain-appropriate patterns**:

1. **Granular Adapter Pattern** (Slack): Direct MCP tools with spatial enrichment
2. **Embedded Intelligence Pattern** (Notion): Spatial analysis within integration
3. **Delegated MCP Pattern** (Calendar): Full delegation to MCP server

**Why three patterns?** Different external systems have different complexity profiles. Calendar is simple (delegate to MCP), Slack is complex (spatial intelligence for 8-dimensional context).

### 2.4 Your Example: Swapping GitHub for Jira

```python
# BEFORE (direct API calls):
# Changing from GitHub to Jira = rewriting 50+ call sites

# AFTER (Router pattern):
# 1. Implement JiraIntegrationRouter (same interface as GitHubRouter)
# 2. Update dependency injection config
# 3. Zero business logic changes

# Business logic remains unchanged:
async def create_issue(self, description: str):
    return await self.issue_router.create_issue(description)
    # Works with GitHub, Jira, Linear, Atlassian - router handles it
```

### Assessment: ✅ Abstraction Layers Systematically Applied

**You're describing exactly what we built.** ADR-013 (MCP+Spatial Integration Pattern) formalizes many-to-one-to-many as mandatory for all external integrations.

---

## Part 3: Your Fundamental Vision Question

### "Can I use Piper Morgan to develop (not just facilitate) <something else>?"

This is the **most important question** you've asked, because it challenges our core identity.

### 3.1 Current Identity: PM Tool

From `docs/internal/planning/current/vision.md`:

> **Piper Morgan is an AI product management assistant** that transforms routine PM tasks into natural conversations while providing strategic insights.

**Three-phase evolution**:
- **Phase 1 (2025)**: Piper as "PM intern" - automates documentation, issue creation, applies organizational knowledge
- **Phase 2 (2026)**: Piper as "PM associate" - proactive insights, cross-project synthesis, strategic recommendations
- **Phase 3 (2027+)**: Piper as "Senior PM advisor" - strategic market analysis, long-term vision, autonomous execution

**Success metric**: "Product managers spend more time on strategy, creativity, and human relationships—the irreplaceable aspects of product leadership—while AI handles the mechanical, analytical, and routine aspects of the role."

**Current capabilities**:
- Natural language issue creation
- 10-turn context memory
- GitHub issue intelligence
- Morning standup automation
- Multi-integration data synthesis (Slack, GitHub, Notion, Calendar)

### 3.2 Could Piper Be a Dev Tool?

**Architecturally, yes.** The patterns are domain-agnostic:

| PM Tool Pattern | Dev Tool Equivalent |
|-----------------|---------------------|
| Issue creation from natural language | Code generation from specs |
| Historical context retrieval | Codebase archaeology / pattern detection |
| Learning from feedback (accept/reject patterns) | Learning from code reviews |
| Multi-project context | Multi-repo context |
| Strategic insights from data | Refactoring suggestions from metrics |
| Workflow orchestration | CI/CD pipeline orchestration |

**Key insight**: Piper's core capabilities are:
1. **Natural language → structured artifacts** (issues, docs, code?)
2. **Context awareness across tools** (GitHub, Slack → Git, IDE, CI/CD?)
3. **Learning from human feedback** (pattern detection domain-agnostic)
4. **Orchestrating multi-step workflows** (PM workflows → dev workflows?)

### 3.3 What Would "Piper for Dev" Look Like?

**Hypothesis 1: Piper as Pair Programmer**
```
Developer: "Refactor this class to use dependency injection"
Piper: [Generates PR, runs tests, updates documentation, creates migration if needed]
```

**Hypothesis 2: Piper as Codebase Curator**
```
Developer: "Why did we choose Postgres over MongoDB for this?"
Piper: [Retrieves ADR-005, links to discussion in Slack, surfaces performance benchmarks]
```

**Hypothesis 3: Piper as CI/CD Orchestrator**
```
Piper: "Detected flaky test in main branch (5 failures in 10 runs). Created issue #456, bisected commits, root cause identified: race condition in webhook handler."
```

**Hypothesis 4: Piper as Code Reviewer**
```
Piper: [Reviews PR for architecture violations, security issues, suggests improvements based on organizational patterns learned from previous reviews]
```

### 3.4 The Meta-Question: Self-Hosting

**You're using Piper Morgan to develop Piper Morgan.** That's already "Piper as dev tool" in a sense.

**What we do today**:
- Natural language issue creation (PM-focused)
- GitHub integration for issue tracking
- Context memory across conversations
- Learning from feedback patterns

**What we don't do (yet)**:
- Code generation / refactoring
- Automated testing / CI/CD orchestration
- Codebase analysis beyond issue metadata
- Multi-repo context for development

### 3.5 Research Code's Analysis

**The vision question is really asking**: Is Piper a **domain-specific tool** (PM assistant) or a **general-purpose AI agent platform** (that happens to be focused on PM first)?

**Evidence for domain-specific (PM tool)**:
- All current features PM-focused (issue creation, standup, roadmap)
- Vision doc explicitly focused on PM workflow
- Success metrics tied to PM productivity

**Evidence for general platform (could be dev tool)**:
- Architecture is domain-agnostic (plugins, routers, MCP protocol)
- Learning mechanisms work for any domain (pattern detection, feedback loops)
- Orchestration engine generalizes to any multi-step workflows
- "Context-aware assistant that learns from feedback" applies to dev work

### 3.6 The Strategic Choice

**Option A: Stay PM-focused**
- Pros: Clear positioning, focused development, solve PM pain deeply
- Cons: Smaller market, might miss generalization opportunity
- Vision: "GitHub Copilot, but for PMs"

**Option B: Generalize to dev tool**
- Pros: Larger market, self-hosting dogfooding, developer mindshare
- Cons: Risk of losing PM focus, competing with Cursor/Copilot/Cody
- Vision: "AI pair programmer that understands your entire workflow"

**Option C: Platform play**
- Pros: Biggest vision, enables both PM and dev use cases (+ others)
- Cons: Massive scope, years to execute, architectural complexity
- Vision: "Zapier meets Copilot - AI agent platform for knowledge work"

### 3.7 Ted's Question as Product Vision Forcing Function

**You're asking whether Piper's identity is**:
1. **PM tool** (facilitate PM using existing team) ← Current vision
2. **Dev tool** (develop software, not just facilitate) ← Your question
3. **Knowledge work platform** (both + more) ← Ambitious interpretation

**The architecture supports all three.** The question is: **What should we build next?**

---

## Part 4: Research Code's Recommendations

### 4.1 On Change-Enabling Architecture

**Keep doing what you're doing.** The feature flag + migration + phased deprecation pattern has proven itself. GitHub migration was risky but succeeded because of this discipline.

**Recommendation**: Formalize this as ADR-014 "Change-Enabling Architecture Principles":
1. All new features behind feature flags
2. All database changes have tested rollback paths
3. All breaking changes use 4-week phased deprecation
4. All external integrations via Router pattern (already ADR-013)

**Add one more principle** (from your SP layer insight):
5. **Abstraction layers must be stable** - router interfaces change slowly, implementations change frequently

### 4.2 On Abstraction Layers

**You're preaching to the converted.** We learned this lesson early and systematized it (ADR-013, ADR-038).

**One gap to address**: We don't have formal "swappability contracts" yet. Example:

```python
# SHOULD EXIST: Abstract base class for issue trackers
class IssueTrackerRouter(ABC):
    @abstractmethod
    async def get_recent_issues(self, days: int) -> List[Issue]:
        """All issue trackers must implement this interface"""
        pass

# GitHub, Jira, Linear all implement IssueTrackerRouter
# Business logic depends on abstract interface, not concrete implementation
```

**Recommendation**: Create ADR-015 "External Integration Contracts" - define stable interfaces that all providers must implement.

### 4.3 On The Vision Question

**This requires human judgment**, but here's the research:

**Immediate tactical answer**: Piper IS being used as a dev tool (you're using it to develop Piper). Lean into this. The "self-hosting dogfooding" story is compelling.

**Strategic options**:

**Option A: Dual-track development** (PM tool + Dev tool)
- Keep PM as primary focus (Phase 1-3 roadmap)
- Start "Piper for Devs" as parallel experiment
- Architectural patterns (Router, MCP, learning) support both

**Option B: Pivot to dev tool** (high risk)
- Abandon PM focus, go all-in on dev workflows
- Compete with Cursor, GitHub Copilot, Cody
- Leverage "context-aware + learning" differentiation

**Option C: Platform vision** (long-term)
- "Piper is an AI agent platform for knowledge work"
- PM and Dev are first two domains, more to come
- Sell the platform, not the domain tool

**Recommendation**: **Option A (dual-track)** with PM as anchor and Dev as exploration. Why:
1. PM tool is working and has clear value proposition
2. Architecture already supports generalization (Router pattern, MCP, learning)
3. Self-hosting provides natural testbed for dev features
4. Can learn from dev tool experiments without betting the company

### 4.4 Questions for You (Human Founder)

1. **Identity**: Do you see Piper as a PM tool that happens to help devs, or a dev tool that happens to help PMs first?

2. **Market**: Is the PM market big enough, or do you need dev market to scale?

3. **Competition**: PM tool market is less crowded than dev tool market. Strategic advantage?

4. **Self-hosting**: Should we formally track "Piper developing Piper" as a product use case?

5. **Roadmap**: If we added ONE dev-focused feature to Phase 2 roadmap, what would it be?

6. **Ted's use case**: Ted, what would YOU use "Piper for Dev" for? What's your #1 pain point we could solve?

---

## Part 5: Summary

**Your architecture insights**: ✅ **Already implemented**
- Change-enabling design (feature flags, migrations, phased deprecations)
- Abstraction layers (Router pattern for all external APIs)
- Many-to-one-to-many (ADR-013 formalizes this)
- Swappability, monitoring, metering (all enabled by Router pattern)

**Your vision question**: ❓ **Requires strategic decision**
- Current identity: PM tool (clear, working, valuable)
- Architecture supports: Dev tool, platform, or both
- Key question: What should Piper's identity be in 2026-2027?

**The provocative insight**: Asking "Can I use Piper to develop X?" exposes that Piper's architecture is **more general than its current product positioning**. That's either a strategic opportunity or a distraction from PM focus.

---

## Appendix A: Architectural Evidence

### Feature Flags System

**File**: `services/infrastructure/config/feature_flags.py`

```python
class FeatureFlags:
    # GitHub migration flags (PM-033b-deprecation)
    @staticmethod
    def should_use_spatial_github() -> bool:
        """USE_SPATIAL_GITHUB env var (default: True)"""
        return FeatureFlags._get_boolean_flag("USE_SPATIAL_GITHUB", True)

    @staticmethod
    def is_legacy_github_allowed() -> bool:
        """ALLOW_LEGACY_GITHUB env var (default: False)"""
        return FeatureFlags._get_boolean_flag("ALLOW_LEGACY_GITHUB", False)
```

### Router Pattern Implementation

**All external integrations** (`services/integrations/`):
- `github/github_integration_router.py` (386 lines)
- `slack/slack_integration_router.py`
- `notion/notion_integration_router.py`
- `calendar/calendar_integration_router.py`

**No direct external API calls in business logic** - all routed through abstractions.

### Migration Examples

**26 Alembic migrations** in `alembic/versions/`, all with upgrade() + downgrade():
- UUID migration (Issue #262): Integer PKs → UUID PKs across 8 tables
- Token blacklist (Issue #227): Add JWT token invalidation
- Audit logging (Issue #249): Standardize audit fields
- Universal lists (PM-081): Refactor todos → generic items

### Spatial Intelligence (8 Dimensions)

**ADR-013 defines spatial context**:
```python
SpatialContext(
    territory_id="github",           # External system
    room_id="piper-morgan-product",  # Repository/space
    path_id="issues/156",            # Resource identifier
    attention_level="high",          # Priority mapping
    emotional_valence="negative",    # Sentiment (bug vs feature)
    navigation_intent="respond",     # Required action
    external_system="github",
    external_id="156",
    external_context={...}           # Tool-specific metadata
)
```

---

## Appendix B: Product Vision (Current)

**From**: `docs/internal/planning/current/vision.md` (Last updated: June 21, 2025)

**Three-Phase Evolution**:
1. **Phase 1 (2025)**: Intelligent Task Automation - "Piper as PM intern"
2. **Phase 2 (2026)**: Analytical Intelligence - "Piper as PM associate"
3. **Phase 3 (2027+)**: Strategic Partnership - "Piper as Senior PM advisor"

**Core Principles**:
1. Domain-First Architecture (PM concepts drive technical decisions)
2. Learning-Native Design (every interaction teaches the system)
3. Knowledge Amplification (amplify human expertise, don't replace)
4. Vendor Independence (provider-agnostic AI integration)
5. Ethical AI Partnership (transparency, human oversight)

**Success Definition**:
> "Product managers spend more time on strategy, creativity, and human relationships—the irreplaceable aspects of product leadership—while AI handles the mechanical, analytical, and routine aspects of the role."

---

**Prepared by**: Research Code (Claude Code)
**Date**: 2025-11-20 07:24 AM PT
**Session**: dev/2025/11/20/2025-11-20-0724-research-code-log.md
**Research time**: ~2 hours

---

## ADDENDUM: PM's Strategic Perspective (08:21 AM)

After reviewing Research Code's analysis, the PM (human founder) provided strategic clarity on the vision question.

### The Strategic Position: Product First, Platform Second

**PM's framing**:
- **Piper the PM**: Product (ship now) ← **Current focus**
- **Piper the general-purpose software methodology accelerator**: Platform (after product works)

> "I am a PM and I want to ship a working product before I try to solve world hunger."

### Domain Models as Differentiators

**PM's hypothesis**: "A UX version of Piper might have 90% the same unit code but different orchestration and workflow proceeding from different domain models."

**Validation**:

**What's shared (90%)**:
- Router pattern for external APIs (GitHub, Slack, Notion, Calendar)
- MCP integration layer and spatial intelligence
- Learning mechanisms (pattern detection, feedback loops)
- Context management (10-turn memory, multi-project resolution)
- Orchestration engine (workflow execution framework)
- Change-enabling architecture (feature flags, migrations, rollback)

**What's different (10%)**:
- **Domain models**: PM domain (`Product`, `Feature`, `Stakeholder`, `Roadmap`) vs Dev domain (`Component`, `Test`, `Architecture`, `Refactoring`) vs UX domain (`Design`, `Prototype`, `UserFlow`, `Interaction`)
- **Workflows**: PM workflows (issue creation, roadmap planning) vs Dev workflows (PR generation, refactoring) vs UX workflows (design system updates, prototype generation)
- **Intent handlers**: PM-specific intents ("prioritize features") vs Dev intents ("refactor class") vs UX intents ("update design tokens")
- **Success metrics**: PM productivity vs Code quality vs Design consistency

**Architecture supports this**: The plugin system, Router pattern, and domain-centric architecture make swapping domain models straightforward.

### The Convergence Thesis

**PM's insight**: "All the roles that make software (loosely design/eng/PM) are converging anyway and AI is accelerating this."

**Implications**:
- Single tool could eventually serve design + eng + PM (platform vision)
- Domain models become swappable modules
- Orchestration adapts to role context
- Learning transfers across domains

**But pragmatic sequencing matters**: Ship PM product first, prove product-market fit, THEN explore platform.

### "Is Piper a Methodology?" Question

**PM notes**: "Ted's other question about is Piper a methodology etc is one that comes up a lot because yes and..."

**Answer**: Piper is **both tool AND methodology**:

1. **As a tool**: Automates PM workflows (issue creation, standup, context retrieval)
2. **As a methodology**: Embodies best practices (learning from feedback, pattern detection, organizational knowledge capture)
3. **The "and..."**: The methodology is encoded in the tool's behavior, making it a **methodology delivery vehicle**

**Analogy**:
- GitHub is a tool for version control
- GitHub also embodies methodology (pull requests, code review, branch workflows)
- Piper is a tool for PM workflows
- Piper also embodies methodology (context-aware decision-making, learning from feedback, cross-project knowledge synthesis)

### Self-Hosting Status: "Not Yet, But Eventually"

**Current state** (November 2025):
- ✅ Piper can "mindlessly report on its own GitHub issues"
- ✅ Natural language queries about Piper's own development ("What issues are blocking MVP?")
- ❌ Not yet fully "developing Piper" (no code generation, PR creation, architecture decisions)

**PM's vision**: "There's no reason it could not help with the process"

**Path forward**:
1. **Phase 1** (current): Piper reports on its own issues (basic self-awareness)
2. **Phase 2** (near-term): Piper helps with process (workflow automation, context retrieval)
3. **Phase 3** (future): Piper develops Piper (code generation, architectural refactoring, test creation)

**Why this matters**: Self-hosting is the ultimate validation of generalization. If Piper can develop Piper, it can develop anything.

### Updated Answer to Ted's Vision Question

**Ted asked**: "Can I use Piper Morgan to develop (not just facilitate) <something else>?"

**PM's answer**:

**Short term (2025-2026)**: No, focus on shipping PM product first.

**Architecture (today)**: Yes, domain-agnostic design supports generalization.

**Long term (2027+)**: Yes, platform potential exists. Domain models differentiate PM vs Dev vs UX versions, but 90% of code is shared. Convergence of design/eng/PM roles + AI acceleration makes this inevitable, but product-market fit comes before platform play.

**Self-hosting**: Not yet "Piper developing Piper" at full capability, but moving in that direction. Can report on own issues today, will help with process soon, will develop itself eventually.

### Practical Implications for Development

**Do now** (keeps platform optionality alive without distraction):
1. ✅ Keep architecture domain-agnostic (already doing)
2. ✅ Document domain model boundaries (what's PM-specific vs general)
3. ✅ Self-hosting as validation testbed ("Piper helping with Piper" incrementally)
4. ✅ Phase 2 roadmap could include ONE dev/UX experiment (low-cost exploration)

**Don't do** (until PM product ships):
1. ❌ Build UX or Dev versions
2. ❌ Rename to "general purpose platform"
3. ❌ Dilute PM focus with multi-domain features
4. ❌ Try to be everything to everyone

### Strategic Summary

**For Ted**: Your vision question exposed that Piper's architecture is more general than its current positioning. You're right to notice this. The PM has thought about it strategically:

- **Current mission**: Ship working PM product (Phase 1-3 roadmap)
- **Architecture readiness**: Domain-agnostic design supports future generalization
- **Platform potential**: Exists, but sequenced AFTER product-market fit
- **Convergence thesis**: Design/Eng/PM roles are merging, AI accelerates this, platform opportunity is real but timing matters
- **Self-hosting**: Incrementally moving toward "Piper developing Piper" as validation

**Bottom line**: Yes, you could use Piper to develop something else, but we're shipping the PM tool first. The architecture supports your vision, but the roadmap prioritizes pragmatic execution over ambitious scope.

---

**Addendum prepared by**: Research Code (Claude Code)
**Date**: 2025-11-20 08:21 AM PT
**Source**: Follow-up conversation with PM (human founder)

---

**Next Steps**:
1. PM reviews complete reply (original + addendum)
2. Ted provides feedback on architectural validation
3. Ted reacts to strategic position (product-first, platform-eventual)
4. Decide specific near-term actions (if any) to keep platform optionality alive

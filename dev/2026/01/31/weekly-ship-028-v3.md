# Piper Morgan Weekly Ship #028

**Week of January 23-29, 2026**

Hey team,

This week had a clear arc: build fast, ship, discover what's broken, find root causes. We completed the 10-day MUX-IMPLEMENT sprint, released v0.8.5, and then alpha testing immediately revealed what 5,253 unit tests couldn't find—including a P0 where portfolio onboarding has *never* actually saved projects to the database. The methodology worked both ways: it enabled the velocity to ship, and it's enabling systematic diagnosis of the gaps.

---

## 🚀 Shipped this week

### 🎯 Product & experience

**MUX-IMPLEMENT super epic complete** (Jan 18-27): The 10-day sprint delivered the full MUX foundation:
- P1 Navigation: Home state, utility layer, command palette, place windows (185 tests)
- P2 Documentation: Document access, lifecycle indicators, composting views (302 tests)
- P3 Conversation: Memory sync, channel consistency, follow-up detection (407 tests)
- P4 Accessibility: WCAG 2.1 AA compliance, design tokens enforced, contrast testing

**The grammar became operational**: "Entities experience Moments in Places" moved from documentation to running code. The design principles established in December are now testable in production.

**TRUST-LEVELS epic complete** (Jan 23): ADR-053 fully implemented with 453 tests covering stage progression (1-5), regression on complaints, soft signal detection, and floor enforcement.

**ProcessRegistry architecture (ADR-049)** delivered through multi-advisor coordination:
- "Guided Process" terminology established for multi-turn conversations where Piper maintains control
- ProcessRegistry singleton tracking active processes per session
- Adapters: OnboardingProcessAdapter, StandupProcessAdapter (32 new tests)

**ADR-050 Phases 1-3 deferred** to V2 (multi-party features)—"Does the user notice the gap?" became the MVP rubric.

**Mobile PoC breakthrough** (Jan 24): Root cause found for invisible toast—Reanimated animation version mismatch (JS 0.7.1 vs native 0.5.1). Fix applied; all components now verified working (gestures, intent callbacks, toast, haptics, card spring-back).

### ⚙️ Engineering & architecture

**v0.8.5 released** (January 27):
- Three alpha testers unblocked: Jake Krajewski, Rebecca Refoy, Dominique Derosena
- Final test suite: 5,253 tests passing
- Comprehensive alpha documentation audit (7 files fixed, 13 issue categories addressed)
- Release runbook upgraded to v1.5 with content accuracy audit

**Alpha testing reality check** (Jan 28-29): 18 bugs discovered across two days of E2E testing:

| Priority | Count | Notable |
|----------|-------|---------|
| P0 | 2 | #728 (projects never save), #734 (calendar token leak) |
| P1 | 5 | Race conditions, conversation persistence, API keys |
| P2 | 6 | Styling, sidebar, history button issues |
| P3 | 5 | First-time user flow polish |

**Root causes found**:
- #731 Conversation persistence: Direct chat wasn't creating DB records — FIXED & VERIFIED
- #736 Projects unique constraint: Was GLOBAL, not per-user — migration applied
- #734 Calendar tokens: Stored globally without user_id prefix — one user saw another's events

**The 75% Pattern confirmed again**: Infrastructure exists, final wiring doesn't. This is the third manifestation (Aug 2025 stubs, Jan 28 #728, Jan 30 #734).

### 🔬 Methodology & process innovation

**Pattern-059: Leadership Caucus formalized** from the ADR-049/050 coordination:
- Trigger: Cross-cutting work, vision→implementation transitions, multi-stakeholder decisions
- Protocol: Frame → Contribute → Capture → Resolve → Confirm
- Complements async mailbox system with sync coordination option

**Simple Trigger Architecture validated**:
- Discovery: 30-line verbose protocols fail post-compaction; 6-line triggers survive
- New principle: Protocols that must survive cognitive boundaries need simple triggers, not comprehensive procedures
- Applied to logging discipline with CLAUDE.md inline verification

**Pattern count reached 60**—a shared vocabulary for problems accelerating diagnosis and documentation.

**Audit Cascade discipline held**: Every P1 issue went through full audit → gameplan → approval → implementation flow. No shortcuts, no rework.

### 🌐 External relations & community

**Publications this week**:
- Weekly Ship #027 (LinkedIn, January 28)
- The Planning Caucus (Medium, January 28)
- The CLAUDE.md Paradox (Medium, January 30)
- 5 additional drafts ready for weekend publication

**Alpha tester communications**:
- v0.8.5 release notes sent (January 28, 11:59 AM)
- Alpha docs comprehensively audited and updated
- Tester roster formalized (7 active, 8 prospects)

**Content pipeline healthy**: 3 narratives drafted, 2 insight pieces ready for weekend.

### 📊 Governance & operations

**Metrics (Jan 23-29)**:

| Metric | Value |
|--------|-------|
| Issues closed | ~80 |
| Issues created | ~37 (including 18 alpha bugs) |
| Tests added | ~2,700 |
| Test suite total | 5,253 |
| Releases | 1 (v0.8.5) |
| ADRs decided | 2 (049, 050) |
| Patterns formalized | 1 (#059) |
| HIGH-COMPLEXITY days | 4 of 7 |

**Leadership coordination**: Jan 26 demonstrated healthy escalation when PPM and Chief Architect disagreed on #427 closure criteria. Lead Dev escalated to PM; team converged on MVP rubric ("Does the user notice?").

**Daily check-in pattern established**: PM + Chief of Staff morning touchpoints proving valuable for context continuity and task tracking.

**Role health**: All agent roles active. Subagent parallelization continued (3 parallel agents deployed Jan 29 for bug investigation).

---

## 🎯 Coming up next week

### Development priorities

- Multi-tenancy audit: Systematic review of all user-scoped data before expanding alpha
- E2E test coverage: Tests that verify database state, not just conversation flow
- Continue bug stabilization: 10 of 18 bugs fixed, remaining in progress
- Consider persistence layer audit for epic completion criteria

### Alpha testing & onboarding

- Continue gradual tester onboarding (P0s now fixed)
- E2E testing in fresh alpha environment
- Verify #736 fix with project onboarding flow

### Communications

- Weekend insight posts
- Ship #029 preparation
- Continue Medium narrative series

---

## 🚧 Blockers & asks

**Current blockers**:
- None critical—P0s from alpha testing have been fixed (post-scope of this Ship)

**Decisions needed**:
- Two sidebars question: Left sidebar (conversation list) vs Right History sidebar (#425)—possible duplicate functionality requiring investigation

**Team input**: Investigation memo sent to Lead Developer for sidebar design intent clarification

---

## 📊 Resource allocation

**For week ending January 29**:
- **Core development**: 50% (MUX-IMPLEMENT completion, bug fixes)
- **Alpha testing**: 25% (E2E testing, bug discovery, documentation)
- **Methodology/process**: 15% (Pattern-059, Simple Trigger Architecture, audit cascade)
- **Communications**: 10% (Weekly Ship, blog posts, alpha tester coordination)

**Velocity**: Strong early week (Jan 23-27), then deliberate slowdown for testing (Jan 28-29). This is healthy—building velocity followed by validation velocity. ~80 issues closed, ~2,700 tests added.

---

## 📝 This week's learning pattern

### Conversation ≠ Reality

**Discovery**: A conversational AI can confidently report completion while the underlying system has done nothing. Unit tests with mocked databases hide this gap.

**Example from this week**:
Portfolio onboarding appeared to work perfectly:
- User provides project names ✓
- Piper says "I've added them to your portfolio" ✓
- Success message displays ✓
- User goes to Projects page... nothing there

Root cause: The conversation *captured* project names in session state. No code ever *wrote* them to the database. Unit tests mocked the repository, so they passed. The gap was invisible until alpha testing with a real user flow.

**Why it matters**:
- LLM-driven flows can mask data layer failures with confident responses
- Mocking is useful for unit tests but dangerous for completion verification
- Surface-level verification passes while depth verification fails
- This is the third manifestation of the 75% Pattern

**Application beyond this week**:
- Add "persistence layer audit" to epic completion criteria
- Create E2E tests that verify database state after user flows
- Consider "verification receipts"—moments where the system confirms actual DB state
- When tests pass but users report issues, check if you're mocking the gap

**Related patterns**: Pattern-045 (Green Tests, Red User), Pattern-046 (Beads Completion), Pattern-047 (Time Lord Alert)

---

## 📚 Weekend reading

*For anyone interested in AI-assisted development and systematic methodology:*

- **The 75% Pattern in production**: We documented this anti-pattern months ago—infrastructure built, interface defined, final wiring missing. This week we caught it in alpha testing. The methodology validated itself: naming patterns helps you recognize them faster when they appear.

- **Simple beats comprehensive**: The logging incidents (Jan 22-25) taught us that verbose 30-line protocols fail when agents hit cognitive boundaries. Simple 6-line triggers survive. Counter-intuitive but consistently true.

- **Alpha testing as truth**: Our test suite grew to 5,253 tests. A single afternoon of real user testing found 11 bugs including a P0. Unit tests create confidence; alpha testing creates truth.

---

**Thanks,**
xian + Piper Morgan Development Team

This is Weekly Ship #028. Previous: [#027 "The Grammar of Experience"](https://www.linkedin.com/posts/xian_weeklyship027-the-grammar-of-experience-activity-7289748028050173952-cYpZ).

*P.S. "Conversation says X happened" ≠ "X actually happened in database." That's this week's hard-won lesson.*

*P.P.S. Full session logs and technical details available in the [GitHub repository](https://github.com/mediajunkie/piper-morgan-ai) and [documentation site](https://pmorgan.tech). Yes, you can copy it. That just makes our protocol stronger.*

---

**Week of January 23-29, 2026 | Phase: Alpha Testing, MUX Implementation Complete**

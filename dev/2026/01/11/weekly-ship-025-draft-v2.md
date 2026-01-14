# Weekly Ship #025: The Milestone Week

**Week of January 2 - January 8, 2026**

Two major milestones this week: Stage 3 (ALPHA Foundation) closed on Sunday, and Epic #242 (Interactive Standup) shipped to production on Wednesday. Between them, the B1 sprint launched with eight quick wins completed and a comprehensive UX documentation reorganization. The foundation is solid; now we're building the features that make Piper feel like a colleague.

---

## 🚀 Shipped this week

### Engineering & architecture

**Stage 3 (ALPHA Foundation) complete** (Jan 5)
- All beads closed, DOC-SURVEY complete
- Quarterly maintenance workflow activated via GitHub Actions
- Inchworm advances from Item 3 → Item 4 (Complete build of MVP)

**Epic #242 (CONV-MCP-STANDUP-INTERACTIVE) complete** (Jan 8)
- 5 sequential sub-issues implemented: State Management, Conversation Flow, Chat Widget, Preference Learning, Performance & Reliability
- 260+ new tests across the standup module
- ~5,800 lines of code delivered
- Floating chat widget with expand/collapse, site-wide integration (17 templates)
- Preference learning system with 5 categories and feedback loop
- Performance optimized to <500ms P95 response time

**Three production releases**
- v0.8.3 (Jan 2): Alpha milestone release
- v0.8.3.1 (Jan 7): B1 sprint fixes
- v0.8.3.2 (Jan 8): Interactive standup feature

**B1 sprint execution** (Jan 6-8)
- FTUX-PIPER-INTRO: Piper greeting added to setup wizard ✅
- FTUX-EMPTY-STATES: Voice guide templates in empty states ✅
- FTUX-POST-SETUP: Post-setup orientation added ✅
- FTUX-QUICK-2: Better defaults for GitHub issue creation ✅
- FTUX-QUICK-3: Calendar context in focus guidance ✅
- FTUX-CHAT-BRIDGE: 'Ask Piper' button in empty states ✅
- FTUX-CONCIERGE: Capability discovery system ✅
- CONV-UX-GREET: Calendar scanning on greeting ✅

**Sprint A12 wrap-up** (Jan 3)
- 5 integration issues completed (#537, #539-541, #528)
- 62 tests passing across OAuth and settings pages
- Issue #484 (ARCH-SCHEMA-VALID): Schema validation safeguard prevents "Green Tests, Red User" pattern at database level

**Architecture milestone** (Jan 4)
- Issue #322 (ARCH-FIX-SINGLETON) complete: ServiceContainer singleton removed
- Enables horizontal scaling for production
- ADR-048 documents the lifecycle pattern
- 404+ tests passing with zero regressions

---

## 📚 Methodology & process innovation

### Lead Developer process improvements

Subagent discipline enhanced: deployed agents now keep strict logs, and we've been rigorous about issue, gameplan, and prompt template audits before proceeding. Results have been very good.

### Role onboarding

- HOSR (Head of Sapient Resources) onboarded Jan 5
- CIO (Chief Innovation Officer) onboarded Jan 5
- Chief Architect context handoff successful after 4+ months

### Pattern Sweep 2.0 results applied

The two TRUE EMERGENCE patterns from December's sweep (Pattern-046 Beads, Pattern-047 Time Lord Alert) are now actively informing sprint execution. The Pattern Amnesia anti-pattern discovery is shaping how we build pattern checkpoints into planning templates.

---

## 🌐 External relations & community

**Newsletter steady state** (736 subscribers)

**Medium posts published:**

- Jan 2: "[When Users Can't Discover](https://medium.com/building-piper-morgan/when-users-cant-discover-267268cae81a)" — narrative covering Dec 20-23
- Jan 3: "[Reactive vs. Systematic: A Tale of Two Approaches](https://medium.com/building-piper-morgan/reactive-vs-systematic-a-tale-of-two-approaches-322deab549ff)" — insight from Nov 18
- Jan 4: "[External Validation as Decision Catalyst](https://medium.com/building-piper-morgan/external-validation-as-decision-catalyst-d584d26511f5)" — insight from Nov 19-20
- Jan 5: "[The Capability Sprint](https://medium.com/building-piper-morgan/the-capability-sprint-8933b6228780)" — narrative covering Dec 24-28
- Jan 8: "[The New Year Build](https://medium.com/building-piper-morgan/the-new-year-build-d6ede16a45e6)" — narrative covering Dec 31 - Jan 1

[IMAGE: The Capability Sprint narrative post illustration - PLACEHOLDER]

**LinkedIn newsletter:**

- Jan 1: Weekly Ship #024 "Consolidation"

---

## 🏛️ Governance & operations

**Weekly Ship #024 published** (Jan 1)
- Covered Dec 26-Jan 1 consolidation period
- Documented Pattern Sweep 2.0 results and Pattern Amnesia discovery

**Documentation reorganization** (Jan 8)
- 37 files consolidated across 5 categories (specs, briefs, research, mux, audits)
- Design System front door created: `docs/internal/design/README.md`
- PDR directory established: `docs/internal/pdr/`
- Design Philosophy v1.0 approved with CXO

**Developer onboarding**
- Ted Nadeau UX onboarding guide created
- AI context document for external tools (ChatGPT, Cursor)

**Alpha testing**
- Lasko onboarded Jan 2 with v0.8.3
- Self-testing revealed needs driving B1 work

---

## 🎯 Coming up next week

### Development priorities

- Continue B1 sprint: CONV-UX-PERSIST, remaining items
- SLACK-ATTENTION-DECAY scope assessment
- Integration test coverage expansion

### Content & learning

- Insight post on integration testing philosophy
- Ship #026 preparation

### Team collaboration

- Ted Nadeau architectural sync for PDR-101
- Alpha tester check-ins

---

## 🚧 Blockers & asks

**Current blockers:** None

**Decisions needed:**
- SLACK-ATTENTION-DECAY scope (Lead Dev recommends remove from B1—4-6 month scope)
- MUX-INTERACT-TRUST-LEVELS timing (no spec yet, defer to MUX epic?)

**Team input:** None required

---

## 📊 Resource allocation

**For week ending January 8:**

- **Core development:** 55% (Epic #242, B1 sprint, architecture fixes)
- **Methodology/process:** 15% (Role onboarding, pattern application)
- **Documentation:** 20% (Design system, Ted onboarding, omnibus synthesis)
- **Strategic planning:** 10% (PDRs, roadmap alignment)

**Velocity:** High. Two major milestones (Stage 3, Epic #242) plus B1 sprint execution. Sustainable but intensive.

---

## 📖 Weekend reading

*For anyone interested in AI-assisted development:*

- **[Claude Cognitive](https://github.com/GMaN1911/claude-cognitive)** — A working memory system for Claude Code with attention-based file injection (HOT/WARM/COLD decay) and multi-instance state sharing. We evaluated this for our multi-agent workflow but found we'd already addressed similar needs through our template and logging improvements. Still, if you're running Claude Code on a large codebase, worth investigating. ([HN discussion](https://news.ycombinator.com/item?id=46438814))

- **[Boris Cherny on Claude Code workflows](https://www.threads.com/@boris_cherny/post/DTBVnkiEpLm)** — The creator of Claude Code shares his setup including Slack MCP integration, custom hooks, and subagent organization. Power user territory, but instructive for anyone building Claude Code into their development process.

- **[One GPU vs 720: How Dreaming Beats Memorizing in AI](https://medium.com/@aedelon/one-gpu-vs-720-how-dreaming-beats-memorizing-in-ai-d62d837bf4c2)** — An argument for world-model approaches over brute-force memorization. Interesting parallel to our spatial intelligence work—first time we've seen "dreaming" used as a model outside our own project.

---

## 📝 This week's learning pattern

### Milestone momentum

**Discovery:** Completing a major milestone creates compound momentum—not just the direct benefit of the work done, but the psychological and organizational clarity that follows.

**Example from this week:** Stage 3 (ALPHA Foundation) closed on January 5. This wasn't just a checkbox—it was 3+ months of foundation work reaching a defined endpoint. The effect on the team was immediate:

- B1 sprint launched the next day with clear scope
- Eight quick wins completed in three days
- Epic #242 went from "in progress" to "production" in 72 hours
- Documentation reorganization that had been deferred finally happened

The milestone didn't *cause* this velocity, but it created the conditions for it. When the foundation is explicitly "done," energy shifts naturally from "are we ready?" to "what's next?"

**Why it matters:**
- Milestones aren't just tracking mechanisms—they're psychological inflection points
- "Done" creates permission to move forward that "mostly done" doesn't
- The discipline of closing (all beads, all docs, explicit declaration) pays dividends in subsequent sprints

**Application beyond this week:**
If you're stuck in a long slog, consider whether you've been avoiding the work of *declaring completion*. Sometimes the meta-work of closing out a phase is exactly what's needed to unlock the next one.

**Related patterns:** Beads Discipline (Pattern-046), Time Lord Alert (Pattern-047), Excellence Flywheel

---

**Thanks,**
xian + Piper Morgan Development Team

*P.S. Full session logs and technical details available in the [GitHub repository](https://github.com/mediajunkie/piper-morgan).*

---

**Building in public:** 736 LinkedIn newsletter subscribers | Weekly Ships + Insight Posts
**Recent posts:** "When Users Can't Discover" (Jan 2), "The Capability Sprint" (Jan 5), "The New Year Build" (Jan 8)

---

*Week of January 2-8, 2026 / Alpha testing*

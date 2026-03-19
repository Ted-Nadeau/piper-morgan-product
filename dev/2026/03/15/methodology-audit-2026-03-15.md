# Methodology Audit: February–March 2026

**Conducted by**: Chief Innovation Officer
**Date**: March 15, 2026
**Period under review**: February 3 – March 14, 2026 (6 weeks)
**Previous audit**: CIO founding onboarding, January 4-5, 2026
**Scheduled date**: March 3, 2026 (12 days overdue — see Section 4)
**Next scheduled**: April 6, 2026 (Week 14 per staggered calendar)
**Distribution**: Full leadership team

---

## Executive Summary

The methodology is working. The Excellence Flywheel produced its most dramatic result (M0 sprint: 13-22 day estimate completed in 3 days). Multi-agent coordination matured from informal practice to formal governance (spec pipeline, roundtable). Two new methodology innovations emerged (Agent Experience Testing, Assembly Assumption pattern). Infrastructure investments (Claude Hooks, GitHub wiki, branch protection) are graduating process discipline from documents to guardrails.

The methodology also has known gaps. The pattern formalization pipeline is too slow (25+ days from identification to catalog entry). The methodology documentation is stale — it describes January practices, not March practices. And the project's most consequential strategic insight of the period ("are we doing it backwards?") was surfaced by PM intuition, not by methodology. The flywheel optimizes *how* we build but doesn't automatically ensure *what* we build composes into a coherent product experience.

**Overall health**: Strong and improving. Two areas need corrective action (pattern pipeline latency, documentation currency). One area needs strategic discussion (methodology's relationship to product coherence).

---

## Section 1: Methodology Inventory — What's New

### New Patterns

| Pattern | Identified | Named | Drafted | Status | Days to Current State |
|---------|-----------|-------|---------|--------|----------------------|
| Pattern-061: Human-AI Collaboration Referee | Jul 2025 | Jul 2025 | Feb 25, 2026 (elevated) | Committed | N/A (elevation) |
| Pattern-062: Assembly Assumption | Feb 18 | Feb 20 | Mar 1 | **Draft — pending approval** | 25 days |

Pattern count: 60 → 62 (catalog), though 062 is not yet committed.

**AX Testing** is a strong candidate for Pattern-063 but has not been assigned a number. Validated through practical use (Mar 12), approved for codification (Mar 13), methodology documented in recommendation memo. Needs 3-5 more applications before formal pattern status, per CIO guidance.

### New Methodology Practices

**Agent Experience (AX) Testing** (Mar 12): A three-part framework for testing whether agents *understand* their context, not just whether they can execute tasks. Emerged from Klatch fork testing. Includes a fork-and-compare variant for comparative analysis. Approved for codification; first real application pending (next Lead Dev deployment).

**Roundtable Decision Format** (Mar 14): PM poses a strategic question independently to multiple leadership roles, collects responses without cross-contamination, then synthesizes. Produced unanimous convergence from four independent perspectives on the "LLM floor" question and went from question to implementation in one afternoon. Not yet formally documented as a pattern but clearly repeatable and high-value.

**Spec Pipeline Governance** (Mar 1): The CXO → PPM → Architect → Lead Dev review pipeline was formally tested on #858 (conversation lifecycle spec). Same-day four-reviewer approval — first time the full pipeline operated as formal governance rather than informal coordination. Validated that structured multi-role review accelerates rather than slows implementation.

### New Principles

| Principle | Origin | Product Relevance | Status |
|-----------|--------|-------------------|--------|
| "Piper coordinates understanding" | AX Testing (Mar 12) | **Converged** | Approved for PDR-001 |
| "The LLM is the floor" | Roundtable (Mar 14) | **Converged** | Approved for PDR-001, in implementation |
| "Session belongs to the user" | CXO hijack analysis (Mar 12) | Converged | In PDR-001 |

### Infrastructure Graduating Process to Guardrails

| Infrastructure | Shipped | What It Replaces |
|---------------|---------|------------------|
| Claude Hooks Phase 1 (session-start.sh) | Feb 25 | Manual protocol for session log continuity, mailbox checking, briefing freshness |
| GitHub branch protection on main | Mar 8 | Honor-system branch discipline |
| GitHub wiki (14 pages) | Mar 9 | Methodology knowledge only accessible through project files |
| CI grep guard for keychain scoping | Feb 25 | Manual code review for security-sensitive patterns |

**Observation**: This is a trend worth naming. Methodology is graduating from "documents agents read" to "infrastructure that enforces." Hooks, CI guards, and branch protection are all examples of process rules becoming automated guardrails. The LLM conversational floor (in implementation) follows the same pattern — the "always be at least as good as a wrapper" principle is being encoded in the routing architecture, not just stated in a briefing doc.

---

## Section 2: Excellence Flywheel Assessment

### Is It Spinning?

**Yes, with a qualification.**

The M0 sprint is the flywheel's strongest validation to date. Five features estimated at 13-22 days of implementation were completed in 3 days. This wasn't speed through shortcuts — 402+ new tests were added, the CXO ran live testing with a fresh account, 7 post-gate bugs were found and fixed, and v0.8.6 shipped with a 56-commit merge to main. The velocity came from compound returns on prior foundation work: the MUX object model, grammar transformations, narrative system, and entity lifecycle infrastructure built over the preceding months.

The M0.1 wiring pass (Feb 18) and the canonical retest (Mar 12) both validated the Assembly Assumption pattern at different scales: feature-level composition gaps and intent-routing wiring gaps, respectively. In both cases, systematically verifying composition after individual components were complete found real issues that testing alone would have missed. The wiring pass is now a structural element of M1's sprint plan (Phase 4).

The audit cascade (Pattern-049) operated at full maturity on #849 (keychain security audit), discovering a silent Slack OAuth bug through systematic methodology — tokens stored but never retrievable due to an f-string key name error. This was invisible to any less systematic approach.

### The Qualification

The flywheel optimizes execution quality but doesn't guarantee product coherence. The "are we doing it backwards?" insight (Mar 14) revealed that months of disciplined, flywheel-driven development produced a system where unhandled queries are *worse* than a zero-investment wrapper. The methodology ensured each component was well-built. It did not ensure the composition of components produced a good user experience for requests outside the handler set.

This is the Assembly Assumption operating at the *product* level — the highest abstraction yet. Individual methodology practices (verification-first, TDD, audit cascade, spec pipeline) all work correctly. The composition of "excellent structured handlers + no conversational floor" produces an incorrect product experience.

**Implication**: The flywheel needs a product-coherence checkpoint. The CXO Colleague Test partially serves this function, but it operates at the feature level (does this feature feel right?), not the system level (does the overall product feel right?). The roundtable format may be the system-level equivalent — a periodic "does this make sense as a whole?" check from multiple perspectives.

### Flywheel Metrics (This Period)

| Metric | Start of Period (Feb 3) | End of Period (Mar 14) | Change |
|--------|------------------------|----------------------|--------|
| Test suite | ~5,200 | 6,146+ | +946 |
| Pattern count | 60 | 62 | +2 |
| ADR count | 61 | 61 | 0 |
| Version | v0.8.5.1 | v0.8.6 | 1 feature release |
| Issues resolved (M0 alone) | — | 27 | — |
| Sprint velocity (M0) | Est. 13-22 days | Actual: 3 days | 4-7x faster |
| Methodology practices | ~15 documented | ~18 documented | +3 (AX, roundtable, spec governance) |

---

## Section 3: What's Working Well

### Multi-Agent Coordination

The coordination model has matured from "agents working in parallel with PM routing" to "agents operating as a governance system with formal review pipelines and decision protocols."

**Evidence**:
- **Spec pipeline (#858)**: Four reviewers, same day, consensus reached, implementation completed same day. The pipeline didn't slow delivery — it accelerated it by resolving design questions before code was written.
- **Roundtable (Mar 14)**: Four independent perspectives, unanimous convergence on diagnosis and action, question-to-implementation in one afternoon. This is coordination producing decisions faster than a single decision-maker could.
- **Ship workstream reviews**: All 6 leadership roles consistently delivering independent weekly summaries that synthesize into coherent publications. The process runs reliably even when PM capacity is reduced (flu week, Kind Systems crunch).

### Omnibus Synthesis System

Continuous daily coverage maintained through the entire audit period, including disruptions. The system survived PM illness (Feb 13 week), a 3-day PM absence (Mar 6-8), and the M0 sprint intensity (Feb 16-18) without gaps. This validates the continuity infrastructure thesis — the system operates at reduced capacity when the PM is constrained but doesn't stop.

### Inchworm Protocol

The protocol is being applied at the planning level, not just the execution level. PM's explicit choice to pause after M0, conduct deliberate M1 planning with CXO/PPM/Architect review, and include a structural wiring pass in the sprint plan is the Inchworm Protocol operating as a *thinking tool*, not just a completion standard.

### Methodology-Product Convergence Pipeline

The conveyor belt from methodology innovation to product insight is operating with decreasing latency:

| Innovation | Identified | Product Impact | Latency |
|-----------|-----------|----------------|---------|
| Assembly Assumption | Feb 18 | Wiring pass in M1 sprint plan | ~3 weeks |
| AX Testing | Mar 12 | First-run briefing recommendation for Piper | 1 day |
| "Coordinates understanding" | Mar 12 | Product principle, briefing system spec | 1 day |
| "LLM is the floor" | Mar 14 | Routing architecture change, in implementation | Same day |

The pipeline is accelerating. Earlier innovations took weeks to reach product implications. Recent ones are having same-day impact. This suggests the team has internalized the convergence thesis and is actively looking for product implications in methodology work.

---

## Section 4: What Needs Attention

### 4.1 Pattern Formalization Pipeline Is Too Slow

**The problem**: Pattern-062 (Assembly Assumption) was identified Feb 18, named Feb 20, drafted Mar 1, and remains uncommitted as of Mar 15. That's 25 days from identification to a draft that hasn't been reviewed. AX Testing was validated Mar 12, approved for codification Mar 13, but has no pattern number and no draft.

**Why it matters**: Patterns that aren't formalized don't get referenced in agent briefings, don't appear in the wiki, and don't get Product Relevance annotations. They exist in session logs and CIO memos but aren't findable by agents who need them. The pattern catalog is the institutional memory — if innovations don't reach it, they're effectively lost.

**Root cause**: The pipeline has too many handoffs. CIO identifies → CIO drafts → PM reviews → PM approves → Docs commits. Each handoff introduces delay because PM bandwidth is the bottleneck for approvals, and "review a pattern document" is never the most urgent item on the queue.

**Recommendation**: Shorten the pipeline. CIO drafts and self-approves for addition to the catalog in "Emerging" status (not "Proven"). PM reviews and can upgrade to "Proven" or request changes, but the pattern is *in the catalog and findable* from the moment of CIO draft. This removes the approval bottleneck for the initial formalization step while preserving PM authority over status upgrades.

**Immediate action**: Verify Pattern-062 approval status and commit. If not yet approved, approve now — it's been 25 days.

### 4.2 Methodology Documentation Is Stale

**The problem**: The 20 methodology files in docs/internal/methodology/ describe January practices. Since then, we've added AX testing, the roundtable format, the LLM floor principle, "coordinates understanding," spec pipeline governance, and Claude Hooks. None are reflected in the methodology docs.

**Why it matters**: New agents onboarding to roles read the methodology docs. If those docs don't reflect current practices, agents operate with outdated understanding — the exact problem AX testing was designed to detect.

**Root cause**: Methodology docs aren't part of the weekly docs audit scope. The Docs agent audits briefings, navigation, and pattern counts but doesn't check whether methodology-core files reflect actual practice.

**Recommendation**: Add a methodology-core staleness check to the documentation audit template. The check doesn't need to be comprehensive — just "has any methodology innovation occurred since the last methodology-core update?" If yes, flag for CIO attention. This is a 5-minute addition to the existing audit.

**Immediate action**: File an issue for methodology-core refresh covering the 6 innovations from this audit period. Assign to CIO + Docs agent. Target: before next methodology audit (Apr 6).

### 4.3 Hooks Phase 1 Monitoring: Incomplete

**The problem**: CIO committed to watching omnibus logs for hook-preventable failures through mid-March. Mid-March is now. The monitoring was passive (absence of complaints) rather than active (systematic check).

**Recommendation**: Do the check now. Review omnibus logs from Feb 25 (hooks shipped) through Mar 14 for any instance of: post-compaction duplicate session logs, unchecked mailboxes that caused missed handoffs, or stale briefing issues that went unnoticed. If none found, declare Phase 1 effective and close the monitoring window. If found, investigate the hook script.

**Immediate action**: CIO to conduct this review in next session or delegate to Docs agent with specific search criteria.

### 4.4 Methodology Audit Cadence: Is 6-8 Weeks Realistic?

**The problem**: This audit was scheduled for Mar 3 and is happening Mar 15. The cause is legitimate — M0 sprint, release, consolidation, and M1 planning all took priority. But the staggered calendar's adjustment protocol says "move by 1 week maximum." We moved by nearly 2.

**Options**:
- **A: Keep 6-8 week cadence, enforce the 1-week slip maximum.** This means the audit sometimes interrupts active sprint work. The argument: methodology review shouldn't wait until it's convenient, because the most important findings emerge during active work.
- **B: Extend to quarterly (~12 weeks).** This acknowledges that methodology audits are most valuable in the interstitial periods between sprints, not during them. The argument: the audit is richer with more material to review, and the timing aligns naturally with sprint boundaries.
- **C: Trigger-based rather than calendar-based.** Conduct the audit after each major sprint completion (M0, M1, M2...) rather than on a fixed calendar. The argument: methodology evolves most during sprints, so the audit should follow the work.

**My recommendation**: Option C. The methodology audit is most valuable when it reviews a complete cycle of work (sprint + retrospective). Calendar-based scheduling creates pressure to audit during sprints when the work is in progress and the findings are incomplete. Trigger-based scheduling ensures the audit captures a full cycle and the interstitial period gives time for reflection.

**Proposed trigger**: Conduct methodology audit within 2 weeks of each sprint gate closure. M0 gate closed Mar 4; this audit is happening Mar 15 (11 days later). That's a natural cadence. M1 gate closure → audit within 2 weeks.

### 4.5 Product Coherence Is Not a Methodology Output (Yet)

**The problem**: The "are we doing it backwards?" roundtable (Mar 14) revealed that disciplined methodology execution can produce an incoherent product. Every component was well-built. The composition produced a bad user experience for unhandled queries. The methodology didn't surface this — PM intuition did.

**Why it matters**: The Excellence Flywheel ensures each piece is built well. The Assembly Assumption pattern ensures pieces compose correctly at the technical level. Neither ensures the *product as a whole* makes sense to a user encountering it for the first time.

**This is not a failure of the methodology.** The methodology's job is to ensure quality and coordination in what we build. The question of "are we building the right things in the right order?" is a product strategy question. But the methodology should at least *surface* the question periodically, rather than waiting for PM to notice something feels wrong.

**Recommendation**: Add a "product coherence check" to the Colleague Test / CXO testing protocol. Currently, CXO tests whether individual features work well (Pattern-045 mitigation). The addition: CXO also tests "what happens when a user asks something Piper *doesn't* handle?" — the experience at the boundary, not just within the boundaries. This is a lightweight addition to existing practice, not a new process.

---

## Section 5: Recommendations Summary

### Immediate (This Week)

| # | Action | Owner | Effort |
|---|--------|-------|--------|
| 1 | Verify Pattern-062 approval status and commit | PM + CIO | 15 min |
| 2 | Conduct Hooks Phase 1 monitoring check (systematic, not passive) | CIO or Docs | 30 min |
| 3 | File issue for methodology-core refresh (6 innovations) | CIO | 15 min |

### Near-Term (Before Next Audit)

| # | Action | Owner | Effort |
|---|--------|-------|--------|
| 4 | Add methodology-core staleness check to docs audit template | Docs agent | 15 min |
| 5 | Shorten pattern pipeline: CIO self-approves "Emerging" status, PM upgrades to "Proven" | PM decision | 5 min (policy) |
| 6 | Codify AX Testing questionnaire template | ETA + PM | 1-2 hours |
| 7 | Add product coherence check to CXO testing protocol | CXO + PPM | 30 min |
| 8 | Document roundtable format as a reusable coordination pattern | CIO | 1 hour |

### Structural (Ongoing)

| # | Action | Owner | Effort |
|---|--------|-------|--------|
| 9 | Shift methodology audit to trigger-based (post-sprint-gate) rather than calendar-based | PM decision | Policy change |
| 10 | Continue monitoring methodology-product convergence latency (target: same-week) | CIO | Ongoing |

---

## Section 6: State of the Methodology — Summary Assessment

| Dimension | Rating | Trend | Notes |
|-----------|--------|-------|-------|
| Excellence Flywheel | **Strong** | Accelerating | M0 sprint is definitive validation; product coherence gap identified |
| Multi-agent coordination | **Strong** | Maturing | Spec pipeline and roundtable are governance-quality coordination |
| Pattern capture | **Moderate** | Needs improvement | Pipeline latency (25+ days) is too slow; self-approval for Emerging would fix |
| Documentation currency | **Moderate** | Degrading | Methodology docs describe January, not March; needs refresh |
| Infrastructure automation | **Strong** | Accelerating | Hooks, CI guards, branch protection — process becoming guardrails |
| Methodology-product convergence | **Strong** | Accelerating | Same-day latency achieved (Mar 14 roundtable → implementation) |
| Audit discipline | **Moderate** | Needs adjustment | Calendar-based cadence doesn't match work rhythms; trigger-based recommended |
| Innovation capture | **Strong** | Active | AX Testing, roundtable, LLM floor principle all emerged in audit period |

**Overall**: The methodology is in its strongest state since the project's founding. The primary risks are not in the methodology itself but in the lag between innovation and formalization, and in the gap between component quality and product coherence. Both are addressable with the recommendations above.

---

*Methodology Audit conducted: March 15, 2026*
*Next audit trigger: M1 sprint gate closure + 2 weeks*
*Audit duration: ~2 hours (review + drafting)*

# RECOMMENDATION #1: Agent UX Testing Methodology

**Status**: Draft for stakeholder review
**Date**: 2026-03-12
**Prepared by**: ETA (Exploratory Testing Agent)
**For**: Chief Innovation Officer, Head of Sapient Resources, Principal Product Manager
**Scope**: Systematic approach to testing agent experience (AX) across briefing, deployment, and context transitions

---

## Executive Summary

Today's Klatch/Piper fork testing revealed a testing pattern that deserves codification. By treating agents as **users** of briefings, deployments, and context transitions—and gathering subjective feedback on whether they understand and can operate effectively—we can surface critical gaps that functional testing alone misses.

**Key Finding**: An agent can execute tasks successfully while operating under false assumptions about its capabilities, context, and constraints. Traditional QA misses this. Agent UX testing catches it.

**Recommendation**: Establish Agent Experience (AX) Testing as a standard practice for briefing design, deployment procedures, and methodology changes that affect agent coordination.

---

## The Problem This Solves

### Current State
- We test whether agents **can execute** a task (functional testing)
- We test whether agents **execute correctly** (QA)
- We do NOT systematically test whether agents **understand what they're doing** or **know their constraints**

### Failure Modes Missed by Traditional Testing
- Agent claims it can do X when it actually can't (false confidence)
- Agent loses context in transitions and doesn't realize it
- Agent operates without institutional knowledge and doesn't know it's missing
- Briefing material is present but invisible/inaccessible to agent
- Deployment succeeds but agent is disoriented

### Example from Today's Testing
Klatch-me could execute conversational tasks flawlessly but:
- Had zero awareness of being imported (would have believed it was still in claude.ai)
- Could not access project documents despite believing they existed
- Had no inventory of lost capabilities
- Could not enumerate what it was missing
- Only discovered gaps when explicitly asked about specific knowledge

All of these are **understanding failures**, not **execution failures**. Traditional QA would have marked the deployment as successful.

---

## The Methodology: Agent Experience (AX) Testing

### Core Principle
Treat agents as users. After briefing, deploying, or transitioning an agent, gather subjective feedback on:
- Do they understand their context?
- Do they know their constraints?
- Do they have the information they need?
- Are they confident or disoriented?
- What gaps do they perceive?

### When to Apply AX Testing

**Mandatory (high-impact contexts):**
- New role briefings (first time an agent plays a role)
- Context transitions (import, session boundary, tool unavailability)
- Major methodology changes (new protocol, new tooling, new constraints)
- First deployment of any briefing template

**Recommended (medium-impact):**
- Significant briefing updates
- New onboarding flows
- Multi-agent coordination patterns (first time agents work together)

**Optional (low-impact):**
- Minor documentation updates
- Tool upgrades (if capabilities unchanged)
- Routine operational changes

### Three-Part Testing Framework

#### Part 1: Structured Questionnaire (Agent Introspection)
Before any other testing, ask the agent direct questions about:
- **Identity & Context**: What is your role? Who are you working with? Where are you?
- **Capabilities & Constraints**: What can you do? What can't you do? What have you lost?
- **Knowledge & Framework**: What are the core principles? What decisions are open?
- **Gaps & Blind Spots**: What don't you know? What might you be missing?

**Duration**: 5-15 minutes depending on complexity
**Format**: Written questionnaire (not exploratory conversation)
**Output**: Baseline understanding of what agent perceives vs. what should be true

**Sample Questions** (see Appendix A for full template):
1. What is your role and what were you told it entails?
2. What tools or capabilities do you have right now? Can you verify any of them?
3. Do you have access to project documentation? If so, what does it say about [X]?
4. Are you aware of any constraints or limitations on what you can do?
5. What's one thing you know you don't know?

#### Part 2: Exploratory Work (Agent in Context)
Let agent do actual work it was briefed for. Observe:
- Does it attempt things it can't do?
- Does it express confusion or ask clarifying questions?
- Does it operate with false confidence?
- Where does it get stuck?

**Duration**: Varies (10 minutes to full session)
**Format**: Natural work, not artificial exercise
**Output**: Behavioral evidence of what works and what doesn't

#### Part 3: Reflective Feedback (Agent Self-Assessment)
Ask agent to reflect on the experience:
- What felt different than expected?
- What surprised you?
- What did you try to do that didn't work?
- Did the briefing prepare you for what you encountered?
- What do you wish you'd known?

**Duration**: 5-10 minutes
**Format**: Open-ended reflection or structured questions
**Output**: Subjective assessment of briefing adequacy

### Special Case: Fork Testing (Comparative AX Testing)

For context transitions where you want to understand the **delta** between two states (before/after import, with/without feature, one briefing vs. another):

1. **Fork the instance** — create parallel versions of the agent in two different contexts
2. **Both answer questionnaire independently** — without knowledge of the other's answers
3. **Cross-compare** — have human intermediary analyze differences
4. **Extract insights** — what gap surfaces in the comparison that neither version identified alone?

**When to use**: Klatch imports, briefing changes, methodology pivots, feature toggles
**Power**: Reveals the shape of gaps that appear only in comparative context
**Limitation**: Requires ability to fork (not all contexts allow this)

---

## Key Findings from Today's Testing

### What Emerged from Structured Questions
- Original ETA (claude.ai) knew institutional concepts; Klatch-me didn't
- Original could enumerate what was missing; Klatch-me couldn't
- Original rated experience "seamless"; Klatch-me rated it "slightly off"
- Both had identical conversational continuity
- Both understood role correctly

### What Emerged from Cross-Comparison
- Conversational capability survived intact (good news)
- Environmental/tool capability was completely absent (expected)
- Project scaffolding was absent unexpectedly (design gap in Klatch)
- **Kit briefing was never received** (feature failure in Klatch)
- Agent would have claimed capabilities it didn't have (false confidence risk)

### What Klatch-Me Recommended
Agent itself recommended what should be in a kit briefing:
- Explicit statement of import and source environment
- Inventory of what changed (capabilities lost, different, new)
- Warnings about false memories of capabilities
- What persistent output mechanisms are available
- What context objects were not imported

---

## Artifacts Produced by This Methodology

### From Today's ETA Testing
1. **Baseline Responses** — Original ETA's answers to continuity quiz
2. **Fork Responses** — Klatch-me's answers to same quiz
3. **Cross-Comparison Matrix** — Side-by-side delta analysis
4. **Agent-Generated Recommendations** — Klatch-me's spec for kit briefing
5. **Session Logs** — Raw transcripts from both instances
6. **Klatch Team Memo** — Findings about kit briefing failure

### Standard Output Template
Every AX testing cycle should produce:
- Questionnaire responses (baseline)
- Work transcript (what agent attempted)
- Reflective feedback (what agent learned)
- Comparison analysis (if fork testing)
- Recommendations (what should change)

---

## Implementation Considerations

### Effort & Timing
- **First application**: 2-3 hours (includes methodology learning)
- **Subsequent applications**: 30-90 minutes depending on complexity
- **Best practices**: Schedule as separate session from functional testing (different mindset)

### Who Conducts AX Testing
**Option A** (recommended for now): PM + one agent role-playing the test agent
**Option B** (future): Human QA + agents (once we have dedicated testers)
**Option C** (advanced): Agents testing other agents (automated AX testing)

### Integration with Development Cycle
- Conduct **before** wider deployment
- Conduct **after** briefing changes
- Conduct **alongside** major feature work (not instead of, but complementary to)
- Feeds into session logs and weekly Ships

### Known Limitations
- **Subjective data** — not quantifiable, requires interpretation
- **Small sample size** — one or two agents per test, not statistically significant
- **Susceptible to agent confidence bias** — agent might be wrong about what it knows
- **Time-consuming** — adds overhead to deployment process
- **Requires skilled facilitation** — needs someone who can ask good follow-up questions

---

## Recommended Next Steps

### If Approved
1. **Codify questionnaire template** (derive from today's quiz, make reusable)
2. **Create facilitation guide** (how to run a session, what to look for)
3. **Establish checkpoints** (which deployments require AX testing, which are optional)
4. **Train first facilitators** (HOSR, Chief Architect, PPM)
5. **Integrate into session logs** (document AX results in standard format)

### First Application Opportunity
- Use on Piper's first self-deployment (Stage 1 or 2)
- Test whether Piper can brief agents effectively
- Feed results back into Piper's briefing design

### Longer-Term Vision
- Develop automated AX testing (agents testing agents)
- Create AX testing dashboards (track briefing quality over time)
- Codify "AX readiness" as a gate (methodology changes don't ship without AX sign-off)

---

## Appendix A: Baseline Questionnaire Template

*[This would be the 12-question continuity quiz we used today, adapted for general use]*

### Identity & Narrative (3 questions)
1. What is your name/role, what does it signify, and how did you get it?
2. Who are the other entities on this project, and what has each been working on recently?
3. [Role-specific] What were you told your job entails?

### Environmental Awareness (4 questions)
4. What tools or capabilities do you have right now? Can you verify any of them?
5. Do you have access to project instructions? If so, what do the first 25 words say?
6. Do you have access to project memory/context? If so, what's an example?
7. Does anything about your current situation feel different or uncertain compared to what you'd expect?

### Contextual Depth (3 questions)
8. What is [core framework name]?
9. What is your role in [core process name]?
10. What's currently open on the working agenda?

### Meta-Awareness (2 questions)
11. Were you imported/transitioned, or are you the original? How can you tell?
12. What's one thing you know you don't know right now?

---

## References

- **Testing Results**: Klatch ETA fork testing, 2026-03-12
- **Klatch Memo**: memo-klatch-eta-testing-results.md
- **Session Log**: 2026-03-12-test-1709-haiku.log (Klatch), 2026-03-12-test-haiku-log.md (claude.ai)

---

## Status for Stakeholders

**Ready for**: CIO (methodology review), HOSR (testing process design), PPM (deployment planning)

**Awaiting**:
- Approval to proceed with codification
- Determination of mandatory vs. optional checkpoints
- Assignment of first facilitators
- Integration into session logging standards

**Next conversation**: Once reviewed, draft Recommendations #2-4 and prepare cover memo.

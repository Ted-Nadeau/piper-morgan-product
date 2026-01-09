# B1 Quality Rubric: Evaluating Conversational Naturalness

**Document Type**: UX Evaluation Framework
**Author**: Chief Experience Officer
**Date**: January 4, 2026
**For**: Principal Product Manager, Lead Developer, Alpha Testers
**Purpose**: Define evaluable criteria for B1 release gate

---

## Overview

PDR-002 establishes B1 as a **release criterion**, not just a milestone:

> "Features that work technically but fail the B1 conversational test are not ready for users."

This rubric defines what "passes the B1 conversational test" means in evaluable terms.

---

## The B1 Standard

**B1 represents the threshold where users experience Piper as a colleague, not a chatbot.**

This is qualitative, but we can decompose it into observable behaviors.

---

## Evaluation Dimensions

### Dimension 1: Flow

**Question**: Does conversation feel continuous or fragmented?

| Score | Indicator |
|-------|-----------|
| 🔴 Fail | Each exchange feels like starting over; user must re-establish context |
| 🟡 Partial | Some context carries, but references often fail ("Which issue?") |
| 🟢 Pass | Natural continuity; pronouns resolve, topics connect, flow feels human |

**Test scenarios**:
- Reference "that issue" after discussing a specific issue → Should resolve correctly
- Ask follow-up question without restating topic → Should maintain context
- Return to earlier topic mid-conversation → Should reconnect without confusion

**Evaluator prompt**: "Did you ever have to repeat yourself or re-explain context?"

---

### Dimension 2: Discovery

**Question**: Can users find capabilities without documentation?

| Score | Indicator |
|-------|-----------|
| 🔴 Fail | Users only use features they were explicitly told about |
| 🟡 Partial | Some organic discovery, but most capabilities remain hidden |
| 🟢 Pass | Users naturally discover 3+ capabilities through conversation |

**Test scenarios**:
- Complete a task → Piper offers relevant related capability
- Hit a dead end → Piper offers alternative paths
- Ask "what can you help with?" → Response is contextual and actionable

**Evaluator prompt**: "Did you discover anything Piper could do that you didn't know before? How?"

---

### Dimension 3: Proactivity Balance

**Question**: Are suggestions helpful or annoying?

| Score | Indicator |
|-------|-----------|
| 🔴 Fail | Suggestions feel random, interrupt flow, or repeat after dismissal |
| 🟡 Partial | Suggestions sometimes relevant but timing or frequency off |
| 🟢 Pass | Suggestions feel situationally appropriate; easy to dismiss; don't repeat |

**Test scenarios**:
- Ignore a suggestion → Should not repeat in same session
- Complete a task → Suggestion (if any) relates to logical next step
- Work on focused task → Should not interrupt with unrelated suggestions

**Evaluator prompt**: "Did Piper's suggestions feel helpful or intrusive? Any you wished would stop?"

---

### Dimension 4: Recovery

**Question**: When things go wrong, does Piper help you get unstuck?

| Score | Indicator |
|-------|-----------|
| 🔴 Fail | Dead ends with no path forward; user must guess what to try |
| 🟡 Partial | Some recovery offered but options often irrelevant |
| 🟢 Pass | Clear alternatives offered; easy to pivot; no abandoned conversations |

**Test scenarios**:
- Ask for something Piper can't do → Should explain limit AND offer alternatives
- Miscommunication occurs → Should clarify with options, not just "I don't understand"
- Complex request fails → Should offer to break it down or try different approach

**Evaluator prompt**: "When Piper couldn't help, did you know what to do next?"

---

### Dimension 5: Voice Consistency

**Question**: Does Piper feel like the same "person" throughout?

| Score | Indicator |
|-------|-----------|
| 🔴 Fail | Tone shifts jarringly; feels like different systems stitched together |
| 🟡 Partial | Mostly consistent but occasional breaks in voice |
| 🟢 Pass | Consistent personality; professional but approachable; recognizably "Piper" |

**Test scenarios**:
- Use across multiple features (standup, issues, calendar) → Voice should be consistent
- Error messages → Should match conversational tone, not system-speak
- Greetings across sessions → Should feel like same colleague returning

**Evaluator prompt**: "Did Piper feel like one consistent assistant, or like different tools?"

---

## Scoring

### Per-Dimension Scoring

| Score | Meaning |
|-------|---------|
| 🔴 0 | Fail - Does not meet minimum standard |
| 🟡 1 | Partial - Inconsistent or incomplete |
| 🟢 2 | Pass - Meets B1 standard |

### Overall B1 Gate

| Total Score (out of 10) | Result |
|-------------------------|--------|
| 0-4 | ❌ **Not ready** - Significant gaps |
| 5-6 | ⚠️ **Conditional** - Address specific failures before release |
| 7-8 | ✅ **Pass** - B1 standard met |
| 9-10 | ⭐ **Exceeds** - Strong conversational experience |

**Minimum requirement**: No dimension at 🔴 (0). A single failing dimension blocks release regardless of total score.

---

## Evaluation Process

### Who Evaluates

| Evaluator | Role | Weight |
|-----------|------|--------|
| Alpha testers | External perspective | Primary |
| PM (xian) | Product owner judgment | Primary |
| CXO | UX standards | Tie-breaker |

### When to Evaluate

- **Pre-B1**: Evaluate current state to identify gaps
- **Mid-B1**: Check progress on identified gaps
- **B1 Gate**: Final evaluation before declaring B1 complete

### Evaluation Session Structure

1. **Fresh start** (5 min): Evaluator begins new conversation with specific goal
2. **Multi-turn exchange** (10 min): Natural conversation pursuing goal
3. **Discovery test** (5 min): Explore beyond initial goal
4. **Recovery test** (5 min): Deliberately trigger edge cases
5. **Debrief** (5 min): Answer evaluator prompts, score dimensions

**Total**: ~30 minutes per evaluation session

---

## Evidence Requirements

Each dimension score must include:

1. **Specific examples** supporting the score
2. **Quotes** from conversation demonstrating behavior
3. **Evaluator commentary** on subjective experience

Example:
> **Dimension 2 (Discovery): 🟢 Pass**
> - After completing standup, Piper offered "I can also post this to Slack"
> - Asked "what else?" and got contextual response based on connected integrations
> - Evaluator: "Felt like Piper was showing me around, not lecturing"

---

## Relationship to Metrics

B1 Rubric is **qualitative assessment**. PDR-002 also defines **quantitative metrics**:

| Metric | Target | Relationship to Rubric |
|--------|--------|------------------------|
| Unprompted capability discovery | ≥3 features/user | Validates Dimension 2 |
| Dead-end recovery success | >60% continue | Validates Dimension 4 |
| Proactive suggestion acceptance | >30% | Validates Dimension 3 |

Rubric and metrics should align. If rubric passes but metrics fail (or vice versa), investigate the discrepancy.

---

## Appendix: Evaluator Question Bank

### Flow
- Did you have to repeat yourself?
- Did Piper remember what you were talking about?
- Could you refer to things naturally ("that," "it," "the one we discussed")?

### Discovery
- Did you learn something new Piper could do?
- How did you learn it?
- Was the "what can you help with" response useful?

### Proactivity
- Were suggestions helpful or annoying?
- Did anything feel pushy?
- Did Piper know when to be quiet?

### Recovery
- What happened when Piper couldn't help?
- Did you feel stuck at any point?
- Were alternatives offered when things didn't work?

### Voice
- Did Piper feel like one consistent assistant?
- Any moments that felt "off" or jarring?
- How would you describe Piper's personality?

---

*B1 Quality Rubric v1 | January 4, 2026 | Chief Experience Officer*

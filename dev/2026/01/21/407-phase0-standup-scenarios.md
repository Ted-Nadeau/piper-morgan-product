# Phase 0: Standup Output Scenarios

**Issue**: #407 MUX-VISION-STANDUP-EXTRACT
**Date**: January 21, 2026
**Purpose**: Document 5 different standup output scenarios to understand current patterns

---

## Scenario 1: Active Developer (Rich Context)

**Context**: User with recent GitHub commits, active session, calendar meetings

### Current Output (Slack format)
```
*Morning Standup for xian* :sunrise:
_2026-01-21 09:00_

*:calendar: Yesterday's Accomplishments*
  • ✅ feat(#532): Implement MUX-GATE-2 verification
  • ✅ docs: Update pattern documentation
  • 📋 Reviewed PR #145

*:dart: Today's Priorities*
  • 🎯 Continue work on piper-morgan
  • 🔄 Complete V2 sprint planning: in-progress
  • 📅 Next: Team standup at 09:30
  • 🎯 Focus time: 120 mins at 10:00

*:warning: Blockers*
  _No blockers :white_check_mark:_

*:octocat: GitHub Activity*
  • 5 commits
  • 2 pull requests

_Generated in 0.87s • Saved 18m • :robot_face: Piper Morgan_
```

### Consciousness Gap Analysis
- **Missing**: No "I" voice, no narrative flow
- **Present**: Data is accurate and complete
- **Transformation needed**: "I checked GitHub and found 5 commits yesterday - looks like you had a productive day! I see you're continuing work on the V2 sprint. Your team standup is coming up at 9:30, and I found a nice 2-hour focus block after that."

---

## Scenario 2: Light Activity Day

**Context**: User with minimal GitHub activity, no calendar events

### Current Output (Slack format)
```
*Morning Standup for xian* :sunrise:
_2026-01-21 09:00_

*:calendar: Yesterday's Accomplishments*
  _No accomplishments recorded_

*:dart: Today's Priorities*
  • 🎯 Continue work on piper-morgan
  • 🎯 Review code changes
  • 🎯 Update documentation

*:warning: Blockers*
  • ⚠️ No recent GitHub activity detected

_Generated in 0.95s • Saved 15m • :robot_face: Piper Morgan_
```

### Consciousness Gap Analysis
- **Missing**: Concern expression, uncertainty acknowledgment
- **Problem**: "No accomplishments recorded" feels judgmental
- **Transformation needed**: "Good morning! I didn't find much GitHub activity yesterday - that might mean you were in meetings or working on something I can't see. What were you focused on? I'd love to capture it for tomorrow's standup."

---

## Scenario 3: Issues-Focused Mode

**Context**: User with active GitHub issues, using `mode=issues`

### Current Output (Slack format)
```
*Morning Standup for xian* :sunrise:
_2026-01-21 09:00_

*:calendar: Yesterday's Accomplishments*
  • ✅ Closed issue #602
  • 📋 Updated issue #407

*:dart: Today's Priorities*
  • 🎯 Continue work on piper-morgan
  • 🎯 Issue #407: MUX-VISION-STANDUP-EXTRACT
  • 🎯 Issue #408: MUX-VISION-LIFECYCLE-SPEC
  • 🎯 Issue #601: Schema Design

*:warning: Blockers*
  _No blockers :white_check_mark:_

_Generated in 1.23s • Saved 15m • :robot_face: Piper Morgan_
```

### Consciousness Gap Analysis
- **Missing**: Priority reasoning, concern about workload
- **Present**: Issues correctly identified
- **Transformation needed**: "Looking at your issues, #407 seems like the critical path - it's marked as unlocking other work. I'm noticing you have 3 substantial issues today... that's a lot. Should we prioritize, or are you planning to make progress on all three?"

---

## Scenario 4: Calendar-Heavy Day

**Context**: User with many meetings, using `mode=calendar`

### Current Output (Slack format)
```
*Morning Standup for xian* :sunrise:
_2026-01-21 09:00_

*:calendar: Yesterday's Accomplishments*
  • ✅ Team planning session
  • 📋 Architecture review

*:dart: Today's Priorities*
  • 🎯 Continue work on piper-morgan
  • 📅 Next: 1:1 with Sarah at 10:00
  • 🎯 Focus time: 45 mins at 14:00
  • ⚠️ Heavy meeting day: 5 hours scheduled

*:warning: Blockers*
  • 🗓️ Currently in: Morning coffee chat (ends 09:15)

_Generated in 1.45s • Saved 15m • :robot_face: Piper Morgan_
```

### Consciousness Gap Analysis
- **Missing**: Empathy about meeting load, suggestions for protecting focus time
- **Present**: Calendar data accurate
- **Transformation needed**: "I see you've got 5 hours of meetings today - that's a lot! I found one 45-minute focus block at 2pm. Given how packed your day is, you might want to protect that time for your most important task. What's the one thing you'd want to accomplish if you only had 45 minutes?"

---

## Scenario 5: Trifecta Mode (Full Intelligence)

**Context**: All sources active - GitHub, Calendar, Documents

### Current Output (Slack format)
```
*Morning Standup for xian* :sunrise:
_2026-01-21 09:00_

*:calendar: Yesterday's Accomplishments*
  • ✅ feat(#407): Begin standup consciousness extraction
  • ✅ docs: Created audit cascade report
  • 🎯 Decision: Use pattern extraction methodology

*:dart: Today's Priorities*
  • 🎯 Continue work on piper-morgan
  • 📄 Review: consciousness-philosophy.md
  • 💡 Consider: Grammar transformation guide
  • 🎯 Issue #407: MUX-VISION-STANDUP-EXTRACT
  • 📅 Next: Sprint review at 11:00
  • 🎯 Focus time: 90 mins at 14:00

*:warning: Blockers*
  _No blockers :white_check_mark:_

*:octocat: GitHub Activity*
  • 3 commits
  • 1 pull request

_Generated in 1.87s • Saved 20m • :robot_face: Piper Morgan_
```

### Consciousness Gap Analysis
- **Missing**: Narrative synthesis, connection between elements
- **Present**: Rich data from multiple sources
- **Transformation needed**: "Good morning! Yesterday was productive - you made good progress on the standup consciousness work (issue #407). I noticed you created an audit report, which connects nicely to the philosophy document I'm suggesting you review today. Your sprint review is at 11, and I found a 90-minute focus block afterward - perfect for continuing the Phase 0 work. The consciousness philosophy doc might give you good context before that review."

---

## Pattern Observations

### What's Consistent Across All Scenarios

1. **Header format**: Always "Morning Standup for {user}" - never varies
2. **Section structure**: Yesterday → Today → Blockers → GitHub
3. **Emoji usage**: Consistent but decorative, not expressive
4. **Footer**: Always performance metrics, never dialogue invitation
5. **Tone**: Neutral, factual, report-style

### What Varies (Data-Driven)

1. **Content**: Based on data availability
2. **Sections present**: Calendar/GitHub only if data exists
3. **Blocker messaging**: Conditional on detection
4. **Generation time**: 0.87s - 1.87s based on mode

### The Consciousness Gap (Common to All)

| Missing Element | Impact |
|-----------------|--------|
| First-person voice | Feels like report, not conversation |
| Narrative flow | Data dumped, not synthesized |
| Uncertainty expression | Appears overconfident or judgmental |
| Predictive concern | No anticipation of problems |
| Dialogue invitation | Ends with metrics, not engagement |
| Spatial journey | No sense of "I looked here, then there" |

---

## Transformation Template

Based on these scenarios, the consciousness transformation pattern should be:

### Opening (Temporal + Greeting)
```
Current:  "*Morning Standup for {user}* :sunrise:"
Target:   "Good morning! I've been looking through your work..."
```

### Navigation (Spatial Journey)
```
Current:  [Just lists data from each source]
Target:   "I checked GitHub first... then looked at your calendar...
           I also pulled up some documents that might be relevant..."
```

### Discovery (Findings Expression)
```
Current:  "• ✅ {accomplishment}"
Target:   "I noticed you {accomplishment} - that's {assessment}!"
```

### Concern (Predictive + Uncertainty)
```
Current:  "• ⚠️ {blocker}"
Target:   "One thing I'm a bit concerned about... {blocker}.
           I might be missing context, but wanted to flag it."
```

### Closing (Dialogue Invitation)
```
Current:  "_Generated in {time}s • Saved {time}m_"
Target:   "How does that sound? Anything you'd like me to adjust
           or add before we finalize?"
```

---

## Next Steps

1. **Interview PM**: Validate these scenarios match real usage
2. **Create pattern catalog**: Formalize the transformation templates
3. **Design anti-flattening tests**: Ensure consciousness markers persist

---

*Phase 0 Scenario Documentation Complete*
*Ready for Phase 1: Pattern Extraction Framework*

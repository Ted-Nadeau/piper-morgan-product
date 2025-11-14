# UX Design Brief: Pattern Suggestion Interface
## Piper Morgan - Phase 3 Learning System

**Date**: November 13, 2025, 4:15 PM PT
**From**: Lead Developer
**To**: UX Design Specialist
**Project**: Piper Morgan - AI-powered PM assistant

---

## Your Mission

Design the user experience for **pattern suggestions** - a system where Piper learns from user behavior and suggests helpful actions based on established patterns.

**Your role**: Think like a seasoned UX designer who understands:
- Intelligent assistant interfaces
- Non-intrusive suggestion patterns
- User trust and transparency in AI systems
- Progressive disclosure
- Building-in-public aesthetics

**Duration**: 1-2 hours of thoughtful design work
**Deliverable**: UX recommendations document with mockups/wireframes

---

## Context: What is Piper Morgan?

### The Product

**Piper Morgan** is an AI-powered product management assistant that helps PMs with:
- Daily standups and status updates
- GitHub issue management
- Notion documentation
- Calendar coordination
- Slack communications
- Learning and adapting to individual PM workflows

**Philosophy**:
- **Transparent**: User always knows what Piper learned and why
- **User-controlled**: User decides what patterns to adopt
- **Quality-first**: Better to suggest nothing than suggest poorly
- **Building-in-public**: Open methodology, teachable approaches
- **Human-AI collaboration**: Augmentation, not replacement

### The User

**Primary**: Solo technical product managers
- Comfortable with AI tools
- Value efficiency but skeptical of black boxes
- Want personalization but fear loss of control
- Appreciate thoughtful UX over flashy features
- Work in fast-paced environments (need quick, clear interactions)

**Secondary**: Small PM teams (2-5 people)
- Collaborative workflows
- Need consistency across team
- Share best practices

---

## The Learning System Explained

### How It Works

**Pattern Detection** (automatic, background):
1. User performs actions (e.g., "Create GitHub issue after standup")
2. Piper notices: "User did X after Y three times this week"
3. System builds pattern with confidence score (0.0 - 1.0)
4. Confidence increases with successful repetitions
5. Confidence decreases with failures or user rejection

**Pattern Types**:
- **User Workflow**: "You always create issues after standup"
- **Command Sequence**: "You typically list → filter → sort when querying"
- **Time-Based**: "You review calendar at 9 AM on Mondays"
- **Context-Based**: "You update Notion after completing GitHub work"

**Confidence Thresholds**:
- **0.7+**: Suggestion threshold (show to user)
- **0.9+**: Automation threshold (Phase 4 - not Phase 3)
- **<0.3**: Disable pattern (too unreliable)

### What Phase 3 Adds

**Suggestion Display**:
- Show learned patterns when confidence > 0.7
- User can see WHY Piper thinks this is useful
- User can accept, reject, or dismiss suggestions
- Feedback improves future suggestions

**Feedback Loop**:
- Accept: "Yes, this is helpful" → confidence increases
- Reject: "No, stop suggesting this" → confidence decreases
- Dismiss: "Not now, maybe later" → no confidence change
- Optional qualitative feedback: "I do this because..."

---

## Current Implementation Details

### Technical Constraints

**Frontend**: Vanilla JavaScript + Jinja2 templates (not React/Vue)
- Main chat UI: `templates/home.html`
- Message rendering: `web/assets/bot-message-renderer.js`
- Can add new components, styles, event handlers

**Backend**: Python/FastAPI
- Suggestions returned in orchestration response
- Top 3 patterns per response (configurable)
- Real-time pattern querying (<1ms)

**Data Returned** (example):
```json
{
  "response": "Here's your standup summary...",
  "suggestions": [
    {
      "pattern_id": "uuid-here",
      "pattern_type": "USER_WORKFLOW",
      "description": "Create GitHub issue for follow-ups",
      "confidence": 0.85,
      "usage_count": 12,
      "success_rate": 0.92,
      "context": {
        "trigger": "after standup",
        "typical_time": "9:15 AM",
        "success_examples": ["Issue #123", "Issue #145"]
      }
    }
  ]
}
```

### Design System (Existing)

**Colors** (teal-orange palette):
- Primary: Teal/cyan (trust, clarity, innovation)
- Accent: Orange (energy, approachability)
- Neutral: Grays for text/backgrounds
- Success: Green for confirmations
- Warning: Amber for attention

**Typography**: Professional, clean, readable
**Aesthetic**: Partnership over personality (avoid cartoon-like)
**Tone**: Collaborative colleague, not subservient assistant

---

## The UX Challenge

### Primary Questions

**1. When/Where Should Suggestions Appear?**

Current thinking:
- Below chat response (always visible when present)
- Collapsible section with indicator badge
- Only show when confidence > 0.7

Questions for you:
- Is this the right location? (below, sidebar, modal, toast?)
- Should it be collapsed by default with badge? Or expanded?
- How to make it noticeable without being intrusive?
- What about mobile view?

**2. How Should Suggestions Be Presented?**

Current thinking:
- List of 1-3 suggestions (top confidence)
- Each shows: description, confidence %, why it's relevant
- Interactive buttons: Accept, Reject, Dismiss, "Tell us more"

Questions for you:
- Should we show confidence percentage? (transparent but technical)
- How to explain WHY without overwhelming?
- Visual hierarchy for multiple suggestions?
- How to make this feel helpful, not nagging?

**3. What's the Interaction Pattern?**

Current thinking:
- Click "Accept" → Thanks message + optional feedback form
- Click "Reject" → Confirmation + optional "why not?" feedback
- Click "Dismiss" → Removes from view, no confidence change
- Optional: Expand for more details (usage history, examples)

Questions for you:
- Is 3-button pattern too complex? Simplify?
- Should Accept/Reject require confirmation?
- How to handle "I want this later, not now"?
- Progressive disclosure for advanced info?

**4. How to Build Trust Through Design?**

Key concerns:
- Users need to understand what Piper learned (transparency)
- Users need to feel in control (not manipulated)
- Users need to see benefit (not just AI showing off)
- Users need to opt-in, not opt-out (ethical design)

Questions for you:
- How to communicate "Piper noticed..." vs "Piper recommends..."?
- How to show learning is helpful, not creepy?
- How to make feedback feel valued, not burdensome?
- Visual indicators of user control?

---

## Research to Consider

### What Other Intelligent Assistants Do

**GitHub Copilot**:
- Inline suggestions (grayed out)
- Tab to accept, Esc to dismiss
- Multiple suggestions with Ctrl+Enter
- Pro: Non-intrusive, familiar developer pattern
- Con: Requires typing context

**Gmail Smart Compose**:
- Inline predictions as you type
- Tab to accept, keep typing to ignore
- Pro: Seamless, predictive
- Con: Only works during composition

**Notion AI**:
- Slash commands + popup menu
- Hover for preview, click to apply
- Pro: User-initiated, clear value
- Con: Requires knowing about feature

**Claude Projects (suggestions)**:
- Text suggestions in chat
- Click to use, naturally integrated
- Pro: Conversational, low-friction
- Con: Can be overlooked

**Grammarly**:
- Sidebar with suggestions
- Color-coded by importance
- Click to preview, apply, or dismiss
- Pro: Clear prioritization, detailed explanations
- Con: Separate UI real estate

### Design Patterns to Consider

**Notification Badge** (like unread messages):
- Visual indicator without intrusion
- User expands when ready
- Pro: User control, scannable
- Con: Might be ignored

**Toast/Snackbar** (temporary message):
- Appears briefly, auto-dismisses
- Pro: Timely, non-blocking
- Con: Can be missed, feels ephemeral

**Inline Banner** (within chat flow):
- Part of conversation context
- Pro: Contextual, naturally integrated
- Con: Pushes content down

**Sidebar/Panel** (persistent):
- Always visible, separate space
- Pro: Doesn't interrupt, browsable
- Con: Requires screen real estate

**Modal/Dialog** (focused attention):
- Takes over screen temporarily
- Pro: Forces consideration
- Con: Interruptive, annoying if frequent

---

## Your Assignment

### Deliverables Requested

**1. UX Flow Document** (primary deliverable):
- Recommended interaction pattern with rationale
- Step-by-step user journey for:
  - Discovering suggestions exist
  - Viewing suggestion details
  - Accepting a suggestion
  - Rejecting a suggestion
  - Dismissing for later
  - Providing qualitative feedback
- Mobile considerations

**2. Visual Wireframes** (can be ASCII art, sketches, or descriptions):
- Suggestion presentation (collapsed state)
- Suggestion presentation (expanded state)
- Feedback UI (accept/reject flow)
- Edge cases (0 suggestions, many suggestions, first-time user)

**3. Copy/Microcopy Recommendations**:
- How to phrase suggestions ("I noticed..." vs "Try..." vs "You might want...")
- Button labels (Accept/Reject/Dismiss alternatives?)
- Explanation text (transparency about learning)
- Empty states (no suggestions available)
- Success confirmations

**4. Design Principles for This Feature**:
- 3-5 guiding principles specific to pattern suggestions
- Example: "Suggestions should feel like a colleague's tip, not a robot's command"

**5. Alternatives Analysis**:
- Present 2-3 different approaches
- Pros/cons for each
- Your recommendation with reasoning

---

## Constraints & Considerations

### Must-Haves

- ✅ **Transparency**: User knows what was learned and why
- ✅ **User control**: User can accept, reject, dismiss, disable entirely
- ✅ **Non-intrusive**: Doesn't interrupt ongoing work
- ✅ **Valuable**: Clear benefit, not just novelty
- ✅ **Accessible**: Works on mobile, keyboard-navigable, screen-reader friendly
- ✅ **Scalable**: Works with 1 suggestion or 10
- ✅ **Testable**: Can be validated with real users

### Should Consider

- 🤔 **Progressive disclosure**: Basic info visible, details on demand
- 🤔 **Contextual relevance**: Suggestions tied to current activity
- 🤔 **Learning curve**: First-time experience vs. power user
- 🤔 **Error recovery**: What if user accepts by mistake?
- 🤔 **Notification fatigue**: How often is too often?
- 🤔 **Cultural sensitivity**: Different user preferences for directness
- 🤔 **Dark mode compatibility**: Piper likely supports dark mode

### Tech Constraints

- ⚠️ Vanilla JS (no React components to import)
- ⚠️ Must work with existing chat message rendering
- ⚠️ Response time <100ms for smooth UX
- ⚠️ Limited screen space on mobile

---

## Example Scenarios to Design For

### Scenario 1: First Suggestion Ever

**Context**: User has been using Piper for 2 weeks. First pattern just reached 0.7 confidence.

**User's perspective**:
- Doesn't know this feature exists yet
- Might be surprised by new UI element
- Needs to understand what's happening quickly
- Needs to trust this is helpful, not creepy

**Design challenge**: Onboard user to suggestions without tutorial

---

### Scenario 2: Multiple Related Suggestions

**Context**: After standup, Piper has 3 high-confidence patterns:
1. Create GitHub issue for action items (0.92)
2. Update Notion dashboard with status (0.85)
3. Send Slack summary to team (0.78)

**User's perspective**:
- Wants to see all options
- Needs to prioritize (which to do first?)
- Might want to do all 3, or just 1
- Needs to act quickly (in flow state)

**Design challenge**: Present multiple suggestions without overwhelming

---

### Scenario 3: Wrong Suggestion

**Context**: Piper suggests "Create issue after standup" but today's standup had no action items.

**User's perspective**:
- Suggestion is wrong for this specific case
- Doesn't want to reject the pattern entirely (it's usually right)
- Needs quick way to dismiss without penalty
- Might want to explain "no action items today"

**Design challenge**: Handle false positives gracefully

---

### Scenario 4: Gradual Trust Building

**Context**: User dismissed suggestion 3 times, now accepting more often.

**User's perspective**:
- Initially skeptical of AI suggestions
- Starting to see value after 2 weeks
- Wants to customize which patterns to keep
- Needs visibility into what Piper learned

**Design challenge**: Support journey from skeptic to power user

---

## Questions to Answer in Your Design

### Core Experience

1. **Discovery**: How does user first learn about suggestions?
2. **Visibility**: How does user know suggestions are available?
3. **Engagement**: What motivates user to interact with suggestions?
4. **Feedback**: How does user understand their feedback matters?
5. **Control**: How does user manage/disable suggestions?

### Interaction Details

6. **Accept flow**: What happens after clicking Accept?
7. **Reject flow**: What happens after clicking Reject?
8. **Dismiss flow**: Different from Reject?
9. **Qualitative feedback**: When/how to ask for more details?
10. **Undo**: Can user reverse a decision?

### Visual Design

11. **Attention**: How to make suggestions noticeable but not annoying?
12. **Hierarchy**: How to show priority between multiple suggestions?
13. **Context**: How to explain why this suggestion now?
14. **Trust**: How to communicate confidence/reliability visually?
15. **Branding**: How to maintain Piper's collaborative, building-in-public aesthetic?

---

## Success Criteria

Your design will be successful if:

**User Perspective**:
- ✅ User immediately understands what suggestions are
- ✅ User feels helped, not nagged or manipulated
- ✅ User knows how to accept, reject, or ignore suggestions
- ✅ User trusts Piper's learning is transparent and controllable
- ✅ User can quickly act on valuable suggestions

**Business Perspective**:
- ✅ Suggestions drive user engagement (accept rate >30%)
- ✅ Users don't disable suggestions (retention >80%)
- ✅ Learning improves over time (confidence increases)
- ✅ Differentiation from competitors (unique value)
- ✅ Scales to team usage (Level 3 roadmap)

**Technical Perspective**:
- ✅ Implementable in vanilla JS (<5 hours frontend work)
- ✅ No performance impact (<100ms)
- ✅ Accessible (WCAG 2.1 AA compliant)
- ✅ Testable (can validate with real users)

---

## Inspiration & References

### Design Systems to Consider

- **GitHub's notification system**: Subtle, informative, actionable
- **Slack's message actions**: Contextual, low-friction interactions
- **VS Code's suggestions**: Developer-friendly, keyboard-accessible
- **Notion's AI blocks**: Inline, natural integration
- **Linear's predictive commands**: Fast, confidence-building

### Research to Review (Optional)

You've been provided:
- [Architecture Research](phase-3-architecture-research.md): Technical constraints
- [Decision Document](phase-3-decisions.md): Current thinking
- [Gameplan 300](gameplan-300-learning-basic-revised.md): Full context

### Visual Design References

Piper Morgan aesthetic:
- Teal-orange color palette (not bright/playful)
- Partnership over personality (no cute mascots)
- Professional yet approachable
- Geometric abstraction over illustration
- Clean typography, plenty of whitespace

---

## Output Format

### Document Structure

```markdown
# Phase 3 Suggestions UI/UX Design Proposal
**Designer**: [Your name/role]
**Date**: November 13, 2025
**Version**: 1.0

## Executive Summary
[2-3 paragraphs: Your recommendation, key insights, why this approach]

## Design Principles
[3-5 principles guiding this design]

## Recommended Approach
[Detailed description of your recommended interaction pattern]

### User Flow
[Step-by-step journey with rationale for each step]

### Visual Design
[Wireframes/mockups/descriptions - ASCII art is fine!]

### Microcopy
[Exact text for buttons, labels, explanations]

### Mobile Considerations
[How design adapts to smaller screens]

## Alternative Approaches Considered
[2-3 other options with pros/cons, why not recommended]

## Implementation Notes
[Guidance for developers - what to build first, what's complex]

## Success Metrics
[How to measure if this design works]

## Open Questions
[What needs user testing? What assumptions need validation?]

## Next Steps
[What happens after design approval]
```

---

## Remember

**You are the UX expert here**. Don't just validate our current thinking - push back if you see better approaches. We want:

- 🎯 **User-centered thinking**: What's best for the PM, not what's easiest to build
- 🎨 **Creative solutions**: Novel patterns that fit Piper's philosophy
- 📊 **Evidence-based**: Reference best practices from other products
- 🏗️ **Practical**: Must be implementable, not just beautiful
- 🔬 **Testable**: Clear success criteria and validation approach

**This is a real product** with real users coming in Alpha. Your design will directly impact whether users trust and value Piper's learning system.

**Building in public**: Your design should feel transparent, educational, and empowering - not black-box AI magic.

---

## Questions for Us?

If anything is unclear or you need more context:
- What existing UI looks like
- Technical constraints
- User research findings
- Product roadmap
- Competitive analysis

Just ask! We want you to have everything needed for great design work.

---

**Status**: Ready for UX specialist
**Expected Duration**: 1-2 hours
**Deliverable**: UX design proposal with wireframes and rationale
**Impact**: Shapes Phase 3 implementation (5 hours of dev work)

---

_"Design is not just what it looks like. Design is how it works."_ - Steve Jobs

_"Good design is obvious. Great design is transparent."_ - Joe Sparano

_"Together we are making something incredible"_ - Xian (Piper's creator)

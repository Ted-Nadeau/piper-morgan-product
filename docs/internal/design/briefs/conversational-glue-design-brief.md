# Design Brief: Conversational Glue for Piper Morgan

**Document Type**: Design Brief
**For Review By**: Principal Product Manager, Chief Experience Officer
**Created By**: Chief Architect
**Date**: December 26, 2025
**Status**: Draft for Discussion

## Executive Summary

Piper currently operates in a command-response paradigm. Users issue queries, Piper responds, interaction ends. This creates a fragmented experience where users must know exactly what to ask and cannot discover capabilities naturally through conversation.

We need "conversational glue" - the connective tissue that transforms isolated interactions into flowing dialogue, making Piper feel like a collaborative colleague rather than a command processor.

## Problem Statement

### Current User Experience Gaps

1. **Discovery Friction**: Users don't know what Piper can do
   - "Menu of services" returns generic response
   - No progressive disclosure of capabilities
   - Must know exact commands to succeed

2. **Context Fragmentation**: Each query starts fresh
   - "Show me that issue" → "Which issue?"
   - No memory of just-discussed topics
   - Repeated context establishment

3. **Dead-End Interactions**: Responses don't lead anywhere
   - User: "Generate standup" → Piper: [standup] → END
   - No natural next actions
   - No proactive assistance

4. **Cognitive Load**: Users must drive everything
   - Remember all commands
   - Explicitly request each step
   - Connect related actions manually

### Impact on Alpha Testing

From December testing:
- Users trying natural phrases fail ("What services do you offer?")
- Testers don't discover capabilities without documentation
- Conversations feel mechanical, not collaborative
- High abandonment after first interaction

## Vision: Piper as Conversational Colleague

### Design Principles

1. **Natural Discovery**: Capabilities revealed through dialogue
2. **Contextual Continuity**: Conversations build and flow
3. **Proactive Assistance**: Anticipate logical next steps
4. **Progressive Disclosure**: Right amount of info at right time
5. **Personality Consistency**: Piper feels like the same "person"

### Example: Current vs. Desired

**Current Experience**:
```
User: Hi
Piper: Hello! I'm Piper, your PM assistant. I can help with task management.

User: What can you do?
Piper: I can help you with various tasks.

User: Show me my tasks
Piper: Error: No integration configured
```

**Desired Experience**:
```
User: Hi
Piper: Good morning! I'm Piper. I can help with tasks, documentation,
        and team coordination. What's on your mind today?

User: What can you do?
Piper: I can help with:
        • Managing todos and projects
        • Creating GitHub issues and tracking PRs
        • Generating daily standups
        • Scheduling meetings and finding calendar time
        • Searching and organizing documents

        What would be most helpful right now?

User: Show me my tasks
Piper: I'll need to connect to your task system first. Would you like to:
        • Connect GitHub for issue tracking
        • Use my built-in todo list
        • Import from another system?
```

## Core Components of Conversational Glue

### 1. Context Awareness System

**What It Tracks**:
- Last 3-5 conversation turns
- Entities mentioned (projects, people, dates)
- User's current task/goal
- Time of day and user patterns

**How It's Used**:
- Resolve pronouns ("it", "that", "the project")
- Maintain topic continuity
- Inform response tone and detail level
- Prioritize relevant suggestions

### 2. Capability Discovery Patterns

**Progressive Revelation**:
- Start with categories, not exhaustive lists
- Reveal details based on interest signals
- Learn from usage patterns
- Surface underused features contextually

**Discovery Mechanisms**:
- Conversational menus ("I can help with X, Y, or Z")
- Contextual suggestions ("Since you mentioned deadlines...")
- Feature spotlights ("Did you know I can also...")
- Help system integration

### 3. Next-Action Suggestions

**After Each Response, Consider**:
- Logical next steps
- Related capabilities
- Preventable problems
- Workflow completion

**Suggestion Patterns**:
```
"I've generated your standup. Would you like me to:
 • Post it to Slack
 • Create issues for the blockers
 • Schedule time to address them?"
```

### 4. Personality & Tone

**Key Attributes**:
- Helpful but not pushy
- Knowledgeable but not condescending
- Proactive but not intrusive
- Professional but approachable

**Adaptation Patterns**:
- Match formality to user's tone
- Adjust verbosity to user's preference
- Learn communication patterns over time

## Design Decisions Needed

### 1. Proactivity Level

**Option A: Minimalist**
- Only respond to direct queries
- No unsolicited suggestions
- Clean, simple interactions
- Risk: Misses opportunities to help

**Option B: Assistant**
- Suggest related actions
- Offer relevant capabilities
- Moderate proactivity
- Risk: Might feel slightly pushy

**Option C: Colleague**
- Anticipate needs
- Proactive problem-solving
- High engagement
- Risk: Could be overwhelming

**Recommendation**: Start with B, allow user preference

### 2. Context Persistence

**Option A: Conversation Only**
- Context lasts current session
- Fresh start each conversation
- Simple, predictable
- Risk: Repetitive interactions

**Option B: 24-Hour Window**
- Remember recent interactions
- Refer to "yesterday" naturally
- More continuity
- Risk: Privacy concerns

**Option C: Full History**
- Complete memory with decay
- Deep personalization
- Most natural
- Risk: Complex, privacy issues

**Recommendation**: B with user control

### 3. Suggestion Frequency

**After Every Response?**
- Maximum discoverability
- Risk: Annoying

**Only on Dead Ends?**
- Minimal intrusion
- Risk: Missed opportunities

**Context-Dependent?**
- Smart but complex
- Risk: Inconsistent

**Recommendation**: Context-dependent with throttling

## Success Metrics

### Quantitative
- Conversation depth (turns per session)
- Discovery success (features found without docs)
- Task completion rate
- Return user rate
- Commands per outcome (fewer is better)

### Qualitative
- "Feels like a colleague"
- "Easy to discover features"
- "Remembers our context"
- "Helpful without being annoying"
- "Natural to interact with"

## Implementation Phases

### Phase 1: Foundation (Beta)
- Basic context tracking (current conversation)
- Simple next-action suggestions
- Capability menus
- Graceful discovery fallbacks

### Phase 2: Enhancement (v1.0)
- Multi-turn context
- Learned user preferences
- Proactive suggestions
- Personality consistency

### Phase 3: Intelligence (v1.1)
- Pattern recognition
- Workflow learning
- Team awareness
- Predictive assistance

## Technical Considerations

### Architecture Requirements
- Session state management
- Context storage (Redis/Database)
- Performance (<50ms context retrieval)
- Fallback handling

### Integration Points
- Intent classification system
- Response generation
- User preference storage
- Analytics pipeline

## Open Questions for Product/Design

1. **Personality Definition**
   - How much personality is too much?
   - Should Piper use "I" or "we"?
   - Humor appropriate? When?
   - Emoji usage?

2. **Error Handling Tone**
   - How apologetic for failures?
   - Technical detail level?
   - Recovery suggestions?

3. **Onboarding Flow**
   - How to introduce capabilities?
   - Tutorial vs. discovery?
   - Progressive complexity?

4. **Team Dynamics**
   - Shared context across team?
   - Privacy boundaries?
   - Collaborative features?

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Too chatty | User annoyance | Preference controls, throttling |
| Not chatty enough | Poor discovery | Progressive disclosure, help system |
| Context confusion | Wrong assumptions | Explicit confirmation, context reset |
| Privacy concerns | Trust issues | Clear boundaries, user control |
| Inconsistent personality | Uncanny valley | Style guide, testing |

## Recommendation

Start with conservative implementation in Beta:
1. Basic context tracking (current session)
2. Simple capability menus
3. Modest next-action suggestions
4. Clear personality guidelines

Iterate based on user feedback, gradually increasing sophistication.

## Next Steps

1. **Product Review**: PPM validates vision alignment
2. **Design Session**: CXO creates interaction patterns
3. **User Research**: Test conversation flows with alpha users
4. **Prototype**: Build minimal conversation engine
5. **A/B Testing**: Compare interaction patterns

## Appendix: Conversation Flow Examples

### Morning Checkin
```
Piper: Good morning! You have 3 todos due today and a standup in an hour.
       Would you like me to help you prepare?

User: Yes, let's do the standup

Piper: I'll generate your standup based on yesterday's GitHub activity.
       Should I include the PR that's been waiting for review?

User: Oh right, which PR?

Piper: PR #456 "Fix authentication flow" - Sarah has been waiting
       since Wednesday. After your standup, shall I schedule time
       to review it?
```

### Discovery Flow
```
User: I need help with project management

Piper: I can help you:
       • Track todos and tasks
       • Manage GitHub issues and PRs
       • Generate status reports
       • Coordinate with your team

       What aspect would be most helpful?

User: GitHub stuff

Piper: For GitHub, I can:
       • Create and update issues
       • Track PR status
       • Show what shipped this week
       • Identify blockers

       Do you want to create an issue or check on existing work?
```

### Context Continuity
```
User: Show me the authentication PR

Piper: Here's PR #456 "Fix authentication flow":
       - Author: Sarah
       - Status: Awaiting your review
       - Changed: 5 files, +247/-183 lines

       Would you like me to summarize the changes?

User: Is it related to the bug we discussed?

Piper: Yes, this PR addresses the FK violation bug from December 17
       where the setup wizard was failing. Sarah's fix prevents
       premature commits in the user_api_key service.
```

---

*This brief presents the conversational glue concept for product and design review. Technical implementation details deliberately minimized in favor of user experience focus.*

# Play Acting Piper Morgan - Context Package Design
*Version 1.0 - August 8, 2025*

## Purpose
This document defines the context package for the "Play Acting Piper Morgan" Claude Project, used for benchmarking the actual Piper Morgan assistant against a well-contexted Claude baseline.

## Design Principles
1. **PM Perspective**: Include what a PM would naturally have, exclude implementation details
2. **Behavioral Clarity**: Teach work patterns without revealing Piper's architecture
3. **Measurable Boundaries**: Clear enough context to be effective, bounded enough to test Piper's advantages
4. **Evolution Tracking**: Document all context changes for experiment validity

---

## Project Instructions (Custom Instructions)

```markdown
You are acting as a senior Product Manager's AI assistant. Your role is to help with product management tasks including feature planning, bug triage, stakeholder communication, and strategic thinking.

## Your PM Context
You work with Christian (xian), a Principal Product Manager who:
- Values systematic thinking and clear documentation
- Prefers breaking large problems into digestible steps
- Runs morning standups to orient the day
- Appreciates honest assessment over optimistic projections
- Works on multiple projects including Piper Morgan (an AI PM assistant) and Kind Systems

## Work Style Preferences
- **Communication**: Concise but complete. Skip unnecessary pleasantries.
- **Problem-solving**: Start with verification before action. Check assumptions.
- **Documentation**: Capture decisions and rationale, not just outcomes
- **Estimates**: Provide ranges with confidence levels, not false precision
- **Status Updates**: Include blockers early, celebrate wins briefly

## Core PM Workflows You Support

### Morning Standup
When asked for morning standup:
1. Review calendar for today's meetings
2. Identify top 3 priorities based on urgency/importance
3. Flag any blockers or dependencies
4. Suggest time blocks for deep work

### Bug Triage
When presented with a bug:
1. Assess severity (Critical/High/Medium/Low)
2. Identify likely affected users
3. Suggest investigation steps
4. Recommend priority relative to current sprint

### Feature Planning
When discussing features:
1. Start with user problem, not solution
2. Consider technical feasibility within constraints
3. Identify MVP vs nice-to-have elements
4. Flag potential risks or dependencies

### Stakeholder Communication
When drafting communications:
1. Lead with key decision/action needed
2. Provide context briefly
3. Include clear next steps
4. Anticipate likely questions

## Response Guidelines
- Acknowledge uncertainty when you have it
- Offer alternatives when blocking issues arise
- Remember context between messages in a session
- Ask clarifying questions rather than making assumptions
- Flag when you need more context to be helpful

You don't have access to actual code, internal systems, or real-time data unless explicitly provided. Work with what's shared in the conversation.
```

---

## Knowledge Base Documents

### Tier 1: Essential Context (Add First)

#### 1. Product Overview (`piper-morgan-product-overview.md`)
```markdown
# Piper Morgan Product Overview

## Vision
An AI-powered Product Manager assistant that understands PM workflows, automates routine tasks, and provides intelligent support for strategic decisions.

## Target Users
- Product Managers overwhelmed by administrative tasks
- PM teams wanting consistent processes
- Organizations scaling PM practices

## Core Capabilities
- Daily standup facilitation
- Bug triage and prioritization
- Feature specification assistance
- Stakeholder communication drafting
- Sprint planning support
- Knowledge management across projects

## Key Differentiators
- Understands PM-specific workflows
- Maintains context across sessions
- Integrates with existing tools (Slack, GitHub, Jira)
- Learns team-specific patterns over time
```

#### 2. Common Workflows (`pm-workflows-guide.md`)
```markdown
# PM Workflows Guide

## Daily Standup Routine
1. Review calendar and commitments
2. Check overnight alerts/messages
3. Identify top 3 priorities
4. Block time for deep work
5. Flag any blockers for resolution

## Bug Triage Process
1. Reproduce/verify the issue
2. Assess user impact (how many, how severe)
3. Check for workarounds
4. Estimate fix effort
5. Assign priority based on impact/effort
6. Communicate decision to stakeholders

## Feature Request Handling
1. Understand the underlying problem
2. Validate with user research/data
3. Define success metrics
4. Create rough specifications
5. Get engineering estimates
6. Make go/no-go recommendation

[Additional workflows...]
```

#### 3. Communication Templates (`communication-patterns.md`)
```markdown
# Communication Patterns

## Bug Status Update
**Subject**: [BUG-XXX] Status Update - [Brief Description]

**Current Status**: [Investigation/In Progress/Ready for QA/Resolved]
**Impact**: [X users affected, Y severity]
**Next Steps**: [Specific actions with owners]
**ETA**: [Best estimate or range]

## Feature Proposal
**Problem**: [User problem we're solving]
**Proposed Solution**: [High-level approach]
**Success Metrics**: [How we'll measure success]
**Resources Needed**: [Team, time, dependencies]
**Recommendation**: [Go/No-go with rationale]

[Additional templates...]
```

### Tier 2: Domain Context (Add for Richer Testing)

#### 4. Project Context (`current-projects.md`)
- Active projects and their goals
- Key stakeholders for each
- Recent decisions and rationale
- Upcoming milestones

#### 5. Team Dynamics (`team-structure.md`)
- Who does what
- Communication preferences by person
- Meeting cadences
- Decision-making processes

#### 6. Historical Patterns (`lessons-learned.md`)
- Common failure modes in past projects
- Successful patterns to repeat
- Technical constraints to remember
- Stakeholder preferences discovered

### Tier 3: Reference Materials (Add as Needed)

- Bug tracking conventions
- Priority definitions
- Release process overview
- Customer segment definitions
- Competitive landscape summary

---

## Context Evolution Protocol

### When to Update Context
1. **After each benchmark**: Note what context was missing
2. **Monthly review**: Prune outdated information
3. **Pattern recognition**: When Claude repeatedly needs same info
4. **Process changes**: When workflows evolve

### How to Document Changes
```markdown
## Context Change Log

### [Date] - Version X.X
**Added**: [What was added and why]
**Modified**: [What was changed and rationale]
**Removed**: [What was removed as outdated]
**Impact**: [How this affects benchmarking]
```

### Versioning Strategy
- Major version: Significant workflow changes
- Minor version: Document additions/updates
- Patch version: Typo fixes, clarifications

---

## Benchmark Test Design Guidelines

### What Makes a Good Test
1. **Bounded**: Can be completed in one session
2. **Realistic**: Actual PM task, not contrived
3. **Measurable**: Clear success criteria
4. **Revealing**: Shows differences in approach

### Example First Test: "Users Can't Log In"

**Setup for Both Systems**:
"I just got a report that several users can't log in to the product this morning. Help me handle this."

**What We're Measuring**:
- Initial questions asked
- Triage approach
- Stakeholder communication suggested
- Investigation steps recommended
- Priority assessment

**Success Criteria**:
- Identifies severity correctly
- Asks about scope/pattern
- Suggests appropriate communication
- Provides clear next steps
- Considers business impact

---

## Notes on Experimental Design

### Avoiding Contamination
- Run tests on different days when possible
- Use predetermined scenarios
- Rotate which system goes first
- Document your state of mind (rushed? focused?)

### Measuring Effort
- Time to useful response
- Number of clarifications needed
- Cognitive load (subjective 1-5)
- Actionability of suggestions

### Recording Results
Create a simple tracker with:
- Date/time of test
- Scenario used
- Claude response summary
- Piper response summary
- Winner and why
- Lessons learned
- Context gaps identified

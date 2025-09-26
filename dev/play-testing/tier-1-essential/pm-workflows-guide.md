# PM Workflows Guide

## Daily Standup Routine

### Morning Orientation Process
1. **Calendar Review** (2 min)
   - Scan for must-attend meetings
   - Note any deadline-driven items
   - Check for stakeholder availability windows

2. **Message Triage** (5 min)
   - Slack: Check #incidents, #product, direct messages
   - Email: Flag anything requiring response today
   - GitHub: Review overnight PR comments and issues

3. **Priority Stack Building** (3 min)
   - Identify top 3 must-do items
   - Consider: urgency, importance, dependencies
   - Flag any blockers needing immediate resolution

4. **Time Blocking** (2 min)
   - Reserve 2-hour deep work block (usually 10am-noon)
   - Buffer time around meetings (15 min minimum)
   - Protect end-of-day wrap-up time

5. **Team Communication** (3 min)
   - Post priorities in team channel
   - Flag any dependencies on others
   - Offer help if ahead of schedule

### Christian's Standup Format
```
Morning update:
1. Today's focus: [Main goal]
2. Blockers: [What's stopping progress]
3. Needs from team: [Specific asks]
4. Available to help with: [Capacity to assist]
```

## Bug Triage Process

### Severity Assessment Framework

#### Critical (P0)
- **Definition**: System unusable, data loss, security breach
- **Response**: Drop everything, all-hands response
- **Timeline**: Fix within 4 hours
- **Communication**: Executive escalation within 30 minutes

#### High (P1)
- **Definition**: Major feature broken, significant user impact
- **Response**: Fix in current sprint
- **Timeline**: Fix within 48 hours
- **Communication**: Stakeholder notification within 2 hours

#### Medium (P2)
- **Definition**: Feature degraded, workaround available
- **Response**: Fix in next sprint
- **Timeline**: Fix within 2 weeks
- **Communication**: Include in weekly status

#### Low (P3)
- **Definition**: Minor issue, cosmetic, edge case
- **Response**: Backlog for future consideration
- **Timeline**: Quarterly cleanup
- **Communication**: Log only

### Bug Investigation Steps
1. **Reproduce** - Can you make it happen?
2. **Scope** - How many users affected?
3. **Workaround** - Is there an alternative path?
4. **Root Cause** - What actually broke?
5. **Fix Effort** - How long to resolve?
6. **Regression Risk** - What might break if we fix it?

### Bug Communication Template
```
Bug Update: [BUG-XXX]
Severity: [P0-P3]
Impact: [X users, Y% of feature]
Status: [Investigating/Fix in progress/Ready for QA]
Workaround: [If available]
ETA: [Best estimate]
Next steps: [Specific actions]
```

## Feature Request Handling

### Intake Process
1. **Problem Validation**
   - What problem does this solve?
   - How are users solving it today?
   - What's the cost of not solving it?

2. **User Research**
   - How many users have asked?
   - What segments are affected?
   - Is this a vocal minority or silent majority?

3. **Solution Exploration**
   - What's the simplest solution?
   - What would delight users?
   - What's technically feasible?

### Prioritization Framework (RICE)
- **Reach**: How many users per quarter?
- **Impact**: How much will it help? (3=massive, 2=high, 1=medium, 0.5=low)
- **Confidence**: How sure are we? (100%=high, 80%=medium, 50%=low)
- **Effort**: Person-months required

**RICE Score = (Reach × Impact × Confidence) / Effort**

### Feature Specification Template
```markdown
## Feature: [Name]

### Problem Statement
[User problem in their words]

### Proposed Solution
[High-level approach]

### Success Metrics
- Primary: [Key metric]
- Secondary: [Supporting metrics]

### MVP Scope
- Must have: [Core elements]
- Nice to have: [Enhancements]
- Out of scope: [Explicitly excluded]

### Risks & Dependencies
- Technical: [Architecture concerns]
- Product: [User experience risks]
- Timeline: [External dependencies]

### Rough Sizing
- Engineering: [X weeks]
- Design: [Y weeks]
- QA: [Z weeks]
```

## Sprint Planning Support

### Pre-Sprint Preparation
1. **Backlog Grooming** (2 hours before sprint)
   - Review all tickets for clarity
   - Ensure acceptance criteria defined
   - Get final estimates from engineering

2. **Capacity Planning**
   - Account for holidays/PTO
   - Reserve 20% for bugs/interrupts
   - Consider on-call rotation impact

3. **Stakeholder Alignment**
   - Confirm priorities with leadership
   - Flag any external dependencies
   - Set realistic expectations

### During Sprint Planning
1. **Goal Setting** - One clear sprint goal
2. **Commitment** - Team agrees on scope
3. **Risk Review** - Identify potential blockers
4. **Success Criteria** - Define "done"

### Sprint Communication
```
Sprint X Planning Complete
Goal: [One sentence goal]
Key Deliverables:
- [Feature/fix 1]
- [Feature/fix 2]
- [Feature/fix 3]
Risks: [Main concerns]
Dependencies: [External needs]
```

## Stakeholder Communication Patterns

### Update Cadences
- **Daily**: Critical issues only
- **Weekly**: Status reports, metrics
- **Biweekly**: Sprint reviews, demos
- **Monthly**: Strategic alignment, roadmap
- **Quarterly**: OKR reviews, planning

### Communication by Audience

#### Engineering
- Lead with technical context
- Focus on implementation details
- Discuss tradeoffs explicitly
- Respect their expertise

#### Executive
- Start with business impact
- Use metrics and data
- Provide clear recommendations
- Anticipate strategic questions

#### Sales/CS
- Emphasize customer value
- Provide talking points
- Share competitive positioning
- Set realistic timelines

#### Users
- Focus on benefits, not features
- Use their language, not jargon
- Show, don't just tell
- Acknowledge current pain

## Knowledge Management

### Documentation Standards
- **Decision Records**: Why we chose X over Y
- **Feature Specs**: What we're building and why
- **Post-Mortems**: What went wrong and lessons learned
- **Process Docs**: How we work together

### Information Hierarchy
1. **Source of Truth**: One canonical location
2. **Cross-References**: Link liberally
3. **Versioning**: Date and author all changes
4. **Archival**: Move outdated content, don't delete

### Meeting Notes Template
```
Date: [YYYY-MM-DD]
Attendees: [Names]
Purpose: [Why we met]

Key Decisions:
- [Decision 1 + rationale]
- [Decision 2 + rationale]

Action Items:
- [ ] [Action] - Owner - Due date
- [ ] [Action] - Owner - Due date

Open Questions:
- [Question needing follow-up]

Next Steps:
- [What happens next]
```

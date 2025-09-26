# Communication Patterns

## Bug Communications

### Critical Bug Escalation
**Subject**: 🔴 CRITICAL: [Brief description] - Immediate action required

**Current Situation**:
- What's broken: [Specific functionality]
- Users affected: [Number and segment]
- Business impact: [Revenue/usage metrics]

**Actions Taken**:
- [X] Incident response team activated
- [X] Root cause identified: [Brief explanation]
- [ ] Fix deployed to staging
- [ ] Production deployment

**ETA**: [Specific time] for resolution

**Need From You**: [Specific ask or FYI only]

---

### Bug Status Update (Standard)
**Subject**: [BUG-XXX] Status Update - [Brief Description]

**Summary**: [One sentence current state]

**Details**:
- Severity: [P0-P3]
- Users affected: [Specific number or percentage]
- Current status: [Investigation/In Progress/Ready for QA/Resolved]
- Workaround: [If available]

**Next Steps**:
- [ ] [Specific action] - [Owner] - [Timeline]
- [ ] [Specific action] - [Owner] - [Timeline]

**ETA**: [Date/time for resolution]

---

## Feature Communications

### Feature Proposal to Leadership
**Subject**: Product Proposal: [Feature Name] - Decision needed by [Date]

**Recommendation**: [GO/NO-GO/DEFER] - [Feature name]

**The Opportunity**:
- Problem: [User problem in one sentence]
- Impact: [X users, $Y revenue potential]
- Confidence: [High/Medium/Low based on data]

**Proposed Solution**:
- Approach: [2-3 sentences max]
- Timeline: [X weeks with Y engineers]
- Success metric: [Primary KPI]

**Tradeoffs**:
- If we do this: [What we gain and lose]
- If we don't: [Risk and opportunity cost]

**Decision Needed**:
Approve [X engineers for Y weeks] starting [date]

**Appendix**: [Link to detailed spec]

---

### Feature Announcement to Team
**Subject**: Shipping this week: [Feature name]

**What's New**: [One sentence description]

**Why It Matters**:
- User problem solved: [Specific pain point]
- Business impact: [Metric improvement expected]

**What to Know**:
- Rollout plan: [Percentage, segments, timeline]
- Success metrics: [What we're tracking]
- Feedback channel: [Where to send user feedback]

**Resources**:
- [Customer facing docs]
- [Internal FAQ]
- [Demo video]

**Thank You**: [Specific callouts to team members]

---

## Status Reports

### Weekly Status to Stakeholders
**Subject**: Product Status - Week of [Date]

**On Track** ✅
- [Project/feature]: [Brief status]
- [Project/feature]: [Brief status]

**Needs Attention** ⚠️
- [Issue]: [Impact and resolution plan]

**Completed This Week** 🎉
- [Achievement with metric]

**Next Week Focus**:
1. [Priority 1]
2. [Priority 2]
3. [Priority 3]

**Metrics Snapshot**:
- [KPI 1]: [Current] (Target: [X])
- [KPI 2]: [Current] (Target: [Y])

---

### Sprint Review Summary
**Subject**: Sprint [X] Complete - [Sprint goal achieved? YES/NO]

**Sprint Goal**: [What we committed to]

**Delivered**:
- ✅ [Feature/fix] - [Impact]
- ✅ [Feature/fix] - [Impact]
- ⏸️ [Carried over] - [Why and when]

**Metrics**:
- Velocity: [X points] (Average: [Y])
- Bug escape rate: [X%]
- Sprint commitment met: [X%]

**Learnings**:
- What worked: [Process improvement]
- What didn't: [Problem to solve]

**Next Sprint Preview**: [One sentence goal]

---

## Stakeholder Requests

### Saying No Diplomatically
**Subject**: Re: [Original request]

Thanks for thinking of us for [request].

**Current Situation**:
We evaluated this against our Q[X] priorities and current commitments.

**Assessment**:
- Value: [Acknowledge the merit]
- Timing: [Why now isn't right]
- Alternative: [What we can offer instead]

**Recommendation**:
Let's revisit this in [timeframe] when [condition].

In the meantime, [alternative solution or workaround].

Happy to discuss if you'd like to explore tradeoffs with current priorities.

---

### Asking for Resources
**Subject**: Resource Request - [Project name] acceleration

**Ask**: [Specific number] additional [engineers/designers] for [timeframe]

**Context**:
- Current trajectory: [Date] delivery
- With resources: [Earlier date] delivery
- Business value of acceleration: [Specific impact]

**Tradeoff Analysis**:
- Option A: Stay the course - [Implications]
- Option B: Add resources - [Benefits and costs]
- Option C: Reduce scope - [What we'd cut]

**Recommendation**: Option [X] because [rationale]

**Decision needed by**: [Date] to maintain accelerated timeline

---

## Meeting Communications

### Meeting Prep Email
**Subject**: [Meeting topic] - Pre-read for [Date]

**Meeting Purpose**: [Decision/Discussion/Update]

**Pre-read** (5 min):
- Context: [2-3 bullets]
- Options: [If decision meeting]
- Questions: [What we need to resolve]

**Desired Outcome**: [Specific result]

**If you only have 30 seconds**: [Key point]

---

### Meeting Follow-up
**Subject**: [Meeting topic] - Decisions and next steps

**Key Decisions**:
1. [Decision]: [Rationale]
2. [Decision]: [Rationale]

**Action Items**:
- [ ] [Action] - @[Owner] - Due: [Date]
- [ ] [Action] - @[Owner] - Due: [Date]

**Open Questions** (for offline follow-up):
- [Question] - @[Owner to investigate]

**Next Meeting**: [If needed, when and why]

---

## Customer Communications

### Feature Update to Users
**Subject**: You asked, we delivered: [Feature name]

Hi [Name],

Remember when you mentioned [specific pain point]?

We've just shipped [feature] that [specific benefit].

**What's New**:
- [Capability 1]
- [Capability 2]

**Getting Started**: [First step to try it]

We'd love your feedback after you've had a chance to try it.

[CTA button: Try it now]

---

### Incident Communication to Users
**Subject**: [Service] issue - We're on it

**Current Status**: [Investigating/Identified/Fixing/Resolved]

**What Happened**: [Plain language explanation]

**Impact**:
- Who's affected: [Segment]
- What's not working: [Specific features]
- Workaround: [If available]

**Timeline**:
- Issue started: [Time]
- Expected resolution: [Time]

**Updates**: [Where they can check for updates]

We apologize for the inconvenience and are working to resolve this quickly.

---

## Templates for Quick Responses

### Need More Context
"To give you the best recommendation, could you help me understand:
- [Specific question 1]
- [Specific question 2]
That context will help me prioritize this appropriately."

### Bandwidth Challenge
"This is a great idea. Given our current sprint commitments to [current priority], we could:
1. Start this in [timeframe]
2. Swap it for [other item]
3. Find a lighter-weight version
What would work best for your needs?"

### Scheduling Time
"Happy to discuss. I have windows:
- [Option 1]: [Date/time]
- [Option 2]: [Date/time]
- [Option 3]: [Date/time]
30 min should be enough, or let me know if you need more."

### Acknowledging Feedback
"Thanks for flagging this. You're right that [acknowledge specific point].
Let me [specific action] and get back to you by [timeframe]."

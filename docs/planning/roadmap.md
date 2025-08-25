# Roadmap Update - Minimum VALUABLE Product Focus

**Date**: August 24, 2025
**Philosophy Shift**: From feature list to complete user stories
**Target**: 2-3 weeks to "actually useful for Xian" MVP

---

## Current State (End of Week 1)

### Completed Features ✅
- **Morning Standup**: Saves 75 min/week (enhanced tonight with issues)
- **Issue Intelligence**: Smart triage with pattern recognition
- **Configuration Separation**: Multi-user ready
- **Canonical Query Architecture**: The foundation for everything

### Built but Not Connected 🔄
- **Document Memory**: Foundation complete, content implementation in progress (PM-126)
- **Cross-Feature Learning**: Enabled but not fully utilized
- **Persistent Context**: Foundation ready, not integrated

### Not Started ❌
- **Calendar Integration**: Critical for morning context
- **Notion Sync**: Where knowledge actually lives
- **Draft Response Generation**: Complete the issue workflow
- **FTUX Wizard**: Needed before external users

---

## User Stories That Define MVP

### Story 1: "My Morning Startup Routine"
**Current State**: 70% complete
**Needs**: Calendar integration, document context

```
As Xian, when I start my day:
- I run 'piper standup' and see:
  - ✅ My focus for today (Morning Standup)
  - ✅ Priority issues needing attention (Issue Intelligence)
  - ❌ Today's meetings and conflicts (Calendar)
  - 🔄 Context from yesterday (Document Memory)
- Time saved: 15-20 minutes daily
```

### Story 2: "Issue Triage and Response"
**Current State**: 60% complete
**Needs**: Draft generation, Notion context

```
As a PM, when GitHub issues arrive:
- Piper automatically:
  - ✅ Prioritizes by impact (Issue Intelligence)
  - ✅ Detects patterns (Learning System)
  - ❌ Drafts initial responses (Generation needed)
  - ❌ Pulls context from Notion docs (Integration needed)
- Time saved: 30-45 minutes per triage session
```

### Story 3: "What Did We Decide About X?"
**Current State**: 20% complete
**Needs**: Document Memory connection, Notion search

```
As a PM, when I need to recall decisions:
- I ask Piper:
  - ❌ "What did we decide about the auth approach?"
  - ❌ "Find the conversation about pricing"
  - ❌ "Summary of last week's architecture discussion"
- Piper searches across GitHub, Notion, and local docs
- Time saved: 10-15 minutes per search
```

### Story 4: "Project Status at a Glance"
**Current State**: 40% complete
**Needs**: Notion integration, unified view

```
As a PM, when stakeholders ask for status:
- Piper provides:
  - ✅ GitHub velocity and blockages
  - ✅ Issue patterns and risks
  - ❌ Notion project docs status
  - ❌ Unified dashboard view
- Time saved: 30 minutes per status report
```

---

## Three-Week Sprint to MVP

### Week 1: Complete Core Connections (Aug 26-30)
**Theme**: Connect what's built

**Monday**:
- Morning: Pattern Sweep + Enhanced Standup testing
- Afternoon: Document Memory integration (3 hours)
- Result: Standup pulls yesterday's context

**Tuesday**:
- Calendar integration basics (4 hours)
- Test with real calendar data
- Result: Standup shows today's meetings

**Wednesday**:
- Notion API exploration (2 hours)
- Read-only integration first
- Result: Can pull Notion pages

**Thursday**:
- Draft response generation for issues (3 hours)
- Use canonical queries for context
- Result: Issue responses auto-drafted

**Friday**:
- Integration testing day
- Fix connection issues
- Pattern Sweep
- Result: All features talking to each other

### Week 2: Complete User Stories (Sept 2-6)
**Theme**: End-to-end workflows

**Monday-Tuesday**:
- Complete "Morning Startup" story
- All data sources integrated
- Real usage testing

**Wednesday-Thursday**:
- Notion two-way sync
- Knowledge retrieval working
- "What did we decide" story complete

**Friday**:
- FTUX wizard development
- New user can set up in <5 minutes
- Configuration validated

### Week 3: Polish and Ship (Sept 9-13)
**Theme**: Production readiness

**Monday-Tuesday**:
- Performance optimization
- Error handling improvement
- Security review

**Wednesday-Thursday**:
- Documentation completion
- Video walkthrough creation
- External user onboarding prep

**Friday**:
- First external user ships! 🚀
- Feedback collection begins
- Celebration!

---

## Success Metrics for MVP

### Minimum VALUABLE Criteria
- [ ] Saves Xian 2+ hours per week (currently ~1.5 hours)
- [ ] Covers 4 complete user stories end-to-end
- [ ] 1 external user successfully onboarded
- [ ] All features connected via canonical queries
- [ ] Learning system shows measurable improvement

### What We're NOT Shipping in MVP
- Advanced analytics
- Multiple AI model support
- Complex automation workflows
- Team collaboration features
- Mobile interface

---

## Critical Path Items

### Must-Have for MVP
1. **Document Memory Integration** (tomorrow!)
2. **Calendar Basic Integration** (Tuesday)
3. **Notion Read Integration** (Wednesday)
4. **FTUX Wizard** (Week 2)

### Nice-to-Have but Deferrable
- Slack integration
- Voice input
- Predictive analytics
- Custom workflows

---

## Risk Mitigation

### Biggest Risks
1. **Notion API Complexity**: Start with read-only
2. **Calendar Permission Maze**: Use minimal scopes
3. **Performance at Scale**: Optimize in Week 3
4. **User Onboarding**: FTUX wizard critical

### Mitigation Strategy
- Time-box integrations (2 days max each)
- Graceful degradation for all external services
- Manual fallbacks for automation
- Daily testing with real data

---

## The North Star

**By September 13, 2025**:
> Xian runs Piper every morning and throughout the day, saving 2+ hours weekly through connected, intelligent assistance that understands context across GitHub, Calendar, Notion, and previous conversations.

**The Test**: Would Xian feel pain if Piper stopped working?
- If yes → MVP achieved
- If no → Keep connecting features

---

## Next Immediate Actions

1. **Tonight**: Complete Standup + Issues integration (in progress)
2. **Tomorrow 9 AM**: Pattern Sweep then Document Memory
3. **Tuesday**: Calendar integration sprint
4. **Wednesday**: Notion exploration day

---

*This is our contract with ourselves: Ship something VALUABLE, not just viable.*

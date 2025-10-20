# Phase 3 Discovery: Slack Reminder Architecture

**Agent**: Cursor (Chief Architect)
**Issue**: #161 (CORE-STAND-SLACK-REMIND)
**Phase**: 0 - Discovery & Architecture
**Date**: October 20, 2025, 7:35 AM
**Estimated Effort**: 2 hours
**Mission**: Discover existing infrastructure and design reminder architecture

---

## Your Role

You are the **Chief Architect** conducting architectural discovery for the Slack reminder system. Your job is to:

1. **Find what exists** - Scheduler, Slack patterns, user preferences
2. **Assess what's usable** - Can we use it as-is or extend it?
3. **Design the architecture** - How components fit together
4. **Create implementation plan** - Clear tasks for Code agent

**You are NOT implementing** - you're designing and planning.

---

## Mission Objectives

### 1. Find Existing Scheduler System

**Question**: Do we have a scheduler/cron system for daily jobs?

**Search for**:
- Background task management (Pattern-017 exists!)
- Scheduler systems (APScheduler, Celery, etc.)
- Cron job configuration
- Daily job examples
- Task queue systems

**Look in**:
- `services/scheduler/` or `services/background/`
- `services/jobs/` or `services/tasks/`
- Config files mentioning scheduler
- Existing daily jobs
- Pattern-017 implementation

**Deliverable**:
- Found: What exists and where?
- Assessment: Can we use it for daily reminders?
- Recommendation: Use as-is, extend, or build new?

---

### 2. Review Slack DM Patterns

**Question**: How do we send Slack direct messages?

**Search for**:
- Slack DM sending patterns
- SlackClient implementation
- Message formatting examples
- Direct message vs channel messages
- Error handling for Slack API

**Look in**:
- `services/integrations/slack/`
- SlackClient class
- Slack spatial intelligence files
- Existing message formatters
- Slack API interaction patterns

**Deliverable**:
- Patterns: How to send DMs?
- Examples: Any existing DM code?
- Limitations: What to watch out for?
- Recommendation: Best approach for reminder DMs?

---

### 3. Assess User Preference Infrastructure

**Question**: How do we store user preferences?

**Search for**:
- User preference model/class
- Database schema for preferences
- Preference API endpoints
- Configuration storage patterns
- User settings examples

**Look in**:
- `services/domain/user*.py`
- `models/user*.py`
- Database migration files
- User preference APIs
- Configuration management

**Deliverable**:
- Model: Current user preference structure
- Storage: How preferences are saved?
- Extension: How to add reminder preferences?
- Recommendation: Best way to add our fields?

---

### 4. Design Reminder Architecture

**Question**: How should all components integrate?

**Design**:
- Component relationships
- Data flow diagram
- Integration points
- Error handling strategy
- Monitoring approach

**Consider**:
- Daily job triggers scheduler
- Scheduler queries user preferences
- For each enabled user, format message
- SlackClient sends DM
- Log results for monitoring

**Deliverable**:
- Architecture diagram (text/ASCII art)
- Component list with responsibilities
- Integration point descriptions
- Data flow documentation

---

### 5. Create Implementation Plan

**Question**: What tasks should Code agent tackle?

**Break down into**:
- Task 1: Scheduler integration
- Task 2: Slack DM implementation
- Task 3: User preference extension
- Task 4: Message formatting
- Task 5: Testing & monitoring

**For each task**:
- What to build/modify
- Which files to change
- Dependencies on other tasks
- Estimated effort

**Deliverable**:
- Ordered task list for Code
- Clear deliverables per task
- Dependency graph
- Time estimates

---

## Discovery Process

### Step 1: Scheduler Discovery (30 minutes)

```bash
# Search for scheduler systems
find . -type f -name "*schedul*" -o -name "*cron*" -o -name "*job*"

# Search for background task patterns
grep -r "apscheduler\|celery\|background.*task\|cron" --include="*.py"

# Check for Pattern-017 implementation
find . -path "*/pattern-017*" -o -name "*background*task*"

# Look for existing daily jobs
grep -r "daily\|schedule.*job\|cron.*job" --include="*.py"
```

**Document**:
- What exists?
- Where is it?
- How does it work?
- Can we use it?

---

### Step 2: Slack DM Discovery (30 minutes)

```bash
# Find SlackClient implementation
find . -type f -name "*slack*client*"

# Search for DM sending patterns
grep -r "dm\|direct.*message\|post.*message" services/integrations/slack/

# Look for message formatters
find services/integrations/slack/ -name "*format*" -o -name "*message*"

# Check for existing DM examples
grep -r "chat.postMessage\|users.conversations" --include="*.py"
```

**Document**:
- How to send DMs?
- Message formatting patterns?
- Error handling approach?
- Rate limiting considerations?

---

### Step 3: User Preference Discovery (30 minutes)

```bash
# Find user preference models
find . -type f -name "*user*" -path "*/models/*" -o -path "*/domain/*"

# Search for preference storage
grep -r "preference\|settings\|config.*user" --include="*.py"

# Look for user API endpoints
find web/api/routes/ -name "*user*" -o -name "*preference*"

# Check database migrations
ls -la alembic/versions/ | grep -i user
```

**Document**:
- Current preference model?
- How to extend it?
- Database migration needed?
- API endpoints required?

---

### Step 4: Architecture Design (30 minutes)

**Create architecture document** covering:

1. **Component Overview**:
   - StandupReminderJob (scheduler job)
   - ReminderService (business logic)
   - SlackClient (message sending)
   - UserPreferences (configuration)

2. **Data Flow**:
   ```
   Scheduler → ReminderJob → UserPreferences (query) → ReminderService → SlackClient → Slack API
   ```

3. **Integration Points**:
   - With existing scheduler system
   - With Slack infrastructure
   - With user preference system
   - With monitoring/logging

4. **Design Decisions**:
   - Scheduler choice (why?)
   - Message format approach
   - Preference storage strategy
   - Error handling approach

---

## Output Format

Create a comprehensive discovery document with these sections:

### 1. Executive Summary

- What we found
- What we can reuse
- What we need to build
- Overall assessment (easy/medium/hard)

### 2. Infrastructure Assessment

**Scheduler**:
- [ ] Exists: Yes/No
- [ ] Location: path/to/scheduler
- [ ] Can use: Yes/No/With changes
- [ ] Recommendation: [details]

**Slack DM**:
- [ ] Pattern exists: Yes/No
- [ ] Example code: [location]
- [ ] Can use: Yes/No/With changes
- [ ] Recommendation: [details]

**User Preferences**:
- [ ] Model exists: Yes/No
- [ ] Location: [path]
- [ ] Extension needed: Yes/No
- [ ] Recommendation: [details]

### 3. Proposed Architecture

```
[ASCII art diagram]

Component descriptions:
- Component 1: [responsibility]
- Component 2: [responsibility]
...

Data flow:
1. [step]
2. [step]
...

Integration points:
- Point 1: [description]
- Point 2: [description]
...
```

### 4. Implementation Plan

**Task 1: [Name]** (X hours)
- Build: [what]
- Modify: [which files]
- Dependencies: [what must be done first]
- Success criteria: [how to verify]

**Task 2: [Name]** (X hours)
- [same structure]

... (continue for all tasks)

### 5. Risk Assessment

**Technical Risks**:
- Risk 1: [description] → Mitigation: [approach]
- Risk 2: [description] → Mitigation: [approach]

**Integration Risks**:
- Risk 1: [description] → Mitigation: [approach]

### 6. Open Questions

- Question 1?
- Question 2?
- [anything unclear that needs PM decision]

---

## Critical Requirements

### Infrastructure Verification

**Before recommending a component**:
1. ✅ Verify it actually exists
2. ✅ Confirm it's operational
3. ✅ Check it can handle our use case
4. ✅ Document how to use it

**Never assume**:
- ❌ "Probably has a scheduler"
- ❌ "Should be able to send DMs"
- ❌ "User preferences likely support this"

**Always verify**:
- ✅ Find the actual files
- ✅ Read the actual code
- ✅ Confirm actual capabilities
- ✅ Document actual usage

---

### Design Principles

**Keep it simple**:
- Use what exists when possible
- Don't over-engineer
- Clear component boundaries
- Straightforward data flow

**Make it reliable**:
- Error handling at every step
- Monitoring and logging
- Graceful degradation
- Retry mechanisms

**Make it maintainable**:
- Follow existing patterns
- Clear documentation
- Testable components
- DDD-compliant structure

---

## What You're NOT Doing

**You are NOT**:
- ❌ Implementing any code
- ❌ Writing tests
- ❌ Making final decisions without PM
- ❌ Assuming without verifying

**You ARE**:
- ✅ Discovering what exists
- ✅ Assessing what's usable
- ✅ Designing architecture
- ✅ Planning implementation
- ✅ Documenting findings
- ✅ Identifying risks

---

## Success Criteria

Discovery is complete when you deliver:

- [ ] Comprehensive infrastructure assessment
- [ ] Clear architecture design
- [ ] Detailed implementation plan
- [ ] Risk analysis with mitigations
- [ ] All findings documented
- [ ] Open questions identified
- [ ] Ready for PM review & Code implementation

---

## Reference Materials

**From kickoff plan**:
- Phase 3 kickoff plan (context)
- Issue #161 description (requirements)
- Success criteria (7 items)

**From knowledge base**:
- Pattern-017: Background Task Error Handling
- Slack integration guide
- Spatial intelligence patterns
- DDD service patterns

**From codebase**:
- services/integrations/slack/
- Existing scheduler systems
- User preference models
- Background task infrastructure

---

## Time Allocation

- **30 min**: Scheduler discovery
- **30 min**: Slack DM discovery
- **30 min**: User preference discovery
- **30 min**: Architecture design

**Total**: 2 hours

---

## Deliverable

**File**: `dev/2025/10/20/phase-3-discovery-architecture.md`

**Format**: Markdown document with all sections above

**Length**: Comprehensive (likely 3-5 pages)

**Quality**: Production-ready architectural design

---

## Remember

**You are the architect**. Your job is to:
1. Find what exists (verify, don't assume)
2. Assess what works (test, don't guess)
3. Design what's needed (clear, not complex)
4. Plan implementation (specific, not vague)

**PM will review your findings** before authorizing Code to implement.

**Take your time**. Better to spend 2 hours on thorough discovery than waste 8 hours fixing assumptions later.

---

**Ready to start discovery!** 🔍

*Created: October 20, 2025, 7:35 AM*
*By: Lead Developer (Claude Sonnet 4.5)*
*For: Phase 3 Discovery*
*Agent: Cursor (Chief Architect)*

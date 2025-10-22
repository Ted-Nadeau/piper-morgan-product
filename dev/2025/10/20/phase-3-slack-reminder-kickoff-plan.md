# Phase 3: CORE-STAND-SLACK-REMIND (#161) - Kickoff Plan

**Date**: October 20, 2025, 7:30 AM
**Issue**: #161 (CORE-STAND-SLACK-REMIND)
**Sprint**: A4 "Standup Epic"
**Estimated Effort**: 1-1.5 days (8-12 hours)

---

## Executive Summary

**Mission**: Add daily Slack reminder functionality for standup generation, leveraging existing Slack infrastructure to deliver timely DM notifications with configurable user preferences.

**Current State**:
- ✅ Issue #162 (Multi-modal API) COMPLETE
- ✅ Slack integration infrastructure exists
- ✅ MCP Slack adapter operational
- ✅ Spatial intelligence patterns proven

**Target State**:
- Daily standup reminders via Slack DM
- User-configurable reminder times
- Enable/disable via preferences
- 95% delivery reliability
- Graceful error handling

---

## What We're Building

### Core Feature: Daily Standup Reminders

**Reminder Message** (production example):
```
🌅 Good morning! Time for your daily standup.

Generate your standup:
• Web: https://piper-morgan.com/standup
• CLI: `piper standup`
• API: POST /api/standup/generate

Disable reminders: /standup-remind off
```

**Key Capabilities**:
1. Scheduled daily delivery via Slack DM
2. Configurable time per user
3. Multiple generation options (web, CLI, API)
4. Easy opt-out mechanism
5. Reliable delivery (95% target)

---

## Infrastructure Assessment

### What Already Exists ✅

**Slack Integration** (Production-ready):
- `services/integrations/slack/` - 11 files
- SlackResponseHandler with message consolidation
- SlackSpatialAdapter (8-dimensional intelligence)
- SlackClient (API communication)
- Webhook router operational
- OAuth configured

**Architecture Patterns**:
- Spatial intelligence (ADR-038)
- Message consolidation (5-second window)
- Rate limiting (3 workflows/minute)
- Graceful degradation patterns
- DDD-compliant structure

**Related Systems**:
- User preference management (exists)
- API endpoints (#162 complete)
- Authentication system

### What Needs Building 🔨

**1. Scheduler Integration**:
- Daily cron/scheduler system
- Per-user reminder time configuration
- Reliable job execution
- Failure recovery

**2. Slack DM Functionality**:
- Direct message formatting
- Link generation (web, CLI, API)
- Message delivery confirmation
- Error handling for failed sends

**3. User Preference Management**:
- Reminder enabled/disabled flag
- Preferred reminder time
- Timezone handling
- Opt-out mechanism

**4. Testing & Reliability**:
- Unit tests for scheduler
- Integration tests for Slack DM
- Delivery reliability monitoring
- Error scenario handling

---

## Implementation Phases

### Phase 0: Discovery & Architecture (2 hours)

**Objectives**:
- Verify existing scheduler system
- Review Slack DM patterns in codebase
- Assess user preference infrastructure
- Design reminder architecture

**Tasks**:
1. Search for existing scheduler/cron implementation
2. Review Slack DM sending patterns
3. Check user preference model
4. Create architectural design
5. Identify integration points

**Deliverable**: Architecture document with implementation plan

---

### Phase 1: Scheduler Integration (3-4 hours)

**Objectives**:
- Implement daily reminder scheduling
- Configure per-user reminder times
- Ensure reliable execution

**Tasks**:
1. Integrate with scheduler system (or implement simple one)
2. Create reminder job definition
3. Implement per-user time configuration
4. Add job monitoring and recovery
5. Test scheduler reliability

**Success Criteria**:
- [ ] Scheduler runs daily at configured times
- [ ] Per-user time configuration works
- [ ] Jobs execute reliably (>95%)
- [ ] Failure recovery implemented
- [ ] Monitoring in place

**Files to Create/Modify**:
- `services/scheduler/standup_reminder_job.py`
- `services/scheduler/cron_config.py`
- Configuration for scheduler

---

### Phase 2: Slack DM Implementation (2-3 hours)

**Objectives**:
- Format reminder messages
- Send Slack DMs reliably
- Generate correct links

**Tasks**:
1. Create reminder message formatter
2. Implement Slack DM sending
3. Generate web/CLI/API links
4. Add delivery confirmation
5. Implement error handling

**Success Criteria**:
- [ ] Messages formatted correctly
- [ ] DMs sent successfully
- [ ] Links work (web, CLI, API)
- [ ] Delivery confirmed
- [ ] Errors handled gracefully

**Files to Create/Modify**:
- `services/integrations/slack/reminder_service.py`
- `services/integrations/slack/message_formatter.py`
- Integration with SlackClient

---

### Phase 3: User Preferences (2-3 hours)

**Objectives**:
- Extend user preferences for reminders
- Implement enable/disable functionality
- Add timezone handling

**Tasks**:
1. Extend user preference model
2. Add reminder enabled/disabled flag
3. Add preferred reminder time
4. Implement timezone conversion
5. Create preference API endpoints

**Success Criteria**:
- [ ] User can enable/disable reminders
- [ ] User can set preferred time
- [ ] Timezone handled correctly
- [ ] Preferences persist
- [ ] API endpoints work

**Files to Create/Modify**:
- `services/domain/user_preferences.py` (extend)
- `web/api/routes/preferences.py` (add reminder endpoints)
- Database migration for new fields

---

### Phase 4: Testing & Reliability (2-3 hours)

**Objectives**:
- Comprehensive test coverage
- Verify 95% delivery reliability
- Test error scenarios

**Tasks**:
1. Unit tests for scheduler
2. Unit tests for message formatting
3. Integration tests for DM sending
4. Reliability monitoring tests
5. Error scenario tests

**Success Criteria**:
- [ ] Unit tests passing (>20 tests)
- [ ] Integration tests passing
- [ ] 95% delivery verified
- [ ] Error handling tested
- [ ] Monitoring in place

**Files to Create**:
- `tests/services/test_standup_reminder_job.py`
- `tests/integration/test_slack_reminder.py`
- `tests/services/test_reminder_service.py`

---

### Phase 5: Documentation & Deployment (1 hour)

**Objectives**:
- Document configuration
- Create user guide
- Deployment instructions

**Tasks**:
1. Configuration documentation
2. User preference guide
3. Troubleshooting guide
4. Deployment checklist
5. Session log completion

**Deliverables**:
- Configuration guide
- User documentation
- Deployment checklist

---

## Technical Design

### Architecture Overview

```
┌─────────────────────┐
│  Scheduler/Cron     │
│  (Daily Jobs)       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ StandupReminderJob  │
│ - Check user prefs  │
│ - Get enabled users │
│ - Send reminders    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐     ┌─────────────────────┐
│  ReminderService    │────▶│  SlackClient        │
│  - Format message   │     │  - Send DM          │
│  - Generate links   │     │  - Handle errors    │
└─────────────────────┘     └─────────────────────┘
           │
           ▼
┌─────────────────────┐
│ UserPreferences     │
│ - reminder_enabled  │
│ - reminder_time     │
│ - timezone          │
└─────────────────────┘
```

### Data Model

**User Preferences Extension**:
```python
class UserPreferences:
    # Existing fields...

    # New fields for reminders
    standup_reminder_enabled: bool = True
    standup_reminder_time: time = time(6, 0)  # 6:00 AM
    standup_reminder_timezone: str = "America/Los_Angeles"
    standup_reminder_days: List[int] = [0,1,2,3,4]  # Mon-Fri
```

**Reminder Job**:
```python
class StandupReminderJob:
    """Daily job to send standup reminders"""

    async def execute(self):
        """
        1. Get all users with reminders enabled
        2. Filter by current time + timezone
        3. Send Slack DM to each user
        4. Log results
        """
        pass
```

---

## Integration Points

### With Existing Systems

**1. Slack Integration**:
- Use existing SlackClient for DM sending
- Follow Slack spatial intelligence patterns
- Leverage error handling patterns
- Respect rate limiting

**2. User Preferences**:
- Extend existing preference model
- Use existing preference API patterns
- Integrate with user authentication

**3. API Endpoints** (#162):
- Link to web standup generation
- Reference CLI command
- Include API endpoint URL

**4. Scheduler**:
- Integrate with existing scheduler (if present)
- Or implement simple cron-based system
- Ensure reliable execution

---

## Success Criteria (Detailed)

### Functional Requirements

- [ ] Daily standup reminders sent via Slack DM
- [ ] User can configure reminder time
- [ ] User can enable/disable reminders
- [ ] User can select reminder days (Mon-Fri, etc.)
- [ ] Timezone handling works correctly
- [ ] Reminder message includes all generation links
- [ ] Opt-out mechanism functional

### Quality Requirements

- [ ] 95% delivery reliability achieved
- [ ] Error handling for Slack API failures
- [ ] Graceful degradation when Slack unavailable
- [ ] Monitoring and alerting in place
- [ ] Comprehensive test coverage (>80%)

### Architecture Requirements

- [ ] Follows existing Slack patterns
- [ ] DDD-compliant structure
- [ ] Integration with spatial intelligence
- [ ] Proper error boundaries
- [ ] Performance acceptable (<100ms per reminder)

### User Experience Requirements

- [ ] Reminder message clear and actionable
- [ ] Links work correctly
- [ ] Easy to disable reminders
- [ ] Timezone selection intuitive
- [ ] No spam (respects user preferences)

---

## Risk Assessment

### Technical Risks

**Scheduler Reliability** (Medium):
- Risk: Scheduler may not exist or be unreliable
- Mitigation: Verify existing system, implement fallback
- Contingency: Use simple cron-based approach

**Slack API Rate Limits** (Low):
- Risk: Too many DMs may hit rate limits
- Mitigation: Batch sends, respect rate limits
- Contingency: Queue system for failed sends

**Timezone Complexity** (Medium):
- Risk: Timezone handling can be tricky
- Mitigation: Use standard timezone library
- Contingency: Start with single timezone, expand

**User Preference Storage** (Low):
- Risk: Preference model may need migration
- Mitigation: Check existing model first
- Contingency: Create minimal new table

### Process Risks

**Scope Creep** (Low):
- Risk: Interactive features deferred to MVP
- Mitigation: Clear scope in issue description
- Contingency: Strict adherence to acceptance criteria

**Integration Complexity** (Medium):
- Risk: Slack integration may have quirks
- Mitigation: Use existing patterns
- Contingency: Leverage knowledge from Slack team

---

## Testing Strategy

### Unit Tests

**Scheduler Tests**:
- Job execution timing
- User filtering logic
- Error recovery
- Configuration handling

**Message Formatting Tests**:
- Link generation
- Message structure
- Timezone conversion
- User preference handling

**Preference Tests**:
- Enable/disable functionality
- Time configuration
- Timezone handling
- Validation

### Integration Tests

**Slack DM Tests**:
- Message sending
- Delivery confirmation
- Error handling
- Rate limiting

**End-to-End Tests**:
- Complete reminder flow
- User preference changes
- Opt-out mechanism
- Failure scenarios

### Reliability Tests

**Delivery Reliability**:
- 95% success rate verification
- Retry mechanism testing
- Failure logging
- Alert triggering

---

## Dependencies

### Completed Dependencies ✅

- #162 (CORE-STAND-MODES-API) - API endpoints ready
- Slack infrastructure - Operational
- User authentication - Working
- API documentation - Complete

### External Dependencies

- Slack API availability (99.9% SLA)
- Scheduler system (to be verified)
- Database for preferences
- Monitoring system

---

## Rollout Plan

### Phase 1: Internal Testing (1 day)

- Deploy to development environment
- Test with 1-2 internal users
- Verify delivery reliability
- Fix any critical bugs

### Phase 2: Limited Rollout (2-3 days)

- Enable for 5-10 alpha users
- Monitor delivery metrics
- Gather user feedback
- Iterate on issues

### Phase 3: General Availability (after MVP)

- Enable for all users
- Full monitoring in place
- Documentation published
- Support ready

---

## Monitoring & Observability

### Key Metrics

**Delivery Metrics**:
- Total reminders sent
- Successful deliveries
- Failed deliveries
- Delivery rate (target: >95%)

**User Engagement**:
- Users with reminders enabled
- Opt-out rate
- Time to standup generation after reminder

**System Health**:
- Scheduler job success rate
- Slack API response times
- Error rates
- Queue depth (if implemented)

### Alerting

**Critical Alerts**:
- Delivery rate <90% for 2 consecutive days
- Scheduler job failures
- Slack API errors >10%

**Warning Alerts**:
- Delivery rate 90-95%
- High opt-out rate (>20%)
- Slow Slack API responses

---

## Documentation Requirements

### Technical Documentation

- Architecture design document
- API endpoint documentation
- Preference model updates
- Scheduler configuration guide

### User Documentation

- How to enable reminders
- How to set reminder time
- How to disable reminders
- Timezone selection guide
- Troubleshooting common issues

### Operational Documentation

- Deployment checklist
- Monitoring setup
- Alert response procedures
- Rollback procedures

---

## Estimated Timeline

**Total Effort**: 8-12 hours (1-1.5 days)

| Phase | Duration | Agent |
|-------|----------|-------|
| Phase 0: Discovery | 2 hours | Cursor/Lead Dev |
| Phase 1: Scheduler | 3-4 hours | Code |
| Phase 2: Slack DM | 2-3 hours | Code |
| Phase 3: Preferences | 2-3 hours | Code |
| Phase 4: Testing | 2-3 hours | Code |
| Phase 5: Documentation | 1 hour | Lead Dev |

**Parallel Work Opportunities**:
- Discovery (Cursor) while previous work completes
- Testing can start alongside Phase 3
- Documentation throughout

---

## Next Steps

### Immediate Actions (Today)

1. **Architectural Discovery** (Cursor):
   - Search for existing scheduler system
   - Review Slack DM patterns
   - Assess user preference model
   - Create implementation plan

2. **Issue Breakdown** (Lead Dev):
   - Create task list for Code
   - Prepare agent prompts
   - Set up monitoring for progress

3. **Kickoff Meeting** (PM + Lead Dev):
   - Review this plan
   - Adjust estimates if needed
   - Assign responsibilities
   - Set daily check-ins

### Tomorrow Actions

1. **Phase 1 Implementation** (Code):
   - Scheduler integration
   - Per-user configuration
   - Reliability testing

2. **Phase 2 Implementation** (Code):
   - Slack DM functionality
   - Message formatting
   - Link generation

---

## Success Definition

**Phase 3 is complete when**:

✅ All 7 success criteria met
✅ 95% delivery reliability verified
✅ Tests passing (unit + integration)
✅ Documentation complete
✅ Issue #161 closed
✅ Ready for Phase 4 (Integration & Documentation)

---

*Created: October 20, 2025, 7:30 AM*
*By: Lead Developer (Claude Sonnet 4.5)*
*For: Phase 3 kickoff (CORE-STAND-SLACK-REMIND)*
*Next: Architectural discovery by Cursor*

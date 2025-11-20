# Multi-Channel Suggestions Proposal
## Pattern Suggestions Beyond Web Chat

**Date**: Thursday, November 13, 2025, 4:50 PM PT
**Author**: UX Design Specialist
**For**: Piper Morgan - Issue #300 Learning System
**Context**: Follow-on to web chat suggestions UX design

---

## Executive Summary

Pattern suggestions are **channel-agnostic by design**—the learning system detects patterns regardless of where the user interacts with Piper. This proposal outlines how to surface suggestions across CLI, Slack, and webhooks while maintaining consistency with the web chat design principles.

**Key Insight**: Each channel has different user expectations and interaction models. The underlying data (pattern confidence, reasoning, feedback loop) remains identical, but the **presentation layer must adapt** to each channel's strengths and constraints.

**Recommendation**: Phased rollout with progressive complexity:
1. **Phase 4**: CLI suggestions (developer-friendly, scriptable)
2. **Phase 5**: Slack DM suggestions (where PMs actually work)
3. **Phase 6**: Webhook notifications (proactive, ambient intelligence)

This approach validates core patterns in simpler channels before adding complexity of proactive notifications.

---

## Design Principles (Cross-Channel)

These principles apply across all channels:

### 1. **Channel-Appropriate Presentation**
*"Match the medium"*

CLI users expect terse, scannable text. Slack users expect rich formatting and quick actions. Webhooks enable proactive timing but require careful privacy controls. Design for each channel's strengths.

### 2. **Consistent Core Feedback Loop**
*"Same learning, different interface"*

Accept/Reject/Dismiss should work identically across channels. Confidence scoring, pattern detection, and feedback processing remain unified in the backend. Only presentation differs.

### 3. **Progressive Privacy Controls**
*"More proactive = more explicit consent"*

CLI and web chat are user-initiated (low privacy concern). Slack DMs are contextual but private. Webhooks are proactive and require explicit opt-in with granular controls.

### 4. **Graceful Degradation**
*"Always provide escape hatch"*

Every channel must support `--no-suggestions`, mute options, or disable flags. Users who find suggestions unhelpful should never feel trapped.

### 5. **Cross-Channel Consistency**
*"One Piper, many touchpoints"*

Accepting a pattern in CLI should affect suggestions in web chat. Feedback is unified across channels. Users should feel they're training one assistant, not multiple systems.

---

## CLI Suggestions

### User Context

**Who**: Technical PMs, developers, power users
**When**: During terminal-based workflows
**Expectation**: Terse, scannable, keyboard-driven
**Mental Model**: Like git status or grep output—informative but minimal

### Design Approach: "One-Line Suggestion Banner"

**Philosophy**: CLI users value efficiency over explanation. Show suggestion inline, make acceptance fast, provide detail on demand.

---

### Basic Interaction Pattern

**After command execution**:
```bash
$ piper standup

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Standup Summary (November 13, 2025)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Active:
  • [CORE-123] Implement pattern suggestions
  • [CORE-124] CLI integration
  • [CORE-125] Holistic UX audit

Blocked:
  • [CORE-120] Waiting on design review

Next: Code review for PR #456

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 Suggestion: Create GitHub issue (85% confident)
   [y] Accept  [n] Reject  [?] Details  [s] Skip
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Minimal version** (when confidence >90%):
```bash
💡 Create GitHub issue? [y/n/?/s]:
```

**Ultra-minimal** (high confidence, frequently accepted):
```bash
💡 Issue? [y/n]: _
```

---

### Interaction Options

**User responses**:
- `y` or `yes` → Accept suggestion, record feedback
- `n` or `no` → Reject suggestion (prompt for reason)
- `?` or `details` → Show full explanation
- `s` or `skip` → Dismiss without feedback
- `[Enter]` → Skip (same as `s`)

**Detail view** (`?` pressed):
```bash
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Pattern: Create GitHub issue after standup
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Why: You typically create issues with follow-up
     tasks right after standup—you've done this
     12 times in the past 3 weeks.

Confidence: 85% (12 successes, 2 skips)

Last used: Yesterday, 9:15 AM

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[y] Accept  [n] Reject  [s] Skip
```

---

### Configuration Options

**Global settings** (`~/.piper/config`):
```yaml
suggestions:
  enabled: true
  cli:
    show_suggestions: true
    auto_show_details: false  # Require '?' for full text
    min_confidence: 0.7
    max_per_command: 1  # Only show top suggestion
    format: "minimal"  # "minimal" | "standard" | "detailed"
```

**Command-line flags**:
```bash
# Disable suggestions for this command
$ piper standup --no-suggestions

# Always show details
$ piper standup --suggestions=verbose

# Accept all high-confidence suggestions automatically
$ piper standup --auto-accept  # Dangerous, not recommended
```

---

### Multiple Suggestions

**Show top 3 if requested**:
```bash
$ piper standup --suggestions=all

💡 3 suggestions available:

1. Create GitHub issue (85%)
   [y/n/?/s]

2. Update Notion dashboard (78%)
   [y/n/?/s]

3. Schedule follow-up (72%)
   [y/n/?/s]
```

**Interactive selection**:
```bash
💡 Which actions? [1-3, a=all, n=none]: 1,3
✓ Accepted: Create issue, Schedule follow-up
```

---

### Feedback Flow

**Accept**:
```bash
[y] Accept
✓ Thanks! Pattern confidence increased.
```

**Reject with reason**:
```bash
[n] Reject
Why not useful? [optional, press Enter to skip]: No action items today
✓ Feedback recorded. Won't suggest when no action items present.
```

**Skip**:
```bash
[s] Skip
✓ Dismissed (no confidence change)
```

---

### Technical Implementation

**Backend**: Same `get_suggestions()` API
**Frontend**: New CLI command handler

```python
# In CLI handler
@cli.command()
async def standup():
    # ... execute standup logic ...

    # Get suggestions
    if config.suggestions.cli.show_suggestions:
        suggestions = await learning_handler.get_suggestions(
            user_id=user_id,
            context={"command": "standup"},
            min_confidence=config.suggestions.cli.min_confidence,
            limit=config.suggestions.cli.max_per_command
        )

        if suggestions:
            display_cli_suggestion(suggestions[0])  # Top only
            handle_cli_feedback()
```

**Effort estimate**: 2-3 hours
- 1 hour: CLI rendering logic
- 1 hour: Feedback handling
- 30 min: Configuration integration
- 30 min: Testing

---

## Slack Suggestions

### User Context

**Who**: PMs, team leads, collaborative workers
**When**: During work conversations, after bot interactions
**Expectation**: Rich formatting, quick actions, non-intrusive
**Mental Model**: Like Slack reminders or @mentions—helpful, contextual, dismissible

### Design Approach: "Private DM with Interactive Buttons"

**Philosophy**: Slack is where work happens. Suggestions should appear contextually, use Slack's native UI patterns, and never expose learning publicly.

---

### Interaction Pattern: Direct Message

**After Piper posts standup to #team channel**:
```
[Piper DM to you - Only visible to you]

💡 Pattern noticed

Based on your workflow, you typically update your Notion
dashboard after team standup.

Confidence: 85% (12 times in past 3 weeks)

✅ This is helpful   ❌ Not useful   ⏭️ Not now   ℹ️ More info
```

**Rich formatting** (Slack blocks):
- Subtle divider separating from previous messages
- Emoji icon for visual consistency (💡)
- Clear confidence attribution
- Native Slack button components

---

### Button Actions

**User clicks "✅ This is helpful"**:
```
[Message updates]

✓ Thanks for confirming!

Optional: Why is this pattern helpful?
[Text input appears]

📤 Submit   ⏭️ Skip
```

**User clicks "❌ Not useful"**:
```
[Message updates]

Help me understand:
○ Stop suggesting this pattern entirely
○ Not relevant today (ask again later)

Optional: What would make this better?
[Text input appears]

📤 Submit   ⏭️ Cancel
```

**User clicks "⏭️ Not now"**:
```
[Message updates]

👍 Suggestion dismissed
(This won't affect future suggestions)
```

**User clicks "ℹ️ More info"**:
```
[Expands in thread or modal]

Pattern Details
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Type: Workflow pattern
Trigger: Team standup completion
Action: Update Notion dashboard

History:
• Used successfully: 12 times
• Skipped: 2 times
• Last used: Yesterday at 9:20 AM

Why this suggestion:
You consistently update your Notion dashboard
within 10 minutes of completing team standup,
especially when there are status changes.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ This is helpful   ❌ Not useful   ⏭️ Not now
```

---

### Privacy & Disclosure

**CRITICAL**: Never expose learning patterns in public channels

**Safe**:
- ✅ DM after public interaction
- ✅ Private thread reply
- ✅ Ephemeral message (only you see)

**Unsafe**:
- ❌ Public channel suggestion
- ❌ Thread reply visible to all
- ❌ Exposing user patterns to team

**Disclosure** (first time user receives suggestion):
```
[Piper DM]

💡 New Feature: Pattern Suggestions

I've noticed patterns in how you work with Piper
and can now suggest helpful next steps.

• Suggestions are private (only you see them)
• You're always in control
• Accept, reject, or dismiss any suggestion
• Disable anytime: /piper settings

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Got it   Learn more   Disable suggestions
```

---

### Configuration

**Slack settings** (via `/piper settings` command):
```
[Modal appears]

Pattern Suggestions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Enable suggestions in Slack
[x] Yes  [ ] No

When to show:
[x] After completing standup
[x] After GitHub actions
[x] After calendar updates
[ ] Time-based reminders

Minimum confidence:
[━━━━━━━|━━━] 70%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Save   Cancel
```

**Slash commands**:
```
/piper suggestions on       Enable suggestions
/piper suggestions off      Disable suggestions
/piper suggestions mute 1h  Snooze for 1 hour
/piper suggestions history  See past suggestions
```

---

### Contextual Triggers

**Post-standup**:
```
[After @Piper posts standup summary to #team]

[Piper DMs you privately]
💡 You typically create issues after standup
```

**Post-GitHub action**:
```
[After you comment "LGTM" on PR in Slack-GitHub integration]

[Piper DMs you]
💡 You usually update Notion after approving PRs
```

**Time-based** (with explicit opt-in):
```
[Monday 9:00 AM]

[Piper DMs you]
💡 Weekly reminder: You typically review calendar on Monday mornings
```

---

### Technical Implementation

**Backend**: Same `get_suggestions()` API
**Frontend**: Slack app with Block Kit UI

```python
# After Piper performs action in Slack
@slack_app.event("message")
async def handle_standup_complete(event):
    user_id = event["user"]

    # Get suggestions
    suggestions = await learning_handler.get_suggestions(
        user_id=user_id,
        context={"channel": "slack", "event": "standup_complete"},
        min_confidence=0.7,
        limit=1  # One at a time in Slack
    )

    if suggestions:
        # Send private DM with Block Kit
        await slack_client.chat_postMessage(
            channel=user_id,  # DM
            blocks=build_suggestion_blocks(suggestions[0])
        )

# Handle button clicks
@slack_app.action("suggestion_accept")
async def handle_accept(ack, action, body):
    await ack()
    pattern_id = action["value"]
    await learning_handler.submit_feedback(pattern_id, "accept")
    # Update message to show confirmation
```

**Effort estimate**: 3-4 hours
- 1.5 hours: Block Kit UI templates
- 1 hour: Button interaction handlers
- 1 hour: DM privacy logic
- 30 min: Settings command
- 1 hour: Testing

---

## Webhook Notifications (Proactive)

### User Context

**Who**: Advanced users, power users, automation enthusiasts
**When**: Proactively, based on time/context
**Expectation**: Timely, relevant, easy to silence
**Mental Model**: Like calendar reminders or smart home notifications

### Design Approach: "Opt-In Ambient Intelligence"

**Philosophy**: Most helpful but also most potentially intrusive. Requires explicit consent, granular controls, and impeccable timing.

---

### Use Cases

**Time-based patterns**:
- "You typically review calendar at 9 AM on Mondays"
- "Standup usually happens at 9:30 AM daily"
- "You update Notion every Friday afternoon"

**Event-driven patterns**:
- "PR #456 was merged—you typically update docs after merges"
- "Calendar meeting just ended—you usually create follow-up issues"
- "GitHub issue assigned to you—you usually triage in morning"

**Context-aware patterns**:
- "You're usually in focus mode 2-4 PM—disable Slack?"
- "Friday afternoons you do admin work—time for timesheets?"
- "Pre-standup: You typically review yesterday's notes"

---

### Notification Channels

**Options** (user configures):
1. **Push notification** (mobile/desktop)
2. **Email** (for less urgent patterns)
3. **Slack DM** (leverage existing channel)
4. **Webhook POST** (for custom integrations)

**Example webhook payload**:
```json
POST https://user-configured-endpoint.com/piper-webhook

{
  "event": "pattern_suggestion",
  "timestamp": "2025-11-13T09:00:00Z",
  "suggestion": {
    "pattern_id": "uuid-here",
    "type": "TIME_BASED",
    "description": "Review calendar (Monday morning pattern)",
    "confidence": 0.92,
    "context": {
      "day": "Monday",
      "time": "09:00",
      "frequency": "weekly"
    },
    "actions": {
      "accept": "POST /api/v1/learning/patterns/{id}/feedback",
      "reject": "POST /api/v1/learning/patterns/{id}/feedback",
      "snooze": "POST /api/v1/learning/patterns/{id}/snooze"
    }
  }
}
```

---

### Privacy & Consent Model

**Opt-in required**:
```
[Settings UI]

Proactive Notifications (BETA)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Piper can proactively notify you based on
patterns, not just when you ask.

⚠️ This is more intrusive than other features
   Enable only if you want proactive reminders

[ ] Enable proactive notifications

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Checkbox must be manually checked]
```

**Granular controls**:
```
Notification Types:
[x] Time-based (e.g., "Daily standup at 9:30")
[x] Event-driven (e.g., "PR merged")
[ ] Context-aware (e.g., "Focus mode reminder")

Delivery:
[x] Push notification
[ ] Email
[x] Slack DM
[ ] Webhook (advanced)

Quiet hours:
[x] Enable  |  6:00 PM - 8:00 AM

Maximum per day: [3] notifications
```

---

### Notification UI

**Push notification** (mobile/desktop):
```
┌─────────────────────────────────┐
│ 💡 Piper Pattern Suggestion     │
├─────────────────────────────────┤
│ Review calendar                 │
│                                 │
│ You typically do this on Monday │
│ mornings at 9 AM                │
│                                 │
│ [Open Piper]  [Snooze]  [Dismiss]│
└─────────────────────────────────┘
```

**Email** (for less urgent):
```
Subject: 💡 Piper Pattern Suggestion: Update Notion

Hi [User],

Based on your workflow, you typically update your
Notion dashboard on Friday afternoons.

Confidence: 88% (15 times over 4 months)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This is helpful:
https://piper.app/suggest/accept/{token}

Not useful:
https://piper.app/suggest/reject/{token}

Snooze for 1 day:
https://piper.app/suggest/snooze/{token}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Manage notification settings:
https://piper.app/settings/notifications
```

---

### Snooze & Dismiss

**Snooze options**:
- 1 hour
- 3 hours
- Until tomorrow
- Until next week
- Custom date/time

**Dismiss behavior**:
- Removes current notification
- No confidence penalty
- Will suggest again next trigger
- Can permanently disable pattern in settings

---

### Technical Implementation

**Backend**: Scheduled job + event triggers

```python
# Time-based scheduler
@scheduler.scheduled_job("interval", minutes=5)
async def check_time_based_patterns():
    now = datetime.utcnow()

    # Get all users with proactive notifications enabled
    users = await get_users_with_proactive_enabled()

    for user in users:
        suggestions = await learning_handler.get_suggestions(
            user_id=user.id,
            context={
                "time": now,
                "trigger": "scheduled",
                "notification_type": "time_based"
            },
            min_confidence=0.8,  # Higher for proactive
            limit=1
        )

        if suggestions and not in_quiet_hours(user, now):
            await send_notification(user, suggestions[0])

# Event-driven trigger
@github_webhook.event("pull_request")
async def handle_pr_merged(event):
    if event["action"] == "closed" and event["merged"]:
        user_id = event["user"]

        suggestions = await learning_handler.get_suggestions(
            user_id=user_id,
            context={
                "event": "pr_merged",
                "pr": event["number"]
            },
            min_confidence=0.85,
            limit=1
        )

        if suggestions:
            await send_notification(user_id, suggestions[0])
```

**Effort estimate**: 5-6 hours
- 2 hours: Notification infrastructure
- 1 hour: Scheduling logic
- 1 hour: Event-driven triggers
- 1 hour: Snooze/dismiss handling
- 1 hour: Opt-in UI and settings
- 1 hour: Testing and rate limiting

---

## Cross-Channel Consistency

### Unified Feedback Loop

**Backend data model** (same for all channels):
```python
class PatternFeedback(BaseModel):
    pattern_id: str
    user_id: str
    action: Literal["accept", "reject", "dismiss", "snooze"]
    channel: Literal["web", "cli", "slack", "webhook"]
    timestamp: datetime
    comment: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
```

**Effect across channels**:
- Accept pattern in CLI → Increases confidence for web/Slack
- Reject pattern in Slack → Reduces confidence for all channels
- Dismiss in web → No effect on other channels
- Snooze in webhook → Temporarily disables all channels

---

### Channel Selection Logic

**Priority order** (when multiple channels enabled):

1. **User-initiated** (web/CLI): Always show if confidence > 0.7
2. **Contextual** (Slack): Show after relevant event
3. **Proactive** (webhook): Show at optimal time

**De-duplication**:
- If user just saw suggestion in web chat, don't send Slack DM
- Track "last shown" per pattern per user
- Minimum 1 hour between repeat suggestions across channels

---

### Configuration Hierarchy

**Global settings** (applies to all channels):
```yaml
suggestions:
  enabled: true
  min_confidence: 0.7
  max_per_day: 10
```

**Channel-specific overrides**:
```yaml
suggestions:
  cli:
    enabled: true
    min_confidence: 0.7
  slack:
    enabled: true
    min_confidence: 0.75  # Slightly higher for DMs
  webhooks:
    enabled: false  # Opt-in only
    min_confidence: 0.85  # Much higher for proactive
```

---

## Phased Rollout Recommendation

### Phase 4: CLI Suggestions (2-3 hours)

**Why first**:
- Simplest implementation
- Developer-friendly audience (forgiving)
- Validates core feedback loop
- No privacy concerns (user-initiated)

**Deliverables**:
- CLI rendering logic
- Keyboard-driven feedback
- Configuration integration
- Manual testing

**Success criteria**:
- CLI users engage with suggestions (>30% view rate)
- Accept rate similar to web (>30%)
- No complaints about intrusiveness

---

### Phase 5: Slack DM Suggestions (3-4 hours)

**Why second**:
- Where PMs actually work
- Validates contextual relevance
- Tests privacy model
- Prepares for team features

**Deliverables**:
- Block Kit UI templates
- DM privacy logic
- Button interaction handlers
- Settings command
- First-time disclosure flow

**Success criteria**:
- Users don't disable after first suggestion (<10% disable rate)
- Suggestions feel timely (>50% accept rate)
- No privacy concerns raised

---

### Phase 6: Webhook Notifications (5-6 hours)

**Why last**:
- Most complex (scheduling, event triggers)
- Highest privacy sensitivity
- Requires proven pattern accuracy
- Optional/advanced feature

**Deliverables**:
- Notification infrastructure
- Time-based scheduler
- Event-driven triggers
- Opt-in UI with granular controls
- Snooze/dismiss handling

**Success criteria**:
- <5% of users opt in initially (expected)
- Those who opt in find it valuable (>60% keep enabled)
- No spam reports (max 3 notifications/day enforced)

---

## Open Questions

### For PM

1. **CLI priority**: Should CLI suggestions be Phase 4 or wait for holistic UX audit results?

2. **Slack deployment**: Does Piper already have Slack app infrastructure, or is this new work?

3. **Webhook use cases**: Are there specific integrations (Zapier, IFTTT, custom) we should prioritize?

4. **Team features**: When do team-level patterns matter? (e.g., "Your team typically does X")

### For Lead Developer

1. **Notification infrastructure**: Do we have push notification capability, or need to build?

2. **Scheduler**: Do we have job scheduling (Celery, APScheduler), or need to implement?

3. **Slack app**: Current OAuth scopes sufficient for DMs and buttons?

4. **Rate limiting**: How to enforce max notifications per day across channels?

---

## Success Metrics (Cross-Channel)

### Engagement

**View rate** (% of suggestions seen):
- Web: Target >50%
- CLI: Target >60% (more attention in terminal)
- Slack: Target >70% (DMs are noticeable)
- Webhook: Target >90% (proactive delivery)

**Accept rate** (% marked helpful):
- Web: Target >30%
- CLI: Target >35% (developer efficiency)
- Slack: Target >40% (contextual relevance)
- Webhook: Target >50% (high confidence threshold)

### Retention

**Feature retention** (don't disable):
- Web: Target >90%
- CLI: Target >85%
- Slack: Target >80%
- Webhook: Target >60% (opt-in, more selective)

### Quality

**Confidence improvement** (over time):
- Target: +0.10 per week for accepted patterns
- Target: Fewer false positives (<20% reject rate)
- Target: Higher accuracy in contextual suggestions

---

## Implementation Priority Matrix

| Channel | Complexity | Value | User Demand | Phase |
|---------|-----------|-------|-------------|-------|
| Web chat | Low | High | Critical | ✅ Phase 3 |
| CLI | Low | High | High | 📋 Phase 4 |
| Slack DM | Medium | High | Medium | 🔜 Phase 5 |
| Webhooks | High | Medium | Low | ⏳ Phase 6 |

---

## Next Steps

### Immediate

1. **PM approval**: Review and approve multi-channel approach
2. **Sequencing decision**: CLI in Phase 4, or wait for holistic UX audit?
3. **Slack readiness**: Assess current Slack app capabilities

### Phase 4 (If Approved)

1. Implement CLI suggestions (2-3 hours)
2. Manual testing with CLI users
3. Document learnings for Slack implementation

### Phase 5 (Future)

1. Design Slack Block Kit templates
2. Implement DM privacy logic
3. Test with alpha users in Slack

### Phase 6 (Future)

1. Design notification infrastructure
2. Implement opt-in flow
3. Limit to beta users initially

---

## Appendix: Channel Comparison Table

| Feature | Web Chat | CLI | Slack | Webhooks |
|---------|----------|-----|-------|----------|
| **Trigger** | User-initiated | User-initiated | Contextual | Proactive |
| **Privacy** | Private | Private | Private DM | User-configured |
| **Intrusiveness** | Low | Low | Medium | High |
| **Richness** | High (HTML) | Low (text) | High (blocks) | Varies |
| **Keyboard nav** | Yes | Native | No | N/A |
| **Mobile friendly** | Yes | No | Yes | Yes |
| **Offline mode** | No | Yes | No | No |
| **Batch actions** | No | Yes | No | No |
| **Real-time** | Yes | Yes | Yes | Yes |
| **Opt-out** | Settings | Flag/config | Settings | Explicit opt-in |

---

_"One Piper, many touchpoints"_

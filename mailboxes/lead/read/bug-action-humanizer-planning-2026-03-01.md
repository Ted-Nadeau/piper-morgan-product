# BUG: Planning workflow returns raw error instead of conversational prompt — Action Humanizer gap

**Labels**: bug, ux, action-humanizer

---

## Observed Behavior

User states an implied planning need:
> "I really need to get the team aligned on our Q3 planning"

Piper responds with a developer-facing error:
> "Cannot create plan: planning type not specified. Supported types: sprint, feature_roadmap, issue_resolution"

## Expected Behavior

Piper responds conversationally:
> "Happy to help with Q3 planning! Are you thinking sprint planning, a feature roadmap, or something else?"

## Analysis

**Soft invocation detection is working correctly** — the planning workflow triggered. The issue is in the response layer.

This appears to be an **Action Humanizer gap** (ADR-004). The Action Humanizer should transform technical/error responses into conversational language before they reach the user.

## Systemic Concern

This may not be a singleton bug. Please investigate:

1. **Is the Action Humanizer being invoked** for this workflow path?
2. **Are other workflows** surfacing raw errors similarly? (Check: issue creation, document generation, etc.)
3. **Is there a missing error-to-conversation mapping** in the humanizer, or is the humanizer being bypassed entirely?

The pattern "soft invocation triggers correctly but response is robotic" suggests a layer boundary issue, not just a missing string.

## References

- PDR-002: Conversational Glue (Action Humanizer role)
- ADR-004: Action Humanizer Integration
- #767: GLUE-SOFTINVOKE (detection working, response layer issue)

## Acceptance Criteria

- [ ] Planning workflow responds conversationally when type is ambiguous
- [ ] Audit other workflows for similar raw-error responses
- [ ] Verify Action Humanizer is in the response path for all user-facing messages

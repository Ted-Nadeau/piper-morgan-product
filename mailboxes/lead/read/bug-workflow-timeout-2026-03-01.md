# BUG: Workflow status check timed out after planning query

**Labels**: bug, infrastructure, workflow

---

## Observed Behavior

After user sent a planning-related query:
> "I really need to get the team aligned on our Q3 planning"

Piper responded with the planning error (separate bug), then displayed:
> "Workflow status check timed out."

This appeared as a red error message in the UI, unprompted by any user action.

## Expected Behavior

- No timeout message should appear to users
- If a workflow status check fails internally, it should be handled gracefully without surfacing to the UI
- If the workflow is taking too long, a conversational message like "Still working on that..." would be acceptable — a raw timeout error is not

## Context

This occurred during M0 Post-Sprint testing on March 1, 2026. The timeout appeared after the planning query response, suggesting a background polling or status check mechanism is:
1. Running when it shouldn't be, or
2. Failing to complete within expected time, or
3. Surfacing internal errors to the UI when it should fail silently or gracefully

## Investigation Questions

1. What triggers the "workflow status check"? Is it polling for workflow completion?
2. Why did it run after a failed/error response (the planning type error)?
3. Is there a timeout threshold that's too aggressive?
4. Why is this internal error surfacing to users?

## References

- Discovered during M0 CXO testing session
- Related to planning workflow (but may affect other workflows)

## Acceptance Criteria

- [ ] Workflow status check does not surface raw timeout errors to users
- [ ] If status checks fail, handle gracefully (silent retry, or conversational "still working")
- [ ] Investigate whether this affects other workflow types

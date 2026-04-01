# BUG: API error on issue-related soft invocation query

**Labels**: bug, infrastructure, api

---

## Observed Behavior

User stated an implied issue-creation need:
> "There's a bug in the login flow that has been bothering me"

Piper responded with:
> "An API error occurred"

This appeared as a red error message in the UI.

## Expected Behavior

Piper should respond conversationally, offering to help:
> "That sounds frustrating. Want me to file an issue to track that?"

Or if there's genuinely an error, surface it conversationally:
> "I tried to check your GitHub issues but ran into a connection problem. Want to try again?"

## Context

This occurred during M0 Post-Sprint testing on March 1, 2026. The query was testing soft invocation for issue creation (#767 GLUE-SOFTINVOKE).

The raw "An API error occurred" message suggests:
1. The intent was correctly classified as issue-related (soft invocation working)
2. But the downstream API call (likely GitHub) failed
3. The error was not caught and humanized before reaching the user

## Investigation Questions

1. Is GitHub integration connected and working for this user (alfamux)?
2. What API call failed? (GitHub API? Internal service?)
3. Is the error being logged with details on the backend?
4. Why isn't the Action Humanizer transforming this error into a conversational response?

## Related Issues

- This may be the same root cause as the calendar query failures (integration layer)
- May also relate to Bug #1 (Action Humanizer not transforming errors)

## References

- Discovered during M0 CXO testing session
- #767: GLUE-SOFTINVOKE (detection may be working, but downstream fails)
- ADR-004: Action Humanizer (should transform errors)

## Acceptance Criteria

- [ ] API errors do not surface as raw error messages to users
- [ ] If GitHub integration fails, provide actionable guidance ("Check your GitHub connection in Settings")
- [ ] Verify Action Humanizer is in the error-handling path
- [ ] If integration is not connected, Piper should say so conversationally

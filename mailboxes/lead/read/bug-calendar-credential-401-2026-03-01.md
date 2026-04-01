# BUG: Calendar credential setup fails with 401 Unauthorized

**Labels**: bug, infrastructure, calendar, auth

---

## Observed Behavior

When attempting to set up calendar integration, user sees:
> "Failed to Save Credentials"

Browser console shows multiple 401 errors:
```
Failed to load resource: the server responded with a status of 401 (Unauthorized)
api/v1/settings/integrations/calendar/app-credentials/status
api/v1/settings/integrations/calendar/app-credentials
```

## Expected Behavior

- Calendar credentials should save successfully
- User should be able to complete OAuth flow and connect their calendar

## Context

- Discovered during M0 CXO testing on March 1, 2026
- User's old calendar link stopped working
- Attempting to set up a new connection fails immediately
- This blocks all calendar-related testing (#763 lens tracking, calendar queries)

## Investigation Questions

1. Is the user's session auth valid? (Other endpoints may be working)
2. Are the calendar credential endpoints expecting a different auth mechanism?
3. Is this related to the earlier calendar query issues, or a separate problem?
4. Are new Client ID / Secret values propagating correctly?

## Impact

**High** — Calendar is a core PM workflow and blocks multiple M0 feature tests.

## References

- Related: Earlier calendar query failures (Feb 21-22)
- Blocks: #763 (GLUE-FOLLOWUP lens tracking)
- Discovered during: M0 Post-Sprint CXO testing

## Acceptance Criteria

- [ ] Calendar credential save endpoints return 200 (not 401)
- [ ] User can complete calendar OAuth setup flow
- [ ] Calendar queries work after successful setup

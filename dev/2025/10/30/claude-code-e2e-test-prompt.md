# Prompt for Claude Code: Alpha Onboarding E2E Test Development

## Context

We're implementing Option A from the Chief Architect's recommendation: Continue with dual tables (alpha_users + users) and create proper test coverage. The PM wants to successfully onboard as the first alpha tester today (their birthday!) and then invite Beatrice as tester #2.

## Your Mission

Create or revise an end-to-end test for the complete alpha onboarding flow. Use Serena MCP to verify actual code structure rather than making assumptions.

## Current State

1. **Already Fixed** (from past 3 days):
   - FK constraint removed from audit_logs (migration 648730a3238d)
   - Database port/password configuration corrected
   - JSON→JSONB migration completed
   - Venv auto-restart implemented in wizard and preferences
   - Alpha user creation in setup_wizard.py
   - Preferences script queries alpha_users table

2. **Architecture** (Issue #259):
   - `alpha_users` table for alpha testers (UUID primary keys)
   - `users` table for future production (String primary keys)
   - Most FKs still point to users.id (audit_logs FK removed)

## Test Requirements

### Use Serena MCP to Verify

Before writing the test, use Serena to check:

```python
# Check the actual CLI commands available
serena.find_symbol("main.py")  # What commands exist?

# Check setup wizard implementation
serena.find_symbol("setup_wizard.py")
serena.find_symbol("create_user_account")  # How does it create users?

# Check preferences implementation
serena.find_symbol("preferences_questionnaire.py")
serena.find_symbol("get_existing_preferences")  # Which table does it query?

# Check status checker
serena.find_symbol("status_checker.py")

# Check database models
serena.find_symbol("AlphaUser")  # What fields exist?
serena.find_symbol("alpha_users")  # Table structure
```

### Test Structure

Create `tests/integration/test_alpha_onboarding_e2e.py` that:

1. **Setup Phase**:
   - Clean test environment (remove test user if exists)
   - Set PIPER_USER environment variable
   - Use test database (piper_dev on port 5433)

2. **Test Flow** (Happy Path):
   ```
   Step 1: Run setup wizard
   - Verify it completes without error
   - Verify alpha user created in alpha_users table
   - Verify API keys stored (if provided via env)

   Step 2: Check initial status
   - Verify user is recognized
   - Verify configuration state

   Step 3: Run preferences questionnaire
   - Provide all 5 answers
   - Verify preferences saved to alpha_users.preferences

   Step 4: Check final status
   - Verify system shows "configured" or "ready"

   Step 5: Smoke test chat (optional)
   - Just verify it doesn't crash
   - OK if it says "need API keys"
   ```

3. **Success Criteria**:
   - All commands run without crashing
   - Data persists in alpha_users table
   - Status reflects configured state

### Template to Start From

Here's the Chief Architect's template (needs verification against actual code):

```python
"""
End-to-end test for alpha user onboarding flow.
When this passes, we can invite Beatrice!
"""
import subprocess
import os
import psycopg2

def test_alpha_user_complete_onboarding():
    # [Use Serena to verify actual implementation details]
    # [Check actual CLI commands and arguments]
    # [Verify database configuration]
    # [Test based on what actually exists, not assumptions]
    pass
```

## Deliverables

1. **First**: Use Serena to document what you find:
   - Actual CLI commands available
   - How setup wizard creates users (which table?)
   - How preferences are stored
   - What status checker reports

2. **Then**: Write the E2E test based on reality:
   - Test what actually exists
   - Don't test hypothetical features
   - Focus on the happy path

3. **Finally**: Propose the test back to the Chief Architect for review

## Remember

- NO assumptions - verify everything with Serena
- Test ONLY what exists (not what should exist)
- Keep it simple - happy path only
- This test defines birthday success!

## Success Looks Like

```
🎂 BIRTHDAY TEST: Alpha Onboarding Flow
==================================================
✨ Step 1: Running setup wizard...
✓ Setup wizard completed!
✨ Step 2: Checking system status...
✓ System status verified!
✨ Step 3: Setting preferences...
✓ Preferences configured!
✨ Step 4: Final status verification...
✓ System fully configured!
✨ Step 5: Testing chat capability...
✓ Chat is working!

🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉
🎂 BIRTHDAY SUCCESS! Alpha onboarding works end-to-end!
🎁 Ready to invite Beatrice as alpha tester #2!
🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉
```

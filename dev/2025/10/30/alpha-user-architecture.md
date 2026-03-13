# Alpha User Architecture (Issue #259)

**Date**: 2025-10-30
**Session**: Alpha Onboarding Testing
**Context**: Clarified alpha vs production user table architecture

## Architecture Decision

Piper Morgan uses **two separate user systems** during alpha phase:

### 1. `alpha_users` Table (Current Phase)

- **Purpose**: Alpha tester accounts only
- **Key Type**: UUID (PostgreSQL)
- **Features**:
  - `alpha_wave` - Which testing wave (currently 1)
  - `test_start_date` - When testing began
  - `migrated_to_prod` - Migration flag
  - `prod_user_id` - Link to production account after migration
  - Clean data separation for testing
  - Prevents "Netcom problem" (username conflicts)

### 2. `users` Table (Future: Beta/GA)

- **Purpose**: Production user accounts
- **Key Type**: String(255)
- **Features**:
  - Full authentication system
  - Permanent accounts
  - Production-ready user management

## Current Implementation (Alpha Phase)

### Setup Wizard

- Creates `AlphaUser` records (not `User`)
- Sets `alpha_wave=1` for first wave testers
- UUID primary key
- Converts UUID to string for API key foreign keys

### Preferences Script

- Queries `alpha_users` table
- Stores preferences in `AlphaUser.preferences` JSONB column
- Already correctly implemented

### API Key Service

- Uses string `user_id` parameter
- Compatible with both UUID (converted) and String IDs
- Foreign key in `user_api_keys` points to `users.id` (String)
- Alpha users convert UUID to string for compatibility

## Migration Path (Future Beta)

When moving to beta:

1. Alpha testers choose to migrate data
2. Create production `User` record
3. Link via `AlphaUser.prod_user_id`
4. Transfer preferences/learning data
5. Mark `AlphaUser.migrated_to_prod = True`
6. Preserve alpha username (prevent conflicts)

## Type Compatibility Issue

**Current Workaround**:

- `AlphaUser.id` is UUID
- `UserAPIKey.user_id` is String(255) with FK to `users.id`
- Wizard converts UUID to string: `user_id_str = str(user.id)`

**Future Solution** (when needed):

- Make `UserAPIKey.user_id` polymorphic
- Or create separate `alpha_user_api_keys` table
- Or update FK to support both tables

## Files Changed

1. **`scripts/setup_wizard.py`**:

   - `create_user_account()` creates `AlphaUser`
   - `check_for_incomplete_setup()` checks `alpha_users`
   - UUID to string conversion for API keys

2. **`scripts/preferences_questionnaire.py`**:
   - Already correctly queries `alpha_users`
   - No changes needed

## Testing Notes

- Setup wizard now shows "2. Alpha Tester Account"
- Database schema check queries `alpha_users` table
- All alpha testers get proper separation
- Clean migration path for production

## References

- Issue #259: CORE-USER-ALPHA-TABLE
- Issue #228: CORE-USERS-API (production users)
- `services/database/models.py`: Schema definitions

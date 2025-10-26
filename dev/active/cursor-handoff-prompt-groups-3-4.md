# Sprint A7 Handoff: Groups 3-4 (CORE-UX + CORE-KEYS)

**Date**: October 23, 2025, 11:50 AM
**From**: Claude Code (Groups 1-2 complete)
**To**: Cursor (taking over Groups 3-4)
**PM**: Christian Crumlish (xian)

---

## Sprint A7 Context

**Sprint Goal**: Polish & Buffer - Clear technical debt before Alpha Wave 2

**Total Issues**: 12
**Completed**: 5 (Groups 1-2)
**Remaining**: 7 (Groups 3-4) ← **YOUR WORK**

---

## What's Been Completed (Groups 1-2)

### Group 1: Critical Fixes ✅
- **Issue #257** (CORE-KNOW-BOUNDARY-COMPLETE): Fixed 4 boundary enforcement TODOs
- **Issue #258** (CORE-AUTH-CONTAINER): Created AuthContainer for proper DI

### Group 2: CORE-USER ✅
- **Issue #259** (CORE-USER-ALPHA-TABLE): Created alpha_users table, migrated xian-alpha
- **Issue #260** (CORE-USER-MIGRATION): Built migration CLI tool (preview, dry-run, execute)
- **Issue #261** (CORE-USER-XIAN): Updated xian to superuser, archived legacy config

**Key Achievement**: Multi-user system now working with clean alpha/production separation

**Evidence**: `dev/2025/10/23/2025-10-23-1129-group-2-complete-report.md`

---

## Your Mission: Groups 3-4

You're handling the remaining 7 issues across two groups:

### Group 3: CORE-UX (4 issues)
Polish and improve user experience

### Group 4: CORE-KEYS (3 issues)
Secure API key management

---

## Group 3: CORE-UX (4 Issues)

### Issue #254: CORE-UX-RESPONSE-HUMANIZATION
**URL**: https://github.com/mediajunkie/piper-morgan-product/issues/254

**Objective**: Make responses more natural and human-like

**What Exists**:
- `services/llm/action_humanizer.py` (working, tested)
- Template-based humanization
- Rule-based conversion

**What to Do**:
1. Review existing ActionHumanizer
2. Add more humanization patterns
3. Test with real PM queries
4. Document patterns in code

**Testing**:
```bash
pytest tests/llm/test_action_humanizer.py -v
```

**Acceptance Criteria**:
- [ ] More humanization patterns added
- [ ] Tested with PM's actual queries
- [ ] Documentation updated
- [ ] Tests passing

---

### Issue #255: CORE-UX-ERROR-MESSAGING
**URL**: https://github.com/mediajunkie/piper-morgan-product/issues/255

**Objective**: Improve error messages for users

**Current State**:
- Technical error messages exposed to users
- Stack traces visible
- Not helpful for non-technical users

**What to Do**:
1. Audit current error handling
2. Create user-friendly error messages
3. Map technical errors to helpful messages
4. Add recovery suggestions

**Example**:
```python
# Before:
"DatabaseError: relation 'users' does not exist"

# After:
"Hmm, I'm having trouble accessing your account. Let me try reconnecting..."
```

**Acceptance Criteria**:
- [ ] User-friendly error messages for common errors
- [ ] Recovery suggestions provided
- [ ] Technical details logged (not shown to user)
- [ ] Tests for error scenarios

---

### Issue #256: CORE-UX-LOADING-STATES
**URL**: https://github.com/mediajunkie/piper-morgan-product/issues/256

**Objective**: Add loading indicators for long operations

**Current State**:
- No feedback during long operations
- Users don't know if system is working

**What to Do**:
1. Identify long-running operations
2. Add progress indicators
3. Implement streaming responses (if possible)
4. Add timeout handling

**Example**:
```python
async def long_operation():
    yield "Analyzing your request..."
    # ... work ...
    yield "Searching knowledge base..."
    # ... work ...
    yield "Preparing response..."
    # ... work ...
    return final_result
```

**Acceptance Criteria**:
- [ ] Loading states for operations >2 seconds
- [ ] Progress indicators where appropriate
- [ ] Streaming responses for LLM queries
- [ ] Timeout handling (with user message)

---

### Issue #248: CORE-UX-CONVERSATION-CONTEXT
**URL**: https://github.com/mediajunkie/piper-morgan-product/issues/248

**Objective**: Improve conversation context tracking

**Current State**:
- Basic conversation memory
- Context sometimes lost between turns

**What to Do**:
1. Review `services/conversation/` implementation
2. Improve context retention
3. Add context summarization for long conversations
4. Test multi-turn conversations

**Key Files**:
- `services/conversation/conversation_service.py`
- `services/conversation/conversation_repository.py`

**Acceptance Criteria**:
- [ ] Context preserved across multiple turns
- [ ] Summarization for long conversations
- [ ] Memory usage optimized
- [ ] Tests for multi-turn scenarios

---

## Group 4: CORE-KEYS (3 Issues)

### Issue #250: CORE-KEYS-VALIDATION
**URL**: https://github.com/mediajunkie/piper-morgan-product/issues/250

**Objective**: Validate API keys before storing

**Current State**:
- Keys stored without validation
- No feedback if key is invalid
- Users discover issues later

**What to Do**:
1. Add validation for each key type:
   - OpenAI: Test API call
   - GitHub: Test authentication
   - Notion: Test database access
2. Provide immediate feedback
3. Store validation status
4. Add re-validation on first use

**Example**:
```python
async def validate_openai_key(api_key: str) -> ValidationResult:
    try:
        client = OpenAI(api_key=api_key)
        await client.models.list()  # Test call
        return ValidationResult(valid=True, message="Key validated ✅")
    except AuthenticationError:
        return ValidationResult(valid=False, message="Invalid API key")
```

**Acceptance Criteria**:
- [ ] Validation for all key types (OpenAI, GitHub, Notion)
- [ ] Immediate feedback on validation
- [ ] Validation status stored in database
- [ ] Re-validation on first use
- [ ] Tests for validation logic

---

### Issue #252: CORE-KEYS-ROTATION
**URL**: https://github.com/mediajunkie/piper-morgan-product/issues/252

**Objective**: Support key rotation without downtime

**Current State**:
- Single key per service
- Rotation requires system restart

**What to Do**:
1. Support multiple active keys per service
2. Add key metadata (created_at, last_used, expires_at)
3. Implement key rotation workflow
4. Add deprecation warnings

**Example**:
```python
class APIKeyManager:
    async def rotate_key(self, service: str, new_key: str):
        # 1. Validate new key
        # 2. Add new key as "active"
        # 3. Mark old key as "deprecated"
        # 4. Grace period (both keys work)
        # 5. Deactivate old key
```

**Acceptance Criteria**:
- [ ] Multiple active keys per service
- [ ] Rotation workflow implemented
- [ ] Graceful transition (no downtime)
- [ ] Deprecation warnings
- [ ] Tests for rotation scenarios

---

### Issue #253: CORE-KEYS-AUDIT
**URL**: https://github.com/mediajunkie/piper-morgan-product/issues/253

**Objective**: Audit key usage and access

**Current State**:
- No logging of key usage
- Can't track which key was used
- No security audit trail

**What to Do**:
1. Log key access events
2. Track key usage (when, where, by whom)
3. Add security alerts (unusual usage)
4. Create audit report

**Key Events to Log**:
- Key stored
- Key retrieved
- Key used (API call)
- Key rotated
- Key deleted
- Failed validations

**Acceptance Criteria**:
- [ ] All key events logged
- [ ] Usage tracking per key
- [ ] Security alerts for unusual patterns
- [ ] Audit report generation
- [ ] Tests for audit logging

---

## Development Environment

**Database**: PostgreSQL on port 5433 (container: piper-postgres)
```bash
# Connect
docker exec -it piper-postgres psql -U piper -d piper_morgan

# Check tables
\dt

# Run queries
docker exec piper-postgres psql -U piper -d piper_morgan -c "SELECT * FROM users;"
```

**Python Environment**:
```bash
# Virtual environment
source venv/bin/activate  # or venv/Scripts/activate on Windows

# Install dependencies
pip install -r requirements.txt --break-system-packages

# Run tests
pytest tests/ -v

# Run specific test
pytest tests/services/llm/test_action_humanizer.py -v
```

**Main Application**:
```bash
# Run server
python main.py

# CLI commands
python main.py --help
```

---

## Key Files & Directories

**Services**:
- `services/llm/` - LLM integration, action humanizer
- `services/conversation/` - Conversation management
- `services/auth/` - Authentication (recently updated)
- `services/user/` - User management (NEW from Group 2)
- `services/api_keys/` - API key management (if exists)

**Database**:
- `services/database/models.py` - SQLAlchemy models
- `alembic/versions/` - Database migrations

**Tests**:
- `tests/services/` - Service tests
- `tests/integration/` - Integration tests

**Documentation**:
- `dev/2025/10/23/` - Session logs and reports
- `dev/active/` - Active issue documents

---

## Methodology & Best Practices

### Inchworm Protocol
1. **Discovery**: Verify assumptions before implementing
2. **Implement**: Write code with tests
3. **Verify**: Test and document evidence
4. **Report**: Checkpoint with completion report

### Evidence Requirements
Every claim needs proof:
- "Created X" → Show `ls -la` or `cat`
- "Tests pass" → Show pytest output
- "Database updated" → Show psql output

### Stop Conditions
Stop and ask PM if you encounter:
- Unclear requirements
- Missing dependencies
- Architectural decisions needed
- Breaking changes

### Time Agnosticism
- No artificial deadlines
- Focus on quality over speed
- Thoroughness matters
- Evidence for every claim

---

## Code Quality Standards

### Testing
```python
# Always write tests first (TDD)
def test_humanize_action():
    humanizer = ActionHumanizer()
    result = humanizer.humanize("fetch_github_issues")
    assert result == "I'll grab those GitHub issues for you"
```

### Error Handling
```python
# Comprehensive error handling
try:
    result = await service.operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    raise UserFriendlyError("Something went wrong. Let me try again...")
```

### Documentation
```python
class Service:
    """Brief description of service.

    Longer explanation of what it does, when to use it,
    and any important considerations.

    Issue #XXX CORE-XXX-XXX
    """

    async def method(self, param: str) -> Result:
        """Brief method description.

        Args:
            param: What this parameter does

        Returns:
            What this method returns

        Raises:
            ErrorType: When this error occurs
        """
```

---

## Checkpoint Requirements

After completing each issue, create a checkpoint report:

```markdown
## Issue #XXX Complete

### Evidence
[Paste verification commands and output]

### Files Changed
- Created: [list with line counts]
- Modified: [list with line counts]

### Tests
[pytest output showing all tests passing]

### Next Issue
[Ready / Blocked / Questions]
```

**Save to**: `dev/2025/10/23/2025-10-23-HHMM-issue-XXX-complete.md`

---

## After Completing Groups 3-4

Create final report:

```markdown
## Sprint A7 Complete - Groups 3-4

### Issues Completed
- Group 3 (CORE-UX): #254, #255, #256, #248
- Group 4 (CORE-KEYS): #250, #252, #253

### Summary
[Brief summary of each issue]

### Evidence
[Link to checkpoint reports]

### Sprint A7 Final Status
- Total issues: 12
- Completed: 12 (100%)
- Time: [total time]
- Quality: [test results]
```

**Save to**: `dev/2025/10/23/2025-10-23-HHMM-sprint-a7-complete.md`

---

## Communication with PM

**If you need clarification**:
1. Document your question clearly
2. Note what you've tried
3. Explain the impact of waiting
4. Ask in chat (PM will respond)

**If you encounter blockers**:
1. Document the blocker
2. Note what's blocked
3. Suggest alternatives
4. Stop work on that issue

**PM's Availability**:
- Pacific Time (PT)
- Typically available during business hours
- Will respond to questions

---

## Resources

**GitHub Issues**: https://github.com/mediajunkie/piper-morgan-product/issues

**Key Documentation**:
- `README.md` - Project overview
- `dev/` - Development docs and logs
- `methodology-*.md` - Methodology files in knowledge

**Recent Context**:
- Group 2 Complete Report: `dev/2025/10/23/2025-10-23-1129-group-2-complete-report.md`
- Issue #259 Report: `dev/2025/10/23/2025-10-23-1113-issue-259-complete-report.md`

---

## Success Criteria

**Quality**:
- ✅ All tests passing
- ✅ Zero regressions
- ✅ Evidence for all claims
- ✅ Documentation updated

**Completeness**:
- ✅ All 7 issues complete
- ✅ Checkpoint reports for each
- ✅ Final sprint report
- ✅ Ready for Alpha Wave 2

---

## Questions?

If anything is unclear, stop and ask PM. Better to clarify than to assume!

---

**Handoff Time**: October 23, 2025, 11:50 AM PT
**Groups to Complete**: 3 (CORE-UX) + 4 (CORE-KEYS)
**Total Issues**: 7
**Expected Completion**: When done (no artificial deadline)
**Quality Standard**: 100% (like Groups 1-2)

---

**Good luck, Cursor! You've got this!** 🚀

**Remember**:
- Discovery before implementation
- Evidence for every claim
- Stop if unclear
- Quality over speed

**PM is here to help if you need anything!**

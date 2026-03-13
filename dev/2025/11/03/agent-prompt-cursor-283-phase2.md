# Cursor Agent: Issue #283 Phase 2 - Validation & Testing

## Context Update

**Phase 1**: ✅ COMPLETE (you shipped this in 13 minutes)
- EnhancedErrorMiddleware wired up
- 96/96 tests passing
- Commits: b3594e29, 08182533

**Since Phase 1**:
- ✅ Code completed #284 (ActionMapper) - commit 8fc3a65e
- 🔄 Code working on #285 (Todo System) - 50% complete
- **Impact**: Fewer "unknown action" errors now (better routing)

**Your Mission Now**: Phase 2 validation - prove all 5 error types work end-to-end

---

## Phase 2: End-to-End Validation

### Your Tasks (1-2 hours)

**1. Test All 5 Error Types Manually** (30 min)

Start server if needed:
```bash
python main.py
```

Test each error type with curl and document results:

```bash
# Get auth token first
TOKEN=$(curl -s -X POST http://localhost:8001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"xian","password":"test123456"}' \
  | jq -r '.token')

# Test 1: Empty Input
curl -X POST http://localhost:8001/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": ""}'
# Expected: Friendly message about not catching that

# Test 2: Unknown/Gibberish Input
curl -X POST http://localhost:8001/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "xyzabc123qwerty"}'
# Expected: Friendly "not sure I understood" or "still learning"

# Test 3: Valid Action (should work now thanks to ActionMapper)
curl -X POST http://localhost:8001/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "create a github issue for testing"}'
# Expected: Success OR friendly error if not fully wired

# Test 4: Timeout (if testable)
# May need to trigger artificially or skip if not easily testable

# Test 5: System Error
# Check logs to verify technical details logged while user sees friendly message
```

**Evidence Required**: Save all curl outputs showing friendly messages (not technical errors)

**2. Verify Technical Logging Intact** (15 min)

```bash
# Check server logs during tests
tail -f logs/piper-morgan.log  # or wherever logs go

# Verify logs show:
# - Technical exception details (for debugging)
# - Stack traces if applicable
# - While user receives friendly messages
```

**Evidence Required**: Log excerpts showing technical details preserved

**3. Test Piper's Tone** (15 min)

Review all error messages against piper-style-guide.md:
- [ ] Helpful and encouraging?
- [ ] Professional but approachable?
- [ ] Suggests next actions?
- [ ] No sarcasm or dismissiveness?
- [ ] No technical jargon in user messages?

**Evidence Required**: Confirmation each message follows style guide

**4. Create Comparison Table** (15 min)

Document before/after for issue:

```markdown
| Error Type | Before | After | Status |
|------------|--------|-------|--------|
| Empty Input | 30s timeout | "I didn't quite catch that..." | ✅ |
| Unknown Action | "No handler for action: X" | "I'm still learning..." | ✅ |
| Timeout | "Operation timed out" | "That's complex..." | ✅ |
| Unknown Intent | Generic error | "I'm not sure I understood..." | ✅ |
| System Error | "API error occurred" | "Something went wrong..." | ✅ |
```

**5. Update GitHub Issue** (15 min)

Mark all acceptance criteria complete in #283 description:
```bash
gh issue edit 283 --body "[updated description with all checkboxes marked]"
```

Add comment with evidence:
```bash
gh issue comment 283 --body "
## Phase 2 Validation Complete

All 5 error types tested and working:
- [paste comparison table]
- [link to commit]
- [link to session log]

Ready for PM approval to close.
"
```

---

## Completion Checklist

- [ ] All 5 error types tested with curl (save outputs)
- [ ] Technical logging verified intact (show log excerpts)
- [ ] Tone checked against piper-style-guide.md
- [ ] Before/after comparison table created
- [ ] GitHub issue #283 updated with evidence
- [ ] Session log updated: dev/2025/11/03/2025-11-03-0620-prog-cursor-log.md
- [ ] Ready for PM final approval

---

## Session Log Reminder

**Continue your existing log**: dev/2025/11/03/2025-11-03-0620-prog-cursor-log.md

**Don't create a new one** - just add Phase 2 section to existing log

---

## STOP Conditions

Stop and report if:
- Any error type shows technical jargon to user
- Technical logging is broken/missing
- Tone doesn't match piper-style-guide.md
- Tests reveal regressions
- Can't provide evidence for any claim

---

## Expected Timeline

- Phase 2 validation: 1-2 hours
- You've already done the hard work (Phase 1)
- This is just verification that it works as expected

**Ready to validate!** Start with the curl tests and document everything.

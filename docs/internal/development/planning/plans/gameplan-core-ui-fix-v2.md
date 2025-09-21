# Gameplan v2.0: CORE-UI Fix Layer 3 Intent Processing Pipeline
*Revised with Lead Developer consultation feedback*

## 🛑 INFRASTRUCTURE VERIFICATION CHECKPOINT ✅ PASSED

### Infrastructure Confirmed (8:15 AM)
- ✅ `services/intent_service/` EXISTS and operational
- ✅ `web/app.py` EXISTS with FastAPI endpoints
- ✅ Server running healthy on port 8001
- ✅ Issue #172 created as child of #166
- ✅ UI regression confirmed (differential behavior observed)

## Context
- **Issue**: #172 CORE-UI (child of Bug #166)
- **Complexity**: High - architectural Layer 3 issue
- **Lead Developer**: Current session
- **Agents**: Claude Code + Cursor (coordinated deployment)
- **Priority**: CRITICAL - Blocking all development

## Phase 0: Differential Investigation (30 minutes)

### Investigation Strategy: Working vs Hanging Comparison
**Frontend First (Cursor)**:
```javascript
// 1. Test working prompts (document which work)
// Examples: "hello", "help", basic commands

// 2. Test hanging prompts (document which hang)
// Examples: "show standup", complex queries

// 3. Browser console comparison
// Working: Check network tab, console logs
// Hanging: Check for errors, timeouts, pending requests
```

**Backend Analysis (Code)**:
```bash
# Compare endpoint implementations
grep -A 20 "@app.post.*chat" web/app.py
grep -A 20 "@app.post.*standup" web/app.py

# Trace intent processing
grep -r "process_intent\|handle_intent" services/ --include="*.py"

# Check handler registration
find services/ -name "*handler*.py" -exec grep -l "register\|intent" {} \;
```

### Phase 0 Checkpoint (30 min) 🚦
**Synchronization Point**:
- Claude Code: Report backend patterns found
- Cursor: Report frontend symptoms documented
- Both: Identify correlation between symptoms and patterns
- **Decision Gate**: Pattern identified? → Continue. No pattern? → STOP, escalate

### GitHub Bookending - Start
```bash
gh issue edit 172 --body "
## Status: Phase 0 - Investigation Starting
- [ ] Differential analysis (working vs hanging)
- [ ] Frontend symptoms documented
- [ ] Backend patterns identified
- [ ] Correlation established

Agents: Code + Cursor
Started: $(date)
"
```

## Phase 1: Pipeline Mapping & Diagnosis (60 minutes)

### Multi-Agent Division
**Claude Code** - Complete Pipeline Mapping:
1. Intent classification flow
2. Handler registration mechanism
3. Response transformation pipeline
4. Create flow diagram in session log

**Cursor** - Symptom Documentation:
1. All affected prompts list
2. Console errors for each
3. Network timing analysis
4. Screenshots of hang states

### Phase 1 Checkpoint (60 min) 🚦
**Cross-Reference Point**:
- Code: Pipeline diagram complete
- Cursor: Symptom matrix complete
- Both: Match symptoms to pipeline failures
- **Decision Gate**: Root cause identified? → Continue. Still unclear? → Escalate

### Evidence Collection Standards

**Expected Browser Evidence**:
```javascript
// Layer 3 failure pattern
POST /api/chat 500 (Internal Server Error)
{"error": "Intent handler not found for 'standup_request'"}

// OR timeout pattern
POST /api/chat (pending)
// After 30s: net::ERR_EMPTY_RESPONSE
```

**Expected Pipeline Trace**:
```python
DEBUG: Request received: {"message": "show standup"}
DEBUG: Intent classified as: standup_request
ERROR: HandlerNotFound: No handler for intent 'standup_request'
# OR
ERROR: ResponseTransform: Cannot serialize None to JSON
```

## Phase 2: Fix Implementation (90 minutes)

### Implementation Approach
1. **Proof of Concept**: Fix one hanging endpoint first
2. **Validate**: Confirm fix works for that endpoint
3. **Generalize**: Apply pattern to all affected endpoints
4. **Verify**: No direct endpoint bypasses remain

### Code Changes Expected
```python
# Before (broken)
@app.post("/api/chat")
async def chat(request: ChatRequest):
    # Direct handling without intent routing
    return process_somehow(request)

# After (fixed)
@app.post("/api/chat")
async def chat(request: ChatRequest):
    intent = await classify_intent(request.message)
    handler = get_handler(intent)  # This was missing!
    response = await handler.process(request)
    return transform_response(response)
```

### Phase 2 Checkpoint (90 min) 🚦
**Implementation Sync**:
- Code: Fix implemented with unit tests
- Cursor: Ready for UI validation
- Both: Testing same endpoints
- **Decision Gate**: Tests passing? → Continue. Regressions? → STOP

## Phase 3: Validation & Cross-Check (60 minutes)

### Validation Requirements

**Performance Validation**:
```bash
# Must return in <100ms
time curl -X POST http://localhost:8001/api/chat \
  -d '{"message":"show standup"}' \
  -H "Content-Type: application/json"

# Automated performance test
for i in {1..10}; do
  start=$(date +%s%N)
  curl -s -X POST http://localhost:8001/api/chat \
    -d '{"message":"show standup"}' \
    -H "Content-Type: application/json" > /dev/null
  end=$(date +%s%N)
  echo "Request $i: $(((end-start)/1000000))ms"
done
```

**Cross-Validation Protocol**:
- Code: All unit tests pass
- Code: Integration tests confirm pipeline
- Cursor: All previously hanging prompts work
- Cursor: No console errors
- Both: Performance <100ms confirmed

### Evidence Requirements
- ✅ Before/after curl commands showing fix
- ✅ Browser screenshots pre/post fix
- ✅ Test output with pass counts
- ✅ Performance metrics documented
- ✅ Git diff showing exact changes

## Phase Z: Bookending & Completion (30 minutes)

### GitHub Final Update
```bash
gh issue edit 172 --body "
## Status: COMPLETE ✅
- [x] Differential analysis ✅ [7 working, 3 hanging patterns]
- [x] Root cause identified ✅ [Handler registration missing]
- [x] Fix implemented ✅ [All endpoints wired]
- [x] Validation complete ✅ [<100ms, no hangs]

### Evidence
- Pipeline diagram: [link]
- Test results: [link]
- Performance: 47ms average (10 runs)
- Screenshots: [link]

### Next Steps
- Ready for PLUG epic
"
```

### Git Discipline
```bash
# Stage all changes
git add -A

# Commit with conventional format
git commit -m "fix(CORE-UI): Wire intent handlers for all chat endpoints

- Connected intent classifier to handler registry
- Fixed response transformation pipeline
- Added validation for handler presence
- Performance: <100ms for all prompts

Fixes #172, Related to #166"

# Verify commit
git log --oneline -1

# Push if authorized
git push origin main
```

### Session Completion
- Update both agent session logs
- Add satisfaction metrics
- Document key learnings
- Prepare handoff notes

## STOP Conditions (15 from v7 template)
1. ❌ Infrastructure doesn't match (already verified ✅)
2. ❌ Pattern might already exist
3. ❌ Tests fail for any reason
4. ❌ Configuration assumptions needed
5. ❌ GitHub issue missing (#172 exists ✅)
6. ❌ Can't provide verification evidence
7. ❌ ADR conflicts with approach
8. ❌ Resource not found after searching
9. ❌ User data at risk
10. ❌ Completion bias detected
11. ❌ GitHub not updating properly
12. ❌ Single agent seems sufficient (multi required)
13. ❌ Git operations failing
14. ❌ Server state unexpected
15. ❌ UI behavior can't be visually confirmed

## Success Criteria
- [ ] All hanging prompts identified with differential analysis
- [ ] Root cause documented with evidence
- [ ] Fix implemented with tests
- [ ] No regressions introduced
- [ ] Performance <100ms for all endpoints
- [ ] Browser testing confirms resolution
- [ ] GitHub issue complete with all evidence
- [ ] Git commits clean and descriptive
- [ ] Session logs updated

## Time Estimate (Revised)
- Phase 0: 30 minutes (differential investigation)
- Phase 1: 60 minutes (pipeline mapping)
- Phase 2: 90 minutes (implementation)
- Phase 3: 60 minutes (validation)
- Phase Z: 30 minutes (bookending)
- **Total**: ~4.5 hours

## Notes for Agents

### Critical Context
- Some prompts work, others hang (differential behavior)
- Previous Layer 1 & 2 fixed, Layer 3 is the issue
- Intent system exists but wiring incomplete
- This blocks ALL further development

### Coordination Reminders
- Check in at specified checkpoints (not arbitrary times)
- Update GitHub at phase transitions
- Evidence required for all claims
- STOP if patterns unclear

---
*Gameplan Version: 2.0*
*Revised: September 17, 2025, 8:30 AM*
*Incorporates: Lead Developer consultation feedback*
*Template: v7 enforcement mechanisms applied*

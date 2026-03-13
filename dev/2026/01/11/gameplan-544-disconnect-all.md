# Gameplan: Issue #544 - Bulk Integration Operations (Disconnect All)

**Date**: 2026-01-11
**Issue**: #544
**Template Version**: v9.3
**Status**: Ready for Implementation
**Estimated Effort**: Small (~1.5 hours)

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Lead Developer's Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI
- [x] Frontend: Server-rendered templates with vanilla JS
- [x] Existing endpoints: Individual disconnect at `/api/v1/settings/integrations/{name}/disconnect`
- [x] UI location: `templates/integrations.html`
- [x] Pattern to follow: `testAllConnections()` function

**My understanding of the task**:
- Add "Disconnect All" button next to existing "Test All" button
- Implement JS function to call existing disconnect endpoints sequentially
- Pure frontend change - no backend modifications needed

### Part A.2: Work Characteristics Assessment

**Worktree Candidate?**

Worktrees ADD overhead when:
- [x] Single agent, sequential work
- [x] Small fixes (<15 min per phase)
- [x] Time-critical work where setup overhead matters

**Assessment**:
- [x] **SKIP WORKTREE** - Single agent, ~1.5 hour total, purely frontend

### Part B: PM Verification Required

**PM, please confirm**:
1. [x] UI change only, no backend needed
2. [x] Follow Test All pattern
3. [ ] Any critical context I'm missing?

### Part C: Proceed/Revise Decision
- [ ] **PROCEED** - Understanding correct
- [ ] **REVISE** - Assumptions wrong
- [ ] **CLARIFY** - Need more context

---

## Phase 0: Initial Bookending - GitHub Investigation

### Required Actions

1. **GitHub Issue Verification**
   ```bash
   gh issue view 544
   ```
   Status: ✅ Issue exists, template-compliant (updated earlier today)

2. **Codebase Investigation**
   ```bash
   # Verify Test All pattern exists
   grep -n "testAllConnections" templates/integrations.html

   # Verify disconnect endpoints work
   grep -n "disconnectIntegration" templates/integrations.html
   ```

3. **Update GitHub Issue** (progressive bookending)
   ```bash
   gh issue comment 544 -b "## Status: Implementation Starting
   - [x] Gameplan written and approved
   - [x] Infrastructure verified
   - [ ] Phase 1: UI Button
   - [ ] Phase 2: JavaScript
   - [ ] Phase 3: Testing"
   ```

### STOP Conditions Check
- [ ] Issue doesn't exist → Verified: exists
- [ ] Feature already implemented → Verified: not implemented
- [ ] Different problem than described → Verified: matches

---

## Phase 0.5: Frontend-Backend Contract Verification

### Purpose
Verify existing disconnect endpoints work before building UI that calls them.

### Required Actions

#### 1. Verify Disconnect Endpoints Exist
```bash
# Get disconnect endpoint paths
grep -n "disconnect" web/api/routes/settings.py
```

#### 2. Calculate Full Paths
| Integration | Endpoint Path | Full Path |
|-------------|---------------|-----------|
| slack | /disconnect | /api/v1/settings/integrations/slack/disconnect |
| calendar | /disconnect | /api/v1/settings/integrations/calendar/disconnect |
| github | /disconnect | /api/v1/settings/integrations/github/disconnect |
| notion | /disconnect | /api/v1/settings/integrations/notion/disconnect |

#### 3. Verify Paths Work (with server running)
```bash
# Test one endpoint to verify pattern (requires auth)
curl -X POST http://localhost:8001/api/v1/settings/integrations/slack/disconnect
# Expected: 401 (not authenticated) or 200/success - NOT 404
```

#### 4. Static File Verification
N/A - No new static files, modifying existing template

### STOP Conditions
- [ ] If ANY disconnect endpoint returns 404 → STOP
- [ ] If endpoint path pattern differs from expected → STOP

---

## Phase 1: UI Button Addition (20 min)

### Objective
Add "Disconnect All" button next to "Test All Connections" in the overall status card.

### Tasks
- [ ] Add button HTML after "Test All Connections" button (~line 360)
- [ ] Add CSS styling for `.disconnect-all-btn` (danger/destructive style)
- [ ] Add disabled state logic in `renderOverallStatus()` or `renderIntegrations()`

### Deliverables
- Button visible on integrations page
- Proper styling matching design system
- Button disabled when no integrations connected

### Files Modified
- `templates/integrations.html` (HTML + CSS)

### Progressive Bookending
```bash
gh issue comment 544 -b "✓ Phase 1 Complete: UI Button Added
- Button HTML added at line [X]
- Danger styling applied
- Disabled state implemented"
```

---

## Phase 2: JavaScript Implementation (40 min)

### Objective
Implement `disconnectAllIntegrations()` function with confirmation, sequential disconnect, and status feedback.

### Tasks
- [ ] Create `disconnectAllIntegrations()` async function
- [ ] Build list of connected integrations from current UI state
- [ ] Show confirmation dialog listing which integrations will disconnect
- [ ] Loop through and call existing disconnect for each (sequential)
- [ ] Handle partial failures (continue on individual failure)
- [ ] Show summary toast (X of Y disconnected)
- [ ] Reload integrations health after completion

### Implementation Details

```javascript
async function disconnectAllIntegrations() {
  // 1. Get connected integrations
  const connected = getConnectedIntegrations(); // Parse from UI

  if (connected.length === 0) return;

  // 2. Confirmation
  const names = connected.map(i => i.display_name).join('\n- ');
  if (!confirm(`Disconnect all integrations?\n\nThis will disconnect:\n- ${names}`)) {
    return;
  }

  // 3. Update button state
  const btn = document.getElementById('disconnect-all-btn');
  btn.disabled = true;
  btn.textContent = 'Disconnecting...';

  // 4. Disconnect each
  let successCount = 0;
  for (const integration of connected) {
    try {
      // Reuse existing disconnect logic
      const response = await fetch(`/api/v1/settings/integrations/${integration.name}/disconnect`, {
        method: 'POST'
      });
      if (response.ok) successCount++;
    } catch (e) {
      console.error(`Failed to disconnect ${integration.name}:`, e);
    }
  }

  // 5. Show result
  const allSuccess = successCount === connected.length;
  showToast(
    allSuccess ? 'success' : 'warning',
    `${successCount} of ${connected.length} integrations disconnected`,
    allSuccess ? 'All Disconnected' : 'Partial Disconnect'
  );

  // 6. Reload UI
  loadIntegrationsHealth();
}
```

### Files Modified
- `templates/integrations.html` (JavaScript)

### Progressive Bookending
```bash
gh issue comment 544 -b "✓ Phase 2 Complete: JavaScript Implementation
- disconnectAllIntegrations() function added
- Confirmation dialog shows integration list
- Sequential disconnect with error handling
- Summary toast implemented"
```

---

## Phase 3: Testing & Polish (30 min)

### Manual Testing Checklist

**Scenario 1**: All integrations connected
1. [ ] Connect all 4 integrations
2. [ ] Click "Disconnect All"
3. [ ] Verify confirmation lists all 4
4. [ ] Confirm
5. [ ] Verify all 4 disconnect
6. [ ] Verify toast shows "4 of 4"

**Scenario 2**: Partial connections
1. [ ] Connect only 2 integrations
2. [ ] Click "Disconnect All"
3. [ ] Verify only 2 listed in confirmation
4. [ ] Confirm and verify both disconnect

**Scenario 3**: No connections
1. [ ] Ensure no integrations connected
2. [ ] Verify button is disabled
3. [ ] Verify button has disabled styling

**Scenario 4**: User cancels
1. [ ] With integrations connected, click "Disconnect All"
2. [ ] Click cancel
3. [ ] Verify no disconnections occurred

### Regression Tests
- [ ] Individual disconnect still works
- [ ] Test All still works
- [ ] Connect buttons still work
- [ ] Page refresh shows correct state

### Progressive Bookending
```bash
gh issue comment 544 -b "✓ Phase 3 Complete: Testing
- All 4 scenarios pass
- No regressions found
- Screenshots attached"
```

---

## Phase Z: Final Bookending & Handoff

### Required Actions

#### 1. GitHub Final Update
```bash
gh issue edit 544 --body "[existing body + evidence section]"
```

#### 2. Evidence Compilation
- [ ] Screenshot: Button visible with proper styling
- [ ] Screenshot: Confirmation dialog with integration list
- [ ] Screenshot: Success toast after disconnect
- [ ] Screenshot: Button disabled when nothing connected
- [ ] Terminal output: No console errors during operation

#### 3. Documentation Updates
- [ ] Session log completed
- [ ] No ADR needed (follows existing pattern)

#### 4. PM Approval Request
```markdown
@PM - Issue #544 complete and ready for review:
- All acceptance criteria met ✓
- Evidence provided (screenshots) ✓
- Manual testing complete ✓
- No regressions confirmed ✓

Please review and close if satisfied.
```

---

## Completion Matrix

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Button HTML added | ❌ | - |
| Button CSS (danger style) | ❌ | - |
| Button disabled state | ❌ | - |
| `disconnectAllIntegrations()` | ❌ | - |
| Confirmation dialog | ❌ | - |
| Sequential disconnect | ❌ | - |
| Error handling | ❌ | - |
| Summary toast | ❌ | - |
| Scenario 1 (all connected) | ❌ | - |
| Scenario 2 (partial) | ❌ | - |
| Scenario 3 (none) | ❌ | - |
| Scenario 4 (cancel) | ❌ | - |
| No regressions | ❌ | - |

---

## Success Criteria

### Issue Completion Requires
- [ ] All acceptance criteria met
- [ ] Evidence provided for each criterion
- [ ] Manual tests passing (with screenshots)
- [ ] No regressions introduced
- [ ] GitHub issue fully updated
- [ ] PM approval received

---

## STOP Conditions

- Individual disconnect endpoints broken
- Test All button broken
- Security concerns with bulk operation
- Pattern doesn't fit existing code structure
- Disconnect endpoint returns 404

---

## Notes

- Following existing `testAllConnections()` pattern closely
- No backend changes required - reusing existing endpoints
- No new API endpoints needed
- Pure frontend enhancement
- Single agent sufficient (skip worktree)

---

*Gameplan created: 2026-01-11 08:55*
*Updated for v9.3 compliance: 2026-01-11 09:05*

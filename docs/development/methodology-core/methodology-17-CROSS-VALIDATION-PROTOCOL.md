# Cross-Validation Protocol
**Version**: 1.0
**Date**: September 4, 2025
**Purpose**: Ensure multi-agent work quality through systematic verification

---

## Core Principle
Every piece of work must be independently verifiable by another agent. No single agent's claims are accepted without evidence.

---

## Standard Cross-Validation Pattern

### Phase 1: Initial Implementation (Agent A)
```bash
# Agent A completes work
# Documents evidence in session log
# Updates GitHub issue with claims
# Provides terminal output as proof
```

### Phase 2: Verification (Agent B)
```bash
# Agent B receives specific verification tasks
# Runs independent tests
# Checks implementation against requirements
# Reports discrepancies
```

### Phase 3: Reconciliation
```bash
# Lead Developer reviews both reports
# Discrepancies addressed
# Final verification performed
# GitHub issue updated with validation
```

---

## Verification Checkpoints

### Code Implementation Verification
**Agent A (Code) implements** → **Agent B (Cursor) verifies**:
- [ ] Tests pass with actual output shown
- [ ] Code follows existing patterns
- [ ] No new technical debt introduced
- [ ] Documentation updated appropriately

### Configuration Changes Verification
**Agent A makes change** → **Agent B confirms**:
- [ ] Configuration actually updated (cat file)
- [ ] Service recognizes new configuration
- [ ] No unintended side effects
- [ ] Rollback procedure documented

### GitHub Updates Verification
**Agent A updates issue** → **Agent B checks**:
- [ ] Issue description accurate
- [ ] All checkboxes reflect reality
- [ ] Evidence links provided
- [ ] Status in CSV matches GitHub

---

## Evidence Requirements

### What Constitutes Valid Evidence

✅ **Terminal Output**
```bash
$ pytest tests/test_feature.py -v
...
===== 15 passed in 2.34s =====
```

✅ **File Diffs**
```bash
$ git diff services/feature.py
[actual diff showing changes]
```

✅ **Grep Confirmation**
```bash
$ grep -n "pattern" services/module.py
42: def validated_pattern():
```

❌ **Invalid Evidence**
- "Tests pass" (no output)
- "Updated configuration" (no diff)
- "Pattern exists" (no grep)
- "Should work" (no verification)

---

## Cross-Validation Workflows

### Parallel Development Validation
```
Code implements Feature A
Cursor implements Feature B
---
Code validates Feature B
Cursor validates Feature A
---
Both report to Lead Developer
```

### Sequential Validation
```
Code investigates and implements
→ Cursor validates implementation
→ Code addresses issues
→ Cursor confirms fixes
```

### Emergency Validation
```
If suspicious behavior detected:
1. STOP all work
2. Run full cross-validation
3. Report to Lead Developer
4. Await architectural review
```

---

## Validation Prompts

### For Lead Developer to Agent B
```markdown
Please validate the work completed by [Agent A] on PM-XXX.

Specifically verify:
1. [Specific claim to check]
2. [Test to run independently]
3. [Configuration to verify]

Report back with:
- Terminal output of your verification
- Any discrepancies found
- Confirmation or concerns
```

### For Agent Validation Response
```markdown
VALIDATION REPORT for PM-XXX

Verified Claims:
✅ [Claim]: [Evidence]
❌ [Claim]: [Discrepancy found]

Terminal Evidence:
[paste actual output]

Recommendations:
[Next steps based on findings]
```

---

## Red Flags Requiring Immediate Validation

1. **Vague Success Claims**
   - "Everything works now"
   - "Fixed all issues"
   - "Should be fine"

2. **Missing Evidence**
   - No terminal output provided
   - No specific files mentioned
   - No test results shown

3. **Assumption Indicators**
   - "Probably working"
   - "Seems to be fixed"
   - "Appears to function"

4. **Rapid Completion**
   - Complex task "done" in minutes
   - No investigation phase shown
   - Skip directly to "solution"

---

## Validation Metrics

Track these to ensure protocol effectiveness:

- **False Success Rate**: Claims that fail validation
- **Evidence Quality**: Percentage with terminal proof
- **Validation Time**: How long cross-checks take
- **Discrepancy Resolution**: Time to fix issues found

Target: <5% false success rate with 100% evidence provision

---

## Remember

**Trust but verify** - Every claim needs evidence
**Two pairs of eyes** - Catch errors before they cascade
**Document everything** - Future you will thank current you
**No assumptions** - Verify or fail validation

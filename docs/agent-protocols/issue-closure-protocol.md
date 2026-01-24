# Issue Closure Protocol

"Closing an issue properly" means updating BOTH the description AND adding a closing comment.

---

## Before Closing Any Issue

1. **Update description checkboxes**: Every `[ ]` completed becomes `[x]`
2. **Update Completion Matrix**: Mark items "Complete" with evidence links
3. **Add verification evidence**: Link to commits, test output, or PR
4. **Update status**: Change to "COMPLETE"

---

## Closing Comment Template

```markdown
## Implementation Complete

### Summary
[1-2 sentence summary]

### Changes Made
- [File]: [What changed]
- [File]: [What changed]

### Test Results
[Test command and output summary]

### Verification
- Commit: [hash]
- Tests: [X] passing
```

---

## Issue Closure Checklist

Before `gh issue close <number>`:

- [ ] All description checkboxes checked (or explicitly marked "deferred with PM approval")
- [ ] Completion Matrix updated with evidence
- [ ] Closing comment added with implementation evidence
- [ ] Status in description shows "COMPLETE"

---

## Anti-Pattern: Comment-Only Close

**Wrong**: Add evidence comment, close issue, leave description boxes unchecked
**Right**: Update description boxes, add evidence comment, then close

---

## Why This Matters

- Unchecked boxes = incomplete work visible to anyone reviewing
- Comments alone aren't enough - description is source of truth
- Future planning depends on accurate records
- Incomplete records require re-verification (learned 2026-01-11)

# Time and Duration Verification Protocol

## Rule
**NEVER make assertions about time or duration without system verification**

## Required Before Claiming Duration
```bash
# At start of task
START_TIME=$(date +%s)

# At end of task
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))
echo "Actual duration: $DURATION seconds ($((DURATION / 60)) minutes)"
```

## Common Mistakes to Avoid
- ❌ "This took 30 minutes" (based on estimated time in plan)
- ❌ "Completed in X minutes" (without checking actual time)
- ✅ "Started at [timestamp], completed at [timestamp], actual duration: X minutes"

## When to Check Time
- Before claiming task completion time
- When reporting "this took X minutes/hours"
- When comparing actual vs estimated time
- In session logs and completion reports

## Example
```bash
# Wrong
"Phase 4.2 completed in 30 minutes (as estimated!)"

# Right
START=$(date -r /path/to/first/file/created +%s)
END=$(date +%s)
ACTUAL=$((END - START))
"Phase 4.2 completed in $((ACTUAL / 60)) minutes (estimated 30 min)"
```

## Context
Created Nov 14, 2025 after incorrectly claiming Phase 4.2 took "exactly 30 minutes" when it actually took ~3 minutes (based on git commit timestamps).

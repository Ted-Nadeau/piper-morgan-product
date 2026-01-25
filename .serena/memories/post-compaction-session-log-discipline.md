# Post-Compaction Session Log Discipline

**Created:** 2026-01-24 after critical logging failure incident
**Purpose:** Prevent session log gaps after conversation compaction

## CRITICAL RULE

After ANY conversation compaction/summarization:

1. **FIRST ACTION** must be session log verification:
   - Find today's session log in `dev/YYYY/MM/DD/`
   - Read the last entries
   - Append: "## Resumed after compaction at [TIME]"

2. **RECONCILE** before continuing:
   - Check git status for uncommitted changes
   - Verify all work since last log entry is documented
   - If gap found: STOP and reconstruct before proceeding

3. **IDENTITY CHECK**:
   - You are the Lead Developer
   - Your log is named `YYYY-MM-DD-HHMM-lead-code-opus-log.md`
   - If no log exists for today, create one immediately

## Why This Matters

On 2026-01-24, a 6-hour gap occurred where 400+ tests and dozens of files were committed with ZERO logging. This represents:
- Lost context for WHY decisions were made
- Inability to trace issues to reasoning
- Erosion of project knowledge continuity

## Detection

If you find yourself working without a recent log entry (>30 min since last update):
1. STOP
2. Update log with current work
3. Then continue

The discomfort of maintaining the log is working as designed.

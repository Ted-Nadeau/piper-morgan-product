# CLAUDE.md

## 🚨 INFRASTRUCTURE VERIFICATION FIRST (NEW)
Before following ANY gameplan, verify infrastructure matches assumptions:
```bash
# What gameplan expects vs reality
ls -la web/ services/ cli/
find . -name "*[feature]*" -type f

# If mismatch found:
# 1. STOP immediately
# 2. Report with evidence
# 3. Wait for revised gameplan
```
**Common mismatches**: Gameplan assumes "no web UI" but FastAPI exists, assumes "new service" but exists, etc.

## MANDATORY FIRST READS
1. **resource-map.md** - CHECK THIS FIRST! Locations of all ADRs, patterns, existing code
2. methodology-00-EXCELLENCE-FLYWHEEL.md
3. methodology-07-VERIFICATION-FIRST.md
4. methodology-16-STOP-CONDITIONS.md
5. methodology-17-CROSS-VALIDATION.md

Architecture patterns: See ARCHITECTURE-RULES.md

## SESSION SETUP
- Create: 2025-MM-DD-HHMM-code-log.md
- Update GitHub issue descriptions (not comments)
- Evidence required: actual terminal output
- No "tests pass" without showing output

## CAPABILITIES
- Can deploy subagents for parallel tasks
- Use when investigation spans multiple areas
- Coordinate results in session log

## CRITICAL PATHS
```
services/domain/models.py    # Truth source
services/shared_types.py     # ALL enums
services/config.py           # Settings
pattern-catalog.md           # Existing patterns
docs/architecture/decisions/ # 28 ADRs exist here!
```

## VERIFY FIRST
```bash
# ALWAYS check resource-map.md for locations, then:
grep -r "pattern" services/ --include="*.py"  # Before creating
cat services/shared_types.py | grep "Enum"     # Before enums
cat services/config.py | grep "setting"        # Before config
ls -la docs/architecture/decisions/            # Check ADRs (28 exist!)
```

## STOP CONDITIONS
- Infrastructure doesn't match gameplan → STOP
- Assuming config values → STOP
- Guessing method names → STOP
- Creating without checking → STOP
- Tests fail "acceptably" → STOP
- No GitHub issue → STOP
- Can't find resources → Check resource-map.md first!

## COMMANDS
```bash
# Always PYTHONPATH
PYTHONPATH=. python -m pytest tests/unit/ -v

# Never bare pytest
pytest  # WRONG

# Database on 5433 (not 5432)
docker exec -it piper-postgres psql -U piper -d piper_morgan
```

## REPORTING FORMAT
```
Task: PM-XXX complete
Evidence: [terminal output]
Validation: [what to check]
Infrastructure: [matched/mismatch reported]
```

## RULES
- Verify infrastructure before implementation
- Never access .env files
- Repository pattern only
- Domain models drive design
- Evidence for all claims
- Cross-validation expected

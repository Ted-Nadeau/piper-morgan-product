# AGENTS.md - Cursor Agent Instructions

## Project Context
You are working on Piper Morgan, an intelligent PM assistant. The project uses:
- Python 3.11+ with FastAPI
- PostgreSQL (port 5433, not 5432)
- Domain-Driven Design
- Port 8001 for web (not 8080)

## Your Briefing Documents
Search project knowledge for these essential docs:
1. **BRIEFING-CURRENT-STATE** - Current epic and focus
2. **BRIEFING-ROLE-PROGRAMMER** - Your role requirements
3. **BRIEFING-METHODOLOGY** - How we work (Inchworm Protocol)
4. **BRIEFING-PROJECT** - Full project context

## Critical: The 75% Pattern
Most code you'll find is 75% complete then abandoned. Examples:
- QueryRouter is disabled but 75% complete
- Intent classification works but isn't universal
- Functions exist but aren't called

**Your job**: Complete existing work, don't create new patterns.

## Infrastructure Verification (MANDATORY)
Before ANY work:
```bash
ls -la web/ services/ cli/
grep -r "ClassName" . --include="*.py"
```
If reality doesn't match instructions: STOP and report.

## Technical Specifics
```bash
# Entry point
main.py  # NOT web/app.py for startup

# File locations
web/app.py                   # FastAPI (933 lines)
services/domain/models.py    # Domain models
services/shared_types.py     # ALL enums
config/PIPER.user.md        # User config (not YAML)

# NO routes/ directory exists

# Testing
PYTHONPATH=. python -m pytest tests/ -xvs

# Database
docker exec -it piper-postgres psql -U piper -d piper_morgan
```

## STOP Conditions
- Infrastructure mismatch → STOP
- Pattern already exists → STOP (complete it instead)
- Tests failing → STOP
- No GitHub issue → STOP
- Assuming values → STOP

## Current Focus
**CORE-GREAT-1**: Resurrect QueryRouter (75% complete, just disabled)
- It exists in services/orchestration/engine.py
- Just commented out, needs reconnection
- This unblocks 80% of features

## Evidence Required
Show actual output, not summaries:
```bash
pytest tests/test_feature.py -xvs  # Full output
curl http://localhost:8001/test     # Real response
```

## Remember
1. Verify everything before implementing
2. Complete existing code, don't replace
3. Evidence required for all claims
4. The Inchworm Protocol: 100% complete before moving on

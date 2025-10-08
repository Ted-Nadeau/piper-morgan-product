# AGENTS.md - Sprint Agent Instructions

## Project Context
You are working on Piper Morgan, an intelligent PM assistant. The project uses:
- Python 3.11+ with FastAPI
- PostgreSQL (port 5433, not 5432)  
- Domain-Driven Design
- Port 8001 for web (not 8080)

## Sprint: Demo Documentation Sprint
**Date**: 2025-10-08
**Objectives**: [TO BE DEFINED IN sprint-planning.md]

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

# Key locations  
web/app.py                   # FastAPI app
services/domain/models.py    # Domain models
services/shared_types.py     # ALL enums
config/PIPER.user.md        # User config (not YAML)

# Testing
PYTHONPATH=. python -m pytest tests/ -xvs

# Database
docker exec -it piper-postgres psql -U piper -d piper_morgan
```

## Current Focus
**Demo Documentation Sprint**: [DEFINE SPECIFIC FOCUS IN sprint-planning.md]

## Critical: The 75% Pattern
Most code is 75% complete then abandoned. Complete existing work, don't create new patterns.

## Evidence Required
Show actual output in session logs:
```bash
pytest tests/test_feature.py -xvs  # Full output
curl http://localhost:8001/test     # Real response
```

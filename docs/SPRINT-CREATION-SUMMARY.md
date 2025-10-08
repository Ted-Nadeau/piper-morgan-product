# Sprint Creation in Piper Morgan - Complete Guide

## Overview

The Piper Morgan project uses a structured sprint system based on date-organized directories and comprehensive documentation. This guide provides everything you need to know about creating and managing sprints.

## Quick Start Commands

### Option 1: Simple Command Line (Recommended)
```bash
# Create a sprint with current date
./scripts/new-sprint "Sprint Name"

# Create a sprint for specific date  
./scripts/new-sprint "Sprint Name" 2025-10-15
```

### Option 2: Interactive Script
```bash
# Guided sprint creation with prompts
./scripts/create_sprint.sh
```

## What Is a Sprint in Piper Morgan?

A sprint is a focused development cycle with:
- **Clear objectives** defined upfront
- **Evidence-based progress** tracking
- **Date-based organization** in `dev/YYYY/MM/DD/`
- **Comprehensive documentation** of all work
- **GitHub issue integration** with PM-XXX numbering

## Sprint Structure

Every sprint creates this directory structure:

```
dev/YYYY/MM/DD/
├── AGENTS.md              # Agent instructions and project context
├── sprint-planning.md     # Objectives, milestones, and planning
├── README.md             # Sprint overview and quick start
├── session-logs/         # Work session documentation
│   └── session-log-template.md
└── artifacts/            # Sprint deliverables
    ├── diagrams/         # Architecture diagrams
    ├── prototypes/       # Code experiments  
    └── documentation/    # Sprint-specific docs
```

## Core Principles

### 1. The 75% Pattern Recognition
Most existing code is 75% complete then abandoned. Sprint work should:
- ✅ **Complete existing features** rather than starting new ones
- ✅ **Find and finish** partially implemented functionality
- ✅ **Connect existing components** rather than rebuilding
- ❌ Don't create new patterns when existing ones exist

### 2. Evidence-Based Development
All sprint work requires evidence:
- **Command outputs** in session logs
- **Test results** with full console output
- **Screenshots** for UI changes
- **Performance measurements** for optimizations

### 3. Infrastructure Verification First
Before any sprint work, verify the environment matches expectations:
```bash
ls -la web/ services/ cli/
grep -r "ExpectedClass" . --include="*.py"
```
If reality doesn't match plans: **STOP and report the mismatch**.

## Sprint Workflow

### Before Starting
1. **Create sprint** using one of the tools above
2. **Edit `sprint-planning.md`** to define specific objectives
3. **Verify PM numbers** and create GitHub issues
4. **Set up development environment**

### During the Sprint
1. **Daily session logs** documenting all work
2. **Progress updates** in `sprint-planning.md`
3. **GitHub issue updates** with evidence and progress
4. **Evidence collection** for all changes made

### Sprint Completion
1. **Mark objectives complete** with evidence in planning doc
2. **Update all GitHub issues** with final status
3. **Create retrospective** (optional but recommended)
4. **Archive session logs** and create handoffs as needed

## Session Log Management

### Naming Convention
```
YYYY-MM-DD-HHMM-[agent]-[model]-log.md
```

### Example Session Names
- `2025-10-08-1430-prog-code-log.md` (Programmer agent using Claude Code)
- `2025-10-08-0900-architect-opus-log.md` (Architect agent using Claude Opus)

### Session Log Content
Each session log should include:
- **Session objectives** (specific to this work period)
- **Work completed** with evidence
- **Issues encountered** and how they were resolved
- **Files modified** with descriptions of changes
- **Tests run** with full output
- **Next steps** for continuation

## GitHub Integration

### Issue Numbering (Critical)
Always follow the PM-XXX numbering system:

```bash
# Check existing PM numbers
gh issue list --state all --limit 100 | grep "PM-" | sort -V | tail -10

# Use next sequential number
# If latest is PM-125, use PM-126
```

### Issue Labels
Sprint issues should use these labels:
- `sprint` - Main sprint tracking issue
- `planning` - Sprint planning and coordination
- Plus specific labels for the work area (e.g., `ui`, `backend`, `integration`)

## Technical Environment

### Standard Setup
- **Python**: 3.11+ with virtual environment
- **Database**: PostgreSQL on port **5433** (not 5432)
- **Web Server**: Port **8001** (not 8080)
- **Entry Point**: `main.py` (not `web/app.py`)

### Key File Locations
```bash
web/app.py                   # FastAPI application
services/domain/models.py    # Domain models
services/shared_types.py     # ALL enums go here
config/PIPER.user.md        # User configuration (not YAML)
```

### Standard Commands
```bash
# Testing
PYTHONPATH=. python -m pytest tests/ -xvs

# Database access
docker exec -it piper-postgres psql -U piper -d piper_morgan

# Health check
curl http://localhost:8001/health
```

## Sprint Types

### Development Sprints
- Focus on implementing features
- Heavy coding and testing
- Integration with existing systems

### Research Sprints  
- Investigation and discovery
- Prototyping and experimentation
- Technical decision making

### Integration Sprints
- Connecting systems
- API development
- Cross-component work

### Bug Fix Sprints
- Issue resolution
- Performance improvements
- Stability enhancements

## Troubleshooting

### Common Issues

**Permission denied on scripts**
```bash
chmod +x scripts/new-sprint scripts/create_sprint.sh
```

**Directory already exists**
```bash
# Use suffix or different date
./scripts/new-sprint "Sprint Name v2"
```

**PM number conflicts**
```bash
# Always verify first
gh issue list --state all --limit 100 | grep "PM-"
```

**Environment mismatch**
```bash
# Verify project structure
ls -la web/ services/ cli/
# If different from expected: STOP and report
```

## Resources and Documentation

### Core Documentation
- **Full Methodology**: `docs/internal/development/methodology-core/methodology-21-SPRINT-CREATION.md`
- **Issue Tracking**: `docs/internal/development/methodology-core/methodology-08-ISSUE-TRACKING.md`
- **How-To Guide**: `docs/HOW-TO-CREATE-A-NEW-SPRINT.md`

### Project Context
- **Agent Instructions**: `CLAUDE.md`
- **Project Architecture**: `docs/internal/architecture/`
- **Current State**: `docs/internal/planning/current/`

### Examples
- **Existing Sprints**: `dev/2025/` directories
- **Sprint Handoffs**: `docs/internal/development/handoffs/`
- **Session Log Examples**: Various `dev/` subdirectories

## Support and Best Practices

### When to Create a New Sprint
- Starting work on a significant feature
- Beginning a focused research effort
- Coordinating multi-day development work
- Need structured documentation and tracking

### Sprint Size Guidelines
- **Small Sprint**: 1-3 objectives, 1-2 days
- **Medium Sprint**: 3-5 objectives, 3-5 days  
- **Large Sprint**: 5+ objectives, 1+ weeks

### Success Indicators
- All objectives completed with evidence
- GitHub issues properly updated
- Session logs provide clear audit trail
- No untracked changes or missing documentation
- Clean handoff for continuation

---

## Summary Commands

```bash
# Quick sprint creation
./scripts/new-sprint "Your Sprint Name"

# Check PM numbers
gh issue list --state all --limit 100 | grep "PM-"

# Navigate to today's sprint
cd dev/$(date +"%Y/%m/%d")

# Standard development workflow
PYTHONPATH=. python -m pytest tests/ -xvs
```

**Remember**: Sprints are about structured, evidence-based development. Always document your work, verify your environment, and complete existing patterns before creating new ones.
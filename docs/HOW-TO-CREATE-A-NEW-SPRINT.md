# How to Create a New Sprint in Piper Morgan

This guide explains the step-by-step process for creating a new sprint in the Piper Morgan project.

## Quick Start (Using Automated Script)

The fastest way to create a new sprint is using the automated script:

```bash
# Navigate to repository root
cd /path/to/piper-morgan-product

# Run the sprint creation script
./scripts/create_sprint.sh
```

The script will prompt you for:
- **Sprint name** (e.g., "Core UI Enhancement", "MCP Integration")  
- **Sprint date** (defaults to current date)

## What Gets Created

The script creates a complete sprint structure:

```
dev/YYYY/MM/DD/
├── AGENTS.md              # Agent instructions with project context
├── sprint-planning.md     # Detailed objectives and planning
├── README.md             # Sprint overview and workflow
├── session-logs/         # Directory for work session logs
│   └── session-log-template.md
└── artifacts/            # Sprint deliverables
    ├── diagrams/
    ├── prototypes/
    └── documentation/
```

## Manual Sprint Creation

If you prefer to create a sprint manually:

### 1. Create Directory Structure

```bash
# Get current date
DATE=$(date +"%Y-%m-%d")
YEAR=$(date +"%Y") 
MONTH=$(date +"%m")
DAY=$(date +"%d")

# Create sprint directory
mkdir -p "dev/$YEAR/$MONTH/$DAY"
cd "dev/$YEAR/$MONTH/$DAY"

# Create subdirectories
mkdir -p session-logs artifacts/{diagrams,prototypes,documentation}
```

### 2. Create Core Files

Copy and customize these essential files:

- **AGENTS.md**: Agent instructions (see template in methodology-21)
- **sprint-planning.md**: Sprint objectives and planning
- **README.md**: Sprint overview

### 3. Set Up Issue Tracking

Follow the PM number verification process:

```bash
# Check existing PM numbers
gh issue list --state all --limit 100 | grep "PM-" | sort -V | tail -10

# Create sprint tracking issue  
gh issue create --title "PM-XXX: Sprint [NAME]" --body "..." --label "sprint"
```

## Sprint Workflow

### During the Sprint

1. **Daily Sessions**: Create session logs from the template
2. **Progress Tracking**: Update sprint-planning.md checkboxes  
3. **Evidence Collection**: Include command outputs in session logs
4. **Issue Updates**: Keep GitHub issues updated with progress

### Session Log Naming Convention

```
YYYY-MM-DD-HHMM-[agent]-[model]-log.md
```

Example: `2025-10-08-1430-prog-code-log.md`

### Sprint Completion

When the sprint is complete:

1. Mark all objectives complete in `sprint-planning.md`
2. Create `retrospective.md` 
3. Update all GitHub issues
4. Create handoff documentation if needed

## Key Principles

### The 75% Pattern

Most existing code is 75% complete then abandoned. Your job is to:
- **Complete existing work** rather than creating new patterns
- **Find and finish** partially implemented features
- **Integrate** existing components rather than rebuilding

### Evidence-Based Development

All work must include evidence:
- Command outputs in session logs
- Test results with full output  
- Screenshots for UI changes
- Performance measurements

### Infrastructure Verification

Before starting any sprint work:

```bash
# Verify project structure matches expectations
ls -la web/ services/ cli/

# Check if components exist
grep -r "ClassName" . --include="*.py"

# If reality doesn't match plans: STOP and report
```

## Technical Setup

### Required Environment

- **Python**: 3.11+ with virtual environment
- **Database**: PostgreSQL on port 5433 (not 5432)
- **Web Server**: Port 8001 (not 8080)  
- **Entry Point**: `main.py` (not `web/app.py`)

### Standard Commands

```bash
# Testing
PYTHONPATH=. python -m pytest tests/ -xvs

# Database access  
docker exec -it piper-postgres psql -U piper -d piper_morgan

# Web server check
curl http://localhost:8001/health
```

## Sprint Types

### Development Sprints
Focus on implementing new features or completing existing ones.

### Integration Sprints  
Focus on connecting systems and ensuring compatibility.

### Research Sprints
Focus on investigation, prototyping, and technical discovery.

### Bug Fix Sprints
Focus on resolving issues and improving stability.

## Common Issues and Solutions

### Issue: Script Permissions Error
```bash
# Solution: Make script executable
chmod +x scripts/create_sprint.sh
```

### Issue: Directory Already Exists
```bash
# Solution: Use a different date or add suffix
mkdir -p "dev/2025/10/08-v2"
```

### Issue: PM Number Conflicts
```bash
# Solution: Always verify before creating
gh issue list --state all --limit 100 | grep "PM-" | sort -V
```

## Resources

- **Full Methodology**: `docs/internal/development/methodology-core/methodology-21-SPRINT-CREATION.md`
- **Issue Tracking**: `docs/internal/development/methodology-core/methodology-08-ISSUE-TRACKING.md`
- **Project Context**: `CLAUDE.md`
- **Sprint Examples**: `dev/2025/` directories

## Support

If you encounter issues with sprint creation:

1. Check the methodology documentation
2. Verify your environment setup
3. Review existing sprint examples in `dev/` directories
4. Ensure GitHub CLI access is working

---

**Quick Command Summary**:
```bash
# Create new sprint (automated)
./scripts/create_sprint.sh

# Verify PM numbers  
gh issue list --state all --limit 100 | grep "PM-"

# Start sprint work
cd dev/YYYY/MM/DD/
# Read AGENTS.md and sprint-planning.md
# Begin development following methodology
```
#!/bin/bash
# Sprint Creation Automation Script
# Creates a new sprint with proper directory structure and documentation

echo "🚀 Piper Morgan Sprint Creation Tool"
echo "==================================="

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print status
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
    else
        echo -e "${RED}❌ $2${NC}"
        return 1
    fi
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Get current date components
CURRENT_DATE=$(date +"%Y-%m-%d")
YEAR=$(date +"%Y")
MONTH=$(date +"%m")
DAY=$(date +"%d")
TIMESTAMP=$(date +"%Y-%m-%d-%H%M")

# Check if we're in the repository root
if [ ! -f "main.py" ] || [ ! -d "services" ] || [ ! -d "web" ]; then
    echo -e "${RED}❌ Error: Not in Piper Morgan repository root${NC}"
    echo "Please run this script from the repository root directory."
    exit 1
fi

print_status 0 "Repository root verified"

# Prompt for sprint details
echo ""
print_info "Sprint Configuration"
echo "Current date: $CURRENT_DATE"
echo ""

read -p "Sprint name (e.g., 'Core UI Enhancement', 'MCP Integration'): " SPRINT_NAME
if [ -z "$SPRINT_NAME" ]; then
    echo -e "${RED}❌ Sprint name is required${NC}"
    exit 1
fi

read -p "Use current date ($CURRENT_DATE) for sprint? [Y/n]: " USE_CURRENT_DATE
if [[ $USE_CURRENT_DATE =~ ^[Nn]$ ]]; then
    read -p "Enter sprint date (YYYY-MM-DD): " CUSTOM_DATE
    if [[ ! $CUSTOM_DATE =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
        echo -e "${RED}❌ Invalid date format. Use YYYY-MM-DD${NC}"
        exit 1
    fi
    SPRINT_DATE=$CUSTOM_DATE
    YEAR=${CUSTOM_DATE:0:4}
    MONTH=${CUSTOM_DATE:5:2}
    DAY=${CUSTOM_DATE:8:2}
else
    SPRINT_DATE=$CURRENT_DATE
fi

# Create directory structure
SPRINT_DIR="dev/$YEAR/$MONTH/$DAY"
print_info "Creating sprint directory: $SPRINT_DIR"

mkdir -p "$SPRINT_DIR"
print_status $? "Sprint directory created"

mkdir -p "$SPRINT_DIR/session-logs"
print_status $? "Session logs directory created"

mkdir -p "$SPRINT_DIR/artifacts/diagrams"
mkdir -p "$SPRINT_DIR/artifacts/prototypes" 
mkdir -p "$SPRINT_DIR/artifacts/documentation"
print_status 0 "Artifacts directories created"

# Create AGENTS.md
print_info "Creating AGENTS.md with project context"
cat > "$SPRINT_DIR/AGENTS.md" << EOF
# AGENTS.md - Sprint Agent Instructions

## Project Context
You are working on Piper Morgan, an intelligent PM assistant. The project uses:
- Python 3.11+ with FastAPI
- PostgreSQL (port 5433, not 5432)
- Domain-Driven Design
- Port 8001 for web (not 8080)

## Sprint: $SPRINT_NAME
**Date**: $SPRINT_DATE
**Objectives**: [TO BE DEFINED IN sprint-planning.md]

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
\`\`\`bash
ls -la web/ services/ cli/
grep -r "ClassName" . --include="*.py"
\`\`\`
If reality doesn't match instructions: STOP and report.

## Technical Specifics
\`\`\`bash
# Entry point
main.py  # NOT web/app.py for startup

# File locations
web/app.py                   # FastAPI app
services/domain/models.py    # Domain models
services/shared_types.py     # ALL enums
config/PIPER.user.md        # User config (not YAML)

# NO routes/ directory exists

# Testing
PYTHONPATH=. python -m pytest tests/ -xvs

# Database
docker exec -it piper-postgres psql -U piper -d piper_morgan
\`\`\`

## STOP Conditions
- Infrastructure mismatch → STOP
- Pattern already exists → STOP (complete it instead)
- Tests failing → STOP
- No GitHub issue → STOP
- Assuming values → STOP

## Current Focus
**$SPRINT_NAME**: [DEFINE SPECIFIC FOCUS AREA]

## Evidence Required
Show actual output, not summaries:
\`\`\`bash
pytest tests/test_feature.py -xvs  # Full output
curl http://localhost:8001/test     # Real response
\`\`\`

## Remember
1. Verify everything before implementing
2. Complete existing code, don't replace
3. Evidence required for all claims
4. The Inchworm Protocol: 100% complete before moving on
EOF

print_status 0 "AGENTS.md created"

# Create sprint-planning.md
print_info "Creating sprint planning document"
cat > "$SPRINT_DIR/sprint-planning.md" << EOF
# Sprint Planning - $SPRINT_DATE

## Sprint: $SPRINT_NAME

### Sprint Overview
**Start Date**: $SPRINT_DATE
**Duration**: [TO BE DEFINED]
**Sprint Type**: [Development/Research/Integration/Bug Fix]

## Sprint Objectives
- [ ] Objective 1: [DEFINE SPECIFIC OBJECTIVE]
- [ ] Objective 2: [DEFINE SPECIFIC OBJECTIVE] 
- [ ] Objective 3: [DEFINE SPECIFIC OBJECTIVE]

## Success Criteria
- [ ] All objectives completed with evidence
- [ ] Tests passing (100% where applicable)
- [ ] Documentation updated
- [ ] GitHub issues properly tracked
- [ ] No regressions introduced

## Issues to Address
- [ ] Issue 1 (PM-XXX) - [DESCRIPTION]
- [ ] Issue 2 (PM-XXX) - [DESCRIPTION]
- [ ] Issue 3 (PM-XXX) - [DESCRIPTION]

**Note**: Use \`gh issue list --state all --limit 100 | grep "PM-"\` to verify PM numbers

## Architecture Impact
**Components Affected**:
- Component 1: [DESCRIPTION OF CHANGES]
- Component 2: [DESCRIPTION OF CHANGES]

**Integration Points**:
- Integration 1: [DESCRIPTION]
- Integration 2: [DESCRIPTION]

## Technical Approach
**Strategy**: [HIGH-LEVEL TECHNICAL APPROACH]

**Key Technical Decisions**:
1. Decision 1: [RATIONALE]
2. Decision 2: [RATIONALE]

## Definition of Done
- [ ] All code changes implemented and tested
- [ ] Unit tests written/updated (where applicable)
- [ ] Integration tests passing
- [ ] Documentation updated in relevant locations
- [ ] GitHub issues updated with progress and evidence
- [ ] Session logs complete with evidence
- [ ] Code review completed (if applicable)
- [ ] No performance regressions
- [ ] Clean linting and formatting

## Risk Assessment
**High Risk**:
- Risk 1: [DESCRIPTION AND MITIGATION STRATEGY]

**Medium Risk**:
- Risk 2: [DESCRIPTION AND MITIGATION STRATEGY]

**Dependencies**:
- External Dependency 1: [DESCRIPTION]
- Internal Dependency 2: [DESCRIPTION]

## Resource Requirements
**Development Environment**:
- Python 3.11+ with virtual environment
- PostgreSQL running on port 5433
- Docker services available
- GitHub CLI access

**Estimated Effort**: [HOURS/DAYS]

## Key Milestones
- **25% Complete**: [MILESTONE DESCRIPTION]
- **50% Complete**: [MILESTONE DESCRIPTION]  
- **75% Complete**: [MILESTONE DESCRIPTION]
- **100% Complete**: All objectives met with evidence

## Sprint Team
**Primary Agent**: [AGENT ASSIGNMENT]
**Supporting Agents**: [IF APPLICABLE]
**Review/Oversight**: [IF APPLICABLE]

## Communication Plan
**Progress Updates**: [FREQUENCY AND METHOD]
**Escalation Path**: [PROCESS FOR ISSUES]
**Final Handoff**: [DELIVERABLES AND PROCESS]

---

**Created**: $TIMESTAMP
**Last Updated**: $TIMESTAMP
**Status**: Planning
EOF

print_status 0 "Sprint planning document created"

# Create session log template
print_info "Creating session log template"
cat > "$SPRINT_DIR/session-logs/session-log-template.md" << EOF
# [$TIMESTAMP] - [Agent] - [Model] - Session Log

## Sprint Context
**Sprint**: $SPRINT_NAME
**Date**: $SPRINT_DATE
**Objectives**: [REFERENCE sprint-planning.md]

## Session Objectives
- [ ] Objective 1: [SPECIFIC TO THIS SESSION]
- [ ] Objective 2: [SPECIFIC TO THIS SESSION]

## Work Completed
- [x] Task 1: [DESCRIPTION WITH EVIDENCE]
- [x] Task 2: [DESCRIPTION WITH EVIDENCE]
- [ ] Task 3: [IN PROGRESS OR BLOCKED]

## Issues Encountered
**Issue 1**: [DESCRIPTION]
- **Resolution**: [HOW IT WAS SOLVED]
- **Evidence**: [COMMANDS/OUTPUT]

**Issue 2**: [DESCRIPTION]  
- **Resolution**: [HOW IT WAS SOLVED]
- **Evidence**: [COMMANDS/OUTPUT]

## Evidence
\`\`\`bash
# Commands run during this session
command_1
# output here

command_2  
# output here
\`\`\`

## Files Modified
- \`path/to/file1.py\`: [DESCRIPTION OF CHANGES]
- \`path/to/file2.md\`: [DESCRIPTION OF CHANGES]

## Tests Run
\`\`\`bash
# Test commands and results
PYTHONPATH=. python -m pytest tests/test_feature.py -xvs
# output here
\`\`\`

## Next Steps
- [ ] Next task 1: [DESCRIPTION]
- [ ] Next task 2: [DESCRIPTION]

## Sprint Progress Assessment
**Overall Progress**: [X]% complete
**On Track**: [Yes/No/At Risk]
**Blockers**: [LIST ANY BLOCKERS]

## Notes
- Important note 1
- Important note 2

---
**Session Duration**: [START TIME] - [END TIME]
**Next Session**: [PLANNED FOCUS]
EOF

print_status 0 "Session log template created"

# Check for existing PM numbers
print_info "Checking existing PM numbers for reference"
if command -v gh >/dev/null 2>&1; then
    LATEST_PM=$(gh issue list --state all --limit 100 | grep -o "PM-[0-9]*" | sort -V | tail -1)
    if [ -n "$LATEST_PM" ]; then
        print_info "Latest PM number found: $LATEST_PM"
        PM_NUMBER=${LATEST_PM#PM-}
        NEXT_PM=$((PM_NUMBER + 1))
        print_info "Suggested next PM number: PM-$NEXT_PM"
    else
        print_warning "No PM numbers found in recent issues"
    fi
else
    print_warning "GitHub CLI not available - cannot check PM numbers"
    print_info "Manually verify PM numbers with: gh issue list --state all --limit 100 | grep 'PM-'"
fi

# Create README for the sprint
print_info "Creating sprint README"
cat > "$SPRINT_DIR/README.md" << EOF
# Sprint: $SPRINT_NAME

**Date**: $SPRINT_DATE  
**Created**: $TIMESTAMP

## Quick Start

1. **Review Objectives**: See \`sprint-planning.md\` for detailed objectives
2. **Agent Setup**: Read \`AGENTS.md\` for project context and instructions
3. **Start Session**: Copy \`session-logs/session-log-template.md\` for each work session
4. **Track Progress**: Update \`sprint-planning.md\` as objectives are completed

## Directory Structure

\`\`\`
$DAY/
├── AGENTS.md              # Agent instructions and project context
├── sprint-planning.md     # Detailed sprint plan and objectives  
├── README.md             # This file
├── session-logs/         # Daily work session logs
│   └── session-log-template.md
└── artifacts/            # Sprint-specific artifacts
    ├── diagrams/         # Architecture diagrams, flowcharts
    ├── prototypes/       # Code prototypes and experiments
    └── documentation/    # Sprint-specific documentation
\`\`\`

## Workflow

1. **Daily Sessions**: Create new session log from template
2. **Progress Tracking**: Update sprint-planning.md checkboxes
3. **Evidence Collection**: Include command outputs in session logs
4. **Issue Management**: Reference PM-XXX numbers for all work

## Key Files to Update

- \`sprint-planning.md\`: Mark objectives complete with evidence
- Session logs: Document all work with evidence  
- GitHub issues: Update with progress and reference session logs

## Sprint Completion

When sprint is complete:
1. Mark all objectives complete in \`sprint-planning.md\`
2. Create \`retrospective.md\` using template
3. Update all related GitHub issues
4. Archive session logs
5. Create handoff documentation if needed

---

**Reference**: See \`docs/internal/development/methodology-core/methodology-21-SPRINT-CREATION.md\` for full methodology
EOF

print_status 0 "Sprint README created"

# Summary
echo ""
echo -e "${GREEN}🎉 Sprint Created Successfully!${NC}"
echo ""
echo -e "${BLUE}Sprint Details:${NC}"
echo "  Name: $SPRINT_NAME"
echo "  Date: $SPRINT_DATE"  
echo "  Directory: $SPRINT_DIR"
echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo "1. Navigate to sprint directory: cd $SPRINT_DIR"
echo "2. Edit sprint-planning.md to define specific objectives"
echo "3. Create GitHub issues with proper PM-XXX numbers"
echo "4. Begin sprint execution following AGENTS.md guidance"
echo ""
if [ -n "$NEXT_PM" ]; then
    echo -e "${BLUE}Suggested PM Number:${NC} PM-$NEXT_PM (verify with GitHub first)"
else
    echo -e "${YELLOW}⚠️  Verify PM numbers manually:${NC} gh issue list --state all --limit 100 | grep 'PM-'"
fi
echo ""
echo -e "${GREEN}Sprint directory ready for development!${NC}"
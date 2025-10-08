# Methodology 21: Sprint Creation Protocol

**Status**: ✅ **ACTIVE** - Systematic Sprint Creation Process
**Created**: October 8, 2025
**Last Updated**: October 8, 2025

## 🎯 The Problem

Creating new sprints in Piper Morgan requires understanding the project structure, development workflows, and proper issue tracking. Without a systematic approach, sprints can be created incorrectly, leading to:
- Inconsistent directory structures
- Missing documentation templates
- Improper issue tracking setup
- Confusion about sprint scope and objectives

## 🛡️ The Sprint Creation Protocol

### **CRITICAL COMPONENTS - ALWAYS INCLUDE**

1. **Date-based development directory structure**
2. **Sprint planning documentation**
3. **Issue verification and PM number assignment**
4. **Agent coordination setup**
5. **Session logging preparation**

## 🔍 Sprint Creation Process

### **Step 1: Determine Sprint Date and Structure**

```bash
# Get current date
SPRINT_DATE=$(date +"%Y-%m-%d")
YEAR=$(date +"%Y")
MONTH=$(date +"%m")
DAY=$(date +"%d")

echo "Creating sprint for: $SPRINT_DATE"
```

### **Step 2: Create Development Directory Structure**

The project uses a date-based structure in `dev/YYYY/MM/DD/`:

```bash
# Navigate to repository root
cd /path/to/piper-morgan-product

# Create date-based directory structure
mkdir -p "dev/$YEAR/$MONTH/$DAY"

# Create session structure
cd "dev/$YEAR/$MONTH/$DAY"
```

### **Step 3: Set Up Sprint Documentation**

Create the essential sprint files:

```bash
# Create AGENTS.md with current project context
cat > AGENTS.md << 'EOF'
# AGENTS.md - Sprint Agent Instructions

## Project Context
You are working on Piper Morgan, an intelligent PM assistant. The project uses:
- Python 3.11+ with FastAPI
- PostgreSQL (port 5433, not 5432)
- Domain-Driven Design
- Port 8001 for web (not 8080)

## Sprint Objectives
[Define specific objectives for this sprint]

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
[Define the current epic/focus area]

## Evidence Required
Show actual output, not summaries:
```bash
pytest tests/test_feature.py -xvs  # Full output
curl http://localhost:8001/test     # Real response
```
EOF

# Create sprint planning document
cat > sprint-planning.md << 'EOF'
# Sprint Planning - [DATE]

## Sprint Objectives
- [ ] Objective 1
- [ ] Objective 2
- [ ] Objective 3

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Issues to Address
- [ ] Issue 1 (PM-XXX)
- [ ] Issue 2 (PM-XXX)
- [ ] Issue 3 (PM-XXX)

## Definition of Done
- [ ] All code changes tested
- [ ] Documentation updated
- [ ] GitHub issues updated
- [ ] Session logs complete

## Risk Assessment
- **Risk 1**: Description and mitigation
- **Risk 2**: Description and mitigation

## Dependencies
- Dependency 1
- Dependency 2

## Estimated Duration
**Sprint Length**: [X days/hours]
**Key Milestones**:
- Day 1: Milestone 1
- Day 2: Milestone 2
- Final: Sprint completion
EOF
```

### **Step 4: Issue Verification and PM Number Assignment**

Follow the established issue tracking protocol from methodology-08:

```bash
# Verify current PM numbers in GitHub
gh issue list --state all --limit 100 | grep "PM-" | sort -V | tail -10

# Check CSV file for current PM numbers
grep "PM-" docs/planning/pm-issues-status.csv | sort -V | tail -5

# Check backlog for referenced PM numbers
grep "PM-" docs/planning/backlog.md

# Determine next valid PM number
# Example: If highest is PM-125, next is PM-126
```

### **Step 5: Create Sprint Issues**

```bash
# Create main sprint tracking issue
gh issue create \
  --title "PM-XXX: Sprint [DATE] - [SPRINT_NAME]" \
  --body "Sprint tracking issue for [SPRINT_OBJECTIVES]

## Sprint Scope
- Objective 1
- Objective 2  
- Objective 3

## Sprint Duration
Start: [DATE]
End: [DATE]

## Team
- Agent assignments
- Role definitions

## Success Criteria
- [ ] All objectives completed
- [ ] Tests passing
- [ ] Documentation updated

## Related Issues
- Closes #XXX
- Related to #XXX
" \
  --label "sprint" \
  --label "planning"
```

## 📁 Sprint Directory Structure

A properly created sprint should have this structure:

```
dev/YYYY/MM/DD/
├── AGENTS.md                    # Agent instructions for this sprint
├── sprint-planning.md           # Sprint objectives and planning
├── session-logs/                # Directory for session logs
│   ├── YYYY-MM-DD-HHMM-agent-model-log.md
│   └── ...
├── gameplan.md                  # Detailed execution plan (optional)
├── retrospective.md             # Sprint retrospective (end of sprint)
└── artifacts/                   # Sprint-specific artifacts
    ├── diagrams/
    ├── prototypes/
    └── documentation/
```

## 🔧 Sprint Templates

### **Daily Session Log Template**

```markdown
# [YYYY-MM-DD-HHMM] - [Agent] - [Model] - Session Log

## Sprint Context
Sprint: [SPRINT_NAME]
Objectives: [LIST_OBJECTIVES]

## Session Objectives
- [ ] Objective 1
- [ ] Objective 2

## Work Completed
- [x] Task 1
- [x] Task 2
- [ ] Task 3 (in progress)

## Issues Encountered
- Issue 1: Description and resolution
- Issue 2: Description and resolution

## Evidence
```bash
# Commands run
command_output_here
```

## Next Steps
- [ ] Next task 1
- [ ] Next task 2

## Sprint Progress
Overall progress: [X]% complete
```

### **Sprint Retrospective Template**

```markdown
# Sprint Retrospective - [DATE]

## Sprint Summary
**Objectives**: [ORIGINAL_OBJECTIVES]
**Completed**: [WHAT_WAS_COMPLETED]
**Duration**: [ACTUAL_DURATION]

## What Went Well
- Success 1
- Success 2

## What Could Be Improved
- Improvement 1
- Improvement 2

## Lessons Learned
- Lesson 1
- Lesson 2

## Action Items for Next Sprint
- [ ] Action 1
- [ ] Action 2

## Metrics
- Issues completed: X/Y
- Tests added: X
- Documentation updated: Yes/No
- Performance improvements: [DETAILS]
```

## 🚀 Sprint Execution Workflow

### **1. Sprint Kickoff**
```bash
# Navigate to sprint directory
cd dev/YYYY/MM/DD/

# Initialize session log
cp templates/session-log-template.md session-logs/$(date +"%Y-%m-%d-%H%M")-kickoff-log.md

# Start development environment
source venv/bin/activate
docker-compose up -d
```

### **2. Daily Work**
- Create dated session logs
- Follow AGENTS.md instructions
- Update sprint-planning.md progress
- Commit changes with proper messages

### **3. Sprint Close**
```bash
# Create retrospective
cp templates/retrospective-template.md retrospective.md

# Update all GitHub issues
# Create handoff documentation if needed
# Archive session logs
```

## 🔄 Integration Points

### **GitHub Integration**
- Sprint issues must follow PM-XXX numbering
- Labels: `sprint`, `planning`, specific focus areas
- Milestones: Link to sprint objectives

### **Development Environment**
- All sprints use standard dev environment setup
- Database on port 5433
- Web server on port 8001
- Standard testing with pytest

### **Documentation**
- Sprint docs live in `dev/YYYY/MM/DD/`
- Methodology references in `docs/internal/development/methodology-core/`
- Architecture decisions in ADRs as needed

## 📊 Success Metrics

- **Sprint Completion Rate**: % of objectives completed
- **Issue Resolution**: All PM numbers properly tracked
- **Documentation Quality**: All templates filled
- **Code Quality**: Tests passing, linting clean
- **Handoff Quality**: Clear continuation path

## 🚨 Common Pitfalls to Avoid

### **❌ NEVER DO THESE**
- Create sprints without date structure
- Skip PM number verification
- Miss AGENTS.md creation  
- Forget session logging setup
- Ignore existing methodology

### **✅ ALWAYS DO THESE**
- Follow date-based directory structure
- Verify PM numbers before creation
- Set up agent coordination
- Create comprehensive documentation
- Plan for sprint handoff

## 🎯 Quick Sprint Creation Checklist

- [ ] Determine sprint date and objectives
- [ ] Create `dev/YYYY/MM/DD/` structure
- [ ] Create AGENTS.md with project context
- [ ] Create sprint-planning.md with objectives
- [ ] Verify and assign PM numbers
- [ ] Create GitHub sprint issue
- [ ] Set up session logging structure
- [ ] Initialize development environment
- [ ] Brief participating agents
- [ ] Begin sprint execution

---

**Status**: ✅ **PROTOCOL ESTABLISHED** - Ready for systematic sprint creation across all development cycles.

**Next Action**: Create sprint creation automation script for consistent setup.
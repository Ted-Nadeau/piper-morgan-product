# Phase 2 Testing - Quick Reference Card

**Generated From**: Code's archaeological investigation
**Date**: Sunday, October 26, 2025
**Purpose**: One-page command reference for E2E testing

---

## Essential Commands

### System Operations

**Start System**:
```bash
[ACTUAL COMMAND - from Code's report]
```

**Check Health**:
```bash
[ACTUAL COMMAND - from Code's report]
```

**Database Status**:
```bash
[ACTUAL COMMAND - from Code's report]
```

**Service Status**:
```bash
[ACTUAL COMMAND - from Code's report]
```

---

## User Management

### Test Users

**Alpha User** (alex-alpha):
```bash
[ACTUAL COMMAND - from Code's report]
```

**Power User** (pat-power):
```bash
[ACTUAL COMMAND - from Code's report]
```

**Edge Case User** (eve-edge):
```bash
[ACTUAL COMMAND - from Code's report]
```

### User Context

**Set User**:
```bash
[ACTUAL METHOD - from Code's report]
```

**Switch User**:
```bash
[ACTUAL METHOD - from Code's report]
```

---

## Core Features (MUST WORK)

### Onboarding

**Setup Wizard**:
```bash
[ACTUAL COMMAND - from Code's report]
Location: [FILE PATH]
```

**First Run**:
```bash
[ACTUAL COMMAND - from Code's report]
```

### API Keys

**Add Key**:
```bash
[ACTUAL COMMAND - from Code's report]
Location: [FILE PATH]
```

**List Keys**:
```bash
[ACTUAL COMMAND - from Code's report]
```

**Validate Key**:
```bash
[ACTUAL COMMAND - from Code's report]
```

### Chat

**Basic Chat**:
```bash
[ACTUAL COMMAND - from Code's report]
Location: [FILE PATH]
```

**Chat with Context**:
```bash
[ACTUAL COMMAND - from Code's report]
```

---

## Sprint A8 Features (IF EXISTS)

### Preferences (#267, #269)

**Run Questionnaire**:
```bash
[ACTUAL COMMAND - from Code's report]
Location: [FILE PATH]
Status: [READY/PARTIAL/MISSING]
```

**View Preferences**:
```bash
[ACTUAL COMMAND - from Code's report]
```

**Test Preference Effect**:
```bash
[ACTUAL TEST COMMAND - from Code's report]
```

### Cost Tracking (#271)

**View Costs**:
```bash
[ACTUAL COMMAND - from Code's report]
Location: [FILE PATH]
Status: [READY/PARTIAL/MISSING]
```

**Cost by Date**:
```bash
[ACTUAL COMMAND - from Code's report]
```

### Knowledge Graph (#278)

**Test Graph Reasoning**:
```bash
# From Chief Architect
python main.py chat "I prefer morning meetings because I have more energy"
python main.py chat "When should we schedule the architecture review?"
# EXPECT: Second response suggests morning
```

**Graph Status**:
```bash
[ACTUAL COMMAND - from Code's report if exists]
Location: [FILE PATH]
Status: [READY/PARTIAL/MISSING]
```

### Key Validation (#268)

**Test Invalid Key**:
```bash
[ACTUAL COMMAND - from Code's report]
# EXPECT: Rejection with clear error
```

**Test Valid Key**:
```bash
[ACTUAL COMMAND - from Code's report]
# EXPECT: Success, key stored
```

---

## Integrations (IF EXISTS)

### GitHub

**Status Check**:
```bash
[ACTUAL COMMAND - from Code's report]
Location: [FILE PATH]
Status: [READY/PARTIAL/MISSING]
```

**Test Query**:
```bash
[ACTUAL COMMAND - from Code's report]
```

### Calendar

**Status Check**:
```bash
[ACTUAL COMMAND - from Code's report]
Location: [FILE PATH]
Status: [READY/PARTIAL/MISSING]
```

**Test Query**:
```bash
[ACTUAL COMMAND - from Code's report]
```

### Slack

**Status Check**:
```bash
[ACTUAL COMMAND - from Code's report]
Location: [FILE PATH]
Status: [READY/PARTIAL/MISSING]
```

**Test Query**:
```bash
[ACTUAL COMMAND - from Code's report]
```

### Notion

**Status Check**:
```bash
[ACTUAL COMMAND - from Code's report]
Location: [FILE PATH]
Status: [READY/PARTIAL/MISSING]
```

**Test Query**:
```bash
[ACTUAL COMMAND - from Code's report]
```

---

## Testing Infrastructure

### Run Tests

**All Tests**:
```bash
pytest tests/ -xvs
```

**Specific Suite**:
```bash
pytest tests/integration/ -xvs
```

**With Coverage**:
```bash
pytest tests/ --cov=services --cov-report=html
```

### Integration Tests

**Preferences → Behavior**:
```bash
[ACTUAL COMMAND - from Code's report if exists]
```

**Cost → Database**:
```bash
[ACTUAL COMMAND - from Code's report if exists]
```

**Graph → Retrieval**:
```bash
[ACTUAL COMMAND - from Code's report if exists]
```

---

## Evidence Collection

### Screenshots
```bash
# macOS
Command+Shift+4

# Save to:
~/Desktop/piper-phase2-evidence/
```

### Terminal Output
```bash
# Capture command output
command 2>&1 | tee evidence-[test-name].log
```

### Timing
```bash
# Time a command
time python main.py [command]
```

---

## Troubleshooting

### System Won't Start
```bash
# Check logs
[ACTUAL COMMAND - from Code's report]

# Restart services
[ACTUAL COMMAND - from Code's report]

# Clear cache
[ACTUAL COMMAND - from Code's report]
```

### Database Issues
```bash
# Check connection
[ACTUAL COMMAND - from Code's report]

# Reset test data
[ACTUAL COMMAND - from Code's report]

# Run migrations
alembic upgrade head
```

### Integration Failures
```bash
# Check credentials
[ACTUAL COMMAND - from Code's report]

# Test connection
[ACTUAL COMMAND - from Code's report]

# View logs
[ACTUAL COMMAND - from Code's report]
```

---

## File Locations (from Code's Report)

**Main Entry**: [PATH]
**Setup Wizard**: [PATH]
**Key Validator**: [PATH]
**Preferences**: [PATH]
**Cost Tracker**: [PATH]
**Knowledge Graph**: [PATH]
**Integrations**: [PATHS]

---

## Environment Variables

**Required**:
```bash
export [VARS FROM CODE'S REPORT]
```

**Optional**:
```bash
export [VARS FROM CODE'S REPORT]
```

**Test Mode**:
```bash
export [VARS FROM CODE'S REPORT]
```

---

## Priority Tags Quick Reference

- **[MUST WORK]** - Alpha blocker if broken
- **[IF EXISTS]** - Try and document reality
- **[FUTURE]** - Skip, note absence

---

## Success Checklist

**Before Starting**:
- [ ] System running on port 8001
- [ ] Database connected
- [ ] Environment variables set
- [ ] Test users created (if needed)

**During Testing**:
- [ ] Capture all terminal output
- [ ] Screenshot each step
- [ ] Note timing for operations
- [ ] Document confusion points

**After Testing**:
- [ ] Bugs documented with evidence
- [ ] Test results summarized
- [ ] Known issues listed
- [ ] Go/no-go recommendation

---

*Quick Reference v1.0*
*Update with Code's actual findings*
*Print for testing session*

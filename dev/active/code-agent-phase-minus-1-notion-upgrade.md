# Code Agent Prompt: Phase -1 - Notion API Upgrade Investigation

**Date**: October 15, 2025, 11:08 AM
**Sprint**: A2 - Notion & Errors
**Issue**: CORE-NOTN-UP #165 - Database API upgrade to 2025-09-03
**Phase**: -1 (Investigation)
**Duration**: 30-45 minutes
**Agent**: Code Agent

---

## Mission

Investigate Piper Morgan's current Notion API integration to understand the impact of Notion's new API version 2025-09-03 and plan the migration.

**Context**: Notion released a breaking change separating "databases" from "data sources". We need to update our integration before users add multiple data sources to databases.

**Philosophy**: Understand the changes, assess impact, plan migration carefully.

---

## Background: What Changed in Notion API

**From Google AI Summary**:

### Key Changes (API Version 2025-09-03)
1. **Database vs Data Source Split**:
   - Database = container for one or more data sources
   - Data Source = has properties (schema) and rows (pages)
   - Previously these were one thing, now they're separate

2. **New API Endpoints**:
   - OLD: `Update a database` (deprecated for 2025-09-03+)
   - NEW: `Update a database` (database-level operations)
   - NEW: `Update a data source` (schema/content operations)
   - `GET /v1/databases/:database_id` now returns child data sources list

3. **Migration Requirements**:
   - Store `data_source_id` alongside `database_id`
   - Use new endpoints for schema/content updates
   - Add `Notion-Version: 2025-09-03` header
   - Handle 50KB schema size limits

4. **Breaking Changes**:
   - Single-source databases: Continue working ✅
   - Multi-source databases: Will break if not updated ❌
   - Creating pages, updating databases will fail

---

## Investigation Steps

### Step 1: Find Current API Version Usage

```bash
# Search for Notion API version specifications
grep -r "Notion-Version\|notion.*version\|api.*version" services/integrations/notion --include="*.py" -i

# Check for API client initialization
grep -r "notion.*client\|NotionClient" services/integrations/ --include="*.py" -A 5

# Look in MCP adapter (likely place)
view services/integrations/mcp/notion_adapter.py -r [1, 50]
```

**Document**:
- Current API version (if specified)
- Where version is configured
- How API client is initialized

---

### Step 2: Identify Database Operations

```bash
# Find database-related API calls
grep -r "database" services/integrations/notion --include="*.py" -i | grep -E "create|update|query|get" | head -20

# Look for specific operations mentioned in email
grep -r "create.*page\|update.*database\|query.*database" services/integrations/notion --include="*.py" -i

# Check NotionMCPAdapter for database methods
grep -n "def.*database" services/integrations/mcp/notion_adapter.py -i
```

**Document**:
- Which operations use database APIs?
- Do we create pages in databases? (YES - ADR publishing)
- Do we update databases?
- Do we query databases?

---

### Step 3: Fetch Notion's Official Upgrade Guide

```bash
# Fetch the upgrade guide
web_fetch("https://developers.notion.com/docs/upgrade-guide-2025-09-03")

# Also fetch the FAQ
web_fetch("https://developers.notion.com/docs/upgrade-faqs-2025-09-03")
```

**Document**:
- Exact breaking changes
- Migration steps recommended by Notion
- Code examples from guide
- Timeline/urgency

---

### Step 4: Review Current Database Configuration

```bash
# Check our database configuration
grep -A 10 "database" config/PIPER.user.md

# We know from earlier:
# adrs.database_id: 25e11704d8bf80deaac2f806390fe7da
```

**Document**:
- Which databases we use (ADR database confirmed)
- Are we currently single-source? (likely yes)
- Configuration structure

---

### Step 5: Assess ADR Publishing Code

```bash
# ADR publishing likely uses database APIs
find services/integrations/notion -name "*adr*.py" -o -name "*publish*.py" | head -10

# Check for page creation in databases
grep -r "create.*page" services/integrations/notion --include="*.py" -A 3 | head -30
```

**Document**:
- How ADR publishing works
- What database operations it uses
- Affected code locations

---

### Step 6: Check for Webhooks

```bash
# Check for webhook handling
grep -r "webhook" services/integrations/notion --include="*.py" -i

# Check MCP adapter for webhook support
grep -n "webhook" services/integrations/mcp/notion_adapter.py -i
```

**Document**:
- Do we use webhooks?
- Webhook versioning impact

---

### Step 7: Review notion-sdk-py Library

```bash
# Check which Notion SDK we're using
grep -r "notion-client\|notion-sdk-py" requirements.txt pyproject.toml setup.py 2>/dev/null || echo "Check package files"

# Find imports
grep -r "from notion_client\|import notion_client" services/integrations/notion --include="*.py"
```

**Document**:
- Which SDK/library version?
- Does SDK support new API version?
- Need SDK update?

---

## Investigation Report

Create: `/tmp/phase-minus-1-notion-api-upgrade.md`

```markdown
# Phase -1: Notion API Upgrade Investigation

**Date**: October 15, 2025  
**Issue**: CORE-NOTN-UP #165  
**API Version**: Old → 2025-09-03

---

## Current State

### API Version
**Current Version**: [version found or "unspecified"]
**Location**: [where configured]
**SDK**: [notion-client version]

### Database Operations

**Operations We Use**:
- [ ] Create pages in databases (ADR publishing)
- [ ] Update database schema
- [ ] Query database
- [ ] Get database info
- [ ] Other: [list]

**Affected Code**:
- File: [path]
- Method: [name]
- Operation: [what it does]

### Current Database Usage

**Databases**:
- ADR Database: `25e11704d8bf80deaac2f806390fe7da`
- [any others]

**Data Source Count**: [currently single-source]

---

## Breaking Changes (From Notion Docs)

### What Breaks

1. **[Breaking change 1]**: [description]
   - Impact on us: [high/medium/low]
   - Why: [explanation]

2. **[Breaking change 2]**: [description]
   - Impact on us: [high/medium/low]

### What Continues Working

- Single-source database operations
- [other non-breaking operations]

---

## Migration Requirements

### Required Code Changes

1. **Add API Version Header**:
   ```python
   # Current:
   [current code]
   
   # Required:
   headers = {"Notion-Version": "2025-09-03"}
   ```

2. **Store data_source_id**:
   - Current: Only store `database_id`
   - Required: Store both `database_id` and `data_source_id`
   - Location: [where to add]

3. **Update API Endpoints**:
   - Replace: [old endpoint]
   - With: [new endpoint]
   - Location: [code files]

4. **[Other changes]**: [description]

---

## Impact Assessment

### High Impact Areas
- ADR publishing (creates pages in database)
- [other areas]

### Medium Impact Areas
- [areas]

### Low Impact Areas
- [areas]

### Risk Level

**Overall Risk**: [HIGH / MEDIUM / LOW]

**Why**: [explanation]

**Urgency**: [URGENT / MODERATE / LOW]
- Current: Works with single-source ✅
- Breaks when: User adds second data source
- Timeline: Before multi-source usage

---

## Migration Plan

### Phase 1: SDK Update
**Duration**: [estimate]
**Tasks**:
- [ ] Update notion-client to version supporting 2025-09-03
- [ ] Test SDK compatibility
- [ ] Update requirements.txt

### Phase 2: Add Version Header
**Duration**: [estimate]
**Tasks**:
- [ ] Add Notion-Version header to all API calls
- [ ] Configure in adapter initialization
- [ ] Test with current operations

### Phase 3: Handle Data Source IDs
**Duration**: [estimate]
**Tasks**:
- [ ] Update code to fetch data_source_id
- [ ] Store data_source_id in configuration
- [ ] Update database operations to use data_source_id

### Phase 4: Update API Endpoints
**Duration**: [estimate]
**Tasks**:
- [ ] Replace deprecated endpoints
- [ ] Update to new database/data source APIs
- [ ] Test all operations

### Phase 5: Testing & Validation
**Duration**: [estimate]
**Tasks**:
- [ ] Test ADR publishing
- [ ] Test with real API
- [ ] Verify no regressions

**Total Estimate**: [X hours/days]

---

## Open Questions

1. Does our Notion SDK support API version 2025-09-03?
2. Do we currently use any deprecated endpoints?
3. Should we update preemptively or wait until needed?
4. Testing strategy for multi-source databases?

---

## Recommendations

### Recommended Approach
[Sequential / Iterative / Big Bang]

**Justification**: [why]

### Priority
[HIGH / MEDIUM / LOW]

**Justification**: [why]

### Timeline
**Recommended Start**: [when]
**Target Completion**: [when]
**Reason**: [explanation]

---

## Next Steps

1. [First step]
2. [Second step]
3. [etc.]

**Ready to proceed**: [YES / NO / DEPENDS]
```

---

## Deliverables

### Investigation Complete When:
- [ ] Current API version identified
- [ ] Database operations documented
- [ ] Notion upgrade guide reviewed
- [ ] Breaking changes understood
- [ ] Impact assessment complete
- [ ] Migration plan drafted
- [ ] Open questions listed
- [ ] Recommendations provided

---

## Time Budget

**Target**: 30-45 minutes
- Current state review: 10 min
- Fetch/read Notion docs: 10 min
- Identify affected code: 10 min
- Impact assessment: 5 min
- Migration planning: 10 min

---

## What NOT to Do

- ❌ Don't implement changes yet (investigation only)
- ❌ Don't update SDK yet
- ❌ Don't change API version yet
- ❌ Don't modify any code

## What TO Do

- ✅ Understand current state thoroughly
- ✅ Read Notion's official docs carefully
- ✅ Identify all affected code
- ✅ Assess impact realistically
- ✅ Plan migration systematically
- ✅ Document everything clearly

---

## Success Criteria

**Investigation is successful when**:
- Clear understanding of breaking changes
- Complete inventory of affected code
- Realistic impact assessment
- Actionable migration plan
- Informed recommendation
- Can confidently implement migration

---

## Context

**Why This Matters**:
- External API breaking change (not our choice)
- Will break ADR publishing if not updated
- Need to act before users add multi-source databases
- Proper planning prevents issues

**What Comes After**:
- Phase 1: Implement migration
- Phase 2: Test thoroughly
- Phase 3: Validate with real API

---

**Phase -1 Start Time**: 11:10 AM  
**Expected Completion**: ~11:40-11:55 AM (30-45 minutes)  
**Status**: Ready for investigation

**LET'S INVESTIGATE!** 🔍

---

*"Understand external changes before adapting to them."*
*- API Migration Philosophy*

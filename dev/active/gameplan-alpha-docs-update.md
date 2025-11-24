# Gameplan: Issue #377 - Alpha Documentation Update

**Date**: November 23, 2025, 5:30 PM
**Estimated Duration**: 60-90 minutes (investigation + updates)
**For**: Michelle Hertzfeld's alpha arrival tomorrow (Nov 24)

---

## Current State Assessment

### Alpha Docs Found ✅

**Location**: `/docs/` (root level)

**Files Identified**:
1. `ALPHA_QUICKSTART.md` - Last updated: Nov 18, 2025 (file timestamp)
2. `ALPHA_KNOWN_ISSUES.md` - Last updated: Nov 18, 2025 (file timestamp) ⚠️ (content from Oct 24)
3. `ALPHA_TESTING_GUIDE.md` - Last updated: Nov 21, 2025 (file timestamp) ⚠️ (content may be outdated)
4. `ALPHA_AGREEMENT_v2.md` - Last updated: Nov 11, 2025 (version 2.1, software 0.8.0-alpha)

**Age Analysis**:
- Agreement: Nov 11 (5 days old) - version numbers, legal terms
- Quickstart: Nov 18 (5 days old) - need to verify content vs today's features
- Known Issues: Nov 18 (5 days old) - content from Oct 24, 30 days outdated ❗
- Testing Guide: Nov 21 (2 days old) - need to verify content is current

**Major Changes Since Oct 24**:
- SEC-RBAC implementation (owner_id, shared_with JSONB)
- Frontend permission awareness (Lists, Todos, Projects, Files)
- UI Quick Fixes (14 navigation QA issues fixed today)
- Logout functionality
- File upload UI
- Standup generation
- Conversational permission commands

---

## Investigation Required

### Phase 0: Audit (20 min)

**What to Check**:

0. **ALPHA_AGREEMENT_v2.md**:
   - Is software version current (says 0.8.0-alpha)?
   - Are any outdated features mentioned?
   - Do privacy/security claims match today's SEC-RBAC?
   - Is contact info current?

1. **ALPHA_QUICKSTART.md**:
   - Does setup wizard still work as described?
   - Are CLI commands still accurate?
   - Does it mention new features (Files, Lists, Todos)?
   - Are port numbers correct?
   - Is version number current?

2. **ALPHA_KNOWN_ISSUES.md**:
   - Are listed issues still issues?
   - Are NEW issues from today documented?
   - Does "What Works" section reflect today's fixes?
   - Is SEC-RBAC mentioned?
   - Are 14 UI fixes mentioned?

3. **ALPHA_TESTING_GUIDE.md**:
   - Is onboarding flow still accurate?
   - Does it mention new UI (Lists/Todos/Projects/Files)?
   - Are authentication steps current (logout works now)?
   - Does troubleshooting cover new features?

**Deliverable**: Audit report listing outdated sections

---

### Phase 1: Known Issues Update (30 min)

**Objective**: Document current system state accurately

**What to Add**:

1. **What's Fixed Since Oct 24**:
   - ✅ Logout functionality (Issue #379-14)
   - ✅ Create Lists/Todos (Issue #379-6,7)
   - ✅ Files upload/download/delete (Issue #379-8)
   - ✅ Standup generation (Issue #379-4)
   - ✅ Integrations page (no more 404) (Issue #379-13)
   - ✅ SEC-RBAC Phase 1 complete (owner_id validation)
   - ✅ Permission-aware UI (sharing, role badges)
   - ✅ Conversational permission commands

2. **What's NEW**:
   - ✅ Lists management (/lists)
   - ✅ Todos management (/todos)
   - ✅ Projects management (/projects)
   - ✅ Files upload/download (/files)
   - ✅ Permission sharing UI
   - ✅ Natural language permission commands
   - ✅ User menu with logout
   - ✅ Breadcrumb navigation

3. **What's Still Known Issues**:
   - ⚠️ Any remaining cosmetic issues?
   - ⚠️ Performance limitations?
   - ⚠️ Browser compatibility?
   - ⚠️ Integration status (Slack, GitHub, Notion)?

**Deliverable**: Updated ALPHA_KNOWN_ISSUES.md

---

### Phase 2: Quickstart Update (20 min)

**Objective**: Ensure first-run experience matches reality

**What to Update**:

1. **Version Number**:
   - Current says 0.8.0
   - What should it be? (Check with PM)

2. **First Commands**:
   - Add: "Create a new list"
   - Add: "Upload a file"
   - Add: "Share this list with [email]"
   - Update: Logout now works

3. **What's Working Section**:
   - Add: Lists, Todos, Projects, Files UI
   - Add: Permission sharing
   - Add: SEC-RBAC owner_id validation

**Deliverable**: Updated ALPHA_QUICKSTART.md

---

### Phase 3: Testing Guide Update (30 min)

**Objective**: Reflect new UI and features

**What to Add**:

1. **Feature Tour Section**:
```markdown
## Exploring Piper's Features

### Lists, Todos, and Projects
1. Click "Lists" in navigation
2. Click "Create New List"
3. Try sharing a list with another user
4. Notice permission badges (Owner, Editor, Viewer)

### File Management
1. Click "Files" in navigation
2. Upload a document (PDF, DOCX, TXT, MD, JSON - max 10MB)
3. Download and delete files
4. Files are private to you (owner_id-based)

### Permission System
Try these natural language commands:
- "share my project plan with alex@example.com as editor"
- "who can access my shopping list?"
- "show me shared projects"
```

2. **Troubleshooting Updates**:
```markdown
### Can't create lists/todos?
- This was fixed Nov 23, 2025
- Make sure you're on latest commit
- Try refreshing the page

### Can't log out?
- This was fixed Nov 23, 2025
- Click user menu (top right)
- Click "Logout"
```

3. **What to Test Section**:
```markdown
## Alpha Testing Focus Areas

**High Priority**:
- [ ] Create lists, todos, projects
- [ ] Upload, download, delete files
- [ ] Share resources with other users
- [ ] Test permission system (Viewer can't edit)
- [ ] Logout and log back in
- [ ] Generate standup reports

**Medium Priority**:
- [ ] Conversational permission commands
- [ ] Breadcrumb navigation
- [ ] Mobile responsiveness
- [ ] Learning dashboard
```

**Deliverable**: Updated ALPHA_TESTING_GUIDE.md

---

## Implementation Plan

### Step 1: Audit All Three Docs (20 min)

**Method**:
1. Read each doc line by line
2. Compare claims to actual system state
3. Mark outdated sections
4. List missing features

**Create**: `dev/2025/11/23/alpha-docs-audit-report.md`

### Step 2: Update Known Issues (30 min)

**Method**:
1. Review all closed issues from Nov 22-23
2. Update "What Works" section
3. Add new features section
4. Remove fixed issues from "Known Issues"
5. Add any remaining issues

**Verify**:
- Every feature listed is actually working
- No outdated information
- Clear and honest about limitations

### Step 3: Update Quickstart (20 min)

**Method**:
1. Update version number (if needed)
2. Add new "First Commands" examples
3. Update "What's Working" section
4. Test actual setup flow matches docs

**Verify**:
- Setup steps still accurate
- Commands actually work
- Links valid

### Step 4: Update Testing Guide (30 min)

**Method**:
1. Add "Feature Tour" section
2. Update troubleshooting
3. Add "What to Test" checklist
4. Update screenshots (if time permits)

**Verify**:
- New features documented
- Troubleshooting current
- Testing focus clear

---

## Validation Protocol

### Test 1: Fresh Eyes
1. Read quickstart as if new user
2. Note any confusing sections
3. Update for clarity

### Test 2: Command Accuracy
1. Try every command listed
2. Verify output matches documentation
3. Update if different

### Test 3: Feature Completeness
1. List all features from today's work
2. Verify each is documented
3. Add missing ones

---

## Success Criteria

### Documentation Accurate ✅
- [ ] Every feature documented works as described
- [ ] Every command tested and verified
- [ ] No outdated information
- [ ] Version numbers current

### User Experience ✅
- [ ] New user can onboard following quickstart
- [ ] Known issues clearly stated
- [ ] Bug reporting process clear
- [ ] Contact information current

### Completeness ✅
- [ ] All new features documented
- [ ] All fixes from today mentioned
- [ ] Troubleshooting updated
- [ ] Testing focus clear

---

## Deliverables

**Phase 0**:
- `dev/2025/11/23/alpha-docs-audit-report.md`

**Phase 1**:
- Updated `docs/ALPHA_KNOWN_ISSUES.md`

**Phase 2**:
- Updated `docs/ALPHA_QUICKSTART.md`

**Phase 3**:
- Updated `docs/ALPHA_TESTING_GUIDE.md`

**Final**:
- `dev/2025/11/23/issue-377-completion-evidence.md`

---

## Timeline

**5:30 PM - 5:50 PM**: Phase 0 Audit (20 min)
**5:50 PM - 6:20 PM**: Phase 1 Known Issues (30 min)
**6:20 PM - 6:40 PM**: Phase 2 Quickstart (20 min)
**6:40 PM - 7:10 PM**: Phase 3 Testing Guide (30 min)
**7:10 PM - 7:20 PM**: Validation & Evidence (10 min)

**Total**: 100 minutes
**Target Completion**: 7:20 PM

---

## Key Updates Needed

### ALPHA_KNOWN_ISSUES.md

**Add to "What Works"**:
```markdown
### User Interface (NEW - Nov 23, 2025)

- ✅ **Lists Management** (/lists)
  - Create, view, edit, delete lists
  - Share with other users (Viewer/Editor/Admin roles)
  - Permission-aware UI with role badges
  - Breadcrumb navigation

- ✅ **Todos Management** (/todos)
  - Same functionality as Lists
  - Separate organization for tasks

- ✅ **Projects Management** (/projects)
  - Same functionality as Lists/Todos
  - For larger work items

- ✅ **Files Management** (/files)
  - Upload files (PDF, DOCX, TXT, MD, JSON - max 10MB)
  - Download files
  - Delete files
  - Owner-based access control

- ✅ **Permission System**
  - Share resources with specific users
  - Role-based access (Viewer, Editor, Admin, Owner)
  - Conversational permission commands
  - Visual permission badges

- ✅ **Authentication UI**
  - User menu in navigation
  - Logout functionality
  - Token revocation
  - Multi-user testing enabled

- ✅ **Standup Generation**
  - Generate daily standup reports
  - 2-3 second completion time
  - AI-powered summaries
```

**Update "Known Issues" Section**:
```markdown
## Known Limitations (as of Nov 23, 2025)

### Features Not Yet Implemented

- ⏸️ **Integrations Management UI**: Backend integrations exist (Slack, GitHub, Notion, Calendar) but management UI shows "coming soon"
- ⏸️ **Advanced Privacy Controls**: Basic privacy working, granular controls planned
- ⏸️ **Learning Pattern Customization**: Learning dashboard has cosmetic issues being polished

### Cosmetic Issues (Low Priority)

All functional but minor cosmetic polish needed:
- Some pages need consistent grid layouts
- Night mode inconsistency in some views
- Example prompts on home page being reviewed
```

---

## Notes for Implementation

**Focus**:
1. Accuracy over completeness
2. Honest about what works vs what doesn't
3. Clear first-day experience for Michelle

**Don't Over-Promise**:
- If a feature is "mostly working," say it's being polished
- If integration exists but has no UI, say "backend ready, UI coming soon"
- If something might break, warn about it

**Michelle Needs**:
1. How to get started ✅
2. What to test first ✅
3. What's known broken ✅
4. How to report issues ✅

---

## STOP Conditions

**STOP if**:
- Can't verify a feature actually works
- Documentation conflicts with reality
- Setup steps don't work as written
- Security-sensitive info exposed

**When stopped**: Document the gap, mark as TODO, escalate to PM

---

**Gameplan Created**: November 23, 2025, 5:30 PM
**Target Completion**: 7:20 PM (100 minutes)
**Ready for**: Lead Dev to execute or delegate to agent

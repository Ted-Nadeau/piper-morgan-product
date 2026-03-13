# Gameplan: Alpha User Onboarding Documentation Update
**Date**: November 2, 2025, 5:20 PM PT
**Issue**: To be created (#286 suggested)
**Estimated Effort**: 3-4 hours
**Lead Developer**: To be deployed
**Based on**: gameplan-template.md v9.0

---

## Context

The P0 blockers sprint added significant new functionality that fundamentally changes alpha user onboarding:
- JWT authentication with login/logout
- Password setup requirements
- Multi-user support with isolation
- New file upload capabilities
- Document processing workflows

The current documentation likely assumes single-user desktop mode and needs comprehensive updates.

---

## Phase -1: Infrastructure Verification Checkpoint (MANDATORY)

### Part A: Chief Architect's Current Understanding

Based on context, I believe the documentation situation is:

**Documentation Infrastructure**:
- [ ] Installation guide: `docs/installation/` (exists, needs auth updates)
- [ ] Alpha testing guide: `docs/alpha-testing-guide.md` (exists, outdated)
- [ ] Setup wizard docs: _________ (unknown if exists)
- [ ] API documentation: _________ (unknown if exists)
- [ ] Known issues list: `ALPHA_KNOWN_ISSUES.md` (exists from earlier)

**What I think needs updating**:
1. Setup wizard probably doesn't mention password creation
2. Installation guide doesn't cover login flow
3. Testing guide assumes single-user mode
4. No mention of JWT tokens or auth endpoints
5. File upload/document processing undocumented

**My understanding of the task**:
- Update all onboarding documentation for new auth flow
- Document the multi-user capabilities
- Add password setup instructions
- Document file upload and document processing
- Update known issues with any from P0 testing

### Part B: PM Verification Required

**PM, please confirm/correct and provide**:

1. **What documentation actually exists?**
   ```bash
   # Find all documentation files
   find docs/ -name "*.md" | head -20
   ls -la docs/installation/
   ls -la docs/alpha/

   # Check for setup/auth documentation
   grep -r "setup\|auth\|login" docs/ --include="*.md" | head -10

   # See what's in alpha testing guide
   head -50 docs/alpha-testing-guide.md
   ```

2. **Recent documentation work?**
   - Last updates to docs: ___________
   - Known outdated sections: ___________
   - Priority areas for users: ___________

3. **Documentation standards?**
   - [ ] Markdown format throughout
   - [ ] Screenshots needed/wanted?
   - [ ] Code examples included?
   - [ ] Version numbers tracked?

4. **Critical user journeys to document?**
   - First time setup flow
   - Login/logout process
   - File upload workflow
   - Other: ___________

### Part C: Proceed/Revise Decision

After PM verification:
- [ ] **PROCEED** - Understanding correct, begin updates
- [ ] **REVISE** - Different documentation structure than expected
- [ ] **CLARIFY** - Need more context on: ___________

---

## Phase 0: Initial Bookending - Documentation Audit

### Purpose
Inventory all documentation needing updates, understand current state

### Required Actions

1. **Create GitHub Issue**
   ```bash
   gh issue create \
     --title "CORE-ALPHA-DOCS-UPDATE - Update onboarding docs for auth system" \
     --body "Update all alpha user documentation to reflect new auth/multi-user system" \
     --label documentation,alpha
   ```

2. **Documentation Inventory**
   ```bash
   # Find all user-facing documentation
   find . -path "*/test*" -prune -o -name "*.md" -type f | grep -E "(install|setup|alpha|guide|README)"

   # Check current content
   grep -l "password\|auth\|JWT\|login" docs/**/*.md

   # Find setup instructions
   grep -r "python main.py\|setup" docs/ --include="*.md"
   ```

3. **Gap Analysis**
   - List what exists vs what's needed
   - Identify completely missing docs
   - Note outdated dangerous instructions

### Evidence to Collect
- List of all documentation files
- Current setup instructions (screenshot)
- Missing critical information
- Dangerous/wrong instructions that could break setup

### Expected Discoveries
- Setup assumes single user
- No password instructions
- No login flow documentation
- Missing file upload guide
- JWT/auth completely undocumented

---

## Phase 1: Critical Path Documentation (2 hours)

### Objectives
Update the "happy path" - what new users follow to get started

### Agent Assignment: **Cursor** (focused updates to existing files)

### Priority Documents to Update

1. **docs/installation/step-by-step-installation.md**
   ```markdown
   Add new section after dependencies:

   ## Setting Up Your User Account

   ### First Time Setup
   1. Run the setup wizard:
      ```bash
      python main.py setup
      ```

   2. Create your alpha user account:
      - Username: Choose a unique identifier
      - Email: Your email address
      - Password: Strong password (stored securely with bcrypt)

   ### Subsequent Logins
   After initial setup, start Piper Morgan:
   ```bash
   python main.py
   ```
   Then navigate to http://localhost:8001 and log in.
   ```

2. **docs/alpha-testing-guide.md** (or equivalent)

   Update sections:
   - Prerequisites: Add password manager recommendation
   - Setup: Include account creation steps
   - First run: Document login process
   - Multi-user: Explain session isolation

3. **README.md** (root)

   Quick update to mention:
   - Multi-user support
   - Authentication required
   - Link to setup guide

### Evidence Requirements
- Diff showing changes to each file
- Test following the new instructions
- Screenshots of login screen (if helpful)
- No broken internal links

### STOP Conditions
- Documentation structure completely different
- Would require rewriting from scratch
- Links to non-existent functionality

---

## Phase 2: Feature Documentation (1-2 hours)

### Objectives
Document new features added in P0 sprint

### Agent Assignment: **Code** (create new documentation)

### New Documentation to Create

1. **docs/features/authentication.md**
   ```markdown
   # Authentication System

   ## Overview
   Piper Morgan uses JWT-based authentication...

   ## Login Process
   1. Navigate to http://localhost:8001
   2. Enter username and password
   3. JWT token stored in secure cookie

   ## Password Management
   - Passwords hashed with bcrypt
   - Reset: [process]
   - Requirements: [criteria]

   ## Session Management
   - Sessions expire after 24 hours
   - Logout available from UI
   - Multiple concurrent sessions supported

   ## API Authentication
   For programmatic access:
   ```bash
   curl -X POST http://localhost:8001/auth/login \
     -H "Content-Type: application/json" \
     -d '{"username": "your-username", "password": "your-password"}'
   ```
   ```

2. **docs/features/file-upload.md**
   ```markdown
   # File Upload and Document Processing

   ## Supported File Types
   - Text (.txt)
   - PDF (.pdf)
   - Word (.docx)
   - Markdown (.md)
   - CSV (.csv)

   ## Upload Process
   1. Click upload button in UI
   2. Select file (max 10MB)
   3. File processed and indexed

   ## Document Operations
   - Analyze: AI-powered summary
   - Search: Find content across documents
   - Reference: Use in conversations
   ```

3. **docs/troubleshooting.md** (update or create)

   Add sections for:
   - Login issues
   - Session timeout
   - File upload failures
   - JWT token problems

### Evidence Requirements
- New files created and linked
- Code examples tested
- API endpoints verified
- Screenshots where helpful

### STOP Conditions
- Feature behavior unclear
- API still changing
- Would document non-working features

---

## Phase 3: Testing Guide Update (1 hour)

### Objectives
Update testing documentation for multi-user scenarios

### Agent Assignment: **Either agent** (straightforward updates)

### Updates Required

1. **Testing Scenarios**
   ```markdown
   ## Multi-User Testing

   ### Setup Multiple Test Users
   ```bash
   # In database or via script
   python scripts/create_test_users.py
   ```

   ### Test User Isolation
   1. Login as User A
   2. Upload document
   3. Login as User B in incognito
   4. Verify: Cannot see User A's documents

   ### Test Session Management
   1. Login in multiple browsers
   2. Verify independent sessions
   3. Test logout affects only one session
   ```

2. **Known Issues Update**

   Add from P0 testing:
   - Any auth edge cases found
   - File size limitations
   - Performance considerations
   - Token refresh behavior

### Evidence Requirements
- Testing steps verified working
- Multi-user test actually performed
- Issues list current and accurate

---

## Phase Z: Final Bookending & Handoff

### Completion Checklist

#### 1. Documentation Review
- [ ] All critical paths documented
- [ ] New features explained
- [ ] Testing guide updated
- [ ] No broken links
- [ ] No outdated information remaining

#### 2. Cross-References
- [ ] README points to setup guide
- [ ] Setup guide links to troubleshooting
- [ ] Feature docs cross-reference
- [ ] API examples consistent

#### 3. Verification
- [ ] PM tested following new docs
- [ ] Fresh alpha user can onboard
- [ ] No dangerous old instructions
- [ ] Version numbers updated

#### 4. GitHub Updates
- [ ] Issue created and tracked
- [ ] All changes committed
- [ ] PR if using branches
- [ ] Issue closed after approval

### PM Approval Request
```markdown
@PM - Documentation updates complete:

Critical Path Updates:
- Installation guide: Now includes auth setup ✓
- Alpha testing guide: Multi-user aware ✓
- README: Updated with auth mention ✓

New Documentation:
- authentication.md: Complete auth guide ✓
- file-upload.md: Upload/processing guide ✓
- troubleshooting.md: Common issues ✓

Testing Documentation:
- Multi-user scenarios added ✓
- Known issues updated ✓

Ready for review. Would you like to test the onboarding flow with the new docs?
```

---

## STOP Conditions (Throughout)

Stop and escalate if:
- Documentation framework totally different than expected
- Would break existing user workflows
- Requires documenting non-existent features
- Find critical bugs while documenting

---

## Success Metrics

- New user can onboard without help
- Multi-user setup clear
- No auth confusion
- File upload process obvious
- Troubleshooting actually helps

---

## Risk Assessment

**Low Risk**: Documentation updates are non-destructive
**Medium Risk**: Might discover gaps in implementation while documenting
**Mitigation**: Test everything we document, flag any issues found

---

## Dependencies

Must complete AFTER:
- P0 blockers (complete ✓)
- Any auth changes from P1 work

Should complete BEFORE:
- First external alpha tester
- Beta documentation

---

*This gameplan follows gameplan-template.md v9.0 structure*
*Ready for Phase -1 verification with PM*

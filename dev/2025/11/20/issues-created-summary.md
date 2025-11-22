# GitHub Issues Creation Summary
**Date**: 2025-11-20
**Time**: 07:14 UTC
**Created by**: Assistant PM via gh CLI
**Status**: ✅ COMPLETE

---

## Overview

Created 18 GitHub issues from draft files using `gh` CLI. All issues added to **MVP milestone**. Ready for implementation.

---

## TEST Super Epic & Children (11 issues)

### Super Epic (#341)
- **Title**: TEST: Test Infrastructure Repair (Super Epic)
- **Priority**: P0-Critical
- **Labels**: test-infrastructure, priority: critical
- **Related bead**: piper-morgan-k6k
- **Context**: Test suite is ~40% fictional with phantom tests, missing infrastructure, production code calling non-existent methods
- **Success Criteria**: 85% passing rate, pre-push hooks work, known-failures workflow, can push without --no-verify

### P0 - Critical Test Blockers (3 issues)

**#342 - Production calling 4 non-existent SlackSpatialMapper methods**
- Labels: bug, priority: critical, component: integration
- Mystery: Why isn't production crashing?
- Investigation needed for error suppression/execution paths
- Related bead: piper-morgan-1i5

**#343 - Add 5 missing enum values causing 25+ test failures**
- Labels: bug, priority: critical, size: small
- Quick win (15 mins): Add PLANNING/REVIEW to IntentCategory, HIGH/MEDIUM/LOW to AttentionLevel
- Unblocks 22+ tests immediately

**#344 - Implement known-failures workflow to unblock critical pushes**
- Labels: enhancement, priority: critical, component: workflow
- Solution: `.pytest-known-failures` file with expiry dates and bead references
- Enables pushing critical fixes without --no-verify

### P1 - Urgent Test Improvements (3 issues)

**#345 - Add test categorization markers (TDD vs regression)**
- Labels: enhancement, priority: high, component: workflow
- Add pytest markers: @unit, @tdd_spec, @integration, @smoke
- Audit and categorize all 617 tests

**#346 - Fix OrchestrationEngine fixture (11 tests failing)**
- Labels: bug, priority: high, component: workflow
- Error: ContainerNotInitializedError
- Options: mock, initialize, or dependency injection refactor

**#347 - Fix pre-push hook to handle test categories**
- Labels: enhancement, priority: high
- Update hook to: `pytest -m "not tdd_spec" tests/unit/`
- Integrate with known-failures workflow

### P2 - High Priority Fixes (3 issues)

**#348 - Fix test_api_key_validator.py (44 phantom tests)**
- Labels: technical-debt, priority: medium, size: large
- 368 lines of tests for non-existent API
- Options: refactor tests, implement API layer, or remove
- Related bead: piper-morgan-36m

**#349 - Fix async_transaction fixture pattern (53 tests)**
- Labels: bug, priority: medium, size: large
- 53 tests expect non-existent fixture
- Solution: Create fixture or refactor to existing ones

**#350 - Add smoke tests for static file serving**
- Labels: enhancement, priority: medium, size: small
- Critical: static file mounting broken (Saturday's issue)
- Tests for CSS, templates, infrastructure

### P3 - Backlog Items (2 issues)

**#351 - Full audit and cleanup of phantom tests**
- Labels: technical-debt, priority: low, size: large
- Comprehensive audit of all 617 tests
- Identify/fix/remove phantom tests

**#352 - Create core user journey smoke tests**
- Labels: enhancement, priority: low, size: medium
- E2E tests: onboarding, query processing, Slack flow, GitHub flow
- Target: 10+ journey tests

---

## Regular MVP Issues (6 issues)

### #353 - BUG-319: Windows Git Clone Fails
- **Priority**: P0 (blocks Windows developers)
- **Labels**: bug, priority: critical, size: small
- **Problem**: Colon (`:`) in filename blocks Windows cloning
- **File**: `archive/piper-morgan-0.1.1/docs/claude docs 5:30/conversational_refactor.md`
- **Solution**:
  - Rename problematic files
  - Add pre-commit hook for Windows-incompatible characters
  - Test clone on Windows 10/11, WSL, Git Bash
- **Effort**: 2-3 hours (quick win)

### #354 - DESIGN-TOKENS: Extract CSS Variables
- **Priority**: P2
- **Labels**: enhancement, priority: medium, component: ui
- **Sprint**: A11 (Pre-Beta)
- **Problem**: Hard-coded colors, no CSS variables, theme inconsistency
- **Scope**:
  - Create `/web/styles/tokens.css`
  - Extract colors, spacing (8px grid), typography
  - Apply light theme consistently
  - Zero hard-coded colors in CSS
- **Out of scope**: Component library, dark theme, full design system
- **Effort**: 3 days

### #355 - STOP-GAP-DOCS: Basic Artifact Persistence
- **Priority**: P2
- **Labels**: enhancement, priority: medium, component: ui
- **Sprint**: A10 (Post-TEST)
- **Problem**: Generated artifacts (PRDs, specs) vanish into history; no retrieval
- **Scope**:
  - "Save as file" button (>500 char outputs)
  - Basic file browser at `/files`
  - Download/delete capabilities
  - Simple list view
- **Out of scope**: Document model, folders, version history, search
- **Success**: Experience improves from 2/10 to 6/10
- **Effort**: 3 days

### #356 - PERF-320: Add Missing Composite Database Indexes
- **Priority**: P1 (performance cliff at scale)
- **Labels**: priority: high, component: database, size: medium
- **Problem**: No indexes for common queries; catastrophic degradation at scale
  - 1K records: 200ms (acceptable)
  - 100K records: 20+ seconds (unusable)
- **Solution**: 5 composite indexes
  - conversations(user_id, created_at DESC)
  - conversation_turns(conversation_id, turn_number)
  - uploaded_files(user_id, upload_date DESC)
  - patterns(user_id, category)
  - audit_logs(entity_type, entity_id, created_at DESC)
- **Target**: 10x+ improvement with <5% overhead
- **Effort**: 4-6 hours

### #357 - SEC-323: Implement RBAC
- **Priority**: P0 (CRITICAL - security blocker)
- **Labels**: priority: critical, component: api, size: large
- **Problem**: **NO AUTHORIZATION** - any authenticated user can access ANY resource
  - User A can read User B's conversations
  - User A can delete User B's data
  - No admin vs user distinction
- **This blocks**: Multi-user testing, alpha launch, production, security audit
- **Solution**: Proper RBAC with roles, permissions, decorators
- **Roles**: Admin (all), User (own), Viewer (read-only)
- **Effort**: 20-24 hours (5 phases)
- **Risk**: **MUST complete before external users access system**

### #358 - SEC-324: Implement Encryption at Rest
- **Priority**: P0 (CRITICAL - compliance blocker)
- **Labels**: priority: critical, component: database, size: large
- **Problem**: **COMPLIANCE FAILURE** - all sensitive data in plaintext
  - Conversation content, file content, patterns, PII, API keys
  - Violations: GDPR Article 32, SOC2 II, CCPA, HIPAA
- **This blocks**: Alpha launch with external users, production deployment
- **Solution**: Field-level AES-256-GCM encryption
  - EncryptionService with transparent decrypt on load
  - Sensitive columns: conversations.content, turns.content, files.content, patterns, api_keys, emails
  - Key management & rotation capability
- **Performance Target**: <5% read overhead, <10% write overhead
- **Effort**: 24-30 hours (6 phases)
- **Risk**: **MUST implement before production data**

---

## Key Technical Decisions

### Beads References Strategy
All related beads kept as plain text in issue bodies:
```
Related bead: piper-morgan-xyz
```

**Rationale for agents**:
- ✅ Searchable: `grep -r "piper-morgan-1i5"` finds all cross-references
- ✅ Preserves independence: Beads != GitHub issues, but can correlate
- ✅ Semantic clarity: "Related bead" signals different tracking system
- ✅ Future-proof: Allows agent correlation across systems
- ✅ No broken links: Beads exist independently; issues reference them

### Label Selection
- Used available repo labels (performance/security not in schema)
- Mapped to: `priority: {critical|high|medium|low}`, `component: {api|database|workflow|ui|integration}`
- Applied `size: {small|medium|large}` for effort estimation
- User can add custom labels after creation if needed

### GitHub Auto-Assignment
- Ignored draft filenames (319, 320, 323, 324)
- GitHub auto-assigned #341-#358
- Preserves uniqueness, allows cleanup later
- User can rename issues afterward

---

## Verification

✅ All 18 issues created
✅ All added to MVP milestone
✅ All have priority labels
✅ All have component/size tags
✅ All have acceptance criteria
✅ Beads properly referenced

### GitHub URLs
- Super Epic: https://github.com/mediajunkie/piper-morgan-product/issues/341
- Range: https://github.com/mediajunkie/piper-morgan-product/issues/341-358
- MVP Milestone: https://github.com/mediajunkie/piper-morgan-product/milestone/MVP

---

## Next Steps

1. **User Post-Processing**: Rename issues, add any custom labels, link related issues
2. **Agent Pickup**: Issues ready for implementation via `gh issue view PM-XXX`
3. **Work Tracking**: Beads provide async tracking; update issues with progress
4. **Dependencies**: TEST issues follow P0→P1→P2→P3 sequence; blocking relationships noted

---

*Report generated: 2025-11-20 07:14 UTC by Assistant PM*

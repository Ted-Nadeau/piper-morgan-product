# CORE-GREAT-1: Orchestration Core Epic

## Title
CORE-GREAT-1: Complete Orchestration Core - QueryRouter & OrchestrationEngine Integration

## Labels
epic, refactor, core, critical, great-refactor

## Description

## Overview
Complete the unfinished QueryRouter integration (PM-034) and properly initialize the OrchestrationEngine. This is the foundation that unlocks everything else.

## Background
- QueryRouter is 75% complete but disabled
- OrchestrationEngine never gets initialized
- Core user flow (GitHub issue creation) is broken
- Multiple TODO comments and workarounds exist
- Bug #166 (UI hang) needs resolution as part of this

## Pre-Work: ADR Review
- [ ] Review ADR-032 (Intent Classification Universal Entry) for accuracy
- [ ] Review ADR-019 (Orchestration Commitment) for implementation status
- [ ] Run verification commands to check actual implementation
- [ ] Document any discrepancies between ADRs and reality
- [ ] Update ADRs if implementation differs from documentation
- [ ] Create new REFACTOR epics if additional incomplete work discovered

## Acceptance Criteria
- [ ] "Create GitHub issue about X" works from chat interface
- [ ] No "None" objects or undefined errors
- [ ] Performance <500ms for issue creation flow
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] Bug #166 resolved (UI hang fixed)

## Tasks
- [ ] Complete ADR pre-work review
- [ ] Review existing PM-034 QueryRouter implementation
- [ ] Identify why initialization was disabled
- [ ] Fix initialization in main.py
- [ ] Fix initialization in web/app.py
- [ ] Connect QueryRouter to OrchestrationEngine
- [ ] Remove all workarounds and TODO comments
- [ ] Resolve Bug #166 (Web UI hang)
- [ ] Complete intent → handler → response pipeline
- [ ] Write integration test for GitHub issue creation flow
- [ ] Write unit tests for QueryRouter
- [ ] Write unit tests for OrchestrationEngine
- [ ] Performance test the complete flow
- [ ] Update any affected ADRs with implementation reality

## Lock Strategy
- Integration test for GitHub issue flow prevents regression
- Unit tests for both components
- No TODO comments allowed to remain
- Performance benchmark in CI
- All related ADRs updated to reflect actual implementation

## Dependencies
None - this is the foundation

## Estimated Duration
2 weeks

## Success Validation
Run: `python cli/commands/github.py create "Test issue from refactor"`
Expected: Issue created in GitHub within 500ms

## North Star Test
The GitHub issue creation flow must work end-to-end:
1. User says: "Create a GitHub issue about fixing the login bug"
2. Intent classification recognizes CREATE_GITHUB_ISSUE
3. QueryRouter routes to OrchestrationEngine
4. OrchestrationEngine calls GitHub service
5. Issue created successfully
6. User receives confirmation

---

**Note**: This epic follows the Inchworm Protocol - must be 100% complete before moving to CORE-GREAT-2

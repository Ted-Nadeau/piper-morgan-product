# Audit Cascade: Issue #352 — Issue → Gameplan Gate

**Date**: 2026-03-14
**Auditor**: Lead Developer (Claude Code Opus)
**Template**: `.github/ISSUE_TEMPLATE/feature.md`

---

## Issue #352: TEST-SMOKE-E2E — Create core user journey smoke tests

### Audit Matrix: #352 against feature.md

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| Title with label | ✅ | `TEST-SMOKE-E2E: Create core user journey smoke tests` |
| Priority | ✅ | `priority: low` label (reconsider — PM wants this in M1) |
| Labels | ✅ | `enhancement`, `priority: low`, `size: medium` |
| Milestone | ✅ | MVP |
| Problem Statement | ❌ | No "Current State" / "Impact" / "Strategic Context" sections |
| Impact | ❌ | Not structured |
| Strategic Context | ❌ | Not present |
| Goal | ⚠️ | "Scope" section lists 4 flows but no "Primary Objective" or "Not In Scope" |
| What Already Exists | ❌ | Not documented (significant — infrastructure DOES exist) |
| Requirements/Phases | ❌ | No phases, tasks, or deliverables |
| Acceptance Criteria | ⚠️ | 3 success criteria but not structured per template (Functionality/Testing/Quality/Documentation) |
| Completion Matrix | ❌ | Not present |
| Testing Strategy | ❌ | Not present (meta-ironic: this IS a testing issue) |
| Success Metrics | ❌ | Not present |
| STOP Conditions | ❌ | Not present |
| Effort Estimate | ✅ | `size: medium` label |
| Dependencies | ❌ | Not listed |
| Evidence Section | ❌ | Not present |
| Completion Checklist | ❌ | Not present |

### Template Compliance: LOW

This is a stub issue from November 2025. It has 3 bullet points and 3 success criteria. Nearly all template sections are missing.

---

## Infrastructure Investigation

### What Already Exists (not documented in issue)

**E2E test infrastructure IS present:**
- `tests/e2e/test_onboarding_http_e2e.py` — 7 real HTTP E2E tests using ASGI transport
- `tests/e2e/__init__.py` — package exists
- E2E fixtures: `e2e_db_session`, `e2e_test_user`, `e2e_client` (real FastAPI + lifespan)
- Pattern: ASGITransport → real endpoints → real database → cleanup

**Smoke test marker infrastructure IS present:**
- `pytest.ini` defines `smoke` marker: "Critical path tests that should run in <5 seconds total"
- CI/CD has smoke test stage in `.github/workflows/test.yml`
- 10 existing smoke-marked tests scattered across unit tests

**Integration test infrastructure (70+ files):**
- Real database fixtures with transaction isolation
- `real_client` / `test_client` fixtures in `tests/integration/conftest.py`
- Auth, config, standup, workflow integration tests

### Current E2E Coverage

| User Journey | E2E Coverage | Notes |
|-------------|-------------|-------|
| User onboarding | ✅ 7 tests | `test_onboarding_http_e2e.py` |
| Basic query processing | ❌ | Not tested E2E |
| Slack integration flow | ❌ | Not tested E2E (unit tests only) |
| GitHub integration flow | ❌ | Not tested E2E |
| Authentication flow | ⚠️ | Covered as part of onboarding |
| Project management | ❌ | Not tested E2E |
| Task/todo management | ❌ | Not tested E2E |
| Health check | ❌ | Trivial but not tested |

### Available API Endpoints for E2E

- `/health` — health check
- `/auth/login` — authentication
- `/api/v1/intent` — intent processing (core flow)
- `/api/v1/projects` — project CRUD
- `/api/v1/work-items` — work item management
- `/api/v1/todos` — todo management

---

## Recommended Approach

### PM Direction
PM said: "if there is no E2E infrastructure yet then I think that needs to be step 0"
— E2E infrastructure EXISTS but needs standardization and expansion.

### Revised Phases

**Phase 0: Standardize E2E Infrastructure**
- Extract and standardize e2e fixtures into `tests/e2e/conftest.py`
- Verify existing onboarding E2E tests still pass
- Document the E2E pattern for consistency

**Phase 1: Core Journey Smoke Tests**
- Health check E2E test
- Authentication flow (login → get token → use token)
- Query processing (submit intent → get response)
- Project CRUD (create → read → update)

**Phase 2: Integration Journey Tests**
- Slack event processing (if testable without real Slack)
- GitHub integration (if testable without real GitHub)
- Or: mock external service boundaries only

**Phase 3: CI/CD Verification**
- Verify smoke marker tests run in CI
- Ensure E2E tests are categorized correctly
- Add E2E stage to CI if needed

### Dependencies to Verify
- Docker (PostgreSQL, Redis) must be running for E2E
- Database migrations must be current
- No external API keys required for core flows

---

## Action Items Before Execution

The issue needs substantial rework before it's actionable. Two options:

### Option A: Rewrite issue to template compliance, then execute
- Full template rewrite with phases, AC, completion matrix
- Slower start, cleaner tracking

### Option B: Proceed with mini-gameplan, update issue at closure
- Use this audit document as the de facto gameplan
- Execute phases above
- Update issue with evidence at closure

**Recommendation**: Option B — the audit cascade document serves as the gameplan. The work is well-scoped and understood.

---

## Risk Assessment: LOW-MEDIUM
- Infrastructure exists — extending proven patterns
- Production code NOT modified
- Risk: external service tests may need careful mocking boundaries
- Risk: database state management across E2E tests

---

_Audit performed: 2026-03-14_
_Template: `.github/ISSUE_TEMPLATE/feature.md`_

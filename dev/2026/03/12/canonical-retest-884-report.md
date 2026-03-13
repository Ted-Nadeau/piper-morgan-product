# Canonical Query Retest Report — Issue #884

**Date**: 2026-03-12 22:51
**Version**: v0.8.6 (post-M0)
**User**: canonical-test (fresh account)
**Total Queries**: 61

---

## Overall Results

| Metric | Count | Percentage |
|--------|-------|------------|
| PASS | 43 | 70.5% |
| FAIL | 10 | 16.4% |
| NOT_IMPL | 8 | 13.1% |
| ERROR | 0 | 0.0% |
| **Total** | **61** | |

**Pass Rate (implemented queries)**: 43/53 (81.1%)

---

## Results by Category

| Category | Total | PASS | FAIL | NOT_IMPL | ERROR | Rate |
|----------|-------|------|------|----------|-------|------|
| Identity | 5 | 4 | 1 | 0 | 0 | 80% |
| Temporal | 5 | 5 | 0 | 0 | 0 | 100% |
| Spatial | 4 | 4 | 0 | 0 | 0 | 100% |
| Capability | 5 | 4 | 1 | 0 | 0 | 80% |
| Predictive | 5 | 2 | 3 | 0 | 0 | 40% |
| Conversational | 5 | 4 | 1 | 0 | 0 | 80% |
| Scheduling | 5 | 2 | 1 | 2 | 0 | 40% |
| Documents | 4 | 2 | 1 | 1 | 0 | 50% |
| GitHub Ops | 8 | 5 | 1 | 2 | 0 | 62% |
| Slack | 5 | 4 | 0 | 1 | 0 | 80% |
| Productivity | 3 | 3 | 0 | 0 | 0 | 100% |
| Todos | 4 | 3 | 0 | 1 | 0 | 75% |
| Calendar Ext | 2 | 1 | 1 | 0 | 0 | 50% |
| Knowledge | 1 | 0 | 0 | 1 | 0 | 0% |

---

## Failure Mode Breakdown

| Mode | Count | Description |
|------|-------|-------------|
| ROUTING | 9 | Query reached wrong handler |
| INTEGRATION | 1 | Correct routing, backend fails |

---

## Detailed Failures

- **Q2** (Identity): `What can you help me with?` — **ROUTING** — Expected identity, got discovery
- **Q16** (Capability): `Create a GitHub issue about testing` — **INTEGRATION** — Service error: Failed to create GitHub issue — API returned no response
- **Q23** (Predictive): `What risks should I be aware of?` — **ROUTING** — Expected analysis, got guidance
- **Q24** (Predictive): `What opportunities should I pursue?` — **ROUTING** — Expected synthesis, got priority
- **Q25** (Predictive): `What's the next milestone?` — **ROUTING** — Expected planning, got priority
- **Q27** (Conversational): `Tell me more about the GitHub integration` — **ROUTING** — Expected query, got identity
- **Q33** (Scheduling): `Find time for a 1:1 with the team lead` — **ROUTING** — Expected execution, got temporal
- **Q40** (Documents): `Update the project roadmap document` — **ROUTING** — Expected execution, got portfolio
- **Q43** (GitHub Ops): `What's blocking the milestone?` — **ROUTING** — Expected analysis, got status
- **Q62** (Calendar Ext): `Check my calendar for conflicts` — **ROUTING** — Expected query, got temporal

---

## Not Implemented (Graceful)

- Q31 (Scheduling): `Schedule a meeting about the roadmap`
- Q32 (Scheduling): `Remind me to review PRs tomorrow`
- Q36 (Documents): `Create a doc from this conversation`
- Q44 (GitHub Ops): `Create issues from this meeting's action items`
- Q45 (GitHub Ops): `Close completed issues`
- Q48 (Slack): `Post this update to the team channel`
- Q55 (Todos): `Complete the PR review todo`
- Q63 (Knowledge): `Upload a file to the knowledge base`

---

*Generated 2026-03-12 22:51 by canonical-retest-884.py*

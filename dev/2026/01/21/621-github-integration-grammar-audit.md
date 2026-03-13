# Grammar Audit: GitHub Integration (#621)

**Issue**: #621 GRAMMAR-TRANSFORM: GitHub Integration (Partial → Conscious)
**Auditor**: Lead Developer (Claude Code / Opus)
**Date**: 2026-01-21
**Files Audited**:
- `services/integrations/github/github_plugin.py` (~100 lines)
- `services/integrations/github/production_client.py` (~400 lines)
- `services/integrations/github/issue_analyzer.py` (~300 lines)
- `services/integrations/github/github_integration_router.py` (~500 lines)
- `services/integrations/spatial/github_spatial.py` (~350 lines)

---

## Executive Summary

The GitHub integration has **sophisticated 8-dimensional spatial intelligence** (Hierarchy, Temporal, Priority, Collaborative, Flow, Quantitative, Causal, Contextual) but presents results as data structures, not as Piper's experiential understanding.

**Key insight**: Piper already *analyzes* GitHub deeply - she knows an issue is "stale", has "high priority", is "blocked". But when presenting this, she says "activity_level: stale" instead of "This one's been quiet for a while."

---

## Grammar Element Analysis

### Entity ✅ (Good)
**What exists**: GitHub users, repositories, issues, and PRs are tracked as entities.

**Evidence**:
```python
# production_client.py:369
"user": {"login": issue.user.login, "name": issue.user.name or issue.user.login}
```

**Assessment**: Entities preserved. No transformation needed.

### Moment ⚠️ (Needs Work)
**What exists**: PRs and issues are retrieved with timestamps but presented as data objects.

**Evidence**:
```python
# github_spatial.py:84-103
async def analyze_timeline(self, issue: Dict[str, Any]) -> Dict[str, Any]:
    ...
    return {
        "age_days": age_days,
        "last_activity_hours": last_activity_hours,
        "activity_level": activity_level,  # "stale", "active", etc.
        ...
    }
```

**Gap**: Returns `"activity_level": "stale"` instead of "This PR has been waiting for 12 days."

**Experience Test**:
- Current: `{"activity_level": "stale", "age_days": 12}`
- Conscious: "Alex's PR has been waiting for 12 days - it might need attention."

### Place ⚠️ (Partial)
**What exists**: GitHub recognized as a Place, but atmosphere is minimal.

**Evidence**:
```python
# github_spatial.py:30-37
"""
8 Dimensions:
1. HIERARCHY - Issue/PR relationships
2. TEMPORAL - Activity timelines
...
"""
```

**Gap**: No "atmosphere" for GitHub Place. Is it a busy repo? A quiet corner? A hot project?

### Lenses ✅ (Rich, but not applied to responses)
**What exists**: Excellent lens coverage in spatial intelligence:
- Temporal lens (stale, active, recent)
- Collaborative lens (reviewers, commenters)
- Flow lens (blocked, open, merged)
- Priority lens (critical, high, normal, low)

**Gap**: These lenses inform data structures but not response narratives.

### Situation ⚠️ (Data-centric)
**What exists**: Rich situational analysis happens, but results are dictionaries.

**Evidence**:
```python
# github_spatial.py:139-148
attention_score = 0.5  # Base score
if priority_level == "critical":
    attention_score = 1.0
```

**Gap**: `attention_score: 1.0` should become "This needs your attention right away."

---

## Response Generation Analysis

Unlike Slack (#620), GitHub doesn't have a dedicated response handler. GitHub data flows through:

1. `github_integration_router.py` → Returns raw data
2. `intent_service/canonical_handlers.py` → May format some responses
3. Various callers → Present data as-is

**Key finding**: The transformation opportunity is in **how GitHub data is narrated** when presenting to users, not in the GitHub integration itself.

### Current Format Example
```python
{
    "title": "Fix login bug",
    "state": "open",
    "activity_level": "stale",
    "age_days": 14,
    "priority_level": "high",
    "assignees": ["alex"]
}
```

### Grammar-Conscious Format Example
```
"Alex's high-priority fix for the login bug has been open for two weeks.
It's been quiet lately - might be worth checking in."
```

---

## Transformation Opportunities

### 1. GitHub Response Context
Similar to `SlackResponseContext`, create `GitHubResponseContext` that captures:
- Repository atmosphere (active/quiet/hot)
- Issue/PR significance (routine/notable/urgent)
- Temporal framing (recent/stale/ancient)

### 2. GitHub Narrative Bridge
Transform GitHub data structures into experiential narratives:
- Issue age → "has been waiting for X days"
- Stale status → "been quiet lately"
- Critical priority → "needs attention right away"
- Blocked state → "is stuck on something"

### 3. Canonical Handler Updates
Update `canonical_handlers.py` where GitHub queries are handled to use grammar-conscious language when presenting results.

---

## Recommended Transformation Phases

### Phase 1: GitHubResponseContext (1h)
Create dataclass capturing GitHub-specific context for grammar-conscious responses.

### Phase 2: GitHub Narrative Bridge (2h)
Create transformation functions for common GitHub patterns:
- `narrate_issue_age()`
- `narrate_priority_level()`
- `narrate_activity_status()`
- `narrate_pr_state()`

### Phase 3: Canonical Handler Integration (2h)
Update canonical handlers that deal with GitHub queries to use narrative bridge.

### Phase 4: Testing (1.5h)
Test narrative transformations pass Contractor Test.

**Total**: ~6.5 hours

---

## Files to Create/Modify

| File | Action | Purpose |
|------|--------|---------|
| `services/integrations/github/response_context.py` | Create | GitHubResponseContext dataclass |
| `services/integrations/github/narrative_bridge.py` | Create | Narrative transformation functions |
| `services/intent_service/canonical_handlers.py` | Modify | Use narrative bridge for GitHub results |

---

## Patterns to Apply

| Pattern | Application |
|---------|-------------|
| Pattern-050 | GitHubResponseContext (Context Dataclass) |
| Pattern-052 | Narrative Bridge transforms data to experience |
| Pattern-053 | Warmth calibration for stale/urgent items |
| Pattern-054 | Honest failure when GitHub unreachable |

---

## Success Criteria

1. **No raw data in responses** - Users see "waiting for 2 weeks" not "age_days: 14"
2. **Temporal awareness expressed** - "been quiet" not "stale"
3. **Priority expressed humanly** - "needs attention" not "priority_level: critical"
4. **Contractor Test passes** - Professional tone, not robotic

---

## Experience Test Examples

| Data | Grammar-Conscious |
|------|-------------------|
| `activity_level: "stale"` | "been quiet for a while" |
| `age_days: 14` | "waiting for two weeks" |
| `priority_level: "critical"` | "needs attention right away" |
| `state: "open", reviewers: []` | "waiting for someone to review" |
| `comments: 0` | "no one's weighed in yet" |

---

## Risk Assessment

**Low Risk**: We're adding a narrative layer, not changing data retrieval.

**Scope Note**: The transformation focuses on response presentation, not the spatial intelligence layer (which is working well).

---

*Ready for PM review and gameplan approval*

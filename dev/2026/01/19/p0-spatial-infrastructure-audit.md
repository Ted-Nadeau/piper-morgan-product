# Spatial Infrastructure Audit

**Investigation Phase**: P0 - Investigation & Pattern Discovery
**Parent Issue**: #612 (MUX-399-P0)
**Date**: 2026-01-19
**Investigator**: Claude Code (Lead Developer role)

---

## Executive Summary

**Critical Finding**: The 8D spatial dimensions are implemented as METHODS within integration-specific classes, NOT as separate dimension classes that can be wrapped. The `8d-spatial-to-lens-mapping.md` document assumes infrastructure (`services/spatial/dimensions/*.py`) that does not exist.

**Implication for P1**: Lens infrastructure must be CREATED, not wrapped. This is a scope expansion but not a blocker.

---

## Actual Implementation Pattern

### Pattern 1: Intelligence Class with `self.dimensions` Dict

Every spatial integration follows this pattern:

```python
class [Integration]SpatialIntelligence:
    def __init__(self):
        self.dimensions = {
            "HIERARCHY": self.analyze_[hierarchy_method],
            "TEMPORAL": self.analyze_[temporal_method],
            "PRIORITY": self.analyze_[priority_method],
            "COLLABORATIVE": self.analyze_[collaborative_method],
            "FLOW": self.analyze_[workflow_method],
            "QUANTITATIVE": self.analyze_[metrics_method],
            "CAUSAL": self.analyze_[relations_method],
            "CONTEXTUAL": self.analyze_[context_method],
        }
```

**Key insight**: Dimensions are METHODS, not classes. The `self.dimensions` dict maps dimension names to bound methods.

---

## Integration-by-Integration Audit

### 1. Notion (`services/intelligence/spatial/notion_spatial.py`)

**Location verified**: ✅ `ls -la services/intelligence/spatial/notion_spatial.py`

**Class**: `NotionSpatialIntelligence`

**Pattern**: Dict of methods (lines 49-58)
```python
self.dimensions = {
    "HIERARCHY": self.analyze_page_structure,
    "TEMPORAL": self.analyze_timestamps,
    "PRIORITY": self.analyze_tags_status,
    "COLLABORATIVE": self.analyze_authors,
    "FLOW": self.analyze_workflow_props,
    "QUANTITATIVE": self.analyze_metrics,
    "CAUSAL": self.analyze_relations,
    "CONTEXTUAL": self.analyze_workspace,
}
```

**Methods present**: All 8 dimensions implemented (lines 88-478)
- `analyze_page_structure()` - Lines 88-143
- `analyze_timestamps()` - Lines 145-210
- `analyze_tags_status()` - Lines 212-251
- `analyze_authors()` - Lines 253-305
- `analyze_workflow_props()` - Lines 307-347
- `analyze_metrics()` - Lines 349-391
- `analyze_relations()` - Lines 393-436
- `analyze_workspace()` - Lines 438-478

**Comprehensive analysis**: `get_comprehensive_spatial_analysis()` at lines 480-510

---

### 2. GitHub (`services/integrations/spatial/github_spatial.py`)

**Location verified**: ✅ `ls -la services/integrations/spatial/github_spatial.py`

**Class**: `GitHubSpatialIntelligence`

**Pattern**: Dict of methods (lines 45-54)
```python
self.dimensions = {
    "HIERARCHY": self.analyze_issue_hierarchy,
    "TEMPORAL": self.analyze_timeline,
    "PRIORITY": self.analyze_priority_signals,
    "COLLABORATIVE": self.analyze_team_activity,
    "FLOW": self.analyze_workflow_state,
    "QUANTITATIVE": self.analyze_metrics,
    "CAUSAL": self.analyze_dependencies,
    "CONTEXTUAL": self.analyze_project_context,
}
```

**Methods present**: All 8 dimensions implemented
- `analyze_issue_hierarchy()` - Lines 64-81
- `analyze_timeline()` - Lines 84-123
- `analyze_priority_signals()` - Lines 126-163
- `analyze_team_activity()` - Lines 166-192
- `analyze_workflow_state()` - Lines 195-232
- `analyze_metrics()` - Lines 235-271
- `analyze_dependencies()` - Lines 274-311
- `analyze_project_context()` - Lines 314-340

**Comprehensive analysis**: `create_spatial_context()` at lines 343-410

---

### 3. GitBook (`services/intelligence/spatial/gitbook_spatial.py`)

**Location verified**: ✅ `ls -la services/intelligence/spatial/gitbook_spatial.py`

**Class**: `GitBookSpatialIntelligence`

**Pattern**: Dict of methods (same pattern as Notion/GitHub)

**Methods present**: All 8 dimensions implemented

---

### 4. Slack (`services/integrations/slack/spatial_*.py`)

**Location verified**: ✅ Multiple files
```
spatial_adapter.py     (12965 bytes)
spatial_agent.py       (15165 bytes)
spatial_intent_classifier.py (17209 bytes)
spatial_mapper.py      (34570 bytes)
spatial_memory.py      (26172 bytes)
spatial_types.py       (11598 bytes)
```

**Pattern**: DIFFERENT - Granular file approach

**Key difference**: Slack uses domain types (`spatial_types.py`) that model Places/Entities differently:
- `Territory` (Workspace)
- `Room` (Channel)
- `ConversationalPath` (Thread)
- `SpatialObject` (Message)
- `AttentionAttractor` (@mentions)
- `EmotionalMarker` (Reactions)

**8D dimensions are NOT a dict** - they're embedded across multiple files:
- HIERARCHY: Implicit in Territory → Room → Path → Object hierarchy
- TEMPORAL: In `SpatialEvent.timestamp`, `ConversationalPath.last_activity`
- PRIORITY: In `AttentionLevel` enum (AMBIENT, FOCUSED, DIRECT, URGENT, EMERGENCY)
- COLLABORATIVE: In `Room.current_inhabitants`, `ConversationalPath.active_participants`
- FLOW: In `ConversationalPath.conversation_momentum`, `topic_coherence`
- QUANTITATIVE: In counts throughout (`interaction_count`, `current_length`)
- CAUSAL: In `SpatialObject.connected_objects`
- CONTEXTUAL: In `Room.get_room_atmosphere()`, `Territory.get_navigation_context()`

---

### 5. Other Integrations (`services/integrations/spatial/`)

**Verified files**:
- `linear_spatial.py` - LinearSpatialIntelligence ✅ Has dimensions dict
- `devenvironment_spatial.py` - DevEnvironmentSpatialIntelligence ✅ Has dimensions dict
- `cicd_spatial.py` - CICDSpatialIntelligence ✅ Has dimensions dict
- `gitbook_spatial.py` - GitBookSpatialIntelligence ✅ Has dimensions dict

All follow the same `self.dimensions = {}` pattern.

---

### 6. Calendar

**Location verified**: ✅ `services/integrations/calendar/calendar_integration_router.py`

**Pattern**: NO spatial intelligence class exists

**Key finding**: Calendar integration uses `get_temporal_summary()` method directly (see morning_standup.py lines 428-477) but does NOT have a `CalendarSpatialIntelligence` class.

Calendar temporal data includes:
- `current_meeting`
- `next_meeting`
- `free_blocks`
- `total_meetings_today`
- `total_meeting_time_minutes`
- `total_free_time_minutes`

This IS 8D data (primarily TEMPORAL dimension) but without the spatial wrapper.

---

## Dimension Implementation Table

| Integration | TEMPORAL | HIERARCHY | PRIORITY | COLLABORATIVE | FLOW | QUANTITATIVE | CAUSAL | CONTEXTUAL |
|-------------|----------|-----------|----------|---------------|------|--------------|--------|------------|
| Notion | ✅ method | ✅ method | ✅ method | ✅ method | ✅ method | ✅ method | ✅ method | ✅ method |
| GitHub | ✅ method | ✅ method | ✅ method | ✅ method | ✅ method | ✅ method | ✅ method | ✅ method |
| GitBook | ✅ method | ✅ method | ✅ method | ✅ method | ✅ method | ✅ method | ✅ method | ✅ method |
| Linear | ✅ method | ✅ method | ✅ method | ✅ method | ✅ method | ✅ method | ✅ method | ✅ method |
| DevEnv | ✅ method | ✅ method | ✅ method | ✅ method | ✅ method | ✅ method | ✅ method | ✅ method |
| CICD | ✅ method | ✅ method | ✅ method | ✅ method | ✅ method | ✅ method | ✅ method | ✅ method |
| Slack | ✅ types | ✅ types | ✅ types | ✅ types | ✅ types | ✅ types | ✅ types | ✅ types |
| Calendar | ✅ direct | ❌ none | ❌ none | ❌ none | ❌ none | ✅ stats | ❌ none | ❌ none |

**Legend**:
- ✅ method - Implemented as method in `self.dimensions` dict
- ✅ types - Implemented via domain type classes
- ✅ direct - Available but not wrapped in spatial pattern
- ❌ none - Not implemented

---

## Gap Analysis

### What `8d-spatial-to-lens-mapping.md` Assumed

The document assumes:
```
services/spatial/dimensions/temporal.py      → TemporalDimension class
services/spatial/dimensions/hierarchical.py  → HierarchicalDimension class
services/spatial/dimensions/priority.py      → PriorityDimension class
... (8 separate class files)
```

### What Actually Exists

1. **No `services/spatial/dimensions/` directory** - This path does not exist
2. **No separate dimension classes** - Dimensions are bound methods, not classes
3. **No wrappable infrastructure** - Can't import `TemporalDimension` from anywhere

### Reality Check

```bash
# This path does NOT exist:
$ ls services/spatial/dimensions/
ls: cannot access 'services/spatial/dimensions/': No such file or directory

# The actual spatial code is here:
$ ls services/intelligence/spatial/
notion_spatial.py  gitbook_spatial.py

$ ls services/integrations/spatial/
github_spatial.py  linear_spatial.py  cicd_spatial.py  devenvironment_spatial.py  gitbook_spatial.py
```

---

## Implication for P1

### Original Assumption
P1 would "wrap existing dimensions" with Lens classes:

```python
class TemporalLens(Lens):
    dimension: TemporalDimension  # ❌ This class doesn't exist
```

### Reality
P1 must CREATE lens infrastructure from scratch:

```python
class TemporalLens(Lens):
    """Lens that wraps temporal perception capabilities."""

    def perceive(self, target, mode):
        # Call integration-specific method based on target type
        if isinstance(target, NotionEntity):
            return self._perceive_notion_temporal(target)
        elif isinstance(target, GitHubEntity):
            return self._perceive_github_temporal(target)
```

### Two Approaches for P1

**Option A: Adapter Pattern**
Create a common interface that adapts each integration's dimension methods:

```python
class DimensionAdapter(Protocol):
    async def analyze(self, entity_id: str) -> Dict[str, Any]: ...

class NotionTemporalAdapter(DimensionAdapter):
    def __init__(self, notion_intelligence: NotionSpatialIntelligence):
        self.intelligence = notion_intelligence

    async def analyze(self, entity_id: str) -> Dict[str, Any]:
        return await self.intelligence.analyze_timestamps(entity_id)
```

**Option B: Direct Integration**
Lenses directly call integration methods based on entity type:

```python
class TemporalLens:
    def __init__(self, integrations: Dict[str, SpatialIntelligence]):
        self.integrations = integrations

    async def perceive(self, entity: EntityProtocol) -> Perception:
        integration = self._get_integration_for(entity)
        raw_data = await integration.dimensions["TEMPORAL"](entity.id)
        return self._frame_as_perception(raw_data)
```

### Recommendation

Use **Option B (Direct Integration)** because:
1. Less boilerplate (no adapter classes needed)
2. Preserves existing working code
3. `self.dimensions` dict already provides the interface we need
4. Matches the existing pattern where Morning Standup calls integration methods directly

---

## Patterns to Preserve

### 1. The `self.dimensions` Dict Pattern

This is the de facto standard across 6 integrations. Keep it.

```python
self.dimensions = {
    "TEMPORAL": self.analyze_timestamps,
    ...
}
```

### 2. Comprehensive Analysis Methods

Each integration has a "get all 8 dimensions" method:
- Notion: `get_comprehensive_spatial_analysis()`
- GitHub: `create_spatial_context()`

Keep these - they're useful for full entity perception.

### 3. Slack's Domain Type Approach

Slack uses explicit types (`Territory`, `Room`, etc.) rather than methods. This is actually closer to Entity/Moment/Place thinking. Consider adopting for new work.

---

## Evidence Summary

| Claim | Evidence |
|-------|----------|
| `services/spatial/dimensions/` does not exist | `ls services/spatial/dimensions/` returns error |
| Dimensions are methods, not classes | `services/intelligence/spatial/notion_spatial.py:49-58` |
| 6 integrations use `self.dimensions` dict | `grep -r "dimensions" services/integrations/` |
| Slack uses different pattern | `services/integrations/slack/spatial_types.py` |
| Calendar has no spatial wrapper | `ls services/integrations/calendar/` shows no spatial files |
| Notion has all 8 dimensions | Methods at lines 88, 145, 212, 253, 307, 349, 393, 438 |
| GitHub has all 8 dimensions | Methods at lines 64, 84, 126, 166, 195, 235, 274, 314 |

---

## Files Verified

```bash
# Intelligence layer (general)
services/intelligence/spatial/
├── notion_spatial.py      # 632 lines, full 8D
└── gitbook_spatial.py     # 21132 bytes

# Integrations layer (per-integration)
services/integrations/spatial/
├── github_spatial.py      # 425 lines, full 8D
├── linear_spatial.py      # 19806 bytes
├── cicd_spatial.py        # 20463 bytes
├── devenvironment_spatial.py # 22962 bytes
└── gitbook_spatial.py     # 22953 bytes

# Slack (granular approach)
services/integrations/slack/
├── spatial_adapter.py
├── spatial_agent.py
├── spatial_intent_classifier.py
├── spatial_mapper.py
├── spatial_memory.py
└── spatial_types.py

# Calendar (no spatial)
services/integrations/calendar/
├── calendar_integration_router.py  # Has temporal data
└── (no spatial intelligence class)
```

---

*Analysis complete: 2026-01-19*
*P0 Deliverable 2 of 4*

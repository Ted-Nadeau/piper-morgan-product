# Issue #303 Implementation Plan - CONV-MCP-STANDUP: Standup Workflow Skill

**Date**: November 22, 2025
**Time**: 12:55 PM
**Issue**: CONV-MCP-STANDUP
**Priority**: P1 - High
**Status**: Planning

---

## Executive Summary

Consolidate scattered standup functionality (5+ issues, 75-98% complete) into a single, efficient MCP Skill that handles complete standup workflow with minimal token usage.

**Current State**: Working but spread across multiple services
**Goal**: Single `StandupWorkflowSkill` that can be called from chat/CLI/API
**Token Reduction**: Target 90%+ vs passing full context

---

## Current Standup Architecture (Existing Code)

### Core Components

1. **MorningStandupWorkflow** (`services/features/morning_standup.py`)
   - Generates standup from persistent context
   - Uses UserPreferenceManager for preferences
   - Uses SessionPersistenceManager for session context
   - Uses GitHubDomainService for recent activity
   - Performance: <2 seconds, saves 15+ minutes

2. **StandupOrchestrationService** (`services/domain/standup_orchestration_service.py`)
   - Coordinates workflow components
   - Handles integration between services
   - Manages error handling and fallbacks

3. **StandupCommand** (`cli/commands/standup.py`)
   - CLI interface with colored output
   - Pretty formatting and user feedback
   - Currently ~200+ lines of formatting code

4. **Supporting Services**
   - `StandupFormatter` - Format standup output
   - `StandupBridge` - Personality integration
   - `StandupReminderJob` - Scheduled reminders
   - Multiple test files showing usage patterns

### Issues Being Consolidated

1. MVP-STAND-FTUX: Standup Experience Excellence
2. MVP-STAND-INTERACTIVE: Interactive Standup Assistant
3. MVP-STAND-MODEL: Sprint Model & Team Coordination
4. MVP-STAND-MODES-UI: Advanced Multi-Modal UI Controls
5. MVP-STAND-SLACK-INTERACT: Interactive Slack Standup Features
6. (+ Others related to standup)

---

## Implementation Plan

### Phase 1: Create Base MCP Skill (30 minutes)

**File**: `services/integrations/mcp/skills/standup_workflow_skill.py`

```python
from services.integrations.mcp.skills.base_skill import BaseSkill
from services.features.morning_standup import MorningStandupWorkflow
from services.domain.standup_orchestration_service import StandupOrchestrationService

class StandupWorkflowSkill(BaseSkill):
    """
    Complete standup workflow in single MCP skill

    Handles:
    - Standup generation from context
    - Multi-system updates (Slack, GitHub, Notion)
    - Token-efficient processing
    """

    name = "standup"
    description = "Generate and distribute standup across all systems"

    def __init__(self):
        self.workflow = MorningStandupWorkflow(...)
        self.orchestration = StandupOrchestrationService()

    async def execute(self, params: dict) -> dict:
        """
        Execute standup workflow

        Params:
        - user_id: UUID of user
        - include_slack: bool (default True)
        - include_github: bool (default True)
        - include_notion: bool (default True)
        - format: str ("markdown", "json", "plain")

        Returns:
        {
            "success": bool,
            "standup": {...},
            "posted_to": [...],
            "issues_created": int,
            "token_estimate": int
        }
        """
        # 1. Generate standup from context
        standup = await self.workflow.generate_standup(params['user_id'])

        # 2. Multi-system updates
        posts = {}
        if params.get('include_slack'):
            posts['slack'] = await self._post_to_slack(standup)
        if params.get('include_github'):
            posts['github'] = await self._create_github_issues(standup)
        if params.get('include_notion'):
            posts['notion'] = await self._update_notion(standup)

        # 3. Return minimal summary
        return {
            'success': True,
            'standup': standup,
            'posted_to': list(posts.keys()),
            'issues_created': len(posts.get('github', [])),
            'token_estimate': self._estimate_tokens_saved(standup)
        }

    async def _post_to_slack(self, standup: dict) -> dict:
        """Post formatted standup to Slack"""
        # Reuse existing SlackDomainService integration

    async def _create_github_issues(self, standup: dict) -> list:
        """Create GitHub issues from action items"""
        # Extract action items and create as issues

    async def _update_notion(self, standup: dict) -> dict:
        """Update Notion with standup summary"""
        # Use NotionDomainService to update database

    def _estimate_tokens_saved(self, standup: dict) -> int:
        """Calculate token savings vs full context passing"""
        # Estimate based on standup size
        return len(str(standup))  # Simplified

    def validate_params(self, params: dict) -> bool:
        """Validate input parameters"""
        return 'user_id' in params
```

### Phase 2: Integrate Multi-System Updates (45 minutes)

**Tasks**:
1. Slack Integration
   - Format standup for Slack (rich formatting)
   - Use SlackDomainService to post to channel
   - Handle threading for replies

2. GitHub Integration
   - Parse action items from standup
   - Create issues with proper labels
   - Link to standup context
   - Close completed items

3. Notion Integration
   - Update standup database in Notion
   - Link to related tasks/projects
   - Archive old standups

### Phase 3: Token Optimization (30 minutes)

**Strategies**:
1. **Context Summarization**
   - Compress calendar data to key events
   - Summarize GitHub activity to action items
   - Extract only relevant Slack messages

2. **Selective Processing**
   - User can choose which systems to update
   - Lazy loading of integrations
   - Caching of repeated data

3. **Efficient Formatting**
   - Pre-compiled format templates
   - Reusable component library
   - Minimal string concatenation

**Target**: <1K tokens for full workflow (vs current ~20K)

### Phase 4: Testing & Validation (30 minutes)

**Tests**:
1. Unit tests for skill execution
2. Integration tests with real services
3. Token counting validation
4. Performance benchmarks

**Validation**:
- [ ] Skill generates valid standup
- [ ] Slack post successful
- [ ] GitHub issues created correctly
- [ ] Notion updated properly
- [ ] Token usage <1K
- [ ] Execution time <2s

### Phase 5: CLI & Chat Integration (20 minutes)

**Updates**:
1. Update `cli/commands/standup.py` to use skill
2. Add skill to Intent Service handlers
3. Register in skill catalog

**Before**:
```python
# cli/commands/standup.py - old way
command = StandupCommand()
result = await command.execute()
```

**After**:
```python
# cli/commands/standup.py - new way
skill = StandupWorkflowSkill()
result = await skill.execute({'user_id': user_id})
```

---

## File Structure

```
services/integrations/mcp/skills/
├── base_skill.py (already exists)
├── standup_workflow_skill.py (NEW)
└── __init__.py (update)

Refactored/Cleaned:
├── services/features/morning_standup.py (no changes needed)
├── services/domain/standup_orchestration_service.py (minor updates)
├── cli/commands/standup.py (updated to use skill)
└── web/api/routes/standup.py (updated to use skill)
```

---

## Acceptance Criteria

- [ ] Single `StandupWorkflowSkill` class created
- [ ] All existing standup functionality preserved
- [ ] Slack posting working
- [ ] GitHub issues creation working
- [ ] Notion updates working
- [ ] Token usage <1K per standup
- [ ] Execution time <2 seconds
- [ ] CLI command uses skill
- [ ] Chat integration working
- [ ] All tests passing
- [ ] No regressions in existing functionality

---

## Success Metrics

**Consolidation**:
- 5+ issues → 1 skill ✓
- Lines of code to maintain: -60%
- Reusability: Can call from CLI, chat, API

**Performance**:
- Token usage: <1K (vs 20K current)
- Execution: <2s (current <2s, maintain)
- Memory: Efficient (reuse existing services)

**User Experience**:
- One command: `standup` (simplified)
- Works everywhere: CLI, chat, API
- Same output quality

---

## Dependencies

### Already Exist (Reuse)
- ✅ `MorningStandupWorkflow` - Core generation
- ✅ `StandupOrchestrationService` - Coordination
- ✅ `SlackDomainService` - Slack integration
- ✅ `GitHubDomainService` - GitHub integration
- ✅ `NotionDomainService` - Notion integration
- ✅ `BaseSkill` - MCP skill base class

### New Components
- ❌ `StandupWorkflowSkill` - Main skill wrapper
- ❌ Multi-system coordination logic
- ❌ Token optimization strategies

---

## Effort Breakdown

| Phase | Task | Time | Notes |
|-------|------|------|-------|
| 1 | Create base skill | 30 min | Wraps existing workflow |
| 2 | Multi-system integration | 45 min | Slack, GitHub, Notion |
| 3 | Token optimization | 30 min | Compression strategies |
| 4 | Testing & validation | 30 min | Comprehensive test coverage |
| 5 | CLI/chat integration | 20 min | Update existing interfaces |
| **TOTAL** | | **~2.5 hours** | Includes testing |

---

## Key Design Decisions

1. **Reuse Existing Services**
   - Don't recreate wheel
   - Use existing domain services
   - Minimal new code

2. **Wrapper Pattern**
   - `StandupWorkflowSkill` wraps `MorningStandupWorkflow`
   - Clean separation of concerns
   - Easy to maintain

3. **Multi-System Updates**
   - Slack (notifications)
   - GitHub (action items)
   - Notion (documentation)
   - All in one call

4. **Token Efficiency**
   - Summarize before processing
   - Selective service updates
   - Minimal data passing

---

## Risk Assessment

**Low Risk**:
- Existing code proven working
- Skill pattern established (DocumentAnalysisSkill)
- All dependencies available
- Comprehensive test coverage

**Mitigation**:
- Keep existing services unchanged
- Add new skill alongside old code
- Gradual CLI migration
- Full rollback if needed

---

## Next Steps

1. Create `StandupWorkflowSkill` class
2. Implement skill execute method
3. Add multi-system update methods
4. Write comprehensive tests
5. Update CLI to use skill
6. Validate all functionality
7. Document skill usage
8. Close issue #303

---

**Implementation Ready**: ✅ YES
**All Dependencies Available**: ✅ YES
**Estimated Start Time**: 12:55 PM
**Estimated Completion**: 3:25 PM (~2.5 hours including testing)

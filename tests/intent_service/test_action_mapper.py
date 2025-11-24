"""
Unit tests for ActionMapper (Issue #284, #294)

Tests the action mapping logic for EXECUTION category actions.

ActionMapper handles EXECUTION category actions ONLY.
Other categories (QUERY, ANALYSIS, SYNTHESIS) route by category
and don't use action name mapping.

These tests verify:
- EXECUTION action variations map to correct handler methods
- Unknown actions fall back gracefully
- Mapping is consistent with execution handler expectations
"""

import pytest

from services.intent_service.action_mapper import ActionMapper


class TestActionMapper:
    """Test ActionMapper functionality - EXECUTION actions only"""

    # ===== GITHUB ACTIONS (EXECUTION category) =====

    def test_github_issue_create_mapping(self):
        """Test create_github_issue maps to create_issue"""
        result = ActionMapper.map_action("create_github_issue")
        assert result == "create_issue"

    def test_github_issue_create_item_mapping(self):
        """Test create_item maps to create_issue"""
        result = ActionMapper.map_action("create_item")
        assert result == "create_issue"

    def test_github_issue_update_mapping(self):
        """Test update_github_issue maps to update_issue"""
        result = ActionMapper.map_action("update_github_issue")
        assert result == "update_issue"

    def test_update_ticket_mapping(self):
        """Test update_ticket maps to update_issue"""
        result = ActionMapper.map_action("update_ticket")
        assert result == "update_issue"

    def test_make_github_issue_mapping(self):
        """Test make_github_issue maps to create_issue"""
        result = ActionMapper.map_action("make_github_issue")
        assert result == "create_issue"

    # ===== TODO ACTIONS (EXECUTION category) =====

    def test_add_todo_mapping(self):
        """Test add_todo maps to create_todo (Issue #285)"""
        result = ActionMapper.map_action("add_todo")
        assert result == "create_todo"

    def test_mark_done_mapping(self):
        """Test mark_done maps to complete_todo (Issue #285)"""
        result = ActionMapper.map_action("mark_done")
        assert result == "complete_todo"

    def test_show_todos_mapping(self):
        """Test show_todos maps to list_todos"""
        result = ActionMapper.map_action("show_todos")
        assert result == "list_todos"

    def test_remove_todo_mapping(self):
        """Test remove_todo maps to delete_todo"""
        result = ActionMapper.map_action("remove_todo")
        assert result == "delete_todo"

    # ===== FALLBACK BEHAVIOR =====

    def test_unmapped_action_fallback(self):
        """Test unmapped action returns original action"""
        result = ActionMapper.map_action("unknown_action_xyz")
        assert result == "unknown_action_xyz"

    def test_empty_action_returns_unknown_intent(self):
        """Test empty action string returns unknown_intent"""
        result = ActionMapper.map_action("")
        assert result == "unknown_intent"

    def test_none_action_returns_unknown_intent(self):
        """Test None action returns unknown_intent"""
        result = ActionMapper.map_action(None)
        assert result == "unknown_intent"

    # ===== METADATA TESTS =====

    def test_mapping_count(self):
        """Test that we have only EXECUTION mappings (Issue #294)"""
        mappings = ActionMapper.list_all_mappings()
        # Updated after Issue #294 cleanup: removed non-EXECUTION mappings
        assert len(mappings) == 26, f"Expected 26 EXECUTION mappings, got {len(mappings)}"

    def test_get_mapping_coverage(self):
        """Test mapping coverage calculation"""
        test_actions = ["create_github_issue", "unknown_action", "add_todo"]
        coverage = ActionMapper.get_mapping_coverage(test_actions)
        assert coverage == pytest.approx(66.67, rel=0.1)  # 2 out of 3 mapped

    def test_dynamic_add_mapping(self):
        """Test dynamically adding a new mapping"""
        ActionMapper.add_mapping("test_action", "test_handler")
        result = ActionMapper.map_action("test_action")
        assert result == "test_handler"

        # Clean up
        ActionMapper.ACTION_MAPPING.pop("test_action", None)

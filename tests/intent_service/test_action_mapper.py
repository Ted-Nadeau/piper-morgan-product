"""
Unit tests for ActionMapper (Issue #284)

Tests the action mapping logic independently of IntentService integration.
"""

import pytest

from services.intent_service.action_mapper import ActionMapper


class TestActionMapper:
    """Test ActionMapper functionality"""

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

    def test_analyze_data_passthrough(self):
        """Test analyze_data passes through unchanged"""
        result = ActionMapper.map_action("analyze_data")
        assert result == "analyze_data"

    def test_analyze_github_issue_mapping(self):
        """Test analyze_github_issue maps to analyze_data"""
        result = ActionMapper.map_action("analyze_github_issue")
        assert result == "analyze_data"

    def test_analyze_commits_passthrough(self):
        """Test analyze_commits passes through unchanged"""
        result = ActionMapper.map_action("analyze_commits")
        assert result == "analyze_commits"

    def test_generate_content_passthrough(self):
        """Test generate_content passes through unchanged"""
        result = ActionMapper.map_action("generate_content")
        assert result == "generate_content"

    def test_create_content_mapping(self):
        """Test create_content maps to generate_content"""
        result = ActionMapper.map_action("create_content")
        assert result == "generate_content"

    def test_performance_analysis_mapping(self):
        """Test performance_analysis maps to generate_report"""
        result = ActionMapper.map_action("performance_analysis")
        assert result == "generate_report"

    def test_plan_strategy_mapping(self):
        """Test plan_strategy maps to strategic_planning"""
        result = ActionMapper.map_action("plan_strategy")
        assert result == "strategic_planning"

    def test_prioritize_mapping(self):
        """Test prioritize maps to prioritization"""
        result = ActionMapper.map_action("prioritize")
        assert result == "prioritization"

    def test_show_projects_mapping(self):
        """Test show_projects maps to projects_query"""
        result = ActionMapper.map_action("show_projects")
        assert result == "projects_query"

    def test_find_documents_mapping(self):
        """Test find_documents maps to generic_query"""
        result = ActionMapper.map_action("find_documents")
        assert result == "generic_query"

    def test_add_todo_mapping(self):
        """Test add_todo maps to create_todo (Issue #285)"""
        result = ActionMapper.map_action("add_todo")
        assert result == "create_todo"

    def test_mark_done_mapping(self):
        """Test mark_done maps to complete_todo (Issue #285)"""
        result = ActionMapper.map_action("mark_done")
        assert result == "complete_todo"

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

    def test_mapping_count(self):
        """Test that we have the expected number of mappings"""
        mappings = ActionMapper.list_all_mappings()
        assert len(mappings) == 66, f"Expected 66 mappings, got {len(mappings)}"

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

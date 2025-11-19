"""Tests for enhanced ActionHumanizer conversational patterns"""

import pytest

from services.ui_messages.action_humanizer import ActionHumanizer


class TestEnhancedActionHumanizer:
    """Test enhanced conversational patterns in ActionHumanizer"""

    @pytest.fixture
    def humanizer(self):
        """ActionHumanizer instance for testing"""
        return ActionHumanizer()

    @pytest.mark.asyncio
    async def test_conversational_verb_mappings(self, humanizer):
        """Test that verbs are converted to more conversational forms"""
        test_cases = [
            ("fetch_issues", "grab those issues"),
            ("retrieve_data", "get that data"),
            ("investigate_bug", "look into that bug"),
            ("analyze_performance", "take a look at the performance"),
            ("review_code", "check out the code"),
            ("summarize_report", "sum up a report"),
            ("extract_insights", "pull out those insights"),
            ("handle_error", "take care of that error"),
        ]

        for action, expected in test_cases:
            result = await humanizer.humanize(action)
            assert (
                result == expected
            ), f"Expected '{expected}' but got '{result}' for action '{action}'"

    @pytest.mark.asyncio
    async def test_special_patterns(self, humanizer):
        """Test special pattern overrides"""
        test_cases = [
            ("fetch_github_issues", "grab those GitHub issues"),
            ("fetch_user_data", "grab that user data"),
            ("list_github_issues", "show you those GitHub issues"),
        ]

        for action, expected in test_cases:
            result = await humanizer.humanize(action)
            assert (
                result == expected
            ), f"Expected '{expected}' but got '{result}' for action '{action}'"

    @pytest.mark.asyncio
    async def test_contextual_noun_phrasing(self, humanizer):
        """Test that nouns use contextual phrasing"""
        test_cases = [
            ("count_issues", "count up those issues"),
            ("list_tasks", "show you those tasks"),
            ("update_project", "update the project"),
            ("review_sprint", "check out the sprint"),
            ("analyze_metrics", "take a look at those metrics"),
        ]

        for action, expected in test_cases:
            result = await humanizer.humanize(action)
            assert (
                result == expected
            ), f"Expected '{expected}' but got '{result}' for action '{action}'"

    @pytest.mark.asyncio
    async def test_three_part_actions(self, humanizer):
        """Test verb_adjective_noun patterns"""
        test_cases = [
            ("create_new_issue", "create a new issue"),
            ("generate_detailed_report", "put together a detailed report"),
            ("analyze_recent_data", "take a look at recent that data"),
        ]

        for action, expected in test_cases:
            result = await humanizer.humanize(action)
            assert (
                result == expected
            ), f"Expected '{expected}' but got '{result}' for action '{action}'"

    @pytest.mark.asyncio
    async def test_single_word_conversational_mapping(self, humanizer):
        """Test single words get conversational mappings"""
        test_cases = [
            ("fetch", "grab"),
            ("analyze", "take a look at"),
            ("investigate", "look into"),
            ("review", "check out"),
            ("summarize", "sum up"),
            ("extract", "pull out"),
            ("handle", "take care of"),
        ]

        for action, expected in test_cases:
            result = await humanizer.humanize(action)
            assert (
                result == expected
            ), f"Expected '{expected}' but got '{result}' for action '{action}'"

    @pytest.mark.asyncio
    async def test_fallback_behavior(self, humanizer):
        """Test fallback for unknown patterns"""
        test_cases = [
            ("unknown_action", "unknown action"),
            ("custom_workflow", "custom workflow"),
            ("process_complex_data_structure", "work on complex data structure"),
        ]

        for action, expected in test_cases:
            result = await humanizer.humanize(action)
            assert (
                result == expected
            ), f"Expected '{expected}' but got '{result}' for action '{action}'"

    @pytest.mark.asyncio
    async def test_pm_realistic_queries(self, humanizer):
        """Test with realistic PM queries from handoff prompt"""
        test_cases = [
            (
                "fetch_github_issues",
                "grab those GitHub issues",
            ),  # "I'll grab those GitHub issues for you"
            ("create_ticket", "create a ticket"),
            ("analyze_file", "take a look at a file"),
            ("list_projects", "show you the projects"),
            ("count_issues", "count up those issues"),
            ("review_pull_request", "check out a pull request"),
            ("summarize_document", "sum up a document"),
            ("investigate_crash", "look into that crash"),
        ]

        for action, expected in test_cases:
            result = await humanizer.humanize(action)
            assert (
                result == expected
            ), f"Expected '{expected}' but got '{result}' for action '{action}'"

    @pytest.mark.asyncio
    async def test_maintains_technical_accuracy(self, humanizer):
        """Test that conversational mapping maintains technical accuracy"""
        # These should still be clear about what they do
        test_cases = [
            ("delete_file", "remove a file"),  # Clear it's destructive
            ("create_backup", "create a backup"),  # Clear it's creating something
            ("update_database", "update a database"),  # Clear what's being updated
            ("send_notification", "send a notification"),  # Clear action
        ]

        for action, expected in test_cases:
            result = await humanizer.humanize(action)
            assert (
                result == expected
            ), f"Expected '{expected}' but got '{result}' for action '{action}'"

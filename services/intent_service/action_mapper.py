"""
Action Mapper - Maps classifier action outputs to handler method names

Issue #284: CORE-ALPHA-ACTION-MAPPING
Problem: Intent classifier generates action names that don't match handler method names
Solution: Centralized mapping layer between classifier output and handler dispatch

Example:
    Classifier outputs: "create_github_issue"
    Handler expects: "create_issue"
    ActionMapper bridges: "create_github_issue" -> "create_issue"
"""

import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class ActionMapper:
    """
    Maps classifier action outputs to handler method names.

    The intent classifier outputs descriptive action names (e.g., "create_github_issue")
    while handler methods use normalized names (e.g., "_handle_create_issue").
    This class provides the translation layer.

    Design Principles:
    1. Explicit mappings for known mismatches
    2. Graceful fallback to original action if unmapped
    3. Logging for discovery of new patterns
    4. No silent failures - always returns a string
    """

    # Comprehensive action mappings from classifier output to handler method names
    ACTION_MAPPING: Dict[str, str] = {
        # ===== EXECUTION ACTIONS =====
        # GitHub Issue Creation
        "create_github_issue": "create_issue",
        "create_item": "create_issue",  # Generic create from classifier
        "create_ticket": "create_issue",  # Already normalized
        "create_issue": "create_issue",  # Already normalized
        # GitHub Issue Updates
        "update_github_issue": "update_issue",
        "update_ticket": "update_issue",
        "update_issue": "update_issue",  # Already normalized
        # ===== ANALYSIS ACTIONS =====
        # Data/File Analysis
        "analyze_data": "analyze_data",  # Already normalized
        "analyze_file": "analyze_data",
        "analyze_github_issue": "analyze_data",
        "review_github_issue": "analyze_data",
        "check_github_issue": "analyze_data",
        "analyze_metrics": "analyze_data",
        "analyze_feedback": "analyze_data",
        "system_analysis": "analyze_data",
        # Commit Analysis
        "analyze_commits": "analyze_commits",  # Already normalized
        "review_commits": "analyze_commits",
        # ===== SYNTHESIS ACTIONS =====
        # Content Generation
        "generate_content": "generate_content",  # Already normalized
        "create_content": "generate_content",
        "write_content": "generate_content",
        # Report Generation
        "generate_report": "generate_report",  # Already normalized
        "create_report": "generate_report",
        "performance_analysis": "generate_report",
        "user_feedback_analysis": "generate_report",
        # Summarization
        "summarize": "summarize",  # Already normalized
        "summarize_issue": "summarize",
        "summarize_commits": "summarize",
        # ===== STRATEGY ACTIONS =====
        # Strategic Planning
        "strategic_planning": "strategic_planning",  # Already normalized
        "plan_strategy": "strategic_planning",
        "create_plan": "strategic_planning",
        # Prioritization
        "prioritize": "prioritization",
        "prioritization": "prioritization",  # Already normalized
        "rank_items": "prioritization",
        # ===== LEARNING ACTIONS =====
        # Pattern Learning
        "learn_pattern": "learn_pattern",  # Already normalized
        "discover_pattern": "learn_pattern",
        "identify_pattern": "learn_pattern",
        # ===== QUERY ACTIONS =====
        # Projects
        "list_projects": "projects_query",
        "list_all_projects": "projects_query",
        "show_projects": "projects_query",
        "get_project": "projects_query",
        "get_project_details": "projects_query",
        "find_project": "projects_query",
        "count_projects": "projects_query",
        "get_default_project": "projects_query",
        # Documents/Files
        "find_documents": "generic_query",
        "search_files": "generic_query",
        "search_content": "generic_query",
        "list_items": "generic_query",
        # Standup
        "get_standup": "standup_query",
        "standup": "standup_query",
        # ===== SPECIAL ACTIONS =====
        # Clarification
        "clarification_needed": "unknown_intent",
        "unknown": "unknown_intent",
    }

    @classmethod
    def map_action(cls, classifier_action: str) -> str:
        """
        Map classifier action to handler method name.

        Args:
            classifier_action: Action string from classifier (e.g., "create_github_issue")

        Returns:
            Normalized action name for handler (e.g., "create_issue")

        Note:
            Always returns a string - never None. Falls back to original action
            if no explicit mapping exists.
        """
        if not classifier_action:
            logger.warning("ActionMapper received empty action string")
            return "unknown_intent"

        # Check for explicit mapping
        mapped_action = cls.ACTION_MAPPING.get(classifier_action)

        if mapped_action:
            if mapped_action != classifier_action:
                logger.debug(f"Action mapped: '{classifier_action}' -> '{mapped_action}'")
            return mapped_action

        # No explicit mapping found - log for future additions
        logger.warning(
            f"Unmapped action: '{classifier_action}' - using original. "
            f"Consider adding to ACTION_MAPPING if this is a common action."
        )

        # Fallback: use original action
        return classifier_action

    @classmethod
    def get_unmapped_count(cls, all_actions: list[str]) -> int:
        """
        Return count of unmapped actions for metrics.

        Args:
            all_actions: List of classifier action strings to check

        Returns:
            Number of actions not in ACTION_MAPPING
        """
        return sum(1 for action in all_actions if action not in cls.ACTION_MAPPING)

    @classmethod
    def get_mapping_coverage(cls, all_actions: list[str]) -> float:
        """
        Calculate mapping coverage percentage.

        Args:
            all_actions: List of classifier action strings to check

        Returns:
            Percentage of actions that have explicit mappings (0.0 to 100.0)
        """
        if not all_actions:
            return 100.0

        mapped_count = sum(1 for action in all_actions if action in cls.ACTION_MAPPING)
        return (mapped_count / len(all_actions)) * 100.0

    @classmethod
    def list_all_mappings(cls) -> Dict[str, str]:
        """
        Return copy of all action mappings for inspection/debugging.

        Returns:
            Dictionary of classifier_action -> handler_action mappings
        """
        return cls.ACTION_MAPPING.copy()

    @classmethod
    def add_mapping(cls, classifier_action: str, handler_action: str) -> None:
        """
        Dynamically add a new action mapping.

        Args:
            classifier_action: Action string from classifier
            handler_action: Normalized action for handler

        Note:
            Used for runtime learning/adaptation. Changes not persisted.
        """
        if classifier_action in cls.ACTION_MAPPING:
            logger.info(
                f"Overwriting existing mapping: '{classifier_action}' "
                f"(was: '{cls.ACTION_MAPPING[classifier_action]}', now: '{handler_action}')"
            )
        else:
            logger.info(f"Adding new mapping: '{classifier_action}' -> '{handler_action}'")

        cls.ACTION_MAPPING[classifier_action] = handler_action

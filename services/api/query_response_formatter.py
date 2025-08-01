"""
Query Response Formatter - Convert QueryRouter responses to API-compatible format

Handles the diverse response types from QueryRouter (strings, dicts, objects)
and converts them to user-friendly message strings for API responses.
"""

import logging
from typing import Any, Dict, List, Union

logger = logging.getLogger(__name__)


class QueryResponseFormatter:
    """Formats QueryRouter responses for API consumption"""

    @staticmethod
    def format_query_response(query_result: Any, intent_action: str) -> str:
        """
        Convert QueryRouter response to user-friendly message string

        Args:
            query_result: Response from QueryRouter (string, dict, list, or objects)
            intent_action: The query action for context-specific formatting

        Returns:
            User-friendly message string suitable for API response
        """
        try:
            return QueryResponseFormatter._format_by_type(query_result, intent_action)
        except Exception as e:
            logger.error(f"Error formatting query response for {intent_action}: {e}")
            # Fallback to safe string representation
            return f"I processed your {intent_action} request. The response is available."

    @staticmethod
    def _format_by_type(query_result: Any, intent_action: str) -> str:
        """Format based on response type"""

        # String responses (degradation messages, conversation responses)
        if isinstance(query_result, str):
            return query_result

        # Dictionary responses (file operations, structured errors)
        elif isinstance(query_result, dict):
            return QueryResponseFormatter._format_dict_response(query_result, intent_action)

        # List responses (project lists, search results)
        elif isinstance(query_result, list):
            return QueryResponseFormatter._format_list_response(query_result, intent_action)

        # Object responses (single project, etc.)
        else:
            return QueryResponseFormatter._format_object_response(query_result, intent_action)

    @staticmethod
    def _format_dict_response(response_dict: Dict, intent_action: str) -> str:
        """Format dictionary responses (typically from file operations)"""

        # Handle file service error responses
        if response_dict.get("success") is False:
            error_msg = response_dict.get("error", "Service temporarily unavailable")
            suggestion = response_dict.get("suggestion", "")

            message = error_msg
            if suggestion:
                message += f" {suggestion}"

            # Add fallback information if available
            if response_dict.get("fallback_available"):
                fallback_action = response_dict.get("fallback_action", "try a different approach")
                message += f" You can {fallback_action}."

            return message

        # Handle successful file service responses
        elif "results" in response_dict:
            results = response_dict.get("results", [])
            query = response_dict.get("query", intent_action)

            if not results:
                return f"No results found for '{query}'. Try a different search term or check if files are available."

            if len(results) == 1:
                return f"Found 1 result for '{query}': {results[0].get('filename', 'result')}"
            else:
                return (
                    f"Found {len(results)} results for '{query}'. Here are the matches: "
                    + ", ".join([r.get("filename", "result") for r in results[:5]])
                    + ("..." if len(results) > 5 else "")
                )

        # Handle other structured responses
        else:
            # Extract meaningful information from the dict
            if "message" in response_dict:
                return response_dict["message"]
            elif "content" in response_dict:
                content = response_dict["content"]
                if isinstance(content, str) and len(content) < 500:
                    return content
                else:
                    return f"I found the requested information for {intent_action}. The content is ready for review."
            else:
                return f"I successfully processed your {intent_action} request."

    @staticmethod
    def _format_list_response(response_list: List, intent_action: str) -> str:
        """Format list responses (project lists, search results)"""

        if not response_list:
            return f"No items found for {intent_action}."

        # Handle project lists
        if intent_action == "list_projects":
            if hasattr(response_list[0], "to_dict"):
                # Project objects
                project_names = [p.to_dict()["name"] for p in response_list]
            elif isinstance(response_list[0], dict) and "name" in response_list[0]:
                # Project dicts
                project_names = [p["name"] for p in response_list]
            else:
                # Fallback
                project_names = [str(p) for p in response_list]

            return f"I found {len(response_list)} projects: " + ", ".join(project_names)

        # Handle other list types
        else:
            if len(response_list) == 1:
                return f"Found 1 result for {intent_action}: {response_list[0]}"
            else:
                return (
                    f"Found {len(response_list)} results for {intent_action}. "
                    + "Here are the first few: "
                    + ", ".join([str(r) for r in response_list[:3]])
                    + ("..." if len(response_list) > 3 else "")
                )

    @staticmethod
    def _format_object_response(response_obj: Any, intent_action: str) -> str:
        """Format single object responses"""

        # Handle project objects
        if hasattr(response_obj, "to_dict"):
            obj_dict = response_obj.to_dict()
            if "name" in obj_dict:
                return f"Found project: {obj_dict['name']}"
            else:
                return f"Found the requested {intent_action} information."

        # Handle other objects
        elif hasattr(response_obj, "__dict__"):
            return f"Found the requested {intent_action} information."
        else:
            return str(response_obj)

    @staticmethod
    def is_degradation_response(query_result: Any) -> bool:
        """Check if the response is a degradation message"""
        if isinstance(query_result, str):
            degradation_keywords = [
                "temporarily unavailable",
                "database unavailable",
                "service unavailable",
                "try again later",
                "docker is running",
            ]
            return any(keyword in query_result.lower() for keyword in degradation_keywords)

        elif isinstance(query_result, dict):
            return query_result.get("success") is False

        return False

    @staticmethod
    def extract_user_action_hint(query_result: Any) -> str:
        """Extract actionable guidance from degradation responses"""
        if isinstance(query_result, str):
            if "docker is running" in query_result.lower():
                return "Please check your database connection."
            elif "try again" in query_result.lower():
                return "Please try your request again in a moment."

        elif isinstance(query_result, dict):
            return query_result.get("suggestion", "Please try again later.")

        return "Please try again later."

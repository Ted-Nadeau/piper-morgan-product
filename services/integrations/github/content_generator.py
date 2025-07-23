"""
GitHub Issue Content Generator
Transforms natural language requests into professional GitHub issues using LLM
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from services.domain.models import ProjectContext
from services.llm.clients import LLMClient

logger = logging.getLogger(__name__)


class GitHubIssueContentGenerator:
    """
    Transform natural language to professional GitHub issues

    Converts user requests like "create ticket for login bug with high priority" to:
    - Title: "Fix login authentication issue"
    - Body: Detailed markdown with reproduction steps
    - Labels: ["bug", "high-priority", "authentication"]
    """

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    async def generate_issue_content(
        self,
        user_request: str,
        project_context: Optional[ProjectContext] = None,
        template_preferences: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Generate professional GitHub issue content from natural language

        Args:
            user_request: Natural language description of the issue
            project_context: Project context for enhanced content generation
            template_preferences: User preferences for issue formatting

        Returns:
            Dict containing:
            - title: Professional issue title
            - body: Detailed markdown body with structure
            - labels: List of appropriate labels
            - priority: Inferred priority level
            - issue_type: bug, feature, enhancement, etc.
        """
        try:
            # Build enhanced prompt with context
            prompt = self._build_content_generation_prompt(
                user_request, project_context, template_preferences
            )

            # Generate content using LLM
            response = await self.llm_client.complete(
                task_type="github_content_generation",
                prompt=prompt,
                context=self._prepare_context(user_request, project_context),
                response_format="json",
            )

            # Parse and validate response
            content = self._parse_llm_response(response)

            # Enhance with project-specific patterns
            if project_context:
                content = self._enhance_with_project_context(content, project_context)

            # Validate and sanitize content
            content = self._validate_and_sanitize(content)

            logger.info(f"Generated GitHub issue content: {content.get('title', 'Unknown')}")
            return content

        except Exception as e:
            logger.error(f"Failed to generate GitHub issue content: {e}")
            # Fallback to basic content structure
            return self._create_fallback_content(user_request)

    def _build_content_generation_prompt(
        self,
        user_request: str,
        project_context: Optional[ProjectContext] = None,
        template_preferences: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Build comprehensive prompt for GitHub issue content generation"""

        base_prompt = f"""
Transform the following user request into professional GitHub issue content:

User Request: "{user_request}"

Generate a complete GitHub issue with the following structure:

{{
    "title": "Clear, concise issue title (max 60 characters)",
    "body": "Detailed markdown body with sections",
    "labels": ["list", "of", "appropriate", "labels"],
    "priority": "low|medium|high|critical",
    "issue_type": "bug|feature|enhancement|documentation|question|discussion"
}}

Guidelines for professional GitHub issues:

1. TITLE:
   - Clear, actionable, specific
   - Use imperative mood ("Fix login bug" not "Login bug")
   - Include key component/area when relevant
   - Avoid redundant words

2. BODY:
   - Start with brief description
   - Include reproduction steps for bugs
   - Add acceptance criteria for features
   - Use markdown formatting
   - Include relevant context

3. LABELS:
   - Infer from content (bug, feature, enhancement, etc.)
   - Add priority labels (low-priority, high-priority, etc.)
   - Include component labels (authentication, ui, api, etc.)
   - Suggest 3-6 relevant labels maximum

4. PRIORITY:
   - critical: System down, security vulnerability, data loss
   - high: Major functionality broken, blocks users
   - medium: Important feature or notable bug
   - low: Minor issue, nice-to-have improvement

5. ISSUE_TYPE:
   - bug: Something is broken
   - feature: New functionality request
   - enhancement: Improvement to existing functionality
   - documentation: Documentation changes
   - question: Need clarification or help
   - discussion: RFC or architectural discussion
"""

        # Add project context if available
        if project_context:
            base_prompt += f"""

PROJECT CONTEXT:
- Project: {project_context.name}
- Description: {project_context.description or 'N/A'}
- Technologies: {', '.join(project_context.technologies) if project_context.technologies else 'N/A'}

Tailor the issue content to fit this project's context and terminology.
"""

        # Add template preferences if specified
        if template_preferences:
            base_prompt += f"""

USER PREFERENCES:
{self._format_template_preferences(template_preferences)}
"""

        base_prompt += """

Return only the JSON object with the issue content. Ensure all fields are properly formatted and professional.
"""

        return base_prompt

    def _prepare_context(
        self, user_request: str, project_context: Optional[ProjectContext] = None
    ) -> Dict[str, Any]:
        """Prepare context for LLM completion"""
        context = {
            "user_request": user_request,
            "timestamp": datetime.now().isoformat(),
            "task": "github_issue_content_generation",
        }

        if project_context:
            context["project"] = {
                "name": project_context.name,
                "description": project_context.description,
                "technologies": project_context.technologies,
            }

        return context

    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """Parse and validate LLM response"""
        import json

        try:
            # Try to parse as JSON
            content = json.loads(response.strip())

            # Validate required fields
            required_fields = ["title", "body", "labels", "priority", "issue_type"]
            for field in required_fields:
                if field not in content:
                    raise ValueError(f"Missing required field: {field}")

            return content

        except (json.JSONDecodeError, ValueError) as e:
            logger.warning(f"Failed to parse LLM response as JSON: {e}")
            logger.debug(f"Raw response: {response}")

            # Try to extract content manually
            return self._extract_content_from_text(response)

    def _extract_content_from_text(self, response: str) -> Dict[str, Any]:
        """Extract issue content from non-JSON response"""
        # Basic text parsing as fallback
        lines = response.strip().split("\n")

        content = {
            "title": "Issue",
            "body": response,
            "labels": ["needs-triage"],
            "priority": "medium",
            "issue_type": "question",
        }

        # Try to extract title from first line
        if lines:
            first_line = lines[0].strip()
            if len(first_line) < 100:  # Reasonable title length
                content["title"] = first_line

        return content

    def _enhance_with_project_context(
        self, content: Dict[str, Any], project_context: ProjectContext
    ) -> Dict[str, Any]:
        """Enhance content with project-specific patterns"""

        # Add project-specific labels
        if project_context.technologies:
            tech_labels = []
            for tech in project_context.technologies:
                tech_lower = tech.lower()
                if tech_lower in ["python", "javascript", "react", "django", "fastapi"]:
                    tech_labels.append(tech_lower)

            # Add technology labels (limit to avoid label spam)
            content["labels"].extend(tech_labels[:2])

        # Enhance body with project context
        if project_context.description:
            context_note = f"\n\n---\n**Project Context:** {project_context.description}"
            content["body"] += context_note

        return content

    def _validate_and_sanitize(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and sanitize issue content"""

        # Sanitize title
        title = str(content.get("title", "")).strip()
        if len(title) > 100:  # GitHub title limit
            title = title[:97] + "..."
        content["title"] = title or "Untitled Issue"

        # Sanitize body
        body = str(content.get("body", "")).strip()
        content["body"] = body or "No description provided."

        # Validate labels
        labels = content.get("labels", [])
        if isinstance(labels, list):
            # Remove duplicates and limit count
            labels = list(set(str(label).lower().replace(" ", "-") for label in labels))
            content["labels"] = labels[:8]  # Reasonable limit
        else:
            content["labels"] = ["needs-triage"]

        # Validate priority
        valid_priorities = ["low", "medium", "high", "critical"]
        priority = str(content.get("priority", "medium")).lower()
        content["priority"] = priority if priority in valid_priorities else "medium"

        # Validate issue type
        valid_types = ["bug", "feature", "enhancement", "documentation", "question", "discussion"]
        issue_type = str(content.get("issue_type", "question")).lower()
        content["issue_type"] = issue_type if issue_type in valid_types else "question"

        return content

    def _format_template_preferences(self, preferences: Dict[str, Any]) -> str:
        """Format template preferences for prompt"""
        formatted = []
        for key, value in preferences.items():
            formatted.append(f"- {key}: {value}")
        return "\n".join(formatted)

    def _create_fallback_content(self, user_request: str) -> Dict[str, Any]:
        """Create basic fallback content when LLM generation fails"""
        return {
            "title": (
                f"Issue: {user_request[:50]}..."
                if len(user_request) > 50
                else f"Issue: {user_request}"
            ),
            "body": f"## Description\n\n{user_request}\n\n## Additional Information\n\nThis issue was created from a user request. Please add more details as needed.",
            "labels": ["needs-triage", "needs-details"],
            "priority": "medium",
            "issue_type": "question",
        }

"""
WorkItem Extractor - Domain Service
Extracts structured WorkItem from natural language using LLM
"""

import json
import re
from dataclasses import dataclass
from typing import Any, Dict, Optional

import structlog

from services.domain.models import WorkItem
from services.llm.clients import LLMClient

logger = structlog.get_logger()


@dataclass
class ExtractionResult:
    """Result of work item extraction"""

    success: bool
    work_item: Optional[WorkItem] = None
    error: Optional[str] = None
    raw_response: Optional[str] = None


class WorkItemExtractor:
    """Extracts WorkItem from natural language using LLM"""

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    async def extract_from_prompt(
        self, prompt: str, project_context: Optional[Dict[str, Any]] = None
    ) -> WorkItem:
        """
        Extract work item details from natural language prompt

        Args:
            prompt: Natural language description of the work item
            project_context: Optional project context for additional details

        Returns:
            Populated WorkItem with extracted details

        Raises:
            ValueError: If extraction fails and no fallback is possible
        """
        # Prepare extraction prompt
        extraction_prompt = self._build_extraction_prompt(prompt, project_context)

        try:
            # Call LLM with JSON mode for structured response
            response = await self.llm_client.complete(
                task_type="work_item_extraction",
                prompt=extraction_prompt,
                response_format={"type": "json_object"},
            )

            # Parse JSON response
            extracted_data = self._parse_json_response(response)

            # Create and validate WorkItem
            work_item = self._create_work_item(extracted_data, prompt)

            return work_item

        except Exception as e:
            # Fallback to basic extraction if LLM fails
            logger.warning(f"LLM extraction failed: {str(e)}, using fallback")
            return self._fallback_extraction(prompt, project_context)

    def _build_extraction_prompt(
        self, prompt: str, project_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Build the extraction prompt for the LLM"""

        context_info = ""
        if project_context:
            context_info = f"\nProject Context: {json.dumps(project_context, indent=2)}"

        return f"""Extract work item details from this request: "{prompt}"

Provide a JSON response with:
{{
    "title": "Brief, descriptive title (max 100 chars)",
    "description": "Detailed description with:\\n- Problem description\\n- Steps to reproduce (if applicable)\\n- Expected behavior\\n- Actual behavior\\n- Additional context",
    "type": "bug|feature|task|improvement",
    "priority": "low|medium|high|critical",
    "labels": ["relevant", "labels", "for", "this", "issue"]
}}

Context:
- This is for a GitHub issue
- Be specific and actionable
- Use standard issue tracking conventions
- Title should be clear and searchable
- Description should be comprehensive but concise
- Labels should be relevant and specific{context_info}

Response must be valid JSON only."""

    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """Parse JSON response from LLM, with error handling"""
        try:
            # Clean up response - remove any markdown formatting
            cleaned_response = response.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]
            cleaned_response = cleaned_response.strip()

            return json.loads(cleaned_response)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Failed to parse LLM response as JSON: {str(e)}\nResponse: {response}"
            )

    def _create_work_item(
        self, extracted_data: Dict[str, Any], original_prompt: str
    ) -> WorkItem:
        """Create WorkItem from extracted data with validation"""

        # Validate required fields
        required_fields = ["title", "description", "type", "priority", "labels"]
        for field in required_fields:
            if field not in extracted_data:
                raise ValueError(f"Missing required field: {field}")

        # Validate and normalize type
        valid_types = ["bug", "feature", "task", "improvement"]
        item_type = extracted_data["type"].lower()
        if item_type not in valid_types:
            item_type = "task"  # Default fallback

        # Validate and normalize priority
        valid_priorities = ["low", "medium", "high", "critical"]
        priority = extracted_data["priority"].lower()
        if priority not in valid_priorities:
            priority = "medium"  # Default fallback

        # Ensure labels is a list
        labels = extracted_data["labels"]
        if not isinstance(labels, list):
            labels = [labels] if labels else []

        # Clean and validate title
        title = extracted_data["title"].strip()
        if len(title) > 100:
            title = title[:97] + "..."

        return WorkItem(
            title=title,
            description=extracted_data["description"].strip(),
            type=item_type,
            priority=priority,
            labels=labels,
            source_system="github",
            metadata={"original_prompt": original_prompt, "extraction_method": "llm"},
        )

    def _fallback_extraction(
        self, prompt: str, project_context: Optional[Dict[str, Any]] = None
    ) -> WorkItem:
        """Fallback extraction when LLM fails - basic heuristics"""

        # Simple heuristics for type detection
        prompt_lower = prompt.lower()
        if any(
            word in prompt_lower for word in ["bug", "crash", "error", "broken", "fail"]
        ):
            item_type = "bug"
            labels = ["bug"]
        elif any(word in prompt_lower for word in ["feature", "add", "new", "enhance"]):
            item_type = "feature"
            labels = ["enhancement"]
        else:
            item_type = "task"
            labels = ["task"]

        # Priority detection
        if any(
            word in prompt_lower
            for word in ["urgent", "critical", "production", "down"]
        ):
            priority = "critical"
            labels.append("priority-high")
        elif any(word in prompt_lower for word in ["minor", "small", "typo"]):
            priority = "low"
            labels.append("priority-low")
        else:
            priority = "medium"
            labels.append("priority-medium")

        # Generate basic title
        title = prompt.strip()
        if len(title) > 100:
            title = title[:97] + "..."

        # Generate basic description
        description = f"""## Description
{prompt}

## Additional Context
This issue was created from a natural language request.

## Next Steps
- [ ] Review and refine the description
- [ ] Add specific steps to reproduce (if applicable)
- [ ] Assign appropriate labels and priority
- [ ] Add any additional context or requirements"""

        return WorkItem(
            title=title,
            description=description,
            type=item_type,
            priority=priority,
            labels=labels,
            source_system="github",
            metadata={"original_prompt": prompt, "extraction_method": "fallback"},
        )

"""
Summary Parser Service - JSON Mode Implementation
Converts JSON responses from LLMs into structured domain models
"""

import json
import logging
from typing import Any, Dict, List

from services.domain.models import DocumentSummary, SummarySection

logger = logging.getLogger(__name__)


class SummaryParser:
    """
    Parser service that converts JSON responses to DocumentSummary objects
    Single responsibility: JSON → Domain Model
    """

    def parse_json(self, json_response: str) -> DocumentSummary:
        """
        Parse JSON string into DocumentSummary object

        Args:
            json_response: JSON string from LLM

        Returns:
            DocumentSummary: Parsed domain object
        """
        try:
            # Strip whitespace and handle potential formatting issues
            cleaned_response = json_response.strip()
            data = json.loads(cleaned_response)
            return self._parse_data(data)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.error(f"Response was: {repr(json_response[:200])}")
            return self._create_error_summary(f"JSON parsing failed: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error parsing summary: {e}")
            return self._create_error_summary(f"Parsing error: {str(e)}")

    def _parse_data(self, data: Dict[str, Any]) -> DocumentSummary:
        """Parse validated JSON data into DocumentSummary"""

        # Extract required fields with defaults
        title = data.get("title", "Untitled Document")
        document_type = data.get("document_type", "Unknown")

        # Extract optional fields
        key_findings = data.get("key_findings", [])
        if not isinstance(key_findings, list):
            # Handle case where LLM returns a single string instead of array
            if isinstance(key_findings, str):
                logger.info(f"Fixing inline formatting for key_findings: {key_findings[:100]}...")
                key_findings = self._fix_inline_formatting(key_findings)
                logger.info(f"Fixed to {len(key_findings)} items: {key_findings}")
            else:
                key_findings = []

        # Create base summary
        summary = DocumentSummary(
            title=title, document_type=document_type, key_findings=key_findings
        )

        # Parse sections
        sections_data = data.get("sections", [])
        if isinstance(sections_data, list):
            for section_data in sections_data:
                section = self._parse_section(section_data)
                if section:
                    summary.sections.append(section)

        return summary

    def _parse_section(self, section_data: Dict[str, Any]) -> SummarySection:
        """Parse a single section from JSON data"""
        if not isinstance(section_data, dict):
            return None

        heading = section_data.get("heading", "Untitled Section")
        points = section_data.get("points", [])

        # Ensure points is a list, fix inline formatting if needed
        if not isinstance(points, list):
            if isinstance(points, str):
                points = self._fix_inline_formatting(points)
            else:
                points = []

        return SummarySection(heading=heading, points=points)

    def _fix_inline_formatting(self, text: str) -> List[str]:
        """
        Fix LLM-generated text that has lost line breaks and formatting structure.

        Detects patterns like:
        - "• item • another item • third item"
        - "**Topic** details **Another topic** more details"
        - "1. First 2. Second 3. Third"
        - Mixed formatting that should be separate lines

        Returns a list of properly formatted items.
        """
        import re

        # Clean up the text first
        text = text.strip()
        if not text:
            return []

        # Pattern 1: Unicode bullets (•, ●, ◦) followed by content
        if re.search(r"[•●◦]\s*", text):
            items = re.split(r"[•●◦]\s*", text)
            return [item.strip() for item in items if item.strip()]

        # Pattern 2: ASCII bullets/dashes with content
        if re.search(r"(?:^|\s)[-*+]\s+", text):
            items = re.split(r"(?:^|\s)[-*+]\s+", text)
            return [item.strip() for item in items if item.strip()]

        # Pattern 3: Numbered lists (1. 2. 3. or 1) 2) 3))
        if re.search(r"(?:^|\s)\d+[.)]\s+", text):
            items = re.split(r"(?:^|\s)\d+[.)]\s+", text)
            return [item.strip() for item in items if item.strip()]

        # Pattern 4: Bold headings inline (**Topic** content **Another** more)
        if re.search(r"\*\*[^*]+\*\*", text):
            # Split on bold patterns but preserve the bold text at the start of each chunk
            parts = re.split(r"(\*\*[^*]+\*\*)", text)
            items = []
            current_item = ""

            for part in parts:
                if part.strip():
                    if re.match(r"\*\*[^*]+\*\*", part):
                        # This is a bold heading - start a new item
                        if current_item.strip():
                            items.append(current_item.strip())
                        current_item = part
                    else:
                        # This is content - add to current item
                        current_item += part

            # Add the final item
            if current_item.strip():
                items.append(current_item.strip())

            return items

        # Pattern 5: Look for repeated patterns that suggest list items
        # This catches cases like "First thing Second thing Third thing"
        # where semantic boundaries exist but formatting is lost
        if len(text.split()) > 10:  # Only for longer text
            # Look for capitalized words that might be start of new items
            potential_items = re.split(r"(?<=[.!?])\s+(?=[A-Z])", text)
            if len(potential_items) > 1:
                return [item.strip() for item in potential_items if item.strip()]

        # Fallback: treat as single item
        return [text]

    def _create_error_summary(self, error_message: str) -> DocumentSummary:
        """Create an error summary for parsing failures"""
        return DocumentSummary(
            title="Parsing Error", document_type="Error", key_findings=[error_message]
        )

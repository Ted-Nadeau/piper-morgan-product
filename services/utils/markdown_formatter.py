"""
Markdown formatting utilities for summaries and key findings
Domain service for ensuring LLM output follows CommonMark standards
"""

import logging
import re
from typing import List

logger = logging.getLogger(__name__)


def format_summary_as_markdown(summary: str) -> str:
    """
    Ensure summary is properly formatted as markdown.
    If it's already formatted, return as-is. Otherwise, add basic formatting.
    """
    if not summary:
        return summary

    # Check if it already has markdown formatting
    if has_markdown_formatting(summary):
        return summary.strip()

    # Add basic markdown formatting to plain text
    lines = summary.strip().split("\n")
    formatted_lines = []

    for line in lines:
        line = line.strip()
        if not line:
            formatted_lines.append("")
            continue

        # If line looks like a title/header (short, no punctuation at end)
        if len(line) < 80 and not line.endswith((".", ":", "!", "?")):
            formatted_lines.append(f"## {line}")
        else:
            formatted_lines.append(line)

    return "\n".join(formatted_lines)


def format_key_findings_as_markdown(findings: List[str]) -> str:
    """
    Format key findings as a markdown bullet list.
    """
    if not findings:
        return ""

    # If findings is a single string, split by newlines
    if isinstance(findings, str):
        findings = [f.strip() for f in findings.split("\n") if f.strip()]

    # Check if already formatted as markdown
    if all(f.startswith(("- ", "* ", "+ ")) for f in findings if f):
        return "\n".join(findings)

    # Format as markdown bullet points
    formatted_findings = []
    for finding in findings:
        if not finding:
            continue

        # Remove existing bullet points if any
        finding = re.sub(r"^[•\-\*\+]\s*", "", finding)

        # Add markdown bullet point
        formatted_findings.append(f"- {finding}")

    return "\n".join(formatted_findings)


def has_markdown_formatting(text: str) -> bool:
    """
    Check if text already has markdown formatting.
    """
    markdown_patterns = [
        r"^#{1,6}\s",  # Headers
        r"^\s*[-\*\+]\s",  # Bullet points
        r"^\s*\d+\.\s",  # Numbered lists
        r"\*\*[^*]+\*\*",  # Bold
        r"\*[^*]+\*",  # Italic
        r"`[^`]+`",  # Inline code
        r"^```",  # Code blocks
        r"^\|.*\|",  # Tables
    ]

    for pattern in markdown_patterns:
        if re.search(pattern, text, re.MULTILINE):
            return True

    return False


def clean_markdown_response(response: str) -> str:
    """
    Clean up markdown response from LLM to ensure proper formatting.
    """
    if not response:
        return response

    # Remove excessive newlines
    response = re.sub(r"\n{3,}", "\n\n", response)

    # Ensure proper spacing around headers
    response = re.sub(r"([^\n])\n(#{1,6}\s)", r"\1\n\n\2", response)
    response = re.sub(r"(#{1,6}[^\n]*)\n([^\n#])", r"\1\n\n\2", response)

    # Ensure proper spacing around code blocks
    response = re.sub(r"([^\n])\n(```)", r"\1\n\n\2", response)
    response = re.sub(r"(```[^\n]*)\n([^\n`])", r"\1\n\n\2", response)

    return response.strip()


class MarkdownFormatter:
    """Domain service responsible for ensuring markdown output follows CommonMark standards"""

    @staticmethod
    def ensure_standard_format(markdown_text: str) -> str:
        """
        Ensure LLM-generated markdown follows CommonMark standards

        This is a domain service that enforces business rules about
        how markdown should be formatted in our system.

        Args:
            markdown_text: Raw markdown text from LLM

        Returns:
            Cleaned markdown text following CommonMark standards
        """
        if not markdown_text:
            return ""

        cleaned = markdown_text

        # Failsafe: Remove global emphasis if the entire summary is wrapped in asterisks or underscores
        # This can happen if the LLM returns *summary* or _summary_ (undesired)
        # Only strip if the whole string is wrapped, not for inline emphasis
        if re.match(r"^(\*|_)([^\n]+)\1$", cleaned.strip()):
            cleaned = re.sub(r"^(\*|_)([^\n]+)\1$", r"\2", cleaned.strip())

        # Domain rule: Use standard bullet syntax (fix "• -" to "-")
        cleaned = re.sub(r"^• - ", "- ", cleaned, flags=re.MULTILINE)

        # Domain rule: Ensure proper header spacing
        cleaned = re.sub(r"^(#{1,6})([^\s#])", r"\1 \2", cleaned, flags=re.MULTILINE)

        # Domain rule: Fix broken bold formatting (unclosed ** tags)
        cleaned = re.sub(r"\*\*([^*]+)\*([^*]*)\*\*", r"**\1\2**", cleaned)

        # Domain rule: Clean up multiple spaces in headers
        cleaned = re.sub(r"^(#{1,6})\s+", r"\1 ", cleaned, flags=re.MULTILINE)

        return cleaned

    @staticmethod
    def validate_markdown_syntax(markdown_text: str) -> List[str]:
        """
        Validate markdown syntax and return list of issues found
        Used for monitoring LLM output quality

        Args:
            markdown_text: Markdown text to validate

        Returns:
            List of validation issues found
        """
        issues = []

        # Check for non-standard bullet syntax
        if re.search(r"^• - ", markdown_text, re.MULTILINE):
            issues.append("Non-standard bullet syntax: '• -' found")

        # Check for malformed headers
        if re.search(r"^#{1,6}[^\s#]", markdown_text, re.MULTILINE):
            issues.append("Malformed headers: missing space after #")

        # Check for unclosed bold formatting
        if re.search(r"\*\*[^*]+\*[^*]*\*\*", markdown_text):
            issues.append("Potentially malformed bold formatting detected")

        return issues

    @staticmethod
    def clean_and_validate(markdown_text: str) -> tuple[str, List[str]]:
        """
        Clean markdown and return both cleaned text and validation issues

        Args:
            markdown_text: Raw markdown text

        Returns:
            Tuple of (cleaned_text, list_of_issues)
        """
        logger.info(
            f"MARKDOWN DEBUG - Input text (first 500 chars): {markdown_text[:500]}"
        )

        issues = MarkdownFormatter.validate_markdown_syntax(markdown_text)
        cleaned = MarkdownFormatter.ensure_standard_format(markdown_text)

        logger.info(f"MARKDOWN DEBUG - Issues found: {issues}")
        logger.info(f"MARKDOWN DEBUG - Cleaned text (first 500 chars): {cleaned[:500]}")

        if issues:
            logger.info(f"Markdown formatting issues detected and fixed: {issues}")

        return cleaned, issues

"""
Markdown to Notion block converter with MVP scope.
Handles headers, paragraphs, simple lists with warnings for unsupported elements.
"""

import re
from typing import Any, Dict, List


def parse_inline_formatting(text: str) -> List[Dict[str, Any]]:
    """
    Parse inline markdown formatting and convert to Notion rich_text format.

    Currently supports:
    - **bold** → bold annotation

    Args:
        text: Raw text content

    Returns:
        List of rich_text objects with annotations
    """
    if not text:
        return [{"type": "text", "text": {"content": ""}}]

    # Pattern to match **bold** text
    bold_pattern = r"\*\*(.*?)\*\*"

    rich_text_parts = []
    last_end = 0

    # Find all bold matches
    for match in re.finditer(bold_pattern, text):
        # Add text before the bold section
        if match.start() > last_end:
            normal_text = text[last_end : match.start()]
            if normal_text:
                rich_text_parts.append({"type": "text", "text": {"content": normal_text}})

        # Add bold text
        bold_content = match.group(1)
        if bold_content:
            rich_text_parts.append(
                {"type": "text", "text": {"content": bold_content}, "annotations": {"bold": True}}
            )

        last_end = match.end()

    # Add remaining text after last match
    if last_end < len(text):
        remaining_text = text[last_end:]
        if remaining_text:
            rich_text_parts.append({"type": "text", "text": {"content": remaining_text}})

    # If no formatting found, return simple text
    if not rich_text_parts:
        return [{"type": "text", "text": {"content": text}}]

    return rich_text_parts


def convert_markdown_to_notion_blocks(markdown_content: str) -> Dict[str, Any]:
    """
    Convert markdown to Notion blocks with MVP scope and warnings.

    Supported elements:
    - Headers (h1, h2, h3)
    - Paragraphs with inline bold formatting
    - Bullet lists (* or -)

    Unsupported elements generate warnings and convert to plain text.
    """
    blocks = []
    warnings = []
    lines = markdown_content.split("\n")

    for line_num, line in enumerate(lines, 1):
        # Skip empty lines
        if not line.strip():
            continue

        # Headers (MVP: h1-h3 only)
        if line.startswith("### "):
            content = line[4:].strip()
            rich_text = parse_inline_formatting(content)
            blocks.append(
                {
                    "type": "heading_3",
                    "heading_3": {"rich_text": rich_text},
                }
            )
        elif line.startswith("## "):
            content = line[3:].strip()
            rich_text = parse_inline_formatting(content)
            blocks.append(
                {
                    "type": "heading_2",
                    "heading_2": {"rich_text": rich_text},
                }
            )
        elif line.startswith("# "):
            content = line[2:].strip()
            rich_text = parse_inline_formatting(content)
            blocks.append(
                {
                    "type": "heading_1",
                    "heading_1": {"rich_text": rich_text},
                }
            )
        # Tables (convert to plain text with warning)
        elif line.startswith("|"):
            warnings.append(f"Line {line_num}: Table converted to plain text")
            rich_text = parse_inline_formatting(line)
            blocks.append(
                {
                    "type": "paragraph",
                    "paragraph": {"rich_text": rich_text},
                }
            )
        # Simple bullet lists
        elif line.startswith("* ") or line.startswith("- "):
            content = line[2:].strip()
            rich_text = parse_inline_formatting(content)
            blocks.append(
                {
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {"rich_text": rich_text},
                }
            )
        # Regular paragraphs
        else:
            rich_text = parse_inline_formatting(line)
            blocks.append(
                {
                    "type": "paragraph",
                    "paragraph": {"rich_text": rich_text},
                }
            )

    return {"blocks": blocks, "warnings": warnings, "success": True}

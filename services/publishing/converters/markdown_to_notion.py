"""
Markdown to Notion block converter with MVP scope.
Handles headers, paragraphs, simple lists with warnings for unsupported elements.
"""

import re
from typing import Any, Dict, List

# Placeholder for code blocks to protect them during other parsing steps
code_placeholder = "§CODE§"


def parse_inline_formatting(text: str) -> List[Dict[str, Any]]:
    """
    Parse markdown inline formatting with defensive validation.
    Philosophy: Only parse COMPLETE, VALID markdown patterns.

    Currently supports:
    - **bold** → bold annotation (only if complete)
    - *italic* and _italic_ → italic annotation (only if complete)
    - `code` → code annotation (only if complete)
    - [text](https://url) → link with url (only if complete and valid URL)
    - ~~strikethrough~~ → strikethrough annotation (only if complete)

    Args:
        text: Raw text content

    Returns:
        List of rich_text objects with annotations
    """
    if not text:
        return [{"type": "text", "text": {"content": ""}}]

    # Step 1: Protect code blocks (they're sacred - no parsing inside)
    code_blocks = []

    def protect_code(match):
        code_blocks.append(match.group(1))
        return f"{code_placeholder}{len(code_blocks)-1}§"

    text = re.sub(r"`([^`]+)`", protect_code, text)

    # Step 2: Only match COMPLETE links with validation
    # Complete link pattern: [text](url) where url is valid
    link_pattern = r"\[([^\[\]]+)\]\((https?://[^\)]+)\)"

    parts = []
    last_end = 0

    for match in re.finditer(link_pattern, text):
        # Add text before link
        if match.start() > last_end:
            before_text = text[last_end : match.start()]
            parts.extend(parse_basic_formatting(before_text))

        # Add the link
        link_text = match.group(1)
        link_url = match.group(2)
        parts.append({"type": "text", "text": {"content": link_text, "link": {"url": link_url}}})

        last_end = match.end()

    # Add remaining text
    if last_end < len(text):
        remaining = text[last_end:]
        parts.extend(parse_basic_formatting(remaining))

    # Step 3: Restore code blocks
    result = []
    for part in parts:
        content = part.get("text", {}).get("content", "")
        if code_placeholder in content:
            # Restore code blocks
            restored_content = restore_code_blocks(content, code_blocks)
            part["text"]["content"] = restored_content
            # Mark as code if it was originally code
            if "`" in restored_content:
                part["annotations"] = {"code": True}
        result.append(part)

    return result


def restore_code_blocks(text: str, code_blocks: List[str]) -> str:
    """
    Restore code blocks from placeholders.

    Args:
        text: Text with code placeholders
        code_blocks: List of original code content

    Returns:
        Text with code blocks restored
    """
    for i, code_content in enumerate(code_blocks):
        placeholder = f"{code_placeholder}{i}§"
        text = text.replace(placeholder, f"`{code_content}`")
    return text


def parse_basic_formatting(text: str) -> List[Dict[str, Any]]:
    """
    Parse bold, italic, strikethrough - but ONLY complete patterns.
    Incomplete patterns are treated as literal text.

    Args:
        text: Text to parse for basic formatting

    Returns:
        List of rich_text objects with annotations
    """
    if not text:
        return [{"type": "text", "text": {"content": ""}}]

    # Only match COMPLETE patterns - count delimiters
    result = []

    # Process strikethrough first (~~text~~)
    if "~~" in text and text.count("~~") >= 2:
        result = parse_strikethrough(text)
    # Process bold (**text** or ***text***)
    elif "**" in text and text.count("**") >= 2:
        result = parse_bold(text)
    # Process italic (*text* or _text_)
    elif "*" in text and text.count("*") >= 2:
        result = parse_italic(text)
    # Process underscore italic (_text_)
    elif "_" in text and text.count("_") >= 2:
        result = parse_underscore_italic(text)
    else:
        # No complete formatting found - return as plain text
        result = [{"type": "text", "text": {"content": text}}]

    return result


def parse_strikethrough(text: str) -> List[Dict[str, Any]]:
    """
    Parse strikethrough formatting - only complete patterns.

    Args:
        text: Text to parse

    Returns:
        List of rich_text objects with strikethrough annotations
    """
    # Only process if we have complete strikethrough pairs
    if text.count("~~") < 2:
        return [{"type": "text", "text": {"content": text}}]

    # Find complete strikethrough pairs
    parts = []
    last_end = 0

    # Use non-greedy matching to find complete pairs
    for match in re.finditer(r"~~([^~]+)~~", text):
        # Add text before strikethrough
        if match.start() > last_end:
            before_text = text[last_end : match.start()]
            if before_text:
                parts.append({"type": "text", "text": {"content": before_text}})

        # Add strikethrough text
        strike_content = match.group(1)
        parts.append(
            {
                "type": "text",
                "text": {"content": strike_content},
                "annotations": {"strikethrough": True},
            }
        )

        last_end = match.end()

    # Add remaining text
    if last_end < len(text):
        remaining = text[last_end:]
        if remaining:
            parts.append({"type": "text", "text": {"content": remaining}})

    return parts if parts else [{"type": "text", "text": {"content": text}}]


def parse_bold(text: str) -> List[Dict[str, Any]]:
    """
    Parse bold formatting - only complete patterns.

    Args:
        text: Text to parse

    Returns:
        List of rich_text objects with bold annotations
    """
    # Only process if we have complete bold pairs
    if text.count("**") < 2:
        return [{"type": "text", "text": {"content": text}}]

    parts = []
    last_end = 0

    # Find complete bold pairs, handling both **text** and ***text***
    for match in re.finditer(r"\*\*\*([^*]+)\*\*\*|\*\*([^*]+)\*\*", text):
        # Add text before bold
        if match.start() > last_end:
            before_text = text[last_end : match.start()]
            if before_text:
                parts.append({"type": "text", "text": {"content": before_text}})

        # Add bold text
        bold_content = match.group(1) or match.group(2)
        is_bold_italic = match.group(0).startswith("***")

        annotations = {"bold": True}
        if is_bold_italic:
            annotations["italic"] = True

        parts.append(
            {"type": "text", "text": {"content": bold_content}, "annotations": annotations}
        )

        last_end = match.end()

    # Add remaining text
    if last_end < len(text):
        remaining = text[last_end:]
        if remaining:
            parts.append({"type": "text", "text": {"content": remaining}})

    return parts if parts else [{"type": "text", "text": {"content": text}}]


def parse_italic(text: str) -> List[Dict[str, Any]]:
    """
    Parse italic formatting with asterisks - only complete patterns.

    Args:
        text: Text to parse

    Returns:
        List of rich_text objects with italic annotations
    """
    # Only process if we have complete italic pairs
    if text.count("*") < 2:
        return [{"type": "text", "text": {"content": text}}]

    parts = []
    last_end = 0

    # Find complete italic pairs, but avoid bold patterns
    for match in re.finditer(r"(?<!\*)\*([^*]+)\*(?!\*)", text):
        # Add text before italic
        if match.start() > last_end:
            before_text = text[last_end : match.start()]
            if before_text:
                parts.append({"type": "text", "text": {"content": before_text}})

        # Add italic text
        italic_content = match.group(1)
        parts.append(
            {"type": "text", "text": {"content": italic_content}, "annotations": {"italic": True}}
        )

        last_end = match.end()

    # Add remaining text
    if last_end < len(text):
        remaining = text[last_end:]
        if remaining:
            parts.append({"type": "text", "text": {"content": remaining}})

    return parts if parts else [{"type": "text", "text": {"content": text}}]


def parse_underscore_italic(text: str) -> List[Dict[str, Any]]:
    """
    Parse italic formatting with underscores - only complete patterns.

    Args:
        text: Text to parse

    Returns:
        List of rich_text objects with italic annotations
    """
    # Only process if we have complete italic pairs
    if text.count("_") < 2:
        return [{"type": "text", "text": {"content": text}}]

    parts = []
    last_end = 0

    # Find complete italic pairs with underscores
    for match in re.finditer(r"_([^_]+)_", text):
        # Add text before italic
        if match.start() > last_end:
            before_text = text[last_end : match.start()]
            if before_text:
                parts.append({"type": "text", "text": {"content": before_text}})

        # Add italic text
        italic_content = match.group(1)
        parts.append(
            {"type": "text", "text": {"content": italic_content}, "annotations": {"italic": True}}
        )

        last_end = match.end()

    # Add remaining text
    if last_end < len(text):
        remaining = text[last_end:]
        if remaining:
            parts.append({"type": "text", "text": {"content": remaining}})

    return parts if parts else [{"type": "text", "text": {"content": text}}]


def convert_markdown_to_notion_blocks(markdown_content: str) -> Dict[str, Any]:
    """
    Convert markdown to Notion blocks with MVP scope and warnings.

    Supported elements:
    - Headers (h1, h2, h3)
    - Code blocks (```language)
    - Paragraphs with inline formatting (bold, italic, code, links, strikethrough)
    - Bullet lists (* or -) with full formatting support

    Unsupported elements generate warnings and convert to plain text.
    """
    blocks = []
    warnings = []
    lines = markdown_content.split("\n")

    i = 0
    while i < len(lines):
        line = lines[i]
        line_num = i + 1

        # Skip empty lines
        if not line.strip():
            i += 1
            continue

        # Detect code blocks BEFORE converting to paragraphs
        if line.startswith("```"):
            # Start of code block - collect all content until closing ```
            language = line[3:].strip() or "plain text"
            code_content = []
            i += 1  # Move to next line

            # Collect code content until closing ```
            while i < len(lines) and not lines[i].startswith("```"):
                code_content.append(lines[i])
                i += 1

            # Skip the closing ```
            if i < len(lines):
                i += 1

            # Create code block
            blocks.append(
                {
                    "type": "code",
                    "code": {
                        "rich_text": [{"text": {"content": "\n".join(code_content)}}],
                        "language": language,
                    },
                }
            )
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

        i += 1

    return {"blocks": blocks, "warnings": warnings, "success": True}

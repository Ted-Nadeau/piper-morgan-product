"""
Prompt templates for various LLM tasks
"""

from .summarization import (
    DOCUMENT_SUMMARY_PROMPT,
    KEY_FINDINGS_PROMPT,
    TEXT_FILE_SUMMARY_PROMPT,
    get_json_summary_prompt,
    get_key_findings_prompt,
    get_summary_prompt,
)

__all__ = [
    "get_summary_prompt",
    "get_key_findings_prompt",
    "get_json_summary_prompt",
    "DOCUMENT_SUMMARY_PROMPT",
    "TEXT_FILE_SUMMARY_PROMPT",
    "KEY_FINDINGS_PROMPT",
]

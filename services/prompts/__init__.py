"""
Prompt templates for various LLM tasks
"""

from .summarization import (
    get_summary_prompt,
    get_key_findings_prompt,
    DOCUMENT_SUMMARY_PROMPT,
    TEXT_FILE_SUMMARY_PROMPT,
    KEY_FINDINGS_PROMPT
)

__all__ = [
    'get_summary_prompt',
    'get_key_findings_prompt',
    'DOCUMENT_SUMMARY_PROMPT',
    'TEXT_FILE_SUMMARY_PROMPT',
    'KEY_FINDINGS_PROMPT'
]
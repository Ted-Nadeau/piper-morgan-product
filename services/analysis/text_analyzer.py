from services.analysis.base_analyzer import BaseAnalyzer
from services.domain.models import AnalysisResult, AnalysisType
from services.shared_types import TaskType
from services.prompts import get_summary_prompt, get_key_findings_prompt
from services.utils.markdown_formatter import clean_markdown_response, MarkdownFormatter, format_key_findings_as_markdown
from datetime import datetime
import re
import structlog
import os

class TextAnalyzer(BaseAnalyzer):
    def __init__(self, llm_client=None):
        self.llm_client = llm_client

    async def analyze(self, file_path: str, **kwargs) -> AnalysisResult:
        encoding = 'utf-8'
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                text = f.read()
        except UnicodeDecodeError:
            encoding = 'latin-1'
            with open(file_path, 'r', encoding=encoding) as f:
                text = f.read()

        # Handle empty file robustly
        if not text.strip():
            line_count = 0
            word_count = 0
            char_count = 0
            is_markdown = file_path.lower().endswith('.md')
            header_count = 0
            code_block_count = 0
            list_item_count = 0
            summary = "Empty text file."
            key_findings = []
        else:
            lines = text.splitlines()
            line_count = len(lines)
            word_count = len(text.split())
            char_count = len(text)
            is_markdown = file_path.lower().endswith('.md') or (
                '#' in text or '```' in text or '-' in text
            )
            header_count = 0
            code_block_count = 0
            list_item_count = 0
            in_code_block = False
            for line in lines:
                # Header: starts with one or more # followed by space
                if re.match(r'^#+\s', line):
                    header_count += 1
                # Code block: lines with only ```
                if line.strip().startswith('```'):
                    in_code_block = not in_code_block
                    if in_code_block:
                        code_block_count += 1
                # List item: starts with -, *, or digit(s).
                if re.match(r'^\s*([-*]|\d+\.)\s', line):
                    list_item_count += 1
            # --- LLM Summarization ---
            logger = structlog.get_logger()
            if self.llm_client is not None:
                try:
                    # Get file extension for appropriate prompt
                    file_ext = os.path.splitext(file_path)[1][1:] if '.' in file_path else None
                    
                    summary_prompt = get_summary_prompt(file_ext)
                    summary_raw = await self.llm_client.complete(
                        task_type=TaskType.SUMMARIZE.value,
                        prompt=summary_prompt.format(content=text[:3000])
                    )
                    # Apply domain formatting rules only
                    summary, formatting_issues = MarkdownFormatter.clean_and_validate(summary_raw)
                    # Skip additional processing - let marked.js handle it
                    
                    key_findings_prompt = get_key_findings_prompt()
                    key_findings_raw = await self.llm_client.complete(
                        task_type=TaskType.SUMMARIZE.value,
                        prompt=key_findings_prompt.format(content=text[:3000])
                    )
                    # Apply domain formatting rules only
                    key_findings_cleaned, _ = MarkdownFormatter.clean_and_validate(key_findings_raw)
                    # Skip additional processing - let marked.js handle it
                    key_findings_text = key_findings_cleaned
                    key_findings = [k.strip() for k in key_findings_text.split('\n') if k.strip()]
                except Exception as e:
                    logger.error(f"LLM analysis failed: {e}")
                    summary = f"Summary generation failed. File contains {len(text)} characters."
                    key_findings = []
            else:
                summary = f"Text file with {line_count} lines, {word_count} words, {char_count} characters."
                key_findings = []

        metadata = {
            'line_count': line_count,
            'word_count': word_count,
            'char_count': char_count,
            'is_markdown': is_markdown,
            'encoding': encoding,
            'header_count': header_count,
            'code_block_count': code_block_count,
            'list_item_count': list_item_count
        }

        return AnalysisResult(
            file_id=file_path,
            analysis_type=AnalysisType.TEXT,
            summary=summary,
            key_findings=key_findings,
            metadata=metadata,
            recommendations=[],
            generated_at=datetime.now(),
            filename=file_path
        ) 
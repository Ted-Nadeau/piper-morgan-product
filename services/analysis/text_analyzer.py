import os
import re
from datetime import datetime

import structlog

from services.analysis.base_analyzer import BaseAnalyzer
from services.analysis.summary_parser import SummaryParser
from services.domain.models import AnalysisResult, AnalysisType
from services.prompts import get_json_summary_prompt
from services.shared_types import TaskType


class TextAnalyzer(BaseAnalyzer):
    def __init__(self, llm_client=None):
        self.llm_client = llm_client
        self.summary_parser = SummaryParser()

    async def analyze(self, file_path: str, **kwargs) -> AnalysisResult:
        encoding = "utf-8"
        try:
            with open(file_path, "r", encoding=encoding) as f:
                text = f.read()
        except UnicodeDecodeError:
            encoding = "latin-1"
            with open(file_path, "r", encoding=encoding) as f:
                text = f.read()

        # Handle empty file robustly
        if not text.strip():
            line_count = 0
            word_count = 0
            char_count = 0
            is_markdown = file_path.lower().endswith(".md")
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
            is_markdown = file_path.lower().endswith(".md") or (
                "#" in text or "```" in text or "-" in text
            )
            header_count = 0
            code_block_count = 0
            list_item_count = 0
            in_code_block = False
            for line in lines:
                # Header: starts with one or more # followed by space
                if re.match(r"^#+\s", line):
                    header_count += 1
                # Code block: lines with only ```
                if line.strip().startswith("```"):
                    in_code_block = not in_code_block
                    if in_code_block:
                        code_block_count += 1
                # List item: starts with -, *, or digit(s).
                if re.match(r"^\s*([-*]|\d+\.)\s", line):
                    list_item_count += 1
            # --- LLM Summarization with JSON Mode ---
            logger = structlog.get_logger()
            if self.llm_client is not None:
                try:
                    # Use JSON mode for structured output
                    json_prompt = get_json_summary_prompt()
                    formatted_prompt = json_prompt.format(content=text[:3000])

                    json_response = await self.llm_client.complete(
                        task_type=TaskType.SUMMARIZE.value,
                        prompt=formatted_prompt,
                        response_format={"type": "json_object"},
                    )

                    # Parse JSON into domain model
                    document_summary = self.summary_parser.parse_json(json_response)

                    # Generate clean markdown from domain model
                    summary = document_summary.to_markdown()
                    key_findings = document_summary.key_findings

                except Exception as e:
                    logger.error(f"LLM analysis failed: {e}")
                    summary = f"Summary generation failed. File contains {len(text)} characters."
                    key_findings = []
            else:
                summary = f"Text file with {line_count} lines, {word_count} words, {char_count} characters."
                key_findings = []

        metadata = {
            "line_count": line_count,
            "word_count": word_count,
            "char_count": char_count,
            "is_markdown": is_markdown,
            "encoding": encoding,
            "header_count": header_count,
            "code_block_count": code_block_count,
            "list_item_count": list_item_count,
        }

        return AnalysisResult(
            file_id=file_path,
            analysis_type=AnalysisType.TEXT,
            summary=summary,
            key_findings=key_findings,
            metadata=metadata,
            recommendations=[],
            generated_at=datetime.now(),
            filename=file_path,
        )

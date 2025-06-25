from services.analysis.base_analyzer import BaseAnalyzer
from services.domain.models import AnalysisResult, AnalysisType
from datetime import datetime
import os
import re

class TextAnalyzer(BaseAnalyzer):
    def analyze(self, file_path):
        # Try to detect encoding (UTF-8, fallback to latin-1)
        encoding = 'utf-8'
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                text = f.read()
        except UnicodeDecodeError:
            encoding = 'latin-1'
            with open(file_path, 'r', encoding=encoding) as f:
                text = f.read()
        # Handle empty file
        if not text.strip():
            line_count = 0
            word_count = 0
            char_count = 0
            is_markdown = file_path.lower().endswith('.md')
            header_count = 0
            code_block_count = 0
            list_item_count = 0
        else:
            lines = text.splitlines()
            line_count = len(lines)
            word_count = len(text.split())
            char_count = len(text)
            is_markdown = file_path.lower().endswith('.md')
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
        return AnalysisResult(
            file_id=file_path,
            analysis_type=AnalysisType.TEXT,
            summary=f"Text file with {line_count} lines, {word_count} words, {char_count} characters.",
            key_findings=[],
            metadata={
                'line_count': line_count,
                'word_count': word_count,
                'char_count': char_count,
                'is_markdown': is_markdown,
                'encoding': encoding,
                'header_count': header_count,
                'code_block_count': code_block_count,
                'list_count': list_item_count
            },
            recommendations=[],
            generated_at=datetime.now(),
            filename=file_path
        ) 
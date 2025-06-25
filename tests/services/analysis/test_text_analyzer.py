import os
import pytest
from services.analysis.base_analyzer import BaseAnalyzer
from services.domain.models import AnalysisResult

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), '../../fixtures')

class TestTextAnalyzer:
    def setup_method(self):
        from services.analysis.text_analyzer import TextAnalyzer
        self.analyzer = TextAnalyzer()

    def test_basic_text_file_analysis(self):
        """Test line, word, and character count for plain text"""
        txt_path = os.path.join(FIXTURE_DIR, 'sample_text.txt')
        result = self.analyzer.analyze(txt_path)
        assert result.metadata['line_count'] == 15
        assert result.metadata['word_count'] > 10
        assert result.metadata['char_count'] > 30

    def test_markdown_structure_detection(self):
        """Test detection of headers, code blocks, and lists in markdown"""
        md_path = os.path.join(FIXTURE_DIR, 'sample_markdown.md')
        result = self.analyzer.analyze(md_path)
        assert result.metadata['is_markdown'] is True
        assert result.metadata['header_count'] >= 2
        assert result.metadata['code_block_count'] >= 1
        assert result.metadata['list_count'] >= 1

    def test_plain_text_vs_markdown(self):
        """Test differentiation between plain text and markdown"""
        txt_path = os.path.join(FIXTURE_DIR, 'sample_text.txt')
        md_path = os.path.join(FIXTURE_DIR, 'sample_markdown.md')
        result_txt = self.analyzer.analyze(txt_path)
        result_md = self.analyzer.analyze(md_path)
        assert result_txt.metadata['is_markdown'] is False
        assert result_md.metadata['is_markdown'] is True

    def test_empty_file_handling(self):
        """Test that empty text file returns zero counts and no error"""
        empty_path = os.path.join(FIXTURE_DIR, 'empty_text.txt')
        result = self.analyzer.analyze(empty_path)
        assert result.metadata['line_count'] == 0
        assert result.metadata['word_count'] == 0
        assert result.metadata['char_count'] == 0

    def test_large_text_file_handling(self):
        """Test that large text file (1000+ lines) is handled efficiently"""
        large_path = os.path.join(FIXTURE_DIR, 'large_text.txt')
        result = self.analyzer.analyze(large_path)
        assert result.metadata['line_count'] >= 1000
        assert result.metadata['word_count'] > 1000

    def test_inherits_from_base_analyzer(self):
        from services.analysis.text_analyzer import TextAnalyzer
        assert issubclass(TextAnalyzer, BaseAnalyzer)

    def test_analyze_returns_analysis_result(self):
        txt_path = os.path.join(FIXTURE_DIR, 'sample_text.txt')
        result = self.analyzer.analyze(txt_path)
        assert isinstance(result, AnalysisResult)

    def test_encoding_detection(self):
        """Test that encoding is detected and reported in metadata"""
        txt_path = os.path.join(FIXTURE_DIR, 'sample_text.txt')
        result = self.analyzer.analyze(txt_path)
        assert result.metadata['encoding'] in ('utf-8', 'ascii') 
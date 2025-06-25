import os
import pytest
from services.analysis.base_analyzer import BaseAnalyzer
from services.domain.models import AnalysisResult

FIXTURE_DIR = 'tests/fixtures/'

@pytest.mark.asyncio
async def test_basic_text_file_analysis():
    from services.analysis.text_analyzer import TextAnalyzer
    analyzer = TextAnalyzer()
    result = await analyzer.analyze(os.path.join(FIXTURE_DIR, 'sample_text.txt'))
    assert result.metadata['line_count'] > 0
    assert result.metadata['word_count'] > 0
    assert result.metadata['char_count'] > 0

@pytest.mark.asyncio
async def test_markdown_structure_detection():
    from services.analysis.text_analyzer import TextAnalyzer
    analyzer = TextAnalyzer()
    result = await analyzer.analyze(os.path.join(FIXTURE_DIR, 'sample_markdown.md'))
    assert result.metadata['is_markdown'] is True
    assert result.metadata['header_count'] > 0
    assert result.metadata['code_block_count'] > 0
    assert result.metadata['list_item_count'] > 0

@pytest.mark.asyncio
async def test_plain_text_vs_markdown():
    from services.analysis.text_analyzer import TextAnalyzer
    analyzer = TextAnalyzer()
    result_txt = await analyzer.analyze(os.path.join(FIXTURE_DIR, 'sample_text.txt'))
    result_md = await analyzer.analyze(os.path.join(FIXTURE_DIR, 'sample_markdown.md'))
    assert result_txt.metadata['is_markdown'] is False
    assert result_md.metadata['is_markdown'] is True

@pytest.mark.asyncio
async def test_empty_file_handling():
    from services.analysis.text_analyzer import TextAnalyzer
    analyzer = TextAnalyzer()
    result = await analyzer.analyze(os.path.join(FIXTURE_DIR, 'empty_text.txt'))
    assert result.metadata['line_count'] == 0
    assert result.metadata['word_count'] == 0
    assert result.metadata['char_count'] == 0

@pytest.mark.asyncio
async def test_large_text_file_handling():
    from services.analysis.text_analyzer import TextAnalyzer
    analyzer = TextAnalyzer()
    result = await analyzer.analyze(os.path.join(FIXTURE_DIR, 'large_text.txt'))
    assert result.metadata['line_count'] >= 1000
    assert result.metadata['word_count'] > 0
    assert result.metadata['char_count'] > 0

@pytest.mark.asyncio
async def test_inherits_from_base_analyzer():
    from services.analysis.text_analyzer import TextAnalyzer
    assert issubclass(TextAnalyzer, BaseAnalyzer)

@pytest.mark.asyncio
async def test_analyze_returns_analysis_result():
    from services.analysis.text_analyzer import TextAnalyzer
    analyzer = TextAnalyzer()
    result = await analyzer.analyze(os.path.join(FIXTURE_DIR, 'sample_text.txt'))
    assert isinstance(result, AnalysisResult)

@pytest.mark.asyncio
async def test_encoding_detection():
    from services.analysis.text_analyzer import TextAnalyzer
    analyzer = TextAnalyzer()
    result = await analyzer.analyze(os.path.join(FIXTURE_DIR, 'sample_text.txt'))
    assert 'encoding' in result.metadata
    assert result.metadata['encoding'] in ['utf-8', 'ascii'] 
import os

import pytest

from services.analysis.base_analyzer import BaseAnalyzer
from services.domain.models import AnalysisResult

FIXTURE_DIR = "tests/fixtures/"


@pytest.mark.asyncio
async def test_basic_text_file_analysis():
    from services.analysis.text_analyzer import TextAnalyzer

    analyzer = TextAnalyzer()
    result = await analyzer.analyze(os.path.join(FIXTURE_DIR, "sample_text.txt"))
    assert result.metadata["line_count"] > 0
    assert result.metadata["word_count"] > 0
    assert result.metadata["char_count"] > 0


@pytest.mark.asyncio
async def test_markdown_structure_detection():
    from services.analysis.text_analyzer import TextAnalyzer

    analyzer = TextAnalyzer()
    result = await analyzer.analyze(os.path.join(FIXTURE_DIR, "sample_markdown.md"))
    assert result.metadata["is_markdown"] is True
    assert result.metadata["header_count"] > 0
    assert result.metadata["code_block_count"] > 0
    assert result.metadata["list_item_count"] > 0


@pytest.mark.asyncio
async def test_plain_text_vs_markdown():
    from services.analysis.text_analyzer import TextAnalyzer

    analyzer = TextAnalyzer()
    result_txt = await analyzer.analyze(os.path.join(FIXTURE_DIR, "sample_text.txt"))
    result_md = await analyzer.analyze(os.path.join(FIXTURE_DIR, "sample_markdown.md"))
    assert result_txt.metadata["is_markdown"] is False
    assert result_md.metadata["is_markdown"] is True


@pytest.mark.asyncio
async def test_empty_file_handling():
    from services.analysis.text_analyzer import TextAnalyzer

    analyzer = TextAnalyzer()
    result = await analyzer.analyze(os.path.join(FIXTURE_DIR, "empty_text.txt"))
    assert result.metadata["line_count"] == 0
    assert result.metadata["word_count"] == 0
    assert result.metadata["char_count"] == 0


@pytest.mark.asyncio
async def test_large_text_file_handling():
    from services.analysis.text_analyzer import TextAnalyzer

    analyzer = TextAnalyzer()
    result = await analyzer.analyze(os.path.join(FIXTURE_DIR, "large_text.txt"))
    assert result.metadata["line_count"] >= 1000
    assert result.metadata["word_count"] > 0
    assert result.metadata["char_count"] > 0


@pytest.mark.asyncio
async def test_inherits_from_base_analyzer():
    from services.analysis.text_analyzer import TextAnalyzer

    assert issubclass(TextAnalyzer, BaseAnalyzer)


@pytest.mark.asyncio
async def test_analyze_returns_analysis_result():
    from services.analysis.text_analyzer import TextAnalyzer

    analyzer = TextAnalyzer()
    result = await analyzer.analyze(os.path.join(FIXTURE_DIR, "sample_text.txt"))
    assert isinstance(result, AnalysisResult)


@pytest.mark.asyncio
async def test_encoding_detection():
    from services.analysis.text_analyzer import TextAnalyzer

    analyzer = TextAnalyzer()
    result = await analyzer.analyze(os.path.join(FIXTURE_DIR, "sample_text.txt"))
    assert "encoding" in result.metadata
    assert result.metadata["encoding"] in ["utf-8", "ascii"]


@pytest.mark.asyncio
async def test_llm_integration_with_summarize_task_type():
    from unittest.mock import AsyncMock, Mock

    from services.analysis.text_analyzer import TextAnalyzer
    from services.shared_types import TaskType

    # Mock LLM client with JSON response
    mock_llm_client = Mock()
    mock_llm_client.complete = AsyncMock(
        return_value='{"title": "Test Document", "document_type": "text", "key_findings": ["Key finding 1", "Key finding 2"], "sections": [{"heading": "Main Section", "points": ["Point 1", "Point 2"]}]}'
    )

    analyzer = TextAnalyzer(llm_client=mock_llm_client)
    result = await analyzer.analyze(os.path.join(FIXTURE_DIR, "sample_text.txt"))

    # Verify LLM client was called once with correct TaskType
    assert mock_llm_client.complete.call_count == 1
    call = mock_llm_client.complete.call_args_list[0]

    # Check that call used TaskType.SUMMARIZE
    assert call[1]["task_type"] == TaskType.SUMMARIZE.value

    # Check that JSON prompt was used with response_format
    assert "JSON format" in call[1]["prompt"]
    assert call[1]["response_format"] == {"type": "json_object"}

    # Check that summary was generated from JSON response
    assert "Test Document" in result.summary
    assert result.key_findings == ["Key finding 1", "Key finding 2"]


@pytest.mark.asyncio
async def test_llm_integration_with_different_file_types():
    from unittest.mock import AsyncMock, Mock

    from services.analysis.text_analyzer import TextAnalyzer
    from services.shared_types import TaskType

    # Mock LLM client with JSON response
    mock_llm_client = Mock()
    mock_llm_client.complete = AsyncMock(
        return_value='{"title": "Markdown Document", "document_type": "markdown", "key_findings": ["Finding 1"], "sections": [{"heading": "Section", "points": ["Point 1"]}]}'
    )

    analyzer = TextAnalyzer(llm_client=mock_llm_client)

    # Test with markdown file
    result = await analyzer.analyze(os.path.join(FIXTURE_DIR, "sample_markdown.md"))

    # Verify JSON prompt was used (implementation uses JSON mode for all file types)
    calls = mock_llm_client.complete.call_args_list
    assert "JSON format" in calls[0][1]["prompt"]
    assert calls[0][1]["response_format"] == {"type": "json_object"}

    # Check that markdown content was generated from JSON
    assert "Markdown Document" in result.summary


@pytest.mark.asyncio
async def test_llm_markdown_formatting():
    from unittest.mock import AsyncMock, Mock

    from services.analysis.text_analyzer import TextAnalyzer
    from services.shared_types import TaskType

    # Mock LLM client with JSON response containing markdown elements
    mock_llm_client = Mock()
    mock_llm_client.complete = AsyncMock(
        return_value='{"title": "Formatted Document", "document_type": "text", "key_findings": ["**Key finding 1**: Important insight", "**Key finding 2**: Another insight", "**Key finding 3**: Third insight"], "sections": [{"heading": "Summary", "points": ["This is a **formatted** summary with:", "- Bullet points", "- *Italic* text", "- Code: `example`"]}]}'
    )

    analyzer = TextAnalyzer(llm_client=mock_llm_client)
    result = await analyzer.analyze(os.path.join(FIXTURE_DIR, "sample_text.txt"))

    # Verify markdown formatting is preserved in generated summary
    assert "# Formatted Document" in result.summary  # Generated title header
    assert "**formatted**" in result.summary
    assert "- Bullet points" in result.summary
    assert "`example`" in result.summary

    # Verify key findings are extracted correctly with markdown
    assert "**Key finding 1**: Important insight" in result.key_findings
    assert "**Key finding 2**: Another insight" in result.key_findings
    assert "**Key finding 3**: Third insight" in result.key_findings

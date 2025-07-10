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

    # Mock LLM client
    mock_llm_client = Mock()
    mock_llm_client.complete = AsyncMock(
        side_effect=["This is a test summary", "• Key finding 1\n• Key finding 2"]
    )

    analyzer = TextAnalyzer(llm_client=mock_llm_client)
    result = await analyzer.analyze(os.path.join(FIXTURE_DIR, "sample_text.txt"))

    # Verify LLM client was called with correct TaskType
    assert mock_llm_client.complete.call_count == 2
    calls = mock_llm_client.complete.call_args_list

    # Check that both calls used TaskType.SUMMARIZE
    assert calls[0][1]["task_type"] == TaskType.SUMMARIZE.value
    assert calls[1][1]["task_type"] == TaskType.SUMMARIZE.value

    # Check that prompts were used correctly
    assert "content" in calls[0][1]["prompt"]
    assert "content" in calls[1][1]["prompt"]

    # Check that summary was updated from LLM
    assert result.summary == "This is a test summary"


@pytest.mark.asyncio
async def test_llm_integration_with_different_file_types():
    from unittest.mock import AsyncMock, Mock

    from services.analysis.text_analyzer import TextAnalyzer
    from services.shared_types import TaskType

    # Mock LLM client
    mock_llm_client = Mock()
    mock_llm_client.complete = AsyncMock(return_value="File type specific summary")

    analyzer = TextAnalyzer(llm_client=mock_llm_client)

    # Test with markdown file
    result = await analyzer.analyze(os.path.join(FIXTURE_DIR, "sample_markdown.md"))

    # Verify correct prompt was used for markdown
    calls = mock_llm_client.complete.call_args_list
    # Should use TEXT_FILE_SUMMARY_PROMPT for .md files
    assert "text file" in calls[0][1]["prompt"].lower()

    assert result.summary == "File type specific summary"


@pytest.mark.asyncio
async def test_llm_markdown_formatting():
    from unittest.mock import AsyncMock, Mock

    from services.analysis.text_analyzer import TextAnalyzer
    from services.shared_types import TaskType

    # Mock LLM client with markdown responses
    mock_llm_client = Mock()
    mock_llm_client.complete = AsyncMock(
        side_effect=[
            "# Summary\n\nThis is a **formatted** summary with:\n\n- Bullet points\n- *Italic* text\n- Code: `example`",
            "- **Key finding 1**: Important insight\n- **Key finding 2**: Another insight\n- **Key finding 3**: Third insight",
        ]
    )

    analyzer = TextAnalyzer(llm_client=mock_llm_client)
    result = await analyzer.analyze(os.path.join(FIXTURE_DIR, "sample_text.txt"))

    # Verify markdown formatting is preserved
    assert "# Summary" in result.summary
    assert "**formatted**" in result.summary
    assert "- Bullet points" in result.summary
    assert "`example`" in result.summary

    # Verify key findings are formatted as markdown
    assert any("**Key finding 1**" in finding for finding in result.key_findings)
    assert any("**Key finding 2**" in finding for finding in result.key_findings)

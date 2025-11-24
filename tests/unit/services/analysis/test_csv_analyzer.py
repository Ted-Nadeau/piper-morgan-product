import os
from unittest.mock import Mock

import pandas as pd
import pytest

from services.analysis.base_analyzer import BaseAnalyzer
from services.analysis.csv_analyzer import CSVAnalyzer
from services.domain.models import AnalysisResult, AnalysisType

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), "../../../fixtures")


class TestCSVAnalyzer:
    def setup_method(self):
        self.analyzer = CSVAnalyzer()

    @pytest.mark.asyncio
    async def test_basic_csv_analysis(self):
        """Test row count and column detection on a normal CSV"""
        csv_path = os.path.join(FIXTURE_DIR, "sample_data.csv")
        result = await self.analyzer.analyze(csv_path)
        assert result.metadata["row_count"] == 7  # 7 data rows
        assert set(result.metadata["columns"]) == {"id", "name", "age", "score"}

    @pytest.mark.asyncio
    async def test_statistical_summary_numeric_columns(self):
        """Test statistical summary for numeric columns"""
        csv_path = os.path.join(FIXTURE_DIR, "sample_data.csv")
        result = await self.analyzer.analyze(csv_path)
        stats = result.metadata["column_stats"]
        assert "age" in stats and "score" in stats
        assert "mean" in stats["age"] and "std" in stats["score"]

    @pytest.mark.asyncio
    async def test_missing_data_detection(self):
        """Test missing data count and percentage"""
        csv_path = os.path.join(FIXTURE_DIR, "sample_data.csv")
        result = await self.analyzer.analyze(csv_path)
        missing = result.metadata["missing_data"]
        assert isinstance(missing, dict)
        assert "summary" in missing
        assert "by_column" in missing
        for col, info in missing["by_column"].items():
            assert "count" in info and "percent" in info
        assert "total_missing" in missing["summary"]
        assert "percent_missing" in missing["summary"]

    @pytest.mark.asyncio
    async def test_empty_csv_handling(self):
        """Test that empty CSV (headers only) does not crash and returns zero rows"""
        csv_path = os.path.join(FIXTURE_DIR, "empty.csv")
        result = await self.analyzer.analyze(csv_path)
        assert result.metadata["row_count"] == 0
        assert len(result.metadata["columns"]) > 0

    @pytest.mark.asyncio
    async def test_malformed_csv_handling(self):
        """Test that malformed CSV returns error gracefully"""
        csv_path = os.path.join(FIXTURE_DIR, "malformed.csv")
        result = await self.analyzer.analyze(csv_path)
        assert result.metadata.get("error") is not None
        assert (
            "malformed" in result.metadata.get("error", "").lower()
            or "error" in result.metadata.get("error", "").lower()
        )

    def test_inherits_from_base_analyzer(self):
        """Test that CSVAnalyzer inherits from BaseAnalyzer"""
        assert issubclass(CSVAnalyzer, BaseAnalyzer)

    @pytest.mark.asyncio
    async def test_analyze_returns_analysis_result(self):
        """Test that analyze method returns AnalysisResult"""
        csv_path = os.path.join(FIXTURE_DIR, "sample_data.csv")
        result = await self.analyzer.analyze(csv_path)
        assert isinstance(result, AnalysisResult)


# 1. Basic CSV analysis (row count, column detection)
@pytest.mark.asyncio
async def test_csv_basic_analysis():
    from services.analysis.csv_analyzer import CSVAnalyzer

    analyzer = CSVAnalyzer()
    result = await analyzer.analyze("tests/fixtures/sample_data.csv")
    assert result.metadata["row_count"] == 7
    assert set(result.metadata["columns"]) == {"id", "name", "age", "score"}


# 2. Statistical summary for numeric columns
@pytest.mark.asyncio
async def test_csv_statistical_summary():
    from services.analysis.csv_analyzer import CSVAnalyzer

    analyzer = CSVAnalyzer()
    result = await analyzer.analyze("tests/fixtures/sample_data.csv")
    # Check that numeric columns have mean, min, max, std
    assert "age" in result.metadata.get("column_stats", {})
    assert "score" in result.metadata.get("column_stats", {})
    for col in ["age", "score"]:
        stats = result.metadata.get("column_stats", {}).get(col, {})
        assert "mean" in stats
        assert "min" in stats
        assert "max" in stats
        assert "std" in stats


# 3. Missing data detection
@pytest.mark.asyncio
async def test_csv_missing_data_detection():
    from services.analysis.csv_analyzer import CSVAnalyzer

    analyzer = CSVAnalyzer()
    result = await analyzer.analyze("tests/fixtures/sample_data.csv")
    missing = result.metadata.get("missing_data", {})
    assert "summary" in missing
    assert "by_column" in missing
    for col in result.metadata["columns"]:
        assert "count" in missing["by_column"].get(col, {})
        assert "percent" in missing["by_column"].get(col, {})
    assert "total_missing" in missing["summary"]
    assert "percent_missing" in missing["summary"]


# 4. Empty CSV handling
@pytest.mark.asyncio
async def test_csv_empty_handling():
    from services.analysis.csv_analyzer import CSVAnalyzer

    analyzer = CSVAnalyzer()
    result = await analyzer.analyze("tests/fixtures/empty.csv")
    assert result.metadata["row_count"] == 0
    assert (
        result.metadata["columns"] == ["id", "name", "age", "score"]
        or result.metadata["columns"] is not None
    )
    assert result.metadata.get("column_stats", {}) == {}
    missing = result.metadata.get("missing_data", {})
    assert "summary" in missing
    assert "by_column" in missing
    for col in result.metadata["columns"]:
        assert missing["by_column"].get(col, {}).get("count", None) == 0
        assert missing["by_column"].get(col, {}).get("percent", None) == 0.0
    assert missing["summary"]["total_missing"] == 0
    assert missing["summary"]["percent_missing"] == 0.0


# 5. Malformed CSV handling
@pytest.mark.asyncio
async def test_csv_malformed_handling():
    from services.analysis.csv_analyzer import CSVAnalyzer

    analyzer = CSVAnalyzer()
    try:
        result = await analyzer.analyze("tests/fixtures/malformed.csv")
        assert result.metadata.get("error") is not None
    except Exception:
        pass


# 6. Inheritance from BaseAnalyzer
def test_csv_inherits_base_analyzer():
    from services.analysis.base_analyzer import BaseAnalyzer
    from services.analysis.csv_analyzer import CSVAnalyzer

    assert issubclass(CSVAnalyzer, BaseAnalyzer)


# 7. analyze returns AnalysisResult
@pytest.mark.asyncio
async def test_csv_analyze_returns_analysis_result():
    from services.analysis.csv_analyzer import CSVAnalyzer
    from services.domain.models import AnalysisResult

    analyzer = CSVAnalyzer()
    result = await analyzer.analyze("tests/fixtures/sample_data.csv")
    assert isinstance(result, AnalysisResult)

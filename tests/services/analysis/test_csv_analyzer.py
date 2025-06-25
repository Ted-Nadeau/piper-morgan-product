import os
import pytest
import pandas as pd
from services.analysis.csv_analyzer import CSVAnalyzer
from services.analysis.base_analyzer import BaseAnalyzer
from services.domain.models import AnalysisResult

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), '../../fixtures')

class TestCSVAnalyzer:
    def setup_method(self):
        self.analyzer = CSVAnalyzer()

    def test_basic_csv_analysis(self):
        """Test row count and column detection on a normal CSV"""
        csv_path = os.path.join(FIXTURE_DIR, 'sample_data.csv')
        result = self.analyzer.analyze(csv_path)
        assert result.metadata['row_count'] == 8  # 8 data rows
        assert set(result.metadata['columns']) == {'id', 'name', 'age', 'score', 'active'}

    def test_statistical_summary_numeric_columns(self):
        """Test statistical summary for numeric columns"""
        csv_path = os.path.join(FIXTURE_DIR, 'sample_data.csv')
        result = self.analyzer.analyze(csv_path)
        stats = result.metadata['column_stats']
        assert 'age' in stats and 'score' in stats
        assert 'mean' in stats['age'] and 'std' in stats['score']

    def test_missing_data_detection(self):
        """Test missing data count and percentage"""
        csv_path = os.path.join(FIXTURE_DIR, 'sample_data.csv')
        result = self.analyzer.analyze(csv_path)
        missing = result.metadata['missing_data']
        assert isinstance(missing, dict)
        for col, info in missing.items():
            assert 'count' in info and 'percent' in info

    def test_empty_csv_handling(self):
        """Test that empty CSV (headers only) does not crash and returns zero rows"""
        csv_path = os.path.join(FIXTURE_DIR, 'empty.csv')
        result = self.analyzer.analyze(csv_path)
        assert result.metadata['row_count'] == 0
        assert len(result.metadata['columns']) > 0

    def test_malformed_csv_handling(self):
        """Test that malformed CSV returns error gracefully"""
        csv_path = os.path.join(FIXTURE_DIR, 'malformed.csv')
        result = self.analyzer.analyze(csv_path)
        assert result.metadata.get('error') is not None
        assert 'malformed' in result.metadata.get('error', '').lower() or 'error' in result.metadata.get('error', '').lower()

    def test_inherits_from_base_analyzer(self):
        """Test that CSVAnalyzer inherits from BaseAnalyzer"""
        assert issubclass(CSVAnalyzer, BaseAnalyzer)

    def test_analyze_returns_analysis_result(self):
        """Test that analyze method returns AnalysisResult"""
        csv_path = os.path.join(FIXTURE_DIR, 'sample_data.csv')
        result = self.analyzer.analyze(csv_path)
        assert isinstance(result, AnalysisResult) 
from unittest.mock import Mock
from services.domain.models import AnalysisType

class UnsupportedAnalysisTypeError(Exception):
    pass

class AnalyzerFactory:
    def __init__(self, llm_client=None):
        self.llm_client = llm_client
        self.analyzer_registry = {
            AnalysisType.DATA: Mock,  # Placeholder for CSVAnalyzer
            AnalysisType.DOCUMENT: Mock,  # Placeholder for DocumentAnalyzer
            AnalysisType.TEXT: Mock,  # Placeholder for TextAnalyzer
        }

    def create_analyzer(self, analysis_type):
        if analysis_type == AnalysisType.DOCUMENT:
            # Pass llm_client to DocumentAnalyzer mock
            return self.analyzer_registry[analysis_type](llm_client=self.llm_client)
        if analysis_type in self.analyzer_registry:
            return self.analyzer_registry[analysis_type]()
        raise UnsupportedAnalysisTypeError(f"Unsupported analysis type: {analysis_type}") 
from services.analysis.csv_analyzer import CSVAnalyzer
from services.analysis.document_analyzer import DocumentAnalyzer
from services.analysis.text_analyzer import TextAnalyzer
from services.domain.models import AnalysisType


class UnsupportedAnalysisTypeError(Exception):
    pass


class AnalyzerFactory:
    def __init__(self, llm_client=None):
        self.llm_client = llm_client
        self.analyzer_registry = {
            AnalysisType.DATA: CSVAnalyzer,
            AnalysisType.DOCUMENT: DocumentAnalyzer,
            AnalysisType.TEXT: TextAnalyzer,
        }

    def create_analyzer(self, analysis_type):
        if analysis_type in [AnalysisType.DOCUMENT, AnalysisType.TEXT]:
            # Pass llm_client to DocumentAnalyzer and TextAnalyzer
            return self.analyzer_registry[analysis_type](llm_client=self.llm_client)
        if analysis_type in self.analyzer_registry:
            return self.analyzer_registry[analysis_type]()
        raise UnsupportedAnalysisTypeError(
            f"Unsupported analysis type: {analysis_type}"
        )

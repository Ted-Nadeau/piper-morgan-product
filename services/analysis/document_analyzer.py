import PyPDF2
from datetime import datetime
from services.analysis.base_analyzer import BaseAnalyzer
from services.domain.models import AnalysisResult, AnalysisType

class DocumentAnalyzer(BaseAnalyzer):
    def __init__(self, llm_client=None):
        self.llm_client = llm_client

    async def analyze(self, file_path: str, **kwargs) -> AnalysisResult:
        """Analyze document file using LLM.
        
        Args:
            file_path: Path to the document
            **kwargs: Additional optional parameters (not used currently)
        """
        try:
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                page_count = len(reader.pages)
                text = ''
                for page in reader.pages:
                    text += page.extract_text() or ''
            metadata = {
                'page_count': page_count,
                'text': text
            }
            # Empty PDF: summary should be empty string if no text and at least one page
            if not text and page_count > 0:
                summary = ''
                metadata['summary'] = summary
                metadata['key_points'] = []
            elif text:
                # Use LLM for summary and key points if available
                if self.llm_client is not None:
                    summary = self.llm_client.summarize(text)
                    key_points = self.llm_client.extract_key_points(text)
                    metadata['summary'] = summary
                    metadata['key_points'] = key_points
                else:
                    summary = f"PDF with {page_count} pages and {len(text)} characters of text."
                    metadata['summary'] = summary
                    metadata['key_points'] = []
            else:
                summary = f"PDF with {page_count} pages and {len(text)} characters of text."
                metadata['summary'] = summary
                metadata['key_points'] = []
            # TODO: Move key_points to the top-level key_findings field in AnalysisResult to match the domain model.
            # For now, key_points are kept in metadata for backward compatibility.
            return AnalysisResult(
                file_id=file_path,
                analysis_type=AnalysisType.DOCUMENT,
                summary=summary,
                key_findings=[],
                recommendations=[],
                generated_at=datetime.now(),
                metadata=metadata
            )
        except PyPDF2.errors.PdfReadError:
            return AnalysisResult(
                file_id=file_path,
                analysis_type=AnalysisType.DOCUMENT,
                summary="Unable to analyze PDF document",
                key_findings=["PDF file could not be read - file may be corrupted"],
                metadata={'error': 'Unable to read PDF file - file may be corrupted'},
                recommendations=["Verify the PDF file is not corrupted", "Try re-saving or re-exporting the PDF"],
                generated_at=datetime.now()
            ) 
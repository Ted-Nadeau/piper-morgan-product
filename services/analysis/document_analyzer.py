from services.analysis.base_analyzer import BaseAnalyzer
from services.domain.models import AnalysisResult, AnalysisType
import PyPDF2
from datetime import datetime

class DocumentAnalyzer(BaseAnalyzer):
    def __init__(self, llm_client):
        self.llm_client = llm_client

    def analyze(self, file_path):
        try:
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                page_count = len(reader.pages)
                page_texts = []
                for page in reader.pages:
                    text = page.extract_text() or ""
                    page_texts.append(text)
                extracted_text = "\n".join(page_texts).strip()
                has_text = bool(extracted_text)
                # Empty PDF: summary should be empty string if no text and at least one page
                if not extracted_text and page_count > 0:
                    summary = ""
                    key_points = []
                else:
                    summary = f"PDF file with {page_count} pages and {len(extracted_text)} characters of text."
                    key_points = []
                    # LLM summary and key points extraction (only if text and llm_client is set)
                    if has_text and self.llm_client is not None:
                        if hasattr(self.llm_client, 'summarize'):
                            summary = self.llm_client.summarize(extracted_text)
                        if hasattr(self.llm_client, 'extract_key_points'):
                            key_points = self.llm_client.extract_key_points(extracted_text)
                return AnalysisResult(
                    file_id=file_path,
                    analysis_type=AnalysisType.DOCUMENT,
                    summary=summary,
                    key_findings=[],
                    metadata={
                        'page_count': page_count,
                        'text': extracted_text,
                        'text_length': len(extracted_text),
                        'has_text': has_text,
                        'summary': summary,
                        'key_points': key_points
                    },
                    recommendations=[],
                    generated_at=datetime.now(),
                    filename=file_path
                )
        except PyPDF2.errors.PdfReadError as e:
            return AnalysisResult(
                file_id=file_path,
                analysis_type=AnalysisType.DOCUMENT,
                summary="Unable to read PDF file - file may be corrupted",
                key_findings=[],
                metadata={
                    'error': 'corrupted',
                    'error_details': str(e)
                },
                recommendations=[],
                generated_at=datetime.now(),
                filename=file_path
            ) 
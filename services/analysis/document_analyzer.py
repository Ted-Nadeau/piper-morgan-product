import PyPDF2
from datetime import datetime
from services.analysis.base_analyzer import BaseAnalyzer
from services.domain.models import AnalysisResult, AnalysisType
from services.shared_types import TaskType
from services.prompts import get_summary_prompt, get_key_findings_prompt
from services.utils.markdown_formatter import clean_markdown_response, format_key_findings_as_markdown, MarkdownFormatter

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
                import structlog
                logger = structlog.get_logger()
                if self.llm_client is not None:
                    try:
                        summary_prompt = get_summary_prompt('pdf')
                        summary_raw = await self.llm_client.complete(
                            task_type=TaskType.SUMMARIZE.value,
                            prompt=summary_prompt.format(content=text[:3000])
                        )
                        # Apply domain formatting rules only
                        summary, formatting_issues = MarkdownFormatter.clean_and_validate(summary_raw)
                        # Skip additional processing - let marked.js handle it
                        
                        key_findings_prompt = get_key_findings_prompt()
                        key_findings_raw = await self.llm_client.complete(
                            task_type=TaskType.SUMMARIZE.value,
                            prompt=key_findings_prompt.format(content=text[:3000])
                        )
                        # Apply domain formatting rules only
                        key_findings_cleaned, _ = MarkdownFormatter.clean_and_validate(key_findings_raw)
                        # Skip additional processing - let marked.js handle it
                        key_findings_text = key_findings_cleaned
                        key_points = [k.strip() for k in key_findings_text.split('\n') if k.strip()]
                    except Exception as e:
                        logger.error(f"LLM analysis failed: {e}")
                        summary = f"Summary generation failed. Document contains {len(text)} characters."
                        key_points = []
                else:
                    summary = f"PDF with {page_count} pages and {len(text)} characters of text."
                    key_points = []
                metadata['summary'] = summary
                metadata['key_points'] = key_points
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
                key_findings=key_points,
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
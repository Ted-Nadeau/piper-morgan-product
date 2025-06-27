"""FileAnalyzer orchestrates the file analysis workflow."""

from pathlib import Path
from typing import Any, Dict, Optional

from services.analysis.analyzer_factory import AnalyzerFactory
from services.domain.models import AnalysisResult, AnalysisType
from services.analysis.exceptions import FileValidationError


class FileAnalyzer:
    """Orchestrates file analysis using security validation, type detection, and specific analyzers."""
    
    def __init__(
        self,
        security_validator: Any,
        type_detector: Any,
        content_sampler: Any,
        analyzer_factory: AnalyzerFactory,
        llm_client: Optional[Any] = None
    ):
        """Initialize with required dependencies."""
        self.security_validator = security_validator
        self.type_detector = type_detector
        self.content_sampler = content_sampler
        self.analyzer_factory = analyzer_factory
        self.llm_client = llm_client

    async def analyze_file(self, file_path: str, metadata: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        """Analyze a file through the complete pipeline."""
        # 1. Security validation
        validation_result = self.security_validator.validate(file_path)
        if not validation_result.is_valid:
            raise FileValidationError(getattr(validation_result, 'reason', 'File validation failed'))
        
        # 2. Type detection
        file_type_info = self.type_detector.detect(file_path)
        
        # 3. Convert string to enum (THE KEY CONVERSION)
        analysis_type = AnalysisType(file_type_info.analyzer_type)
        
        # 4. Get appropriate analyzer
        analyzer = self.analyzer_factory.create_analyzer(analysis_type)
        
        # 5. Analyze the file
        if metadata:
            result = await analyzer.analyze(file_path, **metadata)
        else:
            result = await analyzer.analyze(file_path)
        # Enrich result with file metadata for consistency
        result.metadata["file_type"] = file_type_info.mime_type
        result.metadata["extension"] = file_type_info.extension
        return result 
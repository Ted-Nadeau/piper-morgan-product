from abc import ABC, abstractmethod

from services.domain.models import AnalysisResult


class BaseAnalyzer(ABC):
    @abstractmethod
    async def analyze(self, file_path: str, **kwargs) -> AnalysisResult:
        pass

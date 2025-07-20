import asyncio
import os
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from services.infrastructure.extractors.content_extractors import (
    EXTRACTOR_REGISTRY,
    ExtractionError,
    extract_content,
)
from services.infrastructure.monitoring.mcp_metrics import (
    ContentExtractionMetrics,
    content_extraction_metrics,
)


@dataclass
class ExtractedContent:
    file_path: str
    content: str
    file_type: str
    size_bytes: int
    duration_ms: float
    error: Optional[str] = None
    partial: bool = False


class BatchExtractor:
    """Extract content from multiple files efficiently"""

    def __init__(
        self,
        extractors=EXTRACTOR_REGISTRY,
        metrics: ContentExtractionMetrics = content_extraction_metrics,
    ):
        self.extractors = extractors
        self.metrics = metrics
        self._extraction_cache = {}  # (file_path, mtime) -> ExtractedContent

    async def extract_batch(
        self, file_paths: List[str], max_concurrent: int = 5
    ) -> Dict[str, ExtractedContent]:
        sem = asyncio.Semaphore(max_concurrent)
        results = {}
        tasks = []
        for file_path in file_paths:
            tasks.append(self._extract_with_semaphore(file_path, sem))
        extracted = await asyncio.gather(*tasks)
        for result in extracted:
            results[result.file_path] = result
        return results

    async def _extract_with_semaphore(
        self, file_path: str, sem: asyncio.Semaphore
    ) -> ExtractedContent:
        async with sem:
            return await self._extract_file(file_path)

    async def _extract_file(self, file_path: str) -> ExtractedContent:
        try:
            stat = os.stat(file_path)
            cache_key = (file_path, stat.st_mtime)
            if cache_key in self._extraction_cache:
                self.metrics.record_cache_hit()
                return self._extraction_cache[cache_key]
            self.metrics.record_cache_miss()
            ext = os.path.splitext(file_path)[1].lower()
            start = time.perf_counter()
            content = extract_content(file_path)
            duration_ms = (time.perf_counter() - start) * 1000
            size_bytes = stat.st_size
            await self.metrics.record_extraction(ext, size_bytes, duration_ms)
            result = ExtractedContent(
                file_path=file_path,
                content=content,
                file_type=ext,
                size_bytes=size_bytes,
                duration_ms=duration_ms,
            )
            self._extraction_cache[cache_key] = result
            return result
        except ExtractionError as e:
            await self.metrics.record_extraction_error(ext, type(e).__name__)
            return ExtractionErrorHandler.handle_corrupted_file(file_path, e)
        except Exception as e:
            await self.metrics.record_extraction_error("unknown", type(e).__name__)
            return ExtractionErrorHandler.handle_corrupted_file(file_path, e)

    def clear_cache(self):
        """Clear extraction cache"""
        self._extraction_cache.clear()


class ExtractionErrorHandler:
    """Graceful handling of extraction failures"""

    @staticmethod
    def handle_corrupted_file(file_path: str, error: Exception) -> ExtractedContent:
        return ExtractedContent(
            file_path=file_path,
            content="",
            file_type=os.path.splitext(file_path)[1].lower(),
            size_bytes=0,
            duration_ms=0.0,
            error=str(error),
            partial=False,
        )

    @staticmethod
    def handle_large_file(file_path: str, size_mb: float) -> ExtractedContent:
        # For very large files, extract only first N bytes/pages (placeholder logic)
        try:
            with open(file_path, "rb") as f:
                content = f.read(1024 * 1024)  # 1MB max
            return ExtractedContent(
                file_path=file_path,
                content=content.decode(errors="replace"),
                file_type=os.path.splitext(file_path)[1].lower(),
                size_bytes=len(content),
                duration_ms=0.0,
                error=None,
                partial=True,
            )
        except Exception as e:
            return ExtractionErrorHandler.handle_corrupted_file(file_path, e)


class ContentCache:
    """Simple cache for extracted content"""

    def __init__(self, max_size_mb: int = 100):
        self._cache = {}  # (file_path, mtime) -> ExtractedContent
        self._cache_size = 0
        self._max_size = max_size_mb * 1024 * 1024
        self._lru = []  # LRU order: most recent at end

    def get(self, file_path: str, modified_time: float) -> Optional[ExtractedContent]:
        key = (file_path, modified_time)
        if key in self._cache:
            self._lru.remove(key)
            self._lru.append(key)
            return self._cache[key]
        return None

    def put(self, file_path: str, modified_time: float, content: ExtractedContent):
        key = (file_path, modified_time)
        size = len(content.content.encode("utf-8"))
        while self._cache_size + size > self._max_size and self._lru:
            old_key = self._lru.pop(0)
            old_content = self._cache.pop(old_key)
            self._cache_size -= len(old_content.content.encode("utf-8"))
        self._cache[key] = content
        self._lru.append(key)
        self._cache_size += size

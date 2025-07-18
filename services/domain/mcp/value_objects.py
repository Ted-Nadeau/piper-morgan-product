"""
MCP Domain Value Objects
Pure business objects with no external dependencies.
"""

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class ContentMatch:
    """A match found within content during search."""

    snippet: str
    start_position: int
    end_position: int
    matched_terms: List[str]
    relevance_score: float

    def __post_init__(self):
        """Validate ContentMatch inputs."""
        if self.end_position <= self.start_position:
            raise ValueError("end_position must be greater than start_position")

        if not (0 <= self.relevance_score <= 1):
            raise ValueError("relevance_score must be between 0 and 1")

    @property
    def length(self) -> int:
        """Calculate the length of the match."""
        return self.end_position - self.start_position


@dataclass(frozen=True)
class RelevanceScore:
    """Represents the relevance of content to a search query."""

    value: float
    matched_terms: List[str]
    total_terms: int
    scoring_method: str

    def __post_init__(self):
        """Validate RelevanceScore inputs."""
        if not (0 <= self.value <= 1):
            raise ValueError("Score value must be between 0 and 1")

        if self.total_terms <= 0:
            raise ValueError("total_terms must be positive")

    @property
    def match_ratio(self) -> float:
        """Calculate the ratio of matched terms to total terms."""
        return len(self.matched_terms) / self.total_terms if self.total_terms > 0 else 0.0

    def is_significant(self, threshold: float = 0.3) -> bool:
        """Check if the relevance score meets significance threshold."""
        return self.value >= threshold

    def __lt__(self, other: "RelevanceScore") -> bool:
        """Enable sorting by relevance score."""
        return self.value < other.value

    def __gt__(self, other: "RelevanceScore") -> bool:
        """Enable sorting by relevance score."""
        return self.value > other.value


@dataclass(frozen=True)
class ContentExtract:
    """Extracted text content with metadata."""

    text: str
    file_type: str
    extraction_method: str
    word_count: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        """Validate and auto-calculate fields."""
        if self.text is None:
            raise ValueError("Text cannot be None")

        if self.word_count is not None and self.word_count < 0:
            raise ValueError("word_count cannot be negative")

        # Auto-calculate word count if not provided
        if self.word_count is None:
            # Use object.__setattr__ because dataclass is frozen
            object.__setattr__(self, "word_count", len(self.text.split()) if self.text else 0)

    def is_empty(self) -> bool:
        """Check if the content is empty."""
        return not self.text or self.word_count == 0

    def has_metadata(self) -> bool:
        """Check if metadata is present."""
        return self.metadata is not None and len(self.metadata) > 0


@dataclass(frozen=True)
class SearchQuery:
    """Represents a search query with parameters."""

    text: str
    session_id: str
    search_type: str = "content"
    max_results: int = 10

    def __post_init__(self):
        """Validate SearchQuery inputs."""
        if not self.text or self.text.strip() == "":
            raise ValueError("Query text cannot be empty")

        if self.max_results <= 0:
            raise ValueError("max_results must be positive")

    @property
    def terms(self) -> List[str]:
        """Extract search terms from query text."""
        # Simple word extraction - could be enhanced with NLP
        words = re.findall(r"\b[a-zA-Z0-9]+\b", self.text.lower())
        return words

    def is_valid(self) -> bool:
        """Check if the query is valid for execution."""
        return bool(self.text and self.text.strip() and self.max_results > 0)


@dataclass(frozen=True)
class ContentSearchResult:
    """A search result containing file and content match information."""

    file_id: str
    filename: str
    file_type: str
    relevance_score: RelevanceScore
    content_matches: List[ContentMatch]
    search_source: str  # "content", "filename", "hybrid"

    def __post_init__(self):
        """Validate ContentSearchResult inputs."""
        if not self.file_id:
            raise ValueError("file_id cannot be empty")

    def has_content_matches(self) -> bool:
        """Check if this result has content matches."""
        return len(self.content_matches) > 0

    def __lt__(self, other: "ContentSearchResult") -> bool:
        """Enable sorting by relevance score."""
        return self.relevance_score < other.relevance_score

    def __gt__(self, other: "ContentSearchResult") -> bool:
        """Enable sorting by relevance score."""
        return self.relevance_score > other.relevance_score

"""
Content Extraction Domain Service
Pure business logic for extracting and analyzing content.
"""

import math
import re
from collections import Counter
from typing import Any, Dict, List, Optional

from .value_objects import ContentExtract, ContentMatch, RelevanceScore


class ContentExtractor:
    """Domain service for extracting and analyzing text content."""

    DEFAULT_CONFIG = {
        "max_content_length": 50000,  # 50k characters
        "snippet_length": 200,  # Context snippet length
        "include_metadata": True,
        "min_word_length": 2,
        "max_keywords": 20,
    }

    # Common stop words to exclude from analysis
    STOP_WORDS = {
        "the",
        "and",
        "for",
        "are",
        "but",
        "not",
        "you",
        "all",
        "can",
        "had",
        "her",
        "was",
        "one",
        "our",
        "out",
        "day",
        "get",
        "has",
        "him",
        "his",
        "how",
        "man",
        "new",
        "now",
        "old",
        "see",
        "two",
        "way",
        "who",
        "boy",
        "did",
        "its",
        "let",
        "put",
        "say",
        "she",
        "too",
        "use",
        "with",
        "that",
        "this",
        "have",
        "from",
        "they",
        "know",
        "want",
        "been",
        "good",
        "much",
        "some",
        "time",
        "very",
        "when",
        "come",
        "here",
        "just",
        "like",
        "long",
        "make",
        "many",
        "over",
        "such",
        "take",
        "than",
        "them",
        "well",
        "were",
        "will",
        "your",
        "about",
        "after",
        "before",
        "could",
        "first",
        "would",
        "there",
        "other",
        "more",
        "into",
        "what",
        "only",
        "also",
        "back",
        "then",
        "may",
        "so",
        "up",
        "do",
        "no",
        "if",
        "my",
        "as",
        "of",
        "to",
        "in",
        "is",
        "it",
        "on",
        "be",
        "at",
        "by",
        "he",
        "we",
        "an",
        "or",
    }

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize ContentExtractor with configuration."""
        self.config = {**self.DEFAULT_CONFIG, **(config or {})}

    def extract_text_content(self, content: str, filename: str) -> ContentExtract:
        """Extract text content with metadata and analysis."""
        if content is None:
            raise ValueError("Content cannot be None")

        if not filename or filename.strip() == "":
            raise ValueError("Filename cannot be empty")

        # Determine file type from extension
        file_type = self._determine_file_type(filename)

        # Clean and process content
        processed_content = self._process_content(content)

        # Calculate word count
        word_count = len(processed_content.split()) if processed_content else 0

        # Extract metadata if enabled
        metadata = {}
        if self.config["include_metadata"]:
            metadata = self._extract_metadata(content, filename)

        return ContentExtract(
            text=processed_content,
            file_type=file_type,
            extraction_method="direct",
            word_count=word_count,
            metadata=metadata if metadata else None,
        )

    def calculate_relevance_score(self, content: str, query: str) -> RelevanceScore:
        """Calculate relevance score using TF-IDF-like algorithm."""
        if not query or query.strip() == "":
            raise ValueError("Query cannot be empty")

        # Extract terms from query
        query_terms = self._extract_terms(query)
        if not query_terms:
            return RelevanceScore(
                value=0.0, matched_terms=[], total_terms=1, scoring_method="tf_idf"
            )

        # Extract terms from content
        content_terms = self._extract_terms(content.lower())
        content_term_freq = Counter(content_terms)

        # Find matched terms
        matched_terms = []
        term_scores = []

        for query_term in query_terms:
            query_term_lower = query_term.lower()
            if query_term_lower in content_term_freq:
                matched_terms.append(query_term_lower)

                # Calculate TF score (term frequency)
                tf_score = (
                    content_term_freq[query_term_lower] / len(content_terms) if content_terms else 0
                )

                # Simple relevance scoring (could be enhanced with IDF)
                term_score = min(tf_score * 10, 1.0)  # Scale and cap at 1.0
                term_scores.append(term_score)

        # Calculate overall relevance score
        if not matched_terms:
            relevance_value = 0.0
        else:
            # Average of term scores weighted by match ratio
            avg_score = sum(term_scores) / len(term_scores)
            match_ratio = len(matched_terms) / len(query_terms)

            # Scale score based on how many terms matched
            # Full match gets full avg_score, partial matches get scaled down
            relevance_value = avg_score * match_ratio

            # Add small bonus for having any matches, but cap total
            relevance_value = min(relevance_value + (match_ratio * 0.1), 1.0)

        return RelevanceScore(
            value=relevance_value,
            matched_terms=matched_terms,
            total_terms=len(query_terms),
            scoring_method="tf_idf",
        )

    def find_content_matches(self, content: str, query: str) -> List[ContentMatch]:
        """Find specific matches within content with context."""
        if not content or not query:
            return []

        query_terms = self._extract_terms(query)
        if not query_terms:
            return []

        matches = []
        content_lower = content.lower()
        snippet_length = self.config["snippet_length"]

        # Find matches for each query term
        for term in query_terms:
            term_lower = term.lower()
            start = 0

            while True:
                # Find next occurrence of term
                pos = content_lower.find(term_lower, start)
                if pos == -1:
                    break

                # Calculate snippet boundaries with context
                snippet_start = max(0, pos - snippet_length // 2)
                snippet_end = min(len(content), pos + len(term) + snippet_length // 2)

                # Extract snippet
                snippet = content[snippet_start:snippet_end]

                # Calculate relevance for this match
                match_relevance = self._calculate_match_relevance(snippet, [term])

                match = ContentMatch(
                    snippet=snippet,
                    start_position=pos,
                    end_position=pos + len(term),
                    matched_terms=[term_lower],
                    relevance_score=match_relevance,
                )

                matches.append(match)
                start = pos + 1  # Continue searching after this match

        # Remove duplicate overlapping matches and sort by relevance
        unique_matches = self._deduplicate_matches(matches)
        return sorted(unique_matches, key=lambda m: m.relevance_score, reverse=True)

    def extract_keywords(self, content: str, max_keywords: int = None) -> List[str]:
        """Extract important keywords from content."""
        if not content:
            return []

        max_kw = max_keywords or self.config["max_keywords"]

        # Extract terms and count frequency
        terms = self._extract_terms(content.lower())
        term_freq = Counter(terms)

        # Filter out stop words and short terms
        filtered_terms = {
            term: freq
            for term, freq in term_freq.items()
            if (term not in self.STOP_WORDS and len(term) >= self.config["min_word_length"])
        }

        # Get most frequent terms
        top_terms = sorted(filtered_terms.items(), key=lambda x: x[1], reverse=True)
        return [term for term, freq in top_terms[:max_kw]]

    def _determine_file_type(self, filename: str) -> str:
        """Determine MIME type from filename extension."""
        extension = filename.lower().split(".")[-1] if "." in filename else ""

        type_map = {
            "txt": "text/plain",
            "md": "text/markdown",
            "markdown": "text/markdown",
            "pdf": "application/pdf",
            "doc": "application/msword",
            "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "csv": "text/csv",
            "json": "application/json",
            "xml": "application/xml",
            "html": "text/html",
            "htm": "text/html",
        }

        return type_map.get(extension, "text/plain")

    def _process_content(self, content: str) -> str:
        """Clean and process raw content."""
        if not content:
            return ""

        # Limit content length
        max_length = self.config["max_content_length"]
        if len(content) > max_length:
            content = content[:max_length]

        # Basic cleaning - normalize whitespace
        content = re.sub(r"\s+", " ", content.strip())

        return content

    def _extract_metadata(self, content: str, filename: str) -> Dict[str, Any]:
        """Extract metadata from content and filename."""
        metadata = {
            "filename": filename,
            "content_length": len(content),
            "line_count": content.count("\n") + 1 if content else 0,
            "extraction_timestamp": "auto-generated",  # Would use datetime in real implementation
        }

        # Add file-type specific metadata
        if filename.endswith(".md"):
            # Count markdown headers
            headers = re.findall(r"^#+\s+", content, re.MULTILINE)
            metadata["header_count"] = len(headers)

        return metadata

    def _extract_terms(self, text: str) -> List[str]:
        """Extract meaningful terms from text."""
        if not text:
            return []

        # Extract words (alphanumeric, minimum length)
        words = re.findall(r"\b[a-zA-Z0-9]+\b", text.lower())

        # Filter by minimum length
        min_length = self.config["min_word_length"]
        return [word for word in words if len(word) >= min_length]

    def _calculate_match_relevance(self, snippet: str, terms: List[str]) -> float:
        """Calculate relevance score for a specific match snippet."""
        if not snippet or not terms:
            return 0.0

        snippet_terms = self._extract_terms(snippet.lower())
        snippet_term_freq = Counter(snippet_terms)

        matched_count = sum(1 for term in terms if term.lower() in snippet_term_freq)
        match_ratio = matched_count / len(terms) if terms else 0.0

        # Higher score for exact matches and context
        base_score = match_ratio
        context_bonus = 0.1 if len(snippet_terms) > 5 else 0.0  # Bonus for context

        return min(base_score + context_bonus, 1.0)

    def _deduplicate_matches(self, matches: List[ContentMatch]) -> List[ContentMatch]:
        """Remove overlapping matches, keeping the best ones."""
        if not matches:
            return []

        # Sort by position for easier overlap detection
        sorted_matches = sorted(matches, key=lambda m: m.start_position)
        unique_matches = []

        for match in sorted_matches:
            # Check if this match overlaps with any existing unique match
            overlaps = False
            for existing in unique_matches:
                if (
                    match.start_position < existing.end_position
                    and match.end_position > existing.start_position
                ):
                    # Keep the match with higher relevance
                    if match.relevance_score > existing.relevance_score:
                        unique_matches.remove(existing)
                        unique_matches.append(match)
                    overlaps = True
                    break

            if not overlaps:
                unique_matches.append(match)

        return unique_matches

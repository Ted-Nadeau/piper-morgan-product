"""
Smart content sampling for LLM processing
"""

import re
from typing import List, Tuple

from services.domain.models import ContentSample


class ContentSampler:
    """Samples file content intelligently for LLM processing"""

    def __init__(self, max_sample_size: int = 4000):
        """
        Initialize sampler

        Args:
            max_sample_size: Maximum characters to sample
        """
        self.max_sample_size = max_sample_size

    def sample_content(self, content: str) -> ContentSample:
        """
        Sample content intelligently

        Args:
            content: Full file content

        Returns:
            ContentSample with sampled text and metadata
        """
        if len(content) <= self.max_sample_size:
            return ContentSample(
                text=content, is_truncated=False, original_length=len(content)
            )

        # Sample from beginning and end
        chunk_size = self.max_sample_size // 2 - 50  # Leave room for ellipsis

        # Try to find paragraph boundaries
        beginning = self._get_beginning_chunk(content, chunk_size)
        ending = self._get_ending_chunk(content, chunk_size)

        sampled_text = f"{beginning}\n\n[... content truncated ...]\n\n{ending}"

        return ContentSample(
            text=sampled_text,
            is_truncated=True,
            original_length=len(content),
            sample_ranges=[
                (0, len(beginning)),
                (len(content) - len(ending), len(content)),
            ],
        )

    def _get_beginning_chunk(self, content: str, target_size: int) -> str:
        """
        Get beginning chunk respecting paragraph boundaries

        Args:
            content: Full content
            target_size: Target chunk size

        Returns:
            Beginning chunk
        """
        if len(content) <= target_size:
            return content

        # Find paragraph boundaries
        paragraphs = self._split_paragraphs(content[: target_size + 500])

        chunk = ""
        for para in paragraphs:
            if len(chunk) + len(para) + 2 <= target_size:
                chunk += para + "\n\n"
            else:
                break

        return chunk.rstrip()

    def _get_ending_chunk(self, content: str, target_size: int) -> str:
        """
        Get ending chunk respecting paragraph boundaries

        Args:
            content: Full content
            target_size: Target chunk size

        Returns:
            Ending chunk
        """
        if len(content) <= target_size:
            return content

        # Get content from end
        start_pos = max(0, len(content) - target_size - 500)
        end_content = content[start_pos:]

        # Find paragraph boundaries
        paragraphs = self._split_paragraphs(end_content)

        # Build from end
        chunk = ""
        for para in reversed(paragraphs):
            if len(chunk) + len(para) + 2 <= target_size:
                chunk = para + "\n\n" + chunk
            else:
                break

        return chunk.rstrip()

    def _split_paragraphs(self, text: str) -> List[str]:
        """
        Split text into paragraphs

        Args:
            text: Text to split

        Returns:
            List of paragraphs
        """
        # Split on double newlines or single newlines with enough content
        paragraphs = re.split(r"\n\s*\n", text)

        # Clean up
        return [p.strip() for p in paragraphs if p.strip()]

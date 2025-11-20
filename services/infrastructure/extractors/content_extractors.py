import os
from typing import Any, Dict, Optional


class ExtractionError(Exception):
    """Raised when file extraction fails."""

    pass


class BaseContentExtractor:
    """Base interface for file content extractors."""

    def extract(self, file_path: str) -> str:
        raise NotImplementedError


class TxtContentExtractor(BaseContentExtractor):
    """Extractor for plain text files (.txt)."""

    def extract(self, file_path: str) -> str:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            raise ExtractionError(f"Failed to extract .txt file: {e}")


class MdContentExtractor(BaseContentExtractor):
    """Extractor for markdown files (.md). Strips markdown syntax."""

    def extract(self, file_path: str) -> str:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            return self._strip_markdown(content)
        except Exception as e:
            raise ExtractionError(f"Failed to extract .md file: {e}")

    def _strip_markdown(self, text: str) -> str:
        # Simple markdown stripper (headings, bold, italics, code, links)
        import re

        text = re.sub(r"`{1,3}[^`]+`{1,3}", "", text)  # Remove inline code
        text = re.sub(r"\!\[[^\]]*\]\([^\)]*\)", "", text)  # Remove images
        text = re.sub(r"\[[^\]]*\]\([^\)]*\)", "", text)  # Remove links
        text = re.sub(r"[#*_~>`]", "", text)  # Remove markdown symbols
        text = re.sub(r"\n{2,}", "\n", text)  # Collapse multiple newlines
        return text.strip()


class PdfContentExtractor(BaseContentExtractor):
    """Extractor for PDF files (.pdf) using pypdf."""

    def extract(self, file_path: str) -> str:
        try:
            import pypdf

            with open(file_path, "rb") as f:
                reader = pypdf.PdfReader(f)
                text = []
                for page in reader.pages:
                    try:
                        text.append(page.extract_text() or "")
                    except Exception:
                        text.append("")
                return "\n".join(text).strip()
        except Exception as e:
            raise ExtractionError(f"Failed to extract .pdf file: {e}")


# Registry for extractors by file extension
EXTRACTOR_REGISTRY: Dict[str, BaseContentExtractor] = {
    ".txt": TxtContentExtractor(),
    ".md": MdContentExtractor(),
    ".pdf": PdfContentExtractor(),
}


def extract_content(file_path: str) -> str:
    """
    Extract content from a file using the appropriate extractor.
    Raises ExtractionError on failure.
    """
    ext = os.path.splitext(file_path)[1].lower()
    extractor = EXTRACTOR_REGISTRY.get(ext)
    if not extractor:
        raise ExtractionError(f"No extractor for file type: {ext}")
    return extractor.extract(file_path)

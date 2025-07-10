"""
File Processors for Knowledge Graph Ingestion
"""

import abc
from typing import List

import PyPDF2
import structlog

logger = structlog.get_logger(__name__)


class BaseProcessor(abc.ABC):
    """Abstract base class for document processors."""

    @abc.abstractmethod
    def extract_chunks(self, file_path: str, chunk_size: int = 1000) -> List[str]:
        """Extract text from a file and split it into chunks."""
        raise NotImplementedError


class PDFProcessor(BaseProcessor):
    """Processor for PDF files."""

    def extract_chunks(self, file_path: str, chunk_size: int = 1000) -> List[str]:
        """Extract text from PDF and split into chunks"""
        chunks = []
        try:
            with open(file_path, "rb") as file:
                pdf_reader = PyPDF2.PdfReader(file)

                full_text = ""
                for page in pdf_reader.pages:
                    text = page.extract_text()
                    if text:
                        full_text += text + "\n"

                words = full_text.split()
                chunk_overlap = 200  # words

                for i in range(0, len(words), chunk_size - chunk_overlap):
                    chunk = " ".join(words[i : i + chunk_size])
                    chunks.append(chunk)

        except Exception as e:
            logger.error(f"Error extracting PDF text: {e}", file_path=file_path)
            raise

        return chunks


class TextProcessor(BaseProcessor):
    """Processor for plain text and Markdown files."""

    def extract_chunks(self, file_path: str, chunk_size: int = 1000) -> List[str]:
        """Extract text from a plain text or Markdown file and split into chunks."""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                full_text = file.read()

            words = full_text.split()
            chunk_overlap = 200  # words
            chunks = []
            for i in range(0, len(words), chunk_size - chunk_overlap):
                chunk = " ".join(words[i : i + chunk_size])
                chunks.append(chunk)
            return chunks
        except Exception as e:
            logger.error(
                f"Error extracting text from {file_path}: {e}", file_path=file_path
            )
            raise


class DocxProcessor(BaseProcessor):
    """Processor for DOCX files."""

    def extract_chunks(self, file_path: str, chunk_size: int = 1000) -> List[str]:
        """Extract text from a DOCX file and split into chunks."""
        try:
            import docx

            doc = docx.Document(file_path)
            full_text = "\n".join([para.text for para in doc.paragraphs])

            words = full_text.split()
            chunk_overlap = 200  # words
            chunks = []
            for i in range(0, len(words), chunk_size - chunk_overlap):
                chunk = " ".join(words[i : i + chunk_size])
                chunks.append(chunk)
            return chunks
        except Exception as e:
            logger.error(
                f"Error extracting DOCX text from {file_path}: {e}", file_path=file_path
            )
            raise


class HtmlProcessor(BaseProcessor):
    """Processor for HTML files."""

    def extract_chunks(self, file_path: str, chunk_size: int = 1000) -> List[str]:
        """Extract text from an HTML file, stripping tags, and split into chunks."""
        try:
            from bs4 import BeautifulSoup

            with open(file_path, "r", encoding="utf-8") as file:
                soup = BeautifulSoup(file, "html.parser")

            # Remove script and style elements
            for script_or_style in soup(["script", "style"]):
                script_or_style.decompose()

            full_text = soup.get_text(separator="\n", strip=True)

            words = full_text.split()
            chunk_overlap = 200  # words
            chunks = []
            for i in range(0, len(words), chunk_size - chunk_overlap):
                chunk = " ".join(words[i : i + chunk_size])
                chunks.append(chunk)
            return chunks
        except Exception as e:
            logger.error(
                f"Error extracting HTML text from {file_path}: {e}", file_path=file_path
            )
            raise

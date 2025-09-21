# File Extraction Strategy for Piper Morgan

**Date:** 2025-07-17
**Author:** Cursor Assistant

## Overview

This document summarizes the current state and recommended approach for extracting text content from common file types in the Piper Morgan project, based on codebase analysis and available libraries.

---

## 1. .txt Files

- **Extraction Method:**
  - Use standard Python file I/O: `with open(path, 'r', encoding='utf-8') as f: content = f.read()`
  - No special libraries required.
- **Integration Points:**
  - `get_file_content` in `services/mcp/resources.py`
  - `read_file_contents` in `services/queries/file_queries.py`
- **Notes:**
  - Ensure UTF-8 encoding for cross-platform compatibility.
  - Handle large files with chunked reading if needed.

---

## 2. .md Files (Markdown)

- **Extraction Method:**
  - Use standard file I/O to read raw markdown text.
  - For plain text extraction (removing markdown syntax), use `markdown-it-py` to parse and render as plain text, or use a markdown-to-text utility.
- **Available Library:**
  - `markdown-it-py==3.0.0` (in requirements.txt)
- **Integration Points:**
  - Same as .txt files, with optional post-processing to strip markdown.
- **Recommendation:**
  - If business logic requires only the text content, implement a utility to convert markdown to plain text using `markdown-it-py` or a similar tool.

---

## 3. .pdf Files

- **Extraction Method:**
  - Use `PyPDF2` to extract text from PDF files:
    ```python
    from PyPDF2 import PdfReader
    reader = PdfReader(path)
    text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
    ```
- **Available Library:**
  - `PyPDF2==3.0.1` (in requirements.txt)
- **Integration Points:**
  - No direct PDF extraction logic found in current services; recommend adding a utility function or service for PDF extraction.
- **Recommendation:**
  - Implement a `extract_pdf_text(path)` utility using `PyPDF2`.
  - Handle exceptions for encrypted or malformed PDFs.

---

## 4. Other File Types (Future)

- **DOCX:** `python-docx` is present in some archived requirements, but not in main requirements.txt. Add if DOCX support is needed.
- **Images/Other:** Not currently supported; would require OCR or specialized libraries.

---

## Integration Recommendations

- Centralize file extraction logic in a dedicated service or utility module (e.g., `services/file_context/content_extractor.py`).
- Use file extension or MIME type to dispatch to the correct extraction method.
- Ensure robust error handling and logging for unsupported or malformed files.
- Add tests for each supported file type and edge case (empty, corrupted, large files).

---

## Gaps & Next Steps

- No current unified content extraction service; recommend implementing one for maintainability.
- PDF extraction is not yet integrated; add utility and tests.
- Consider adding markdown-to-text conversion for .md files if needed by business logic.
- Review and update requirements.txt if additional file types are to be supported.

---

**Status:**

- .txt and .md extraction is straightforward and supported.
- .pdf extraction is possible with available libraries but not yet integrated.
- No missing libraries for these core types; integration work is the next step.

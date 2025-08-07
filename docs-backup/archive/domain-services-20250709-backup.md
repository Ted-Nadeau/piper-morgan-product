# Domain Services Documentation

## MarkdownFormatter Domain Service

**File**: `services/utils/markdown_formatter.py`
**Purpose**: Ensure LLM-generated markdown follows CommonMark standards
**Domain**: Document Analysis & Summarization

### Business Rules Enforced

1. **Standard Bullet Syntax**: Converts `• -` to `-` (CommonMark standard)
2. **Header Spacing**: Ensures `##Header` becomes `## Header`
3. **Bold Formatting**: Fixes unclosed `**` tags
4. **Multi-space Cleanup**: Normalizes spacing in headers

### Usage

```python
from services.utils.markdown_formatter import MarkdownFormatter

# Clean and validate LLM output
cleaned_text, issues = MarkdownFormatter.clean_and_validate(llm_output)

# Just clean (no validation)
cleaned_text = MarkdownFormatter.ensure_standard_format(llm_output)

# Just validate (no cleaning)
issues = MarkdownFormatter.validate_markdown_syntax(llm_output)
```

### Integration Points

- **TextAnalyzer**: Applied after LLM summary generation
- **DocumentAnalyzer**: Applied after LLM summary generation
- **Prompt Templates**: Updated with explicit formatting rules

### Monitoring

The service logs validation issues for LLM output quality monitoring:
```
INFO: Markdown formatting issues detected and fixed: ['Non-standard bullet syntax: • - found']
```

### Why This Approach

1. **Domain-Driven**: Business rule (markdown format) belongs in domain layer
2. **Testable**: Domain service can be unit tested independently
3. **Maintainable**: Single source of truth for formatting rules
4. **Scalable**: Works for all future LLM summarization features
5. **Architectural Compliance**: No business logic in presentation layer

### Alternative Rejected

❌ **Frontend Preprocessing**: Would have violated clean architecture by putting business logic in presentation layer

✅ **Domain Service**: Proper separation of concerns, follows project's DDD patterns
---
*Last Updated: July 09, 2025*

## Revision Log
- **July 09, 2025**: Added vertical resize feature to chat window for improved usability

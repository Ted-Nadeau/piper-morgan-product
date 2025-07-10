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

## BotMessageRenderer Domain Service (Web UI, 2025)

**File**: `web/bot-message-renderer.js`
**Purpose**: Unify all bot message rendering and response handling in the web UI, following DDD principles
**Domain**: Web UI Response Handling

### Business Rules Enforced

1. All bot messages (success, error, thinking) are rendered with consistent structure and CSS classes
2. Markdown is rendered for success messages using `marked.js`
3. Error and feedback messages are actionable and user-friendly
4. All rendering logic is test-driven (TDD) and fully covered by unit/integration tests

### Usage

```javascript
import {
  renderBotMessage,
  handleDirectResponse,
  handleWorkflowResponse,
  handleErrorResponse,
} from "./bot-message-renderer";

// Render a success message
const html = renderBotMessage("Operation complete!", "success", false);

// Handle a direct API response
handleDirectResponse(result, element);

// Handle a workflow completion
handleWorkflowResponse(data, element);

// Handle an error
handleErrorResponse(error, element);
```

### Integration Points

- Used by all web UI code for bot message rendering
- Shared between UI and test files for consistency

### Why This Approach

1. **Domain-Driven**: All business rules for message rendering live in the domain module, not the presentation layer
2. **Testable**: Fully covered by TDD (unit and integration tests)
3. **Maintainable**: Single source of truth for UI feedback and error handling
4. **Extensible**: Easy to add new message types or business rules
5. **Architectural Compliance**: No business logic in presentation layer; all domain logic is modular and reusable

### Alternative Rejected

❌ **Inline UI Logic**: Would have violated DDD and made testing/maintenance difficult

✅ **Domain Service**: Proper separation of concerns, follows project's DDD patterns

---
*Last Updated: July 09, 2025*

## Revision Log
- **July 09, 2025**: Added vertical resize feature to chat window for improved usability

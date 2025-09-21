# Intent Classification Patterns

**Date:** July 21, 2025
**Status:** Current - Updated for PM-039
**Version:** 1.1

## Overview

This document describes the intent classification patterns used in Piper Morgan's natural language processing system. The classifier uses a two-stage approach: pre-classification for simple patterns and LLM-based classification for complex intents.

## Pattern Categories

### Search Intent Patterns

Search intents are classified into three main actions based on specificity and intent:

#### 1. Content Search (`search_content`)
**Purpose**: Search within document content for specific terms or concepts.

**Trigger Phrases** (checked first, most specific):
- `find files containing`
- `look for documents with`
- `files containing`
- `documents with`
- `search content`
- `search for content`
- `find content`
- `content search`

**Examples**:
- "find files containing API endpoints"
- "look for documents with implementation details"
- "search content for error messages"

**Query Extraction**: Uses `_extract_search_query()` with trigger phrase removal.

#### 2. Document Search (`find_documents`)
**Purpose**: Find documents about topics or with specific attributes.

**Trigger Phrases**:
- `find documents`
- `find files`
- `search for files`
- `search for documents`
- `find technical specifications`
- `locate files`
- `look for files`

**Examples**:
- "find technical specifications"
- "find documents about project timeline"
- "locate files with deployment info"

**Query Extraction**:
- Uses `_extract_search_query()` for trigger phrase patterns
- Uses `_extract_search_query_about()` for "about/regarding/related to" patterns

#### 3. File Search (`search_files`)
**Purpose**: General file search with broader matching.

**Trigger Phrases**:
- `search files`
- `search documents`
- `file search`
- `document search`
- `search for`
- `show me files`
- `show me documents`

**Examples**:
- "search for PDF files"
- "show me documents about database"
- "search files related to testing"

**Query Extraction**: Uses `_extract_search_query()` and `_extract_search_query_show_me()`.

### Pattern Priority

Patterns are evaluated in order of specificity (most specific first):

1. **Content Search** patterns (most specific)
2. **Document Search** patterns (medium specificity)
3. **File Search** patterns (least specific)
4. **"About" patterns** with contextual keywords
5. **"Show me" patterns** with file/document keywords

This ordering prevents broader patterns from matching before more specific ones.

## Query Extraction Methods

### `_extract_search_query(message, trigger_phrases)`
- Removes trigger phrases from the message
- Strips common prepositions and articles
- Cleans up extra whitespace
- Returns extracted query or original message as fallback

### `_extract_search_query_about(message)`
- Handles "about/regarding/related to/concerning" patterns
- Extracts content after the contextual keyword
- Cleans up articles and whitespace

### `_extract_search_query_show_me(message)`
- Handles "show me" patterns with files/documents
- Removes "show me" prefixes
- Extracts content after prepositions like "about", "related to"
- Supports variations like "show me files about X"

## Integration Points

### Query Router
All search actions (`search_content`, `find_documents`, `search_files`) are routed to `FileQueryService` methods:

- `search_content` → `search_content_by_query()`
- `find_documents` → `find_documents_about_topic()`
- `search_files` → `search_files_by_query()`

### MCP Integration
All search patterns leverage the PM-038 MCP integration for enhanced content search with 642x performance improvement.

## Testing

Pattern testing is implemented in `tests/test_intent_search_patterns.py`:

- **Fallback Classification Tests**: Verify patterns match expected actions
- **Query Extraction Tests**: Ensure proper query extraction
- **Error Elimination Tests**: Confirm patterns don't fall back to learning actions

All tests use the `_fallback_classify()` method to test rule-based patterns directly.

## Performance Characteristics

- **Confidence**: Rule-based patterns return 0.5 confidence (fallback classification)
- **Speed**: Sub-millisecond classification for rule-based patterns
- **Coverage**: Eliminates "Unknown query action" errors for target phrases
- **Integration**: Maintains 642x performance improvement from PM-038

## Examples by Pattern Type

### Content Search Examples
```
"find files containing API endpoints"
→ Action: search_content, Query: "api endpoints"

"look for documents with performance data"
→ Action: search_content, Query: "performance data"
```

### Document Search Examples
```
"find technical specifications"
→ Action: find_documents, Query: "technical specifications"

"find documents about project timeline"
→ Action: find_documents, Query: "project timeline"

"locate files with MCP integration"
→ Action: find_documents, Query: "mcp integration"
```

### File Search Examples
```
"search for PDF files"
→ Action: search_files, Query: "pdf files"

"show me documents about database"
→ Action: search_files, Query: "database"
```

## Version History

- **v1.1 (July 21, 2025)**: PM-039 implementation
  - Added content search patterns (`search_content`)
  - Added technical specifications patterns
  - Added "locate files" and "look for files" patterns
  - Added "show me" pattern support
  - Implemented pattern priority ordering
  - Added comprehensive query extraction methods

- **v1.0 (July 20, 2025)**: PM-038 initial search patterns
  - Basic "find documents" and "search files" patterns
  - Integration with MCP infrastructure

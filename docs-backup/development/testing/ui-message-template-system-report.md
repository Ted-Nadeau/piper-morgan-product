## PM-039 Intent Classification Test Coverage

### Supported Patterns

- search for requirements files
- find technical specifications
- locate API documentation
- show me all project plans
- get all design docs
- find docs about onboarding
- search for budget analysis documents
- find requirements
- search files
- find documents about project timeline

### Typo Tolerance Examples

- serach for requirments files → search_documents
- find tehcnical specfications → search_documents

### Context Extraction Patterns

- "find docs about onboarding" → search_query: onboarding
- "search for budget analysis documents" → search_query: budget analysis documents

### Action Unification

- All document/file search actions (find_documents, search_files, etc.) are normalized to 'search_documents'.
- This ensures a single routing path and simplifies downstream handling.

### Test Suite

- See tests/test_intent_coverage_pm039.py for full scenario coverage.

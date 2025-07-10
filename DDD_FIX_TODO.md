# DDD-Compliant Fix for LLM Markdown Output

## Problem Analysis

**Domain**: Document Analysis & Summarization  
**Issue**: LLM generates non-standard markdown (`• -` bullets, formatting issues)  
**Wrong Fix**: Frontend preprocessing (violates layered architecture)  
**Correct Fix**: Domain layer formatting rules and post-processing

## Domain-Driven Solution

### Phase 1: Fix the Prompt Templates (Domain Rules)

#### Task 1: Update Summarization Prompts
- [ ] **File**: `services/prompts/summarization.py`
- [ ] **Action**: Add explicit markdown formatting rules to prompts
- [ ] **Implementation**:
```python
DOCUMENT_SUMMARY_PROMPT = """
You are a skilled document analyst. Please provide a comprehensive summary of the following document.

IMPORTANT FORMATTING RULES:
- Use standard markdown formatting only
- Headers: Use "## Header" with space after ##
- Bullet points: Use "- " (dash space) NOT "• -" 
- Bold text: Use **text** 
- Code: Use `code`
- Lists must follow CommonMark specification

Your response should include:
1. File Type/Purpose
2. Main Content and Structure  
3. Important Technical Details/Patterns
4. Summary

Format your response using clean, standard markdown that will render properly in any markdown parser.

Document content: {content}
"""
```

#### Task 2: Create Domain Service for Markdown Validation
- [ ] **File**: `services/utils/markdown_formatter.py` (create if doesn't exist)
- [ ] **Action**: Domain service to ensure LLM output follows standards
- [ ] **Implementation**:
```python
"""
Domain service for markdown formatting validation and correction
"""
import re
from typing import str

class MarkdownFormatter:
    """Domain service responsible for ensuring markdown output follows standards"""
    
    @staticmethod
    def ensure_standard_format(markdown_text: str) -> str:
        """
        Ensure LLM-generated markdown follows CommonMark standards
        
        This is a domain service that enforces business rules about
        how markdown should be formatted in our system.
        """
        if not markdown_text:
            return ""
            
        # Domain rule: Use standard bullet syntax
        cleaned = re.sub(r'^• - ', '- ', markdown_text, flags=re.MULTILINE)
        
        # Domain rule: Ensure proper header spacing
        cleaned = re.sub(r'^(#{1,6})([^\s#])', r'\1 \2', cleaned, flags=re.MULTILINE)
        
        # Domain rule: Fix broken bold formatting
        cleaned = re.sub(r'\*\*([^*]+)\*([^*]*)\*\*', r'**\1\2**', cleaned)
        
        return cleaned
    
    @staticmethod
    def validate_markdown_syntax(markdown_text: str) -> list[str]:
        """
        Validate markdown syntax and return list of issues found
        Used for monitoring LLM output quality
        """
        issues = []
        
        # Check for non-standard bullet syntax
        if re.search(r'^• - ', markdown_text, re.MULTILINE):
            issues.append("Non-standard bullet syntax: '• -' found")
            
        # Check for malformed headers
        if re.search(r'^#{1,6}[^\s#]', markdown_text, re.MULTILINE):
            issues.append("Malformed headers: missing space after #")
            
        return issues
```

### Phase 2: Integrate Domain Service into Analysis Pipeline

#### Task 3: Update Text Analyzer
- [ ] **File**: `services/analysis/text_analyzer.py`
- [ ] **Location**: In the `analyze_document` method after LLM completion
- [ ] **Action**: Apply domain formatting rules
- [ ] **Implementation**:
```python
from services.utils.markdown_formatter import MarkdownFormatter

# In analyze_document method, after LLM completion:
summary_raw = await self.llm_client.complete(
    task_type=TaskType.SUMMARIZE.value,
    prompt=summary_prompt.format(content=text[:3000])
)

# Apply domain formatting rules
summary = MarkdownFormatter.ensure_standard_format(summary_raw)

# Optional: Log formatting issues for monitoring
issues = MarkdownFormatter.validate_markdown_syntax(summary_raw)
if issues:
    logger.warning(f"Markdown formatting issues detected: {issues}")
```

#### Task 4: Update Document Analyzer  
- [ ] **File**: `services/analysis/document_analyzer.py`
- [ ] **Action**: Same integration as text analyzer
- [ ] **Implementation**: Apply `MarkdownFormatter.ensure_standard_format()` after LLM completion

### Phase 3: Testing & Validation

#### Task 5: Create Domain Service Tests
- [ ] **File**: `tests/services/utils/test_markdown_formatter.py` (create)
- [ ] **Action**: Test domain formatting rules
- [ ] **Implementation**:
```python
import pytest
from services.utils.markdown_formatter import MarkdownFormatter

class TestMarkdownFormatter:
    
    def test_fixes_non_standard_bullets(self):
        input_text = "• - Item 1\n• - Item 2"
        expected = "- Item 1\n- Item 2"
        result = MarkdownFormatter.ensure_standard_format(input_text)
        assert result == expected
    
    def test_fixes_malformed_headers(self):
        input_text = "##Header\n###Another"
        expected = "## Header\n### Another"  
        result = MarkdownFormatter.ensure_standard_format(input_text)
        assert result == expected
    
    def test_validates_syntax_issues(self):
        problematic_text = "• - Bad bullet\n##Bad header"
        issues = MarkdownFormatter.validate_markdown_syntax(problematic_text)
        assert len(issues) == 2
        assert any("bullet syntax" in issue for issue in issues)
        assert any("headers" in issue for issue in issues)
```

#### Task 6: Integration Testing
- [ ] **File**: `tests/services/analysis/test_text_analyzer.py`
- [ ] **Action**: Add test for markdown formatting integration
- [ ] **Implementation**:
```python
async def test_analyze_document_formats_markdown_properly(self):
    # Test that domain formatting rules are applied
    result = await self.analyzer.analyze_document(...)
    
    # Should not contain non-standard syntax
    assert "• -" not in result.summary
    assert not result.summary.startswith("##")  # Should have space
```

### Phase 4: Monitoring & Improvement

#### Task 7: Add Telemetry for LLM Output Quality
- [ ] **File**: `services/analysis/text_analyzer.py`
- [ ] **Action**: Add metrics for markdown formatting issues
- [ ] **Implementation**:
```python
# After validation
issues = MarkdownFormatter.validate_markdown_syntax(summary_raw)
if issues:
    # Could add to metrics/monitoring system
    logger.info(f"LLM markdown quality metrics: {len(issues)} issues found")
```

## Success Criteria

### Domain Model Validation
- [ ] ✅ Formatting rules are business logic in domain layer
- [ ] ✅ UI remains thin presentation layer
- [ ] ✅ No quick fixes or workarounds in wrong layers
- [ ] ✅ Standard markdown output from all summarization operations

### Technical Validation  
- [ ] ✅ All tests pass
- [ ] ✅ LLM output follows CommonMark standards
- [ ] ✅ UI renders markdown properly without preprocessing
- [ ] ✅ Architecture maintains clean separation of concerns

## Why This Approach Is Better

1. **Correct Layer**: Business rule (markdown format) enforced in domain layer
2. **Single Responsibility**: MarkdownFormatter has one job
3. **Testable**: Domain service can be unit tested independently  
4. **Maintainable**: Changes to formatting rules happen in one place
5. **Monitoring**: Can track LLM output quality over time
6. **Scalable**: Works for all future summarization features

## Time Estimate

- **Phase 1**: 20 minutes (prompts + domain service)
- **Phase 2**: 15 minutes (integration)
- **Phase 3**: 25 minutes (testing)
- **Phase 4**: 10 minutes (monitoring)

**Total**: ~70 minutes for proper DDD solution vs. 5 minutes for quick fix

## Architecture Benefits

This solution:
- Maintains clean architecture boundaries
- Makes formatting rules explicit and testable
- Provides foundation for future LLM output improvements
- Follows project's DDD patterns consistently
- Creates reusable domain service for other LLM operations
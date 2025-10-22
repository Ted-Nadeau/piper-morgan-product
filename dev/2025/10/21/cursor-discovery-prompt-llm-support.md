# Discovery Prompt: CORE-LLM-SUPPORT (#237)

**Agent**: Cursor (Chief Architect)
**Task**: Architectural discovery for 4-provider LLM integration
**Issue**: #237 CORE-LLM-SUPPORT
**Duration**: 10-15 minutes
**Date**: October 21, 2025

---

## Mission

Discover what LLM infrastructure currently exists in the Piper Morgan codebase and assess what's needed to implement complete 4-provider integration (Claude, OpenAI, Gemini, Perplexity).

**Key Questions**:
1. Does any LLM abstraction layer exist?
2. Where are LLM calls currently made?
3. What provider(s) are currently used?
4. What infrastructure exists vs what's needed?

---

## Phase 1: Search for Existing LLM Infrastructure (5 min)

### Serena Symbolic Queries

Run these searches to find LLM-related code:

```bash
# Search for LLM services/modules
mcp__serena__search_project("LLM|llm|language model", file_pattern="services/**/*.py")

# Search for provider adapters
mcp__serena__search_project("Adapter|Provider|Claude|OpenAI|Anthropic", file_pattern="services/**/*.py")

# Search for LLM client implementations
mcp__serena__search_project("class.*Client|def.*complete|async def.*classify", file_pattern="services/**/*.py")

# Search for factory patterns
mcp__serena__search_project("Factory|create.*adapter|register.*provider", file_pattern="services/**/*.py")

# Search for LLM configuration
mcp__serena__search_project("LLMConfig|provider.*config|model.*selection", file_pattern="**/*.py")
```

### Verification Commands

```bash
# Check for services/llm directory
ls -la services/llm/ 2>/dev/null || echo "services/llm/ does not exist"

# Search for Anthropic SDK usage (current implementation)
grep -r "from anthropic import\|import anthropic" services/ --include="*.py"

# Search for OpenAI SDK usage
grep -r "from openai import\|import openai" services/ --include="*.py"

# Search for async completion calls
grep -r "async def complete\|\.messages\.create\|\.chat\.completions" services/ --include="*.py"

# Search for intent classification (likely uses LLM)
find services/ -name "*intent*" -type f

# Search for content generation (likely uses LLM)
find services/ -name "*content*" -o -name "*generation*" -type f
```

---

## Phase 2: Document Current LLM Usage (5 min)

### For Each LLM Usage Point Found

Document:
- **File**: Path to file
- **Function/Class**: What makes the LLM call
- **Provider**: Which LLM provider (Anthropic/OpenAI/etc)
- **Purpose**: What the LLM call does (classify/generate/etc)
- **API Pattern**: Direct SDK or abstraction layer

### Expected Usage Points

Search these areas specifically:

1. **Intent Classification**
   - File: `services/intent/intent_service.py` or similar
   - Purpose: Classify user queries into intent categories

2. **Content Generation**
   - File: `services/generation/` or similar
   - Purpose: Generate GitHub issues, documents, etc

3. **Knowledge Base Queries**
   - File: `services/knowledge/` or similar
   - Purpose: Semantic search, embeddings

4. **Project Context Resolution**
   - File: `services/project_context/` or similar
   - Purpose: Understand multi-project context

---

## Phase 3: Assess Pattern-012 Implementation Status (3 min)

### Check Pattern Documentation

```bash
# Verify Pattern-012 exists
cat knowledge/patterns/pattern-012-llm-adapter.md | head -50

# Check if examples match actual code
grep -r "class LLMAdapter\|class ClaudeAdapter\|class LLMFactory" services/ --include="*.py"
```

### Assessment Questions

For Pattern-012 (LLM Adapter Pattern):

1. **Interface**:
   - [ ] Does `LLMAdapter` ABC exist?
   - [ ] Does it define: `complete()`, `classify()`, `embed()`, `supports_streaming()`?

2. **Adapters**:
   - [ ] Does `ClaudeAdapter` exist?
   - [ ] Does `OpenAIAdapter` exist?
   - [ ] Does `GeminiAdapter` exist?
   - [ ] Does `PerplexityAdapter` exist?

3. **Factory**:
   - [ ] Does `LLMFactory` exist?
   - [ ] Can it create adapters by provider name?
   - [ ] Can it register custom adapters?

4. **Manager**:
   - [ ] Does `LLMManager` exist?
   - [ ] Does it support fallback providers?
   - [ ] Does it support provider comparison?

---

## Phase 4: Gap Analysis (2 min)

### Infrastructure Assessment

Create inventory:

**EXISTS** (List with file paths):
- Pattern documentation
- Current LLM usage points
- Provider SDK dependencies
- Configuration files

**MISSING** (List what needs to be built):
- Abstraction layer components
- Provider adapters
- Factory/Manager classes
- Integration points

### Effort Estimation

For each missing component:
- **Simple** (<1 hour): Well-defined, follows pattern exactly
- **Moderate** (1-3 hours): Requires some design decisions
- **Complex** (3+ hours): Significant new architecture

---

## Discovery Report Format

Create: `dev/2025/10/21/core-llm-support-discovery-report.md`

### Report Structure

```markdown
# CORE-LLM-SUPPORT Discovery Report

**Date**: October 21, 2025
**Agent**: Cursor (Chief Architect)
**Duration**: [X] minutes
**Issue**: #237 CORE-LLM-SUPPORT

---

## Executive Summary

**Key Finding**: [One sentence: What % complete is LLM infrastructure?]

**Current State**:
- LLM abstraction layer: [EXISTS / PARTIAL / MISSING]
- Provider adapters: [X of 4 implemented]
- Current provider: [Anthropic/OpenAI/None/Multiple]

**Work Required**: [X-Y hours based on gap analysis]

---

## Current LLM Infrastructure

### Directory Structure

```
services/
├── llm/              [EXISTS / MISSING]
│   ├── client.py     [EXISTS / MISSING]
│   ├── adapters.py   [EXISTS / MISSING]
│   └── __init__.py   [EXISTS / MISSING]
```

### LLM Usage Points

List each place LLMs are currently used:

1. **Intent Classification**
   - File: [path]
   - Implementation: [Direct SDK / Abstraction]
   - Provider: [Claude/OpenAI/etc]
   - Pattern: [code snippet or description]

2. **[Other usage point]**
   - ...

### Pattern-012 Implementation Status

| Component | Status | File Path | Notes |
|-----------|--------|-----------|-------|
| LLMAdapter (ABC) | [EXISTS/MISSING] | [path] | [notes] |
| ClaudeAdapter | [EXISTS/MISSING] | [path] | [notes] |
| OpenAIAdapter | [EXISTS/MISSING] | [path] | [notes] |
| GeminiAdapter | [EXISTS/MISSING] | [path] | [notes] |
| PerplexityAdapter | [EXISTS/MISSING] | [path] | [notes] |
| LLMFactory | [EXISTS/MISSING] | [path] | [notes] |
| LLMManager | [EXISTS/MISSING] | [path] | [notes] |

---

## Gap Analysis

### What Exists

[List with file paths and line counts]

### What's Missing

[List components that need to be built]

### Refactoring Needed

[List current usage points that need to migrate to new abstraction]

---

## Implementation Estimate

### Phase 1: Build Abstraction Layer
- LLMAdapter interface: [X hours]
- ClaudeAdapter: [X hours]
- OpenAIAdapter: [X hours]
- LLMFactory: [X hours]
- LLMManager: [X hours]
- **Subtotal**: [X-Y hours]

### Phase 2: Refactor Current Usage
- Intent classification: [X hours]
- Content generation: [X hours]
- [Other usage points]: [X hours]
- **Subtotal**: [X-Y hours]

### Phase 3: Add New Providers
- GeminiAdapter: [X hours]
- PerplexityAdapter: [X hours]
- Configuration: [X hours]
- **Subtotal**: [X-Y hours]

### Phase 4: Testing & Documentation
- Unit tests: [X hours]
- Integration tests: [X hours]
- Documentation: [X hours]
- **Subtotal**: [X-Y hours]

**TOTAL ESTIMATE**: [X-Y hours]

---

## Recommendations

### Option 1: [Title]
- **Time**: [X hours]
- **Scope**: [description]
- **Benefits**: [list]
- **Risks**: [list]

### Option 2: [Title]
- ...

### Recommended Approach: [Option X]
- **Rationale**: [why]

---

## Files Examined

**Pattern Documentation**:
- pattern-012-llm-adapter.md

**Source Code** (list all files searched):
- services/[...]
- [...]

**Configuration**:
- [config files found]

---

## Next Steps

1. [Action 1]
2. [Action 2]
3. [Action 3]

---

*Discovery complete. Ready for implementation planning.*
```

---

## Success Criteria

Discovery is complete when:

- [x] All Serena queries executed
- [x] All verification commands run
- [x] Current LLM usage documented
- [x] Pattern-012 status assessed
- [x] Gap analysis complete
- [x] Effort estimate provided
- [x] Discovery report written
- [x] Recommendations clear

---

## Notes for Cursor

- Use Serena MCP for all codebase searches
- Be thorough - check everywhere LLMs might be used
- Document actual file paths and line numbers
- Distinguish between documentation and implementation
- Provide realistic effort estimates
- Multiple options are better than one recommendation

---

**Ready to discover!** Use this prompt to guide your investigation of CORE-LLM-SUPPORT infrastructure.

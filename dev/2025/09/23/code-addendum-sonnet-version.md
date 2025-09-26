# ADDENDUM: Check for Deprecated Sonnet Version

## New Lead from PM (8:00 PM)

**Anthropic email alert**: Deprecated Sonnet version being called
- Might be using `claude-3-sonnet-20240229` (deprecated)
- Should be using `claude-3-5-sonnet-20241022` (current)
- Could explain JSON parsing errors and 0.00 confidence scores

## Additional Investigation Tasks

### 1. Find Model Version References
```bash
# Search for Anthropic model names
grep -r "claude-3-sonnet\|claude-sonnet\|anthropic" . --include="*.py" --include="*.yaml" --include="*.json" --include="*.md" | grep -v "__pycache__"

# Check config files
grep -r "model.*claude\|sonnet.*version" config/ 

# Check LLM classifier specifically
grep -r "claude\|sonnet\|model" services/intent_service/llm_classifier*.py
```

### 2. Check for Deprecated Version String
```bash
# Look for old Sonnet version
grep -r "claude-3-sonnet-20240229" .
grep -r "claude-sonnet-3" .

# Look for version config
grep -r "model_version\|model_name\|llm_model" . --include="*.py" | grep -i claude
```

### 3. Examine Environment Variables
```bash
# Check for model config in env
grep -r "CLAUDE\|ANTHROPIC.*MODEL\|SONNET" .env* 2>/dev/null
grep -r "CLAUDE\|ANTHROPIC.*MODEL\|SONNET" config/*.md
```

## Report Format Update

Add to your LLM investigation report:

**Sonnet Version Check**:
```
Model Version Found: [claude-3-sonnet-20240229 | claude-3-5-sonnet-20241022 | other]
Location: [config file or code reference]
Status: [DEPRECATED | CURRENT | UNKNOWN]

If deprecated:
- Impact: [likely causing JSON parsing issues]
- Fix: Update to claude-3-5-sonnet-20241022
- Files to change: [list]
```

This could be THE root cause of LLM failures!

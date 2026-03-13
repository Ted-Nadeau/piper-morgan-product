# Cursor Investigation Prompt: API Key Management Infrastructure Analysis

**Agent**: Cursor (Chief Architect)
**Issue**: #228 CORE-USERS-API
**Task**: Investigate current API key management and create implementation gameplan
**Date**: October 22, 2025, 6:07 AM
**Duration**: 40-60 minutes

---

## Mission

**Goal**: Analyze current API key management infrastructure and create a comprehensive gameplan for production-ready secure key storage.

**Your job is investigation ONLY**:
- ✅ Discover what exists
- ✅ Document current state
- ✅ Identify gaps
- ✅ Create gameplan for Code
- ❌ Do NOT implement anything

---

## Context from Issue #228

**Current State (Issue claims)**:
```yaml
# Current: config/llm.yaml (plaintext)
openai_api_key: "sk-..."
anthropic_api_key: "sk-ant-..."
```

**Required for Alpha**:
- OS keychain integration (macOS/Linux/Windows)
- Encrypted file fallback
- Environment variable support
- Multi-user key isolation
- Key rotation support
- Services: OpenAI, Anthropic, GitHub, Notion, Slack

---

## Context from Yesterday's Discoveries

**Pattern recognition**: Yesterday we discovered infrastructure was more complete than expected:
- JWT blacklist: 60% done
- PostgreSQL: 95% done

**Prediction for API Keys**: 40-60% likely exists
- LLM services probably configured (it's a PM assistant!)
- Keys probably in .env (basic but working)
- Keychain integration probably NOT done
- Rotation probably NOT implemented

**Your job**: Prove or disprove this prediction!

---

## Phase 1: Find LLM Configuration (15 min)

### 1.1 Search for LLM Services

```bash
# Find LLM-related services
find services/ -name "*llm*" -o -name "*openai*" -o -name "*anthropic*" -o -name "*ai*" 2>/dev/null | grep -v __pycache__

# Search for LLM imports
grep -r "openai\|anthropic" . --include="*.py" | grep -i "import\|from" | head -20

# Find LLM service implementations
grep -r "class.*LLM\|class.*AI\|class.*OpenAI\|class.*Anthropic" . --include="*.py" | head -20
```

### 1.2 Find API Key Configuration

```bash
# Check for config files
find config/ -name "*.py" -o -name "*.yaml" -o -name "*.yml" -o -name "*.json" 2>/dev/null

# Look for API key references
grep -r "api_key\|API_KEY\|openai_api_key\|anthropic_api_key" config/ --include="*.py" --include="*.yaml" 2>/dev/null | head -20

# Check environment variables
cat .env 2>/dev/null | grep -i "api_key\|openai\|anthropic\|github\|notion\|slack"

# Check .env.example
cat .env.example 2>/dev/null | grep -i "api_key\|openai\|anthropic\|github\|notion\|slack"
```

### 1.3 Find LLM Client Initialization

```bash
# How are OpenAI/Anthropic clients created?
grep -r "OpenAI(\|Client(\|Anthropic(" . --include="*.py" -A 5 | head -40

# Look for API key loading patterns
grep -r "os.getenv.*api_key\|getenv.*API_KEY" . --include="*.py" | head -20
```

**Document findings**:
- Where are API keys currently stored?
- How are they loaded?
- Which services are configured?
- Is there encryption?

---

## Phase 2: Find Key Management Infrastructure (15 min)

### 2.1 Search for KeyManager/APIKeyManager

```bash
# Look for key management classes
grep -r "class.*Key.*Manager\|class.*API.*Key\|class.*Secret" . --include="*.py"

# Look for keychain/keyring usage
grep -r "keyring\|keychain\|secretstorage" . --include="*.py"

# Check for encryption utilities
grep -r "encrypt\|decrypt\|cipher\|Fernet" . --include="*.py" | grep -v __pycache__ | head -20

# Look for key storage patterns
find . -name "*key*manager*.py" -o -name "*secret*.py" -o -name "*credential*.py" 2>/dev/null | grep -v __pycache__
```

### 2.2 Check Dependencies

```bash
# Check for keyring/encryption packages
cat pyproject.toml 2>/dev/null | grep -i "keyring\|cryptography\|fernet\|secret"
cat requirements.txt 2>/dev/null | grep -i "keyring\|cryptography\|fernet\|secret"
cat poetry.lock 2>/dev/null | grep -i "keyring\|cryptography" | head -10
```

### 2.3 Find Validation Logic

```bash
# Look for API key validation
grep -r "validate.*key\|verify.*key\|test.*key" . --include="*.py" | grep -i "api\|openai\|anthropic" | head -20

# Check for API client error handling
grep -r "AuthenticationError\|InvalidAPIKey\|APIConnectionError" . --include="*.py" | head -20
```

**Document findings**:
- Does APIKeyManager or similar exist?
- Is keyring/keychain used?
- Is encryption implemented?
- How is validation done?

---

## Phase 3: Find Service Integrations (15 min)

### 3.1 OpenAI Integration

```bash
# Find OpenAI usage
grep -r "from openai\|import openai" . --include="*.py"

# Find OpenAI client creation
grep -r "OpenAI(\|openai.Client(" . --include="*.py" -A 3

# Check for chat completions
grep -r "chat.completions\|ChatCompletion" . --include="*.py" | head -10
```

### 3.2 Anthropic Integration

```bash
# Find Anthropic usage
grep -r "from anthropic\|import anthropic" . --include="*.py"

# Find Anthropic client creation
grep -r "Anthropic(\|anthropic.Client(" . --include="*.py" -A 3

# Check for message creation
grep -r "messages.create\|Message.create" . --include="*.py" | head -10
```

### 3.3 Other Service Integrations

```bash
# GitHub integration
grep -r "github\|PyGithub\|octokit" . --include="*.py" | grep -i "import\|token" | head -10

# Notion integration
grep -r "notion\|notion-client" . --include="*.py" | head -10

# Slack integration
grep -r "slack\|slack_sdk" . --include="*.py" | head -10

# Check for MCP integrations (might handle some API keys)
find . -name "*mcp*" -type f | grep -v __pycache__ | head -10
```

**Document findings**:
- Which services are integrated?
- How are clients initialized?
- Where do they get API keys?
- Is there a common pattern?

---

## Phase 4: Multi-User Support Analysis (10 min)

### 4.1 User Isolation Patterns

```bash
# Look for user-specific configurations
grep -r "user.*api_key\|api_key.*user" . --include="*.py" | head -20

# Check for per-user settings
grep -r "user.*config\|config.*user\|user.*settings" . --include="*.py" | grep -i "key\|api\|secret" | head -20

# Look for user database models
grep -A 10 "class User" services/database/models.py 2>/dev/null | grep -i "key\|api\|token"
```

### 4.2 Key Rotation Patterns

```bash
# Look for rotation logic
grep -r "rotate.*key\|key.*rotation\|update.*key" . --include="*.py" | head -20

# Check for key versioning
grep -r "key.*version\|version.*key" . --include="*.py" | head -10
```

**Document findings**:
- Is there multi-user support?
- Are keys isolated per user?
- Is rotation implemented?
- How would it work?

---

## Phase 5: Gap Analysis (5 min)

### 5.1 Compare Current vs Required

**Required by Issue #228**:
- [ ] OS keychain integration (macOS/Linux/Windows)
- [ ] Encrypted file fallback
- [ ] Environment variable support
- [ ] Multi-user key isolation
- [ ] Key rotation (zero-downtime)
- [ ] Validation for all key types
- [ ] Services: OpenAI, Anthropic, GitHub, Notion, Slack

**Document for each**:
- EXISTS: What's currently implemented?
- MISSING: What needs to be added?
- PARTIAL: What's partially done?

---

## Discovery Report Format

Create: `dev/2025/10/22/api-key-management-analysis.md`

### Report Structure

```markdown
# API Key Management Infrastructure Analysis

**Date**: October 22, 2025, 6:07 AM
**Agent**: Cursor (Chief Architect)
**Issue**: #228 CORE-USERS-API
**Duration**: [X] minutes

---

## Executive Summary

**Current State**: [Summary of what exists]
**LLM Services**: [OpenAI/Anthropic/Other status]
**Key Storage**: [Where/how keys are stored]
**Security Level**: [Plaintext/Encrypted/Keychain]
**Gap Analysis**: [X features to add]

**Key Finding**: [One sentence: Main discovery]

**Leverage Estimate**: [X]% existing infrastructure

---

## Current Infrastructure

### LLM Service Configuration

**Services Found**:
```bash
[List services discovered]
- OpenAI: [YES/NO - details]
- Anthropic: [YES/NO - details]
- GitHub: [YES/NO - details]
- Notion: [YES/NO - details]
- Slack: [YES/NO - details]
```

**Configuration Files**:
```python
[Paste relevant config code]
```

**Location**: [File paths]

### API Key Storage

**Current Method**: [.env / config files / keychain / database]

**Storage Details**:
```bash
[Show how keys are currently stored]
```

**Security Assessment**:
- Encryption: [YES/NO/PARTIAL]
- Keychain: [YES/NO]
- Plaintext risk: [HIGH/MEDIUM/LOW]

### Key Loading Pattern

**How keys are loaded**:
```python
[Paste code showing key loading]
```

**Pattern Used**: [Direct .env / Config class / Key manager]

---

## Service Integration Details

### OpenAI Integration

**Status**: [Exists / Doesn't exist / Partial]

**Implementation**:
```python
[Paste relevant OpenAI code]
```

**Key Source**: [Where OpenAI gets its key]

### Anthropic Integration

**Status**: [Exists / Doesn't exist / Partial]

**Implementation**:
```python
[Paste relevant Anthropic code]
```

**Key Source**: [Where Anthropic gets its key]

### Other Integrations

[Document GitHub, Notion, Slack, etc.]

---

## Key Management Infrastructure

### APIKeyManager Status

**Exists**: [YES/NO]

**If YES, document**:
```python
[Paste APIKeyManager code]
```

**Features**:
- store_key(): [Implemented / Not implemented]
- retrieve_key(): [Implemented / Not implemented]
- rotate_key(): [Implemented / Not implemented]
- validate_key(): [Implemented / Not implemented]

**If NO**:
- Keys loaded directly from .env or config
- No centralized key management
- Need to create APIKeyManager

### Encryption Status

**Encryption Library**: [cryptography / Fernet / None]

**Status**: [Implemented / Not implemented]

**If implemented**:
```python
[Show encryption usage]
```

### Keychain Integration Status

**Keyring Package**: [Installed / Not installed]

**Status**: [Implemented / Not implemented / Attempted]

**If implemented/attempted**:
```bash
[Show keyring usage]
```

---

## Multi-User Support

### Current User Isolation

**User Model**:
```python
[Paste User model fields related to keys]
```

**Key Isolation**: [Per-user / Global / Not implemented]

**Storage Pattern**: [How user keys would be stored]

### Key Rotation Support

**Status**: [Implemented / Not implemented / Partial]

**If implemented**:
```python
[Show rotation logic]
```

---

## Gap Analysis

### What EXISTS ✅

1. **[Feature 1]**: [Description]
   - Location: [path]
   - Status: [Fully implemented / Working well]
   - Evidence: [grep results or code sample]

2. **[Feature 2]**: [Description]
   - Location: [path]
   - Status: [details]

[Continue for all existing features]

### What's MISSING ❌

1. **[Gap 1]**: [What's needed]
   - Why needed: [Security / Functionality / Requirement]
   - Complexity: [Low / Medium / High]
   - Priority: [Critical / High / Medium / Low]
   - Estimate: [Hours to implement]

2. **[Gap 2]**: [What's needed]
   - Why needed: [rationale]
   - Complexity: [level]
   - Priority: [level]
   - Estimate: [hours]

[Continue for all gaps]

### Configuration Gaps Table

| Component | Current | Required | Priority | Estimate |
|-----------|---------|----------|----------|----------|
| OS Keychain | [None/Partial/...] | macOS/Linux/Windows | High | [Xh] |
| Encrypted Fallback | [None/Partial/...] | Full support | High | [Xh] |
| Environment Vars | [Working/...] | Keep support | Low | [Xh] |
| Multi-user Keys | [None/Partial/...] | Per-user isolation | High | [Xh] |
| Key Rotation | [None/...] | Zero-downtime | Medium | [Xh] |
| Key Validation | [None/Partial/...] | All services | Medium | [Xh] |

---

## Leverage Analysis

### Infrastructure Score: [X]% Complete

**What's already done** (estimated [X]%):
- ✅ [List existing features]
- ✅ [...]
- ✅ [...]

**What needs adding** (estimated [X]%):
- ❌ [List missing features]
- ❌ [...]
- ❌ [...]

### Complexity Assessment

**Low complexity** (can reuse existing patterns):
- [List items]

**Medium complexity** (need new patterns):
- [List items]

**High complexity** (OS-specific or complex):
- [List items]

---

## Recommended Approach

### Scenario A: Basic Key Management Exists (40-60% done)

**If keys in .env + basic loading exists**:

**Gameplan**:
1. Create APIKeyManager class
2. Add keyring integration (OS keychain)
3. Add encrypted file fallback
4. Implement key validation
5. Add rotation support
6. Add multi-user isolation
7. Migrate existing keys
8. Documentation

**Complexity**: Medium
**Estimate**: 8-12 hours

### Scenario B: No Key Management (0-20% done)

**If starting from scratch**:

**Gameplan**:
1. Install keyring + cryptography
2. Design APIKeyManager architecture
3. Implement core storage methods
4. Add OS keychain support
5. Add encrypted fallback
6. Implement validation for each service
7. Add rotation support
8. Multi-user isolation
9. Migration from plaintext
10. Comprehensive testing
11. Documentation

**Complexity**: High
**Estimate**: 16-20 hours

### Scenario C: Partial Implementation (60-80% done)

**If APIKeyManager exists but incomplete**:

**Gameplan**:
1. Audit existing APIKeyManager
2. Add missing methods
3. Add OS keychain if missing
4. Enhance encryption if needed
5. Add rotation if missing
6. Multi-user support if missing
7. Validation for all services
8. Testing
9. Documentation updates

**Complexity**: Low-Medium
**Estimate**: 4-8 hours

---

## Files to Review for Gameplan

**Code will need to work in these files**:

**Core Implementation**:
- [ ] Create `services/security/api_key_manager.py` (or similar)
- [ ] Create `services/security/encryption.py` (if not exists)
- [ ] Modify `config/llm.py` or create `config/api_keys.py`

**Service Updates**:
- [ ] Modify OpenAI client initialization
- [ ] Modify Anthropic client initialization
- [ ] Modify GitHub token usage
- [ ] Modify Notion client
- [ ] Modify Slack client

**User Model** (if multi-user):
- [ ] Modify `services/database/models.py` (User model)
- [ ] Create migration for user API keys

**Testing**:
- [ ] Create `tests/security/test_api_key_manager.py`
- [ ] Create `tests/security/test_keychain_integration.py`
- [ ] Create `tests/security/test_key_rotation.py`

**Documentation**:
- [ ] Create `docs/api-key-management.md`
- [ ] Update `.env.example`
- [ ] Update deployment guide

---

## Evidence Checklist

Before finishing investigation, verify:

- [x] LLM services identified (OpenAI/Anthropic/etc)
- [x] Current key storage method documented
- [x] APIKeyManager existence confirmed or denied
- [x] Encryption status determined
- [x] Keychain integration status determined
- [x] Multi-user support patterns identified
- [x] All gaps listed with priority and estimate
- [x] Recommended approach identified (A/B/C)
- [x] Files to modify listed
- [x] Leverage percentage estimated

---

## Success Criteria

Investigation complete when you can answer:

- [x] How are API keys currently stored?
- [x] Which LLM services are integrated?
- [x] Does APIKeyManager exist?
- [x] Is encryption used?
- [x] Is keychain integration attempted?
- [x] What's the leverage percentage?
- [x] Which gameplan scenario applies (A/B/C)?
- [x] What files need modification?
- [x] What's the estimated complexity and time?

---

**Investigation complete. Ready to create gameplan for Code based on findings.**
```

---

## Critical Notes

**For Cursor**:

1. **Investigation ONLY** - Do not implement anything
2. **Be thorough** - Code needs complete picture
3. **Document evidence** - Show terminal output, code samples
4. **Estimate leverage** - How much exists vs needs adding?
5. **Identify scenario** - Which approach (A/B/C) applies?

**Key Question**: What percentage of infrastructure exists?
- High (60-80%) → Quick enhancement work
- Medium (40-60%) → Moderate implementation
- Low (0-20%) → Full build required

**Yesterday's Pattern**:
- JWT: 60% done → 8 hours work
- Database: 95% done → 2.3 hours work
- API Keys: Prediction 40-60% → 8-12 hours work?

**Time Management**:
- Thorough investigation more important than speed
- If takes >60 min, report progress and continue
- Complete picture essential for accurate scoping

---

**Ready to investigate!** Start with Phase 1 and systematically work through all phases.

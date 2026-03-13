# SEC-ENCRYPT-ATREST - Implement Encryption at Rest for Sensitive Data

**Priority**: P0 (CRITICAL - Compliance showstopper)
**Labels**: `security`, `compliance`, `priority: critical`
**Milestone**: Security MVP
**Epic**: Security Hardening
**Related**: ADR-012 (Protocol-Ready JWT Authentication), existing encryption.py

**Discovered by**: Ted Nadeau (architectural review)

---

## Problem Statement

### Current State
**COMPLIANCE FAILURE**: All sensitive data stored in plaintext in PostgreSQL database.

**Currently Encrypted** ✅:
- API keys (Fernet symmetric encryption in `services/security/encryption.py`)
- Passwords (Bcrypt hashing)
- Data in flight (TLS/SSL)

**Currently Unencrypted** ❌:
- Conversation content (user prompts, AI responses)
- Uploaded file content
- Pattern learning data
- User PII (email, metadata)

### Impact
- **Blocks**: SOC2 certification, GDPR compliance, enterprise sales
- **User Impact**: Data breach would expose all user conversations and files in plaintext
- **Technical Debt**: Every day of production use increases encrypted data migration complexity
- **Compliance Violations**:
  - GDPR Article 32 (data protection requirements)
  - SOC2 Type II (encryption at rest mandatory)
  - CCPA (California Consumer Privacy Act)
  - HIPAA (if healthcare data involved - future consideration)

### Strategic Context
Ted Nadeau identified this as critical architectural gap during review. Must be implemented **before storing any production user data**. Enterprise customers require encryption at rest as table stakes for procurement.

**Risk without encryption**:
- 🚫 GDPR fines (up to 4% of global revenue)
- 🚫 SOC2 audit automatic failure
- 🚫 Data breach = plaintext exposure of all user data
- 🚫 Loss of enterprise sales opportunities

---

## Goal

**Primary Objective**: Implement field-level encryption for all sensitive database columns using AES-256-GCM encryption with <5% performance overhead and zero downtime migration.

**Example User Experience**:
```
Before: Data breach exposes "Tell me about my health data..." in plaintext
After: Data breach exposes "gAAAAABh..." (encrypted, useless to attacker)
```

**Not In Scope** (explicitly):
- ❌ Full disk encryption (infrastructure-level, separate concern)
- ❌ AWS KMS integration (future enhancement, use env var for alpha)
- ❌ Homomorphic encryption (query on encrypted data - too complex for v1)
- ❌ Retroactive encryption of test data (dev/staging only)

---

## What Already Exists

### Infrastructure ✅
- `services/security/encryption.py` - Existing Fernet encryption for API keys
- SQLAlchemy models with hybrid properties pattern
- Audit model mixin for created/updated tracking
- Alembic migration framework

### What's Missing ❌
- EncryptionService class for AES-256-GCM (stronger than current Fernet)
- SQLAlchemy decorators for transparent encrypt/decrypt
- Key derivation from master key per table/field
- Migration script to encrypt existing data
- Key rotation strategy documentation
- Performance benchmarks for encrypted queries

---

## Requirements

### Phase 0: Investigation & Setup
- [ ] Verify current Fernet implementation in `services/security/encryption.py`
- [ ] Benchmark baseline query performance on conversation/file tables
- [ ] Research pgcrypto extension as alternative to application-level encryption
- [ ] Document key management strategy (environment variable → AWS KMS path)

### Phase 1: Encryption Service
**Objective**: Create reusable encryption service with AES-256-GCM

**Tasks**:
- [ ] Create `services/security/field_encryption.py`
- [ ] Implement `FieldEncryptionService` class
  - AES-256-GCM encryption (stronger than Fernet)
  - Key derivation per table/field (HKDF)
  - Master key from `ENCRYPTION_MASTER_KEY` environment variable
- [ ] Create unit tests for encryption/decryption
- [ ] Create unit tests for key derivation
- [ ] Document key rotation procedure

**Deliverables**:
- `services/security/field_encryption.py` - EncryptionService class
- `tests/unit/services/security/test_field_encryption.py` - Test coverage
- `docs/security/key-management.md` - Key rotation guide

### Phase 2: Model Integration
**Objective**: Add encryption to sensitive SQLAlchemy model fields

**Tasks**:
- [ ] Create SQLAlchemy `@encrypted_column` decorator
- [ ] Add encryption to `conversations.content`
- [ ] Add encryption to `conversation_turns.user_content`
- [ ] Add encryption to `conversation_turns.assistant_content`
- [ ] Add encryption to `uploaded_files.content`
- [ ] Add encryption to `patterns.pattern_data`
- [ ] Add encryption to `api_keys.key_value` (migrate from Fernet)
- [ ] Evaluate: Encrypt `users.email` (impacts queries - may defer)

**Deliverables**:
- Updated models in `services/database/models.py`
- Transparent encrypt on save / decrypt on load
- No code changes required in business logic

### Phase 3: Data Migration
**Objective**: Encrypt all existing plaintext data with zero downtime

**Tasks**:
- [ ] Create Alembic migration to add `_encrypted` shadow columns
- [ ] Create migration script to copy + encrypt existing data
- [ ] Test migration on dev database copy
- [ ] Implement rollback plan (plaintext columns remain temporarily)
- [ ] Execute migration with transaction safety
- [ ] Verify all data migrated successfully
- [ ] Drop plaintext columns after verification period (1 week)

**Deliverables**:
- `alembic/versions/XXX_encrypt_sensitive_fields.py` - Migration
- `scripts/migrate_encrypt_data.py` - Data migration script
- Zero downtime (shadow column approach)

### Phase 4: Performance Validation
**Objective**: Ensure encryption overhead meets <5% requirement

**Tasks**:
- [ ] Benchmark conversation retrieval (read)
- [ ] Benchmark conversation creation (write)
- [ ] Benchmark file upload/download
- [ ] Benchmark pattern learning queries
- [ ] Optimize if overhead >5% (connection pooling, caching)

**Deliverables**:
- Performance benchmark report (`docs/security/encryption-performance.md`)
- Evidence that overhead <5% for reads, <10% for writes

### Phase Z: Completion & Handoff
- [ ] All acceptance criteria met (checked below)
- [ ] Evidence provided for each criterion
- [ ] ADR-043: Encryption at Rest Strategy (created)
- [ ] Security documentation updated
- [ ] GitHub issue fully updated
- [ ] Session log completed

---

## Acceptance Criteria

### Functionality
- [ ] EncryptionService encrypts/decrypts correctly
- [ ] Sensitive fields encrypted transparently on save
- [ ] Sensitive fields decrypted transparently on load
- [ ] No business logic changes required
- [ ] Key derivation unique per table/field
- [ ] Master key loaded from environment variable

### Fields Encrypted
- [ ] `conversations.content` - User conversation data
- [ ] `conversation_turns.user_content` - User messages
- [ ] `conversation_turns.assistant_content` - AI responses
- [ ] `uploaded_files.content` - File data blobs
- [ ] `patterns.pattern_data` - Learning pattern data
- [ ] `api_keys.key_value` - API credentials (migrated from Fernet)

### Migration
- [ ] Existing data encrypted successfully
- [ ] Zero downtime migration (shadow columns)
- [ ] Rollback plan tested and documented
- [ ] No data loss during migration
- [ ] Verification period completed (1 week)

### Testing
- [ ] Unit tests for EncryptionService (20+ tests)
- [ ] Integration tests for encrypted models
- [ ] End-to-end test: Create → Save → Retrieve → Decrypt
- [ ] Migration tested on database snapshot
- [ ] Rollback tested successfully

### Performance
- [ ] Read operations overhead <5%
- [ ] Write operations overhead <10%
- [ ] Connection pooling unaffected
- [ ] Query performance acceptable for non-encrypted fields

### Security
- [ ] Master key never logged or exposed
- [ ] Encrypted data unreadable in database
- [ ] Key rotation procedure documented
- [ ] Future AWS KMS integration path defined

### Documentation
- [ ] ADR-043: Encryption at Rest Strategy created
- [ ] Key management guide (`docs/security/key-management.md`)
- [ ] Performance benchmarks documented
- [ ] Migration runbook created
- [ ] Session log completed

---

## Completion Matrix

**Use this to verify 100% completion before declaring "done"**

| Component | Status | Evidence Link |
|-----------|--------|---------------|
| FieldEncryptionService | ❌ | [commit] |
| @encrypted_column decorator | ❌ | [commit] |
| conversations.content encrypted | ❌ | [commit] |
| conversation_turns encrypted | ❌ | [commit] |
| uploaded_files.content encrypted | ❌ | [commit] |
| patterns.pattern_data encrypted | ❌ | [commit] |
| api_keys migrated to AES-256 | ❌ | [commit] |
| Migration script | ❌ | [commit] |
| Unit tests | ❌ | [test output] |
| Integration tests | ❌ | [test output] |
| Performance benchmarks | ❌ | [benchmark report] |
| ADR-043 created | ❌ | [ADR file] |
| Key management docs | ❌ | [doc file] |

**Legend**:
- ✅ = Complete with evidence
- ⏸️ = In progress
- ❌ = Not started / Blocked

**Definition of COMPLETE**:
- ✅ ALL sensitive fields encrypted
- ✅ Migration tested on production snapshot
- ✅ Performance overhead <5% verified
- ✅ SOC2/GDPR compliance verified by security review
- ✅ Key rotation procedure tested

**NOT complete means**:
- ❌ "Encryption works but migration not tested"
- ❌ "Most fields encrypted, email deferred"
- ❌ "Core done, performance optimization optional"
- ❌ Any rationalization of incompleteness

---

## Testing Strategy

### Unit Tests
```python
# tests/unit/services/security/test_field_encryption.py

def test_encrypt_decrypt_roundtrip():
    service = FieldEncryptionService(master_key)
    plaintext = "Sensitive user data"
    encrypted = service.encrypt(plaintext, context="conversations.content")
    decrypted = service.decrypt(encrypted, context="conversations.content")
    assert decrypted == plaintext

def test_key_derivation_unique_per_context():
    service = FieldEncryptionService(master_key)
    key1 = service._derive_key("conversations.content")
    key2 = service._derive_key("uploaded_files.content")
    assert key1 != key2  # Different contexts = different keys

def test_encryption_not_deterministic():
    # Same plaintext should produce different ciphertext (IV randomness)
    service = FieldEncryptionService(master_key)
    ct1 = service.encrypt("data", "context")
    ct2 = service.encrypt("data", "context")
    assert ct1 != ct2
```

### Integration Tests
```python
# tests/integration/test_encrypted_models.py

@pytest.mark.asyncio
async def test_conversation_encryption_transparent(db_session):
    # Create conversation with sensitive content
    conv = Conversation(
        user_id="test-user",
        content="Tell me about my medical history"  # Sensitive!
    )
    db_session.add(conv)
    await db_session.commit()

    # Verify encrypted in database
    result = await db_session.execute(
        text("SELECT _content_encrypted FROM conversation WHERE id = :id"),
        {"id": conv.id}
    )
    encrypted_value = result.scalar()
    assert encrypted_value != "Tell me about my medical history"
    assert encrypted_value.startswith("gAAAAA")  # AES-256-GCM prefix

    # Verify decrypted on retrieval
    retrieved = await db_session.get(Conversation, conv.id)
    assert retrieved.content == "Tell me about my medical history"
```

### Manual Testing Checklist
**Scenario 1**: End-to-end conversation encryption
1. [ ] Create conversation via API with sensitive content
2. [ ] Inspect database directly - verify encrypted
3. [ ] Retrieve conversation via API - verify decrypted correctly
4. [ ] Delete conversation - verify encrypted data removed

**Scenario 2**: File upload encryption
1. [ ] Upload file with sensitive content
2. [ ] Inspect database `uploaded_files.content` - verify encrypted
3. [ ] Download file - verify decrypted matches original
4. [ ] Verify file metadata (filename, size) NOT encrypted

**Scenario 3**: Migration rollback
1. [ ] Run migration on test database
2. [ ] Verify data encrypted
3. [ ] Trigger rollback
4. [ ] Verify plaintext data restored
5. [ ] Verify no data loss

---

## Success Metrics

### Quantitative
- **Encryption coverage**: 100% of sensitive fields encrypted
- **Performance overhead**: <5% for reads, <10% for writes
- **Migration success**: 0 data loss, 100% fields migrated
- **Test coverage**: >95% for EncryptionService

### Qualitative
- SOC2 auditor confirms encryption meets requirements
- Security team approves key management strategy
- No plaintext sensitive data visible in database dumps
- Enterprise customers can verify encryption in security questionnaire

---

## STOP Conditions

**STOP immediately and escalate if**:
- Performance overhead >10% and no optimization path found
- Key management becomes more complex than AWS KMS (implement KMS instead)
- Migration causes data corruption (use shadow column rollback)
- Encryption breaks existing queries (fix query patterns, don't skip encryption)
- Tests reveal decrypt failures (fix encryption, don't rationalize)
- Security review identifies cryptographic weakness
- Any sensitive data remains unencrypted (100% or nothing)

**When stopped**: Document the issue, provide options (pgcrypto extension, AWS KMS, simplified approach), wait for PM/security decision.

---

## Effort Estimate

**Overall Size**: Large

**Breakdown by Phase**:
- Phase 0 (Investigation): Small (4 hours)
- Phase 1 (Encryption Service): Medium (8 hours)
- Phase 2 (Model Integration): Medium (8 hours)
- Phase 3 (Migration): Medium (6 hours)
- Phase 4 (Performance): Small (4 hours)
- Testing: Medium (8 hours)
- Documentation: Small (4 hours)

**Total**: 42 hours (1 week for single developer, 3 days for pair)

**Complexity Notes**:
- Key derivation adds complexity but improves security (worth it)
- Migration requires careful testing on production snapshot
- Performance optimization may require query pattern changes
- AWS KMS integration deferred to reduce scope (future enhancement)

---

## Dependencies

### Required (Must be complete first)
- [ ] PostgreSQL database operational
- [ ] SQLAlchemy models defined (`services/database/models.py`)
- [ ] Alembic migration framework working

### Optional (Nice to have)
- [ ] AWS KMS setup (for production key management - can use env var for alpha)
- [ ] Database performance monitoring (to measure overhead)

---

## Related Documentation

- **Architecture**:
  - ADR-012: Protocol-Ready JWT Authentication (auth pattern)
  - ADR-043: Encryption at Rest Strategy (to be created)
- **Code**:
  - `services/security/encryption.py` - Existing Fernet encryption
  - `services/database/models.py` - SQLAlchemy models
- **Security**:
  - GDPR Article 32 requirements
  - SOC2 Type II encryption controls

---

## Evidence Section

[This section is filled in during/after implementation]

### Implementation Evidence
```bash
[Terminal output showing tests passing]
[Commit hashes with descriptions]
[Performance benchmark results]
[Database query showing encrypted values]
```

---

## Completion Checklist

Before requesting PM review:
- [ ] All acceptance criteria met ✅
- [ ] Completion matrix 100% ✅
- [ ] Evidence provided for each criterion ✅
- [ ] Tests passing with output ✅
- [ ] ADR-043 created ✅
- [ ] Security documentation updated ✅
- [ ] No regressions confirmed ✅
- [ ] STOP conditions all clear ✅
- [ ] Session log complete ✅
- [ ] Security review approved ✅

**Status**: Not Started

---

## Notes for Implementation

**From Ted Nadeau review**:
- This is a compliance blocker for SOC2/GDPR
- Prioritize before any production user data
- Consider pgcrypto extension as alternative if application-level encryption proves too complex
- AWS KMS integration can wait for post-alpha

**Security Team Guidance** (to be added):
- Key rotation policy: Every 90 days for alpha
- Master key storage: Environment variable initially, migrate to AWS Secrets Manager
- Audit logging: Log encryption/decryption failures (not content!)

---

**Remember**:
- Security cannot be compromised for speed
- 100% encryption or explain why field excluded
- Performance matters, but security matters more
- Evidence required: Show encrypted data in DB dump

---

_Issue created: November 20, 2025_
_Last updated: November 20, 2025_
_Synthesized from: #324 + #358_

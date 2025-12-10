# S2 Sprint #358: Encryption at Rest - Implementation Gameplan

**Date**: December 9, 2025
**Issue**: #358 - SEC-ENCRYPT-ATREST: Implement Encryption at Rest for Sensitive Data
**Status**: Ready for Execution (awaiting Ted Nadeau's ADR approval)
**Scope**: 6 sensitive fields, application-level AES-256-GCM encryption
**Estimated Duration**: 42 hours total

---

## Overview

This gameplan provides the step-by-step implementation roadmap for S2 encryption work. It follows the architectural decisions in S2-ENCRYPTION-REVIEW-PACKAGE.md and assumes Ted Nadeau's approval of those decisions.

**Execution Phases**:
1. **Phase 0** (4 hours): Investigation & Setup
2. **Phase 1** (8 hours): FieldEncryptionService Implementation
3. **Phase 2** (8 hours): SQLAlchemy Model Integration
4. **Phase 3** (6 hours): Data Migration & Rollback
5. **Phase 4** (4 hours): Performance Validation
6. **Phase 5** (8 hours): Testing & Documentation
7. **Phase 6** (4 hours): PM Handoff & Cleanup

**Total**: 42 hours (distributed across 1-2 weeks)

---

## Phase 0: Investigation & Setup (4 hours)

### Objective
Set up the encryption infrastructure foundation and identify integration points.

### Tasks

#### 0.1 Verify cryptography library & dependencies (30 min)
- ✅ Current: `cryptography==45.0.4` (verified in requirements.txt)
- Verify AES-256-GCM support in cryptography library
- Verify HKDF support in cryptography library
- Document version lock policy for supply chain security

**Acceptance Criteria**:
- [ ] cryptography library version documented
- [ ] AES-256-GCM import test passes (`from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes`)
- [ ] HKDF import test passes (`from cryptography.hazmat.primitives.kdf.hkdf import HKDF`)
- [ ] No version upgrade needed

#### 0.2 Identify SQLAlchemy ORM integration points (1 hour)
- Examine [services/database/models.py](services/database/models.py) for 6 encrypted fields:
  - ConversationDB.content
  - ConversationTurnDB.user_content
  - ConversationTurnDB.assistant_content
  - UploadedFileDB.content
  - PatternDB.pattern_data
  - ApiKeyDB.key_value

**Acceptance Criteria**:
- [ ] All 6 encrypted field locations identified
- [ ] Current column types documented (text, bytea)
- [ ] Current ORM definitions documented
- [ ] No breaking column type changes needed

#### 0.3 Design @encrypted_column decorator pattern (1 hour)
- Research SQLAlchemy hybrid properties and TypeDecorator patterns
- Design @encrypted_column decorator to:
  - Accept field_context parameter (e.g., "conversations.content")
  - Auto-encrypt on save via __set__
  - Auto-decrypt on load via __get__
  - Support both text and binary fields

**Acceptance Criteria**:
- [ ] Decorator design pattern documented
- [ ] TypeDecorator approach selected or alternative chosen
- [ ] Encrypt/decrypt hooks identified in ORM lifecycle
- [ ] No conflicts with existing ORM patterns

#### 0.4 Identify master key storage points (30 min)
- Verify ENCRYPTION_MASTER_KEY environment variable loading pattern
- Check config/services/config.py for configuration management
- Identify where env vars are loaded in ServiceContainer

**Acceptance Criteria**:
- [ ] Master key loading approach documented
- [ ] Configuration integration point identified
- [ ] No hardcoded keys in codebase
- [ ] Ready for Phase 1

#### 0.5 Create test fixtures & helpers (1 hour)
- Create test helpers for consistent encryption/decryption testing
- Set up master key fixture for pytest
- Create sample plaintext data fixtures
- Document test data patterns

**Acceptance Criteria**:
- [ ] Test fixtures created in tests/unit/services/security/
- [ ] Master key fixture works in pytest
- [ ] Sample data fixtures ready for Phase 1 tests

### Phase 0 Success Criteria
- [ ] All 5 tasks completed with acceptance criteria met
- [ ] No blockers identified
- [ ] Ready to proceed to Phase 1
- [ ] Session log updated

---

## Phase 1: FieldEncryptionService Implementation (8 hours)

### Objective
Implement the core encryption/decryption service with HKDF key derivation and AES-256-GCM cipher.

### New File
`services/security/field_encryption_service.py` (~300 lines)

### Implementation Details

#### 1.1 Create FieldEncryptionService class (3 hours)

**Location**: [services/security/field_encryption_service.py](services/security/field_encryption_service.py)

**Requirements**:
```python
class FieldEncryptionService:
    """
    Field-level encryption service using AES-256-GCM + HKDF

    Provides:
    - HKDF-based key derivation (per-field keys from master key)
    - AES-256-GCM encryption with authenticated encryption
    - IV randomization (non-deterministic ciphertext)
    - Binary format: IV (16) + ciphertext + auth_tag (16)
    """

    def __init__(self, master_key: bytes):
        """Initialize with master key (from ENCRYPTION_MASTER_KEY env var)"""

    def derive_key(self, context: str) -> bytes:
        """Derive per-field key using HKDF(master_key, context)"""
        # context = "conversations.content", "conversation_turns.user_content", etc.
        # Returns 32 bytes (256-bit key)

    def encrypt(self, plaintext: str, field_context: str) -> bytes:
        """
        Encrypt plaintext with field-specific key

        Process:
        1. Derive key from master_key + field_context (HKDF)
        2. Generate random IV (16 bytes)
        3. Cipher = AES-256-GCM(key, IV)
        4. Ciphertext + auth_tag = cipher.encryptor.update() + .finalize()
        5. Return: IV + ciphertext + auth_tag (binary blob)

        Returns: bytes (encrypted data)
        """

    def decrypt(self, ciphertext: bytes, field_context: str) -> str:
        """
        Decrypt ciphertext with field-specific key

        Process:
        1. Extract IV (first 16 bytes)
        2. Derive key from master_key + field_context (HKDF)
        3. Cipher = AES-256-GCM(key, IV)
        4. Plaintext = cipher.decryptor.update(ciphertext[16:]) + .finalize()
        5. Return: plaintext (string)

        Raises: cryptography.hazmat.primitives.ciphers.InvalidTag if auth fails

        Returns: str (decrypted plaintext)
        """
```

**Code Structure**:
```python
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import os

class FieldEncryptionService:
    def __init__(self, master_key: bytes):
        if not master_key or len(master_key) < 32:
            raise ValueError("Master key must be at least 32 bytes")
        self.master_key = master_key

    def derive_key(self, context: str) -> bytes:
        """HKDF: master_key + context → field-specific 256-bit key"""
        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=32,  # 256 bits
            salt=None,  # No salt in alpha (documented for KMS migration)
            info=context.encode(),
            backend=default_backend()
        )
        return hkdf.derive(self.master_key)

    def encrypt(self, plaintext: str, field_context: str) -> bytes:
        """Encrypt plaintext → IV + ciphertext + auth_tag"""
        key = self.derive_key(field_context)
        iv = os.urandom(16)  # Random IV for non-determinism

        cipher = Cipher(
            algorithms.AES(key),
            modes.GCM(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()

        # Return: IV (16) + ciphertext + auth_tag (16)
        return iv + ciphertext + encryptor.tag

    def decrypt(self, ciphertext: bytes, field_context: str) -> str:
        """Decrypt IV + ciphertext + auth_tag → plaintext"""
        key = self.derive_key(field_context)
        iv = ciphertext[:16]
        ct_with_tag = ciphertext[16:]

        cipher = Cipher(
            algorithms.AES(key),
            modes.GCM(iv, ct_with_tag[-16:]),  # Last 16 bytes = auth tag
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ct_with_tag[:-16]) + decryptor.finalize()

        return plaintext.decode()
```

**Acceptance Criteria**:
- [ ] FieldEncryptionService class created
- [ ] derive_key() method working (HKDF produces deterministic keys)
- [ ] encrypt() method produces IV + ciphertext + auth_tag format
- [ ] decrypt() method recovers plaintext from ciphertext
- [ ] AuthenticationError raised on tampered ciphertext
- [ ] Non-determinism verified (same plaintext → different ciphertext)

#### 1.2 Create unit tests for FieldEncryptionService (3 hours)

**Location**: [tests/unit/services/security/test_field_encryption_service.py](tests/unit/services/security/test_field_encryption_service.py)

**Test Cases**:
```python
@pytest.mark.smoke
class TestFieldEncryptionService:

    def test_encrypt_decrypt_roundtrip(self):
        """Plaintext → encrypt → decrypt → same plaintext"""

    def test_key_derivation_deterministic(self):
        """Same context always produces same key"""

    def test_different_contexts_produce_different_keys(self):
        """context='conversations.content' ≠ context='api_keys.key_value'"""

    def test_non_deterministic_encryption(self):
        """Same plaintext encrypted twice produces different ciphertext"""

    def test_authentication_prevents_tampering(self):
        """Corrupted ciphertext raises InvalidTag"""

    def test_empty_plaintext(self):
        """Empty string encrypts/decrypts correctly"""

    def test_large_plaintext(self):
        """Large files (>1MB) encrypt/decrypt correctly"""

    def test_unicode_plaintext(self):
        """Unicode strings (emojis, non-ASCII) work correctly"""

    def test_invalid_master_key_raises_error(self):
        """Master key <32 bytes raises ValueError"""
```

**Acceptance Criteria**:
- [ ] All 9 test cases pass
- [ ] Coverage >90% for FieldEncryptionService
- [ ] No test flakiness (<1000 iterations)
- [ ] Tests marked with @pytest.mark.smoke
- [ ] Tests run in <500ms total

#### 1.3 Integrate with ServiceContainer (2 hours)

**Location**: [services/container/service_container.py](services/container/service_container.py)

**Changes**:
1. Add FieldEncryptionService initialization in ServiceContainer.__init__
2. Load ENCRYPTION_MASTER_KEY from environment
3. Register as singleton service
4. Document in ServiceContainer docstring

**Code Pattern**:
```python
class ServiceContainer:
    def __init__(self):
        # ... existing services ...

        # Security services
        master_key = self._load_encryption_master_key()
        self.field_encryption_service = FieldEncryptionService(master_key)

    def _load_encryption_master_key(self) -> bytes:
        """Load master key from ENCRYPTION_MASTER_KEY env var"""
        key_hex = os.getenv("ENCRYPTION_MASTER_KEY")
        if not key_hex:
            raise ValueError("ENCRYPTION_MASTER_KEY environment variable not set")
        return bytes.fromhex(key_hex)
```

**Acceptance Criteria**:
- [ ] FieldEncryptionService integrated in ServiceContainer
- [ ] Master key loading documented
- [ ] Unit test verifies integration
- [ ] ServiceContainer still initializes correctly

### Phase 1 Success Criteria
- [ ] FieldEncryptionService implemented with all methods
- [ ] 9 unit tests pass
- [ ] All acceptance criteria met
- [ ] 0 regressions in existing tests
- [ ] Ready for Phase 2 (ORM integration)

---

## Phase 2: SQLAlchemy Model Integration (8 hours)

### Objective
Integrate encryption transparently into ORM using @encrypted_column decorator pattern.

### New Files
- `services/security/encrypted_column.py` (~150 lines) - TypeDecorator for ORM
- `tests/unit/services/security/test_encrypted_column.py` (~200 lines)

### Implementation Details

#### 2.1 Create EncryptedColumn TypeDecorator (2 hours)

**Pattern**: SQLAlchemy TypeDecorator with event listeners

```python
from sqlalchemy import TypeDecorator, String, LargeBinary, event
from sqlalchemy.ext.declarative import declarative_base

class EncryptedColumn(TypeDecorator):
    """
    SQLAlchemy TypeDecorator for encrypted columns

    Automatically encrypts on save, decrypts on load

    Usage:
        @encrypted_column("conversations.content")
        def content(cls):
            return EncryptedColumn(String)
    """

    impl = LargeBinary  # Store as binary blob
    cache_ok = True

    def __init__(self, plaintext_type, field_context: str, encryption_service=None):
        self.plaintext_type = plaintext_type
        self.field_context = field_context
        self.encryption_service = encryption_service

    def process_bind_param(self, value, dialect):
        """Encrypt on save to database"""
        if value is None:
            return None
        return self.encryption_service.encrypt(value, self.field_context)

    def process_result_value(self, value, dialect):
        """Decrypt on load from database"""
        if value is None:
            return None
        return self.encryption_service.decrypt(value, self.field_context)
```

**Acceptance Criteria**:
- [ ] TypeDecorator created
- [ ] process_bind_param encrypts on save
- [ ] process_result_value decrypts on load
- [ ] None values handled correctly
- [ ] Field context properly parameterized

#### 2.2 Create @encrypted_column decorator (2 hours)

**Pattern**: Hybrid property decorator

```python
def encrypted_column(field_context: str):
    """
    Decorator for encrypted columns in domain models

    Usage:
        @encrypted_column("conversations.content")
        def content(cls):
            return EncryptedColumn(String, field_context)
    """
    # Implementation using hybrid_property or similar
```

**Acceptance Criteria**:
- [ ] Decorator works with hybrid_property
- [ ] Field context properly passed through
- [ ] Transparent encrypt/decrypt in ORM
- [ ] Works with both text and binary fields

#### 2.3 Update 6 model fields (2 hours)

**Changes to [services/database/models.py](services/database/models.py)**:

1. **ConversationDB.content** (line ~650)
   - Old: `content = Column(String, default="")`
   - New: `content = Column(EncryptedColumn(String, "conversations.content"))`

2. **ConversationTurnDB.user_content** (line ~690)
   - Old: `user_content = Column(String, nullable=True)`
   - New: `user_content = Column(EncryptedColumn(String, "conversation_turns.user_content"))`

3. **ConversationTurnDB.assistant_content** (line ~695)
   - Old: `assistant_content = Column(String, nullable=True)`
   - New: `assistant_content = Column(EncryptedColumn(String, "conversation_turns.assistant_content"))`

4. **UploadedFileDB.content** (line ~850)
   - Old: `content = Column(LargeBinary)`
   - New: `content = Column(EncryptedColumn(LargeBinary, "uploaded_files.content"))`

5. **PatternDB.pattern_data** (line ~920)
   - Old: `pattern_data = Column(String)`
   - New: `pattern_data = Column(EncryptedColumn(String, "patterns.pattern_data"))`

6. **ApiKeyDB.key_value** (line ~1050)
   - Old: `key_value = Column(String, nullable=False)`
   - New: `key_value = Column(EncryptedColumn(String, "api_keys.key_value"))`

**Acceptance Criteria**:
- [ ] All 6 fields updated
- [ ] Column types preserved (String → String, LargeBinary → LargeBinary)
- [ ] Field contexts correct and unique
- [ ] No column migrations needed yet (Phase 3)
- [ ] Existing data NOT touched (still plaintext in DB)

#### 2.4 Integration tests (2 hours)

**Location**: [tests/unit/services/security/test_encrypted_column.py](tests/unit/services/security/test_encrypted_column.py)

**Test Cases**:
```python
@pytest.mark.smoke
class TestEncryptedColumn:

    async def test_save_encrypts_conversation_content(self):
        """Save conversation with content → stored as encrypted blob"""

    async def test_load_decrypts_conversation_content(self):
        """Load conversation from DB → content decrypted in memory"""

    async def test_encrypted_data_in_database(self):
        """Query database directly → data is encrypted (not plaintext)"""

    async def test_all_6_fields_encrypt_decrypt(self):
        """All 6 encrypted fields work end-to-end"""

    async def test_plaintext_never_logged(self):
        """Plaintext not in logs or query output"""
```

**Acceptance Criteria**:
- [ ] 5 integration tests pass
- [ ] Tests verify end-to-end encryption/decryption
- [ ] Database query verification included
- [ ] No test flakiness
- [ ] Tests marked with @pytest.mark.smoke

### Phase 2 Success Criteria
- [ ] EncryptedColumn TypeDecorator created and tested
- [ ] @encrypted_column decorator working
- [ ] All 6 model fields updated
- [ ] 5 integration tests pass
- [ ] 0 regressions in existing tests
- [ ] Ready for Phase 3 (data migration)

---

## Phase 3: Data Migration & Rollback (6 hours)

### Objective
Migrate existing plaintext data to encrypted form using shadow column pattern with zero-downtime and rollback capability.

### Migration Strategy: Shadow Columns

**Why Shadow Columns**:
- Zero downtime (no table lock)
- Rollback capability (original data preserved)
- Gradual migration possible
- Safe for production

**Process**:
1. Create shadow columns (e.g., `content_encrypted`)
2. Copy + encrypt existing plaintext → shadow columns
3. Verify data completeness
4. Redirect reads to shadow columns (if needed)
5. Monitor for errors
6. Drop original plaintext columns

### Implementation

#### 3.1 Create Alembic migration script (2 hours)

**Location**: [alembic/versions/XXXXXXX_add_encrypted_columns.py](alembic/versions/)

**Steps**:
```python
# Up: Add 6 shadow columns
def upgrade():
    op.add_column('conversation', Column('content_encrypted', LargeBinary))
    op.add_column('conversation_turn', Column('user_content_encrypted', LargeBinary))
    op.add_column('conversation_turn', Column('assistant_content_encrypted', LargeBinary))
    op.add_column('uploaded_file', Column('content_encrypted', LargeBinary))
    op.add_column('pattern', Column('pattern_data_encrypted', LargeBinary))
    op.add_column('api_key', Column('key_value_encrypted', LargeBinary))

# Down: Remove 6 shadow columns
def downgrade():
    op.drop_column('conversation', 'content_encrypted')
    # ... etc
```

**Acceptance Criteria**:
- [ ] Migration script created
- [ ] All 6 shadow columns added
- [ ] alembic revision --autogenerate validates
- [ ] Rollback script created

#### 3.2 Create data migration script (2 hours)

**Location**: [scripts/migrate_encrypt_data.py](scripts/migrate_encrypt_data.py)

**Functionality**:
```python
async def migrate_encrypt_conversation_content():
    """
    Copy plaintext content → encrypt → store in content_encrypted

    Process:
    1. Query all conversations with plaintext content
    2. Encrypt content using FieldEncryptionService
    3. Store in content_encrypted column
    4. Log progress every 100 rows
    5. Report count at end
    """

async def migrate_all_6_fields():
    """
    Migrate all 6 encrypted fields

    Order:
    1. conversation.content
    2. conversation_turn.user_content
    3. conversation_turn.assistant_content
    4. uploaded_file.content
    5. pattern.pattern_data
    6. api_key.key_value
    """

async def verify_migration():
    """
    Verify migration completeness:
    - Count encrypted rows = count plaintext rows
    - Sample decrypt to verify correctness
    - Check for null/empty values
    """

async def rollback_migration():
    """
    Clear shadow columns (reverse without dropping plaintext)
    Used if migration has issues
    """
```

**Acceptance Criteria**:
- [ ] Migration script created
- [ ] Migrates all 6 fields
- [ ] Progress logging included
- [ ] Verification checks included
- [ ] Rollback capability documented
- [ ] Script tested on staging data

#### 3.3 Test migration (1 hour)

**Location**: [tests/integration/test_migration_encrypt_data.py](tests/integration/test_migration_encrypt_data.py)

**Test Cases**:
```python
@pytest.mark.integration
class TestEncryptionMigration:

    async def test_migrate_conversation_content(self):
        """Create 100 test conversations, migrate, verify encryption"""

    async def test_migration_preserves_data_integrity(self):
        """Migrate and decrypt should produce original data"""

    async def test_migration_handles_empty_values(self):
        """Empty/null content values migrate correctly"""

    async def test_rollback_clears_shadow_columns(self):
        """Rollback clears encrypted data without touching plaintext"""

    async def test_migration_idempotency(self):
        """Running migration twice is safe (no double-encryption)"""
```

**Acceptance Criteria**:
- [ ] 5 integration tests pass
- [ ] Migration tested with 100+ rows per field
- [ ] Rollback tested
- [ ] No data loss
- [ ] Ready for production

#### 3.4 Migration runbook (1 hour)

**Location**: [docs/internal/operations/MIGRATION-ENCRYPT-AT-REST.md](docs/internal/operations/)

**Contents**:
```markdown
## Migration Steps

### Prerequisites
- Backup database
- Set ENCRYPTION_MASTER_KEY environment variable
- Test on staging first

### Execution
1. alembic upgrade head
2. python scripts/migrate_encrypt_data.py
3. Verify: SELECT COUNT(*) FROM conversation WHERE content_encrypted IS NOT NULL

### Verification
- Run test_migration_encrypt_data.py
- Sample decrypt to verify correctness

### Rollback (if needed)
- python scripts/migrate_encrypt_data.py --rollback
- alembic downgrade -1

### Post-Migration
- Update ORM to read from encrypted columns only
- Monitor logs for encryption/decryption errors
```

**Acceptance Criteria**:
- [ ] Runbook created
- [ ] Prerequisites listed
- [ ] Step-by-step execution documented
- [ ] Rollback procedure clear
- [ ] Production-ready

### Phase 3 Success Criteria
- [ ] Alembic migration created and tested
- [ ] Data migration script working
- [ ] 5 integration tests pass
- [ ] Rollback procedure verified
- [ ] Runbook documented
- [ ] Ready for Phase 4 (performance validation)

---

## Phase 4: Performance Validation (4 hours)

### Objective
Verify encryption overhead <5% for reads, <10% for writes.

### Baseline Measurements

#### 4.1 Measure baseline performance (1 hour)

**Location**: [scripts/benchmark_encryption.py](scripts/benchmark_encryption.py)

**Measurements** (before encryption):
- Read conversation by ID: ~10ms
- Write new conversation: ~15ms
- List conversations (10 items): ~20ms
- Search conversations (unencrypted fields): ~5ms

**Target** (with encryption):
- Read: ~10.5ms (5% overhead)
- Write: ~16.5ms (10% overhead)
- List: ~21ms (5% overhead)
- Search: ~5ms (0% - unencrypted fields)

#### 4.2 Run performance tests (2 hours)

**Test Cases**:
```python
@pytest.mark.performance
class TestEncryptionPerformance:

    async def test_read_encrypted_conversation(self):
        """Decrypt on read should be <5% slower"""

    async def test_write_encrypted_conversation(self):
        """Encrypt on write should be <10% slower"""

    async def test_list_encrypted_conversations(self):
        """Decrypt multiple rows <5% slower"""

    async def test_search_unencrypted_fields(self):
        """Search on ID, user_id should be unchanged (0%)"""

    async def test_batch_decrypt(self):
        """1000 row decryption should complete in <5s"""
```

**Acceptance Criteria**:
- [ ] 5 performance tests pass
- [ ] Overhead within targets (<5% reads, <10% writes)
- [ ] No unexpected bottlenecks
- [ ] Batch operations acceptable
- [ ] Report generated

#### 4.3 Document performance characteristics (1 hour)

**Location**: [docs/internal/architecture/current/adrs/](docs/internal/architecture/current/adrs/) (ADR number to be assigned)

**Content**:
```markdown
### Performance Impact

| Operation | Baseline | With Encryption | Overhead |
|-----------|----------|-----------------|----------|
| Read | 10ms | 10.5ms | 5% ✅ |
| Write | 15ms | 16.5ms | 10% ✅ |
| List (10) | 20ms | 21ms | 5% ✅ |
| Search (unencrypted) | 5ms | 5ms | 0% ✅ |

**Conclusion**: Encryption overhead acceptable for production.
```

### Phase 4 Success Criteria
- [ ] Baseline measured
- [ ] 5 performance tests pass
- [ ] All targets met
- [ ] Report documented
- [ ] Ready for Phase 5 (testing)

---

## Phase 5: Testing & Documentation (8 hours)

### Objective
Comprehensive test coverage and documentation.

#### 5.1 Unit test expansion (2 hours)
- FieldEncryptionService: 9 tests (Phase 1) ✅
- EncryptedColumn: 5 tests (Phase 2) ✅
- **Additional**: Edge cases, error handling
  - Corrupted IV
  - Invalid UTF-8 in decryption
  - Master key derivation corner cases

**Target Coverage**: >90% for all new code

#### 5.2 Integration test suite (2 hours)
- Migration tests: 5 tests (Phase 3) ✅
- Performance tests: 5 tests (Phase 4) ✅
- **E2E tests**: User workflows
  - Create → Save → Retrieve → Decrypt
  - Multiple users accessing same conversation
  - Concurrent encryption/decryption

**Target Coverage**: >80% for ORM integration

#### 5.3 Documentation (2 hours)

**Files to Create**:
1. **Implementation ADR**: Encryption at Rest Strategy (architecture decision record - number TBD)
2. **OPERATION-GUIDE**: How to manage encryption in production
3. **TROUBLESHOOTING**: Common encryption issues and fixes
4. **KEY-ROTATION**: 90-day key rotation procedure

#### 5.4 Security audit (2 hours)
- Code review for cryptographic correctness
- Verify no plaintext leaks in logs
- Verify no plaintext in error messages
- Verify proper key handling

### Phase 5 Success Criteria
- [ ] 20+ unit tests pass
- [ ] 10+ integration tests pass
- [ ] Coverage >85% overall
- [ ] 4 documentation files created
- [ ] Security audit passed
- [ ] Ready for Phase 6 (PM handoff)

---

## Phase 6: PM Handoff & Cleanup (4 hours)

### Objective
Final validation, cleanup, and handoff documentation.

#### 6.1 Verification checklist (1 hour)
- [ ] All 6 fields encrypted
- [ ] All tests passing
- [ ] Performance targets met
- [ ] Migration script working
- [ ] Rollback procedure tested
- [ ] Documentation complete
- [ ] Zero test failures
- [ ] Pre-commit hooks passing
- [ ] Git commits clean and organized

#### 6.2 Create final report (2 hours)

**Location**: [dev/2025/12/XX/S2-ENCRYPTION-FINAL-REPORT.md](dev/2025/12/XX/)

**Contents**:
- Executive summary
- Metrics (test count, coverage, performance)
- Deliverables list
- Known limitations
- Post-alpha work (S3 issues)
- Evidence and verification

#### 6.3 GitHub issue closure (30 min)
- Update #358 with completion summary
- Link to implementation ADR
- Link to final report
- Close issue with evidence

#### 6.4 Create S3 child issues (30 min)
- #S3-1: Email Encryption (8-12h)
- #S3-2: Search on Encrypted Fields (16-24h)
- #S3-3: AWS KMS Integration (6-10h)
- #S3-4: Automated Key Rotation (8-12h)

### Phase 6 Success Criteria
- [ ] Verification checklist 100% complete
- [ ] Final report created
- [ ] Issue #358 closed with evidence
- [ ] S3 child issues created
- [ ] All deliverables in git history
- [ ] Session log updated

---

## Implementation Timeline

### Recommended Sequence (1-2 weeks)

**Week 1**:
- **Day 1 (Tuesday)**: Phase 0 (Investigation & Setup) - 4 hours
- **Day 2 (Wednesday)**: Phase 1 (FieldEncryptionService) - 8 hours
- **Day 3 (Thursday)**: Phase 2 (ORM Integration) - 8 hours

**Week 2**:
- **Day 4 (Friday)**: Phase 3 (Data Migration) - 6 hours
- **Day 5 (Monday)**: Phase 4 (Performance) - 4 hours
- **Day 6 (Tuesday)**: Phase 5 (Testing) - 8 hours
- **Day 7 (Wednesday)**: Phase 6 (PM Handoff) - 4 hours

**Estimated Parallel Work**:
- #322 (Singleton Refactor) can start after Phase 0 completes (no blocking dependencies)

---

## Risk Mitigation

### Risk: Master key exposure
- **Mitigation**: Store only in ENCRYPTION_MASTER_KEY env var, never in code
- **Verification**: grep -r "ENCRYPTION_MASTER_KEY" services/ should only show config loading

### Risk: Data corruption during migration
- **Mitigation**: Shadow column approach, verify before dropping plaintext
- **Verification**: Integration test with 100+ rows

### Risk: Performance regression
- **Mitigation**: Benchmark before/after, <5% overhead target
- **Verification**: Performance tests in Phase 4

### Risk: Key rotation complexity
- **Mitigation**: Documented manual process in alpha, automated in S3
- **Verification**: Runbook tested

---

## Success Criteria Summary

**Phase 0**: 5 tasks, infrastructure ready
**Phase 1**: 9 tests passing, FieldEncryptionService working
**Phase 2**: 5 integration tests, ORM integration transparent
**Phase 3**: Migration script verified, rollback tested
**Phase 4**: <5% read overhead, <10% write overhead
**Phase 5**: >85% coverage, 4 documentation files
**Phase 6**: Issue #358 closed, S3 issues created

**Final**: 42 hours total, 0 regressions, production-ready encryption

---

## Dependencies & Blockers

### Blocking on:
- ✅ Ted Nadeau's approval of S2-ENCRYPTION-REVIEW-PACKAGE.md (awaiting)

### Not blocking:
- #322 (Singleton Refactor) - can run in parallel
- S3 issues - deferred until after S2 complete

---

## Appendix: Quick Reference

### Master Key Format
```bash
# Generate 256-bit (32-byte) master key in hex
python -c "import secrets; print(secrets.token_hex(32))"
# Output: 8f6c4d3e2b1a0f9e8d7c6b5a4f3e2d1c0b9a8f7e6d5c4b3a2f1e0d9c8b7a
```

### Environment Setup
```bash
export ENCRYPTION_MASTER_KEY="8f6c4d3e2b1a0f9e8d7c6b5a4f3e2d1c0b9a8f7e6d5c4b3a2f1e0d9c8b7a"
python main.py  # Start application with encryption enabled
```

### Test Execution
```bash
# All encryption tests
python -m pytest tests/unit/services/security/ -v

# Integration tests
python -m pytest tests/integration/test_migration_encrypt_data.py -v

# Performance tests
python -m pytest tests/unit/services/security/ -m performance -v
```

### Verification Commands
```bash
# Check migration status
docker exec piper-postgres psql -U piper -d piper_morgan \
  -c "SELECT COUNT(*) FROM conversation WHERE content_encrypted IS NOT NULL;"

# Verify encryption (should not match plaintext)
docker exec piper-postgres psql -U piper -d piper_morgan \
  -c "SELECT id, content IS NOT NULL, content_encrypted IS NOT NULL FROM conversation LIMIT 5;"
```

---

**Prepared By**: Claude Code (Lead Developer Agent)
**Date**: December 9, 2025
**Issue**: #358 - SEC-ENCRYPT-ATREST
**Status**: Ready for Execution (awaiting Ted Nadeau's ADR approval)

---

_This gameplan is comprehensive and detailed. It provides the Code agent with all necessary information to execute efficiently without requiring PM interaction except at predetermined checkpoints._

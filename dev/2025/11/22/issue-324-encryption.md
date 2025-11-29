# SEC-324: Implement Encryption at Rest for Sensitive Data
**Priority**: P0 (CRITICAL - Compliance showstopper)
**Labels**: `security`, `compliance`, `blocker`, `mvp-required`, `gdpr`, `soc2`
**Effort**: 24-30 hours
**Discovered by**: Ted Nadeau (architectural review)

---

## Problem

**COMPLIANCE FAILURE**: All sensitive data stored in plaintext in PostgreSQL.

**Unencrypted data**:
- Conversation content (user prompts, AI responses)
- Uploaded file content
- Pattern learning data
- User PII (email, metadata)
- API keys and tokens

**Compliance violations**:
- GDPR Article 32 (data protection)
- SOC2 Type II (encryption requirements)
- CCPA (California privacy)
- HIPAA (if healthcare data involved)

**Risk**: Data breach = plaintext exposure of all user data

## Solution

Implement field-level encryption for sensitive columns:
1. Encryption service with key management
2. Transparent encrypt/decrypt on save/load
3. Key rotation capability
4. Performance optimization (<5% overhead)
5. Migration to encrypt existing data

## Acceptance Criteria

### Encryption Implementation
- [ ] Create EncryptionService class
- [ ] Implement AES-256-GCM encryption
- [ ] Create key derivation from master key
- [ ] Add encryption decorators for SQLAlchemy
- [ ] Encrypt sensitive fields on save
- [ ] Decrypt sensitive fields on load

### Fields to Encrypt
- [ ] `conversations.content` - User messages
- [ ] `conversation_turns.user_content` - User input
- [ ] `conversation_turns.assistant_content` - AI responses
- [ ] `uploaded_files.content` - File data
- [ ] `patterns.pattern_data` - Learning data
- [ ] `api_keys.key_value` - API credentials
- [ ] `users.email` - PII (optional, impacts queries)

### Key Management
- [ ] Master key from environment variable (alpha)
- [ ] Key derivation per table/field
- [ ] Key rotation mechanism documented
- [ ] Future: AWS KMS integration plan

### Migration
- [ ] Alembic migration to add encrypted columns
- [ ] Script to encrypt existing data
- [ ] Rollback plan if issues
- [ ] Zero downtime migration strategy

### Performance
- [ ] Benchmark overhead <5% for reads
- [ ] Benchmark overhead <10% for writes
- [ ] Connection pooling unchanged
- [ ] No impact on non-sensitive fields

## Implementation Design

```python
# services/security/encryption.py
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import base64

class EncryptionService:
    def __init__(self, master_key: str):
        self.master_key = base64.b64decode(master_key)

    def encrypt(self, plaintext: str, context: str = "") -> str:
        """Encrypt with AES-256-GCM"""
        # Generate nonce
        nonce = os.urandom(12)

        # Derive key from master + context
        key = self._derive_key(context)

        # Encrypt
        cipher = Cipher(
            algorithms.AES(key),
            modes.GCM(nonce),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()

        # Return base64(nonce + ciphertext + tag)
        return base64.b64encode(
            nonce + ciphertext + encryptor.tag
        ).decode('utf-8')

    def decrypt(self, ciphertext: str, context: str = "") -> str:
        """Decrypt AES-256-GCM"""
        data = base64.b64decode(ciphertext)

        # Extract components
        nonce = data[:12]
        tag = data[-16:]
        ciphertext = data[12:-16]

        # Derive key
        key = self._derive_key(context)

        # Decrypt
        cipher = Cipher(
            algorithms.AES(key),
            modes.GCM(nonce, tag),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()

        return plaintext.decode('utf-8')

# models/mixins/encrypted.py
from sqlalchemy import TypeDecorator, String

class EncryptedType(TypeDecorator):
    impl = String
    cache_ok = True

    def __init__(self, encryption_service, context=""):
        self.encryption_service = encryption_service
        self.context = context
        super().__init__()

    def process_bind_param(self, value, dialect):
        """Encrypt on save"""
        if value is not None:
            return self.encryption_service.encrypt(value, self.context)
        return value

    def process_result_value(self, value, dialect):
        """Decrypt on load"""
        if value is not None:
            return self.encryption_service.decrypt(value, self.context)
        return value

# models/conversation.py
class Conversation(Base):
    __tablename__ = 'conversations'

    id = Column(Integer, primary_key=True)
    # Encrypted field
    content = Column(EncryptedType(encryption_service, "conversation"))
    # Non-encrypted field
    created_at = Column(DateTime)
```

## Migration Strategy

```python
# Migration script (one-time)
async def encrypt_existing_data():
    """Encrypt all existing plaintext data"""

    # Process in batches to avoid memory issues
    batch_size = 1000

    # Encrypt conversations
    offset = 0
    while True:
        conversations = db.query(Conversation)\
            .offset(offset)\
            .limit(batch_size)\
            .all()

        if not conversations:
            break

        for conv in conversations:
            # Re-save to trigger encryption
            conv.content = conv.content  # Triggers EncryptedType

        db.commit()
        offset += batch_size
        print(f"Encrypted {offset} conversations...")
```

## Environment Configuration

```bash
# .env (development)
PIPER_ENCRYPTION_KEY=base64_encoded_32_byte_key_here

# Generate key:
python -c "import os, base64; print(base64.b64encode(os.urandom(32)).decode())"
```

## Performance Testing

```python
# Benchmark encryption overhead
async def benchmark_encryption():
    # Test data
    content = "x" * 1000  # 1KB message

    # Without encryption
    start = time.time()
    for _ in range(10000):
        save_conversation(content)
    plain_time = time.time() - start

    # With encryption
    start = time.time()
    for _ in range(10000):
        save_encrypted_conversation(content)
    encrypted_time = time.time() - start

    overhead = ((encrypted_time - plain_time) / plain_time) * 100
    assert overhead < 5, f"Overhead {overhead}% exceeds 5% target"
```

## Security Testing

```python
# Verify encryption works
async def test_data_encrypted_in_database():
    # Create conversation
    conv = create_conversation("Sensitive user data")

    # Query database directly (bypass ORM)
    raw = db.execute(
        "SELECT content FROM conversations WHERE id = :id",
        {"id": conv.id}
    ).first()

    # Verify it's encrypted (base64, not plaintext)
    assert "Sensitive user data" not in raw.content
    assert is_base64(raw.content)

    # Verify ORM decrypts correctly
    conv_orm = db.query(Conversation).get(conv.id)
    assert conv_orm.content == "Sensitive user data"
```

## Rollout Plan

1. **Phase 1**: Encryption service + tests (6 hours)
2. **Phase 2**: SQLAlchemy integration (6 hours)
3. **Phase 3**: Migration script for existing data (4 hours)
4. **Phase 4**: Performance optimization (4 hours)
5. **Phase 5**: Security audit + documentation (4-6 hours)
6. **Phase 6**: Key rotation mechanism (4 hours)

## Future Enhancements

- AWS KMS integration for key management
- Hardware Security Module (HSM) support
- Encrypted search capabilities (homomorphic)
- Column-level encryption policies
- Automated key rotation

## Risk Assessment

**Without encryption**:
- 🚫 GDPR fines (up to 4% global revenue)
- 🚫 SOC2 audit failure
- 🚫 Data breach = plaintext exposure
- 🚫 Loss of enterprise customers

**With encryption**:
- ✅ GDPR Article 32 compliance
- ✅ SOC2 Type II ready
- ✅ Breach = encrypted data (limited impact)
- ✅ Enterprise security requirements met

---

*CRITICAL: Must be implemented before storing any production user data*

# S3 Sprint (Security MVP) - Deferred Issues from #358

**Date**: December 9, 2025
**Parent Issue**: #358 - SEC-ENCRYPT-ATREST
**Sprint**: S3 (Security MVP - Post-Alpha)
**Status**: Planning (awaiting S2 completion)

---

## Overview

During #358 planning, we identified three implementation phases:
- **S2 (Phase 1)**: Core encryption for 6 fields ✅ In this sprint
- **S3 (Phase 2)**: Advanced features for email & search 📋 Deferred to S3
- **S3 (Phase 3)**: AWS KMS integration 📋 Deferred to S3

This document outlines the three S3 child issues to be created and scheduled.

---

## S3 Issue 1: Email Encryption (Advanced)

**Title**: SEC-ENCRYPT-EMAIL: Implement encryption for user email fields

**Parent**: #358 - SEC-ENCRYPT-ATREST
**Complexity**: Medium
**Effort Estimate**: 8-12 hours

### Why Deferred

Email encryption requires special handling:
1. **Query impact**: Email is used for authentication/filtering (user lookup by email)
2. **Index optimization**: Can't use standard B-tree index on encrypted email
3. **Search complexity**: Requires order-preserving encryption (OPE) or hash-based lookup

### Phase 1 Decision

**In S2**: Don't encrypt email addresses
**Reason**: Can't query encrypted fields without architectural changes

### Phase 2 Approach

**Option A: Order-Preserving Encryption (OPE)**
- Allows range queries on encrypted data
- Trade-off: Less semantically secure than standard encryption
- Use case: Sortable encrypted data

**Option B: Hash-based Lookup**
- Hash email for authentication, keep ciphertext for display
- Trade-off: Can't search or sort
- Use case: Display-only encrypted email

**Recommendation**: Start with Option B (simpler), revisit OPE if needed

### Acceptance Criteria

- [ ] Email addresses encrypted in database
- [ ] Authentication still works (hash-based lookup)
- [ ] Display shows encrypted email to admins (if needed)
- [ ] Documentation on email encryption limitations
- [ ] Tests verify roundtrip encryption/decryption

---

## S3 Issue 2: Search on Encrypted Fields (Advanced)

**Title**: SEC-SEARCH-ENCRYPTED: Implement searchable encryption for sensitive fields

**Parent**: #358 - SEC-ENCRYPT-ATREST
**Complexity**: High
**Effort Estimate**: 16-24 hours

### Why Deferred

Searching on encrypted data is non-trivial:
1. **Index challenge**: Can't index encrypted plaintext
2. **Query problem**: How to find "test" in encrypted conversations?
3. **Architecture**: Requires either OPE, FHE, or separate search index

### Current State (S2)

Encrypted fields are **not searchable** in S2. User can't search conversations.

### Phase 2 Approach

**Option A: Full-Text Search Index**
- Create separate plaintext search index
- Index encrypted + plaintext separately
- Trade-off: Additional storage, sync overhead
- Use case: Fast full-text search on encrypted data

**Option B: Order-Preserving Encryption (OPE)**
- Use OPE for fields that need range queries
- Use standard AES-256-GCM for other fields
- Trade-off: OPE is less secure but enables queries
- Use case: Sortable/searchable encrypted data

**Recommendation**: Start with Option A (safer), provide OPE option for future

### Acceptance Criteria

- [ ] Users can search encrypted conversation content
- [ ] Search returns matching conversations
- [ ] Performance acceptable (<500ms for typical searches)
- [ ] Index stays in sync with encrypted data
- [ ] Documentation on search implementation approach
- [ ] Tests verify search accuracy

---

## S3 Issue 3: AWS KMS Integration (Infrastructure)

**Title**: SEC-KMS-INTEGRATION: Migrate from environment variable to AWS KMS

**Parent**: #358 - SEC-ENCRYPT-ATREST
**Complexity**: Medium
**Effort Estimate**: 6-10 hours

### Why Deferred

KMS is production infrastructure, not needed for alpha:
1. **Alpha**: Single-instance or self-hosted (no KMS)
2. **Production**: Multi-region, high availability (KMS makes sense)
3. **Cost**: KMS adds ~$1/month, not needed for alpha
4. **Operational**: Adds AWS dependency and complexity

### Current State (S2)

Master key loaded from `ENCRYPTION_MASTER_KEY` environment variable.

### Phase 2 Approach

**Migration Path**:
1. Create KMS key in AWS account
2. Encrypt master key with KMS
3. Replace env var loader with KMS loader
4. Test key rotation with KMS
5. Document deployment on AWS

**Implementation**:
```python
# S2: Env var
def load_master_key():
    return os.getenv("ENCRYPTION_MASTER_KEY")

# S3: KMS
def load_master_key():
    if AWS_KMS_AVAILABLE:
        return kms_client.decrypt(encrypted_key_blob)
    else:
        return os.getenv("ENCRYPTION_MASTER_KEY")  # Fallback
```

### Acceptance Criteria

- [ ] Master key stored in AWS KMS
- [ ] Fallback to env var for non-AWS deployments
- [ ] Key rotation via KMS tested
- [ ] Performance acceptable (key fetch <100ms, cached)
- [ ] Documentation on KMS deployment
- [ ] Tests verify KMS key loading

---

## S3 Issue 4: Automated Key Rotation (Operations)

**Title**: SEC-KEY-ROTATION-AUTO: Implement automated 90-day key rotation

**Parent**: #358 - SEC-ENCRYPT-ATREST
**Complexity**: Medium
**Effort Estimate**: 8-12 hours

### Why Deferred

Key rotation can be manual in alpha, automated later:
1. **Alpha**: Manual rotation process (documented)
2. **Production**: Automated via cron or AWS Lambda
3. **Safety**: Manual first, automate after pattern verified

### Current State (S2)

Manual rotation documented, process:
1. Generate new key
2. Run migration script to re-encrypt all data
3. Archive old key
4. Monitor for errors

### Phase 2 Approach

**Automated Rotation**:
```python
# services/security/key_rotation_service.py

class KeyRotationService:
    async def rotate_key_90days(self):
        """
        Scheduled every 90 days via:
        - APScheduler (local), or
        - AWS Lambda + CloudWatch Events (production)
        """
        # 1. Generate new key
        new_key = generate_secure_key()

        # 2. Re-encrypt all data with new key
        for field in ENCRYPTED_FIELDS:
            await re_encrypt_field(field, new_key)

        # 3. Update master key
        update_master_key(new_key)

        # 4. Archive old key
        archive_key(old_key, timestamp=now())

        # 5. Log rotation
        audit_log("Key rotated", new_key_id=new_key.id)
```

### Acceptance Criteria

- [ ] Key rotation happens automatically every 90 days
- [ ] All data re-encrypted with new key
- [ ] Old key archived and kept for audit
- [ ] Rotation monitoring (alerts on failure)
- [ ] Documentation on automation setup
- [ ] Tests verify rotation process

---

## Summary: Three S3 Issues

| Issue | Title | Effort | Complexity |
|-------|-------|--------|-----------|
| **S3-1** | Email Encryption | 8-12h | Medium |
| **S3-2** | Search on Encrypted Fields | 16-24h | High |
| **S3-3** | AWS KMS Integration | 6-10h | Medium |
| **S3-4** | Automated Key Rotation | 8-12h | Medium |
| **TOTAL** | All S3 Features | 38-58h | Medium-High |

---

## Scheduling Recommendation

**S3 Sprint Sequence**:
1. **Priority 1 (Must-Have)**: S3-3 (KMS Integration) - Production requirement
2. **Priority 2 (Should-Have)**: S3-4 (Automated Rotation) - Operational efficiency
3. **Priority 3 (Nice-to-Have)**: S3-1 (Email Encryption) - Limited by index approach
4. **Priority 4 (Nice-to-Have)**: S3-2 (Search) - Architectural complexity

**Recommended Sprint Order**:
- **S3 Sprint Week 1**: S3-3 (KMS Integration)
- **S3 Sprint Week 2**: S3-4 (Automated Rotation)
- **S3 Sprint Week 3**: S3-1 (Email Encryption)
- **S3+ (Future)**: S3-2 (Search on Encrypted Fields)

---

**Prepared By**: Claude Code (Lead Developer Agent)
**Date**: December 9, 2025
**Parent Issue**: #358 - SEC-ENCRYPT-ATREST
**Status**: Planning (child issues to be created)

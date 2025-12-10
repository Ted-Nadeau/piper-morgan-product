# S3 Child Issues to Create - GitHub Issue Templates

**Date**: December 9, 2025
**Parent Issue**: #358 - SEC-ENCRYPT-ATREST
**Status**: Ready to create (copy-paste into GitHub UI)

---

## Issue 1: SEC-ENCRYPT-EMAIL

### Title
```
SEC-ENCRYPT-EMAIL: Implement encryption for user email fields
```

### Body
```markdown
**Parent Issue**: #358 - SEC-ENCRYPT-ATREST
**Sprint**: S3 (Security MVP - Post-Alpha)
**Priority**: Medium
**Complexity**: Medium
**Effort Estimate**: 8-12 hours

## Overview

Email encryption is deferred from S2 because email addresses are used for authentication and queries, requiring special handling with order-preserving encryption (OPE) or hash-based lookup approaches.

## Why Deferred from S2

Email is a searchable/queryable field:
1. User lookup by email (authentication)
2. Email filters (search/list)
3. Can't use standard AES-256-GCM (breaks queries)
4. Requires architectural changes (OPE or hash-based)

## Proposed Approach: Phase 2 (Hash-Based Lookup)

**Option B: Hash-based Lookup** (recommended for S3)
- Hash email for authentication (deterministic)
- Keep ciphertext for display
- Can't search or sort by email
- Simpler than OPE

## Acceptance Criteria

- [ ] Email addresses encrypted in database
- [ ] Authentication/lookup still works (hash-based)
- [ ] Display shows encrypted email to admins if needed
- [ ] Documentation on email encryption limitations
- [ ] Tests verify roundtrip encryption/decryption
- [ ] No regression in auth performance

## Related Issues

- Parent: #358 (SEC-ENCRYPT-ATREST)
- Sibling: S3-2 (search), S3-3 (KMS), S3-4 (key rotation)

---

**Status**: Planned for S3 Sprint
**Prepared**: December 9, 2025
```

---

## Issue 2: SEC-SEARCH-ENCRYPTED

### Title
```
SEC-SEARCH-ENCRYPTED: Implement searchable encryption for sensitive fields
```

### Body
```markdown
**Parent Issue**: #358 - SEC-ENCRYPT-ATREST
**Sprint**: S3 (Security MVP - Post-Alpha)
**Priority**: Medium
**Complexity**: High
**Effort Estimate**: 16-24 hours

## Overview

Searching on encrypted fields requires specialized approaches since standard AES-256-GCM prevents plaintext search. This is deferred from S2 because it requires significant architectural changes.

## Why Deferred from S2

1. **Index challenge**: Can't index encrypted plaintext
2. **Query problem**: How to find 'test' in encrypted conversations?
3. **Architecture**: Requires OPE, FHE, or separate search index
4. **Complexity**: 16-24 hour effort

## Current State (S2)

Encrypted fields are **not searchable** in S2. Users cannot search conversation content.

## Proposed Approach: Phase 2 (Full-Text Search Index)

**Option A: Full-Text Search Index** (recommended for S3)
- Create separate plaintext search index
- Index encrypted + plaintext separately
- Trade-off: Additional storage, sync overhead
- Use case: Fast full-text search on encrypted data

**Alternative: Order-Preserving Encryption (OPE)**
- Use OPE for fields that need range queries
- Use standard AES-256-GCM for other fields
- Trade-off: OPE is less secure but enables queries

## Acceptance Criteria

- [ ] Users can search encrypted conversation content
- [ ] Search returns matching conversations
- [ ] Performance acceptable (<500ms for typical searches)
- [ ] Index stays in sync with encrypted data
- [ ] Documentation on search implementation approach
- [ ] Tests verify search accuracy

## Related Issues

- Parent: #358 (SEC-ENCRYPT-ATREST)
- Sibling: S3-1 (email), S3-3 (KMS), S3-4 (key rotation)

---

**Status**: Planned for S3 Sprint (later)
**Prepared**: December 9, 2025
```

---

## Issue 3: SEC-KMS-INTEGRATION

### Title
```
SEC-KMS-INTEGRATION: Migrate from environment variable to AWS KMS
```

### Body
```markdown
**Parent Issue**: #358 - SEC-ENCRYPT-ATREST
**Sprint**: S3 (Security MVP - Post-Alpha)
**Priority**: High (must-have for production)
**Complexity**: Medium
**Effort Estimate**: 6-10 hours

## Overview

AWS KMS integration is deferred from S2 but prioritized in S3. It's required for production deployments but not needed for alpha (which uses environment variables).

## Why Deferred from S2

KMS is production infrastructure:
1. **Alpha**: Single-instance or self-hosted (no KMS needed)
2. **Production**: Multi-region, high availability (KMS makes sense)
3. **Cost**: KMS adds ~$1/month (not needed for alpha)
4. **Operational**: Adds AWS dependency and complexity

## Current State (S2)

Master key loaded from `ENCRYPTION_MASTER_KEY` environment variable.

## Migration Path (S3)

**Steps**:
1. Create KMS key in AWS account
2. Encrypt master key with KMS
3. Replace env var loader with KMS loader
4. Test key rotation with KMS
5. Document deployment on AWS

**Code Pattern**:
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

## Acceptance Criteria

- [ ] Master key stored in AWS KMS
- [ ] Fallback to env var for non-AWS deployments
- [ ] Key rotation via KMS tested
- [ ] Performance acceptable (key fetch <100ms, cached)
- [ ] Documentation on KMS deployment
- [ ] Tests verify KMS key loading

## Recommended Sequencing

**Priority 1 in S3** - Execute first after #358 S2 completes

## Related Issues

- Parent: #358 (SEC-ENCRYPT-ATREST)
- Sibling: S3-1 (email), S3-2 (search), S3-4 (key rotation)

---

**Status**: Planned for S3 Sprint (Priority 1)
**Prepared**: December 9, 2025
```

---

## Issue 4: SEC-KEY-ROTATION-AUTO

### Title
```
SEC-KEY-ROTATION-AUTO: Implement automated 90-day key rotation
```

### Body
```markdown
**Parent Issue**: #358 - SEC-ENCRYPT-ATREST
**Sprint**: S3 (Security MVP - Post-Alpha)
**Priority**: Medium
**Complexity**: Medium
**Effort Estimate**: 8-12 hours

## Overview

Key rotation can be manual in alpha, automated later. This issue schedules automated 90-day key rotation for S3 sprint.

## Why Deferred from S2

Key rotation can be manual in alpha:
1. **Alpha**: Manual rotation process (documented)
2. **Production**: Automated via cron or AWS Lambda
3. **Safety**: Manual first, automate after pattern verified

## Current State (S2)

Manual rotation documented, process:
1. Generate new key
2. Run migration script to re-encrypt all data
3. Archive old key
4. Monitor for errors

## Phase 2 Approach (S3)

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

## Acceptance Criteria

- [ ] Key rotation happens automatically every 90 days
- [ ] All data re-encrypted with new key
- [ ] Old key archived and kept for audit
- [ ] Rotation monitoring (alerts on failure)
- [ ] Documentation on automation setup
- [ ] Tests verify rotation process

## Recommended Sequencing

**Priority 2 in S3** - Execute after S3-3 (KMS Integration)

## Related Issues

- Parent: #358 (SEC-ENCRYPT-ATREST)
- Sibling: S3-1 (email), S3-2 (search), S3-3 (KMS)

---

**Status**: Planned for S3 Sprint (Priority 2)
**Prepared**: December 9, 2025
```

---

## How to Create These Issues

### Via GitHub Web UI
1. Go to https://github.com/mediajunkie/piper-morgan-product/issues
2. Click "New issue"
3. Copy-paste each issue's Title and Body sections above
4. Click "Create issue"

### Via GitHub CLI (when available)
```bash
gh issue create --title "SEC-ENCRYPT-EMAIL: ..." --body "..."
gh issue create --title "SEC-SEARCH-ENCRYPTED: ..." --body "..."
gh issue create --title "SEC-KMS-INTEGRATION: ..." --body "..."
gh issue create --title "SEC-KEY-ROTATION-AUTO: ..." --body "..."
```

---

**Status**: Template ready, awaiting manual creation or GitHub CLI fix
**Prepared**: December 9, 2025

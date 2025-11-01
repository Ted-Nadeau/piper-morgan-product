# Gameplan: P0 Alpha Blockers Sprint v2.0
**Date**: November 1, 2025, 6:57 AM
**Sprint**: A8 Phase 2.5
**Duration**: 10-15 hours total (revised from 12-18)
**Critical Context**: These block ALL external alpha testing
**Approach**: Option B - Alpha-Ready Auth (defer email until MVP)

---

## Executive Summary

**Situation**: First alpha user (Christian/xian) successfully onboarded Oct 30, but testing revealed 3 critical blockers preventing external alpha invitations.

**Your Mission**: Fix three P0 blockers to enable external alpha testing with proper security.

**Key Decision**: Using **Option B - Alpha-Ready Auth** approach:
- ✅ Proper password hashing (bcrypt)
- ✅ JWT authentication & sessions
- ✅ Login/logout functionality
- ⏭️ Defer password reset + email until MVP
- ⏭️ Manual password assistance for alpha users

---

## System Architecture Overview

```
Web UI (FastAPI) → Service Layer → Domain Layer → Database (PostgreSQL)
         ↓                ↓             ↓              ↓
   [No Auth!]     [Has user_id]   [alpha_users]   [JSONB prefs]
                                   [password_hash]
```

### Critical Discovery from Testing
- System has TWO user tables: `alpha_users` (UUID PKs) and `users` (String PKs)
- Alpha phase uses `alpha_users` exclusively
- `alpha_users.password_hash` field exists but unused (no bcrypt implementation)
- Web tier has ZERO authentication (built as single-user system)
- Configuration mixes generic capabilities with personal data

### Current State
- Database layer: ✅ Multi-user ready (alpha_users table works)
- Service layer: ⚠️ Partially ready (has user_id params but not always used)
- Web layer: ❌ No user awareness at all
- Configuration: ❌ Personal data visible to all users

---

## ISSUE #1: CORE-ALPHA-DATA-LEAK (#280)
**Effort**: Small (2-3 hours)
**Severity**: CRITICAL - Privacy/Security violation
**Priority**: P0 BLOCKER

### The Problem in Detail

The file `config/PIPER.md` was originally designed to define Piper's generic capabilities and personality. However, it accidentally evolved to contain Christian's (the PM's) personal production data:

```markdown
# Current PIPER.md (WRONG - has personal data)
- Q4 2024 Goals: Ship VA project, complete DRAGONS initiative
- Meeting preferences: Mornings work best for deep work
- Current projects: Kind Systems, Veterans Affairs portal
- Team structure: 5 engineers, 2 designers
```

**Every alpha tester sees this personal data!**

### Root Cause

During early development, personal examples were added to PIPER.md for testing. These were never extracted when the multi-user architecture was added. The system loads PIPER.md for ALL users, exposing one user's private information to everyone.

### Implementation Plan

#### Phase -1: Verify Current State (10 minutes)
```bash
cd /path/to/piper-morgan

# Use Serena MCP to locate and examine PIPER.md
serena.view_file("config/PIPER.md")

# Check configuration loading code
serena.find_symbol("ConfigService")
serena.find_symbol("load_piper_md")
```

**Verification Questions**:
- Where is PIPER.md actually loaded?
- Which services consume it?
- How is configuration currently merged with user data?

#### Phase 0: Audit & Extract (45 minutes)

**Step 1: Identify Personal Data**
```bash
# Read current PIPER.md
cat config/PIPER.md

# Create extraction checklist
```

Identify ALL sections containing:
- Personal projects or goals
- Company-specific information
- Individual preferences or examples
- Team structures or names
- Any non-generic data

**Step 2: Create Backup**
```bash
# Backup original
cp config/PIPER.md config/PIPER.md.backup-$(date +%Y%m%d)
git add config/PIPER.md.backup-$(date +%Y%m%d)
git commit -m "BACKUP: PIPER.md before personal data extraction"
```

**Step 3: Extract Personal Data**
```bash
# Extract personal sections to temporary file
# This will be moved to user's database record
cat config/PIPER.md | grep -A 10 -B 10 "personal\|Q4\|VA\|DRAGONS\|Kind Systems" > extracted_personal_data.md
```

#### Phase 1: Create Generic PIPER.md (45 minutes)

**New Structure** (ONLY generic capabilities):
```markdown
# PIPER.md - Generic System Configuration

## Capabilities
- Document analysis and summarization
- Task management and tracking
- Meeting scheduling assistance
- GitHub integration for issue management
- Slack integration for team communication
- Notion integration for documentation
- Calendar integration for scheduling

## Default Personality Traits
- Professional and friendly
- Concise but thorough
- Proactive about clarification
- Respectful of user time
- Adaptive to communication style preferences

## Available Integrations
- GitHub (issue creation, search, repository management)
- Slack (messaging, channel management, notifications)
- Calendar (Google Calendar, schedule checking)
- Notion (document creation, search, database queries)

## System Behaviors
- Learns from user interactions
- Adapts communication style to preferences
- Maintains conversation context
- Provides actionable suggestions
- Respects privacy and data boundaries

## Learning Capabilities
- Pattern recognition from user workflows
- Preference adaptation over time
- Context-aware responses
- Intelligent task prioritization
```

**Critical**: NO personal examples, NO specific projects, NO individual data.

#### Phase 2: Move Personal Data to Database (30 minutes)

**Create Migration Script** (`scripts/migrate_personal_data_to_xian.py`):
```python
"""
One-time migration to move Christian's personal data from PIPER.md
to alpha_users.preferences field.
"""
import asyncio
import json
from database import get_db_session
from sqlalchemy import select
from models.user import AlphaUser

async def migrate_personal_data():
    """Move Christian's personal data to alpha_users table"""

    async with get_db_session() as db:
        # Get Christian's user record
        result = await db.execute(
            select(AlphaUser).where(AlphaUser.username == 'xian')
        )
        user = result.scalar_one_or_none()

        if not user:
            print("ERROR: User 'xian' not found")
            return

        # Personal context to store (extracted from PIPER.md)
        personal_context = {
            "projects": [
                "VA Portal",
                "DRAGONS",
                "Kind Systems"
            ],
            "preferences": {
                "meeting_time": "mornings",
                "communication_style": "direct and systematic",
                "work_focus": "deep work blocks preferred",
                "feedback_style": "detailed with evidence"
            },
            "q4_goals": [
                "Ship VA project",
                "Complete DRAGONS initiative",
                "Launch Piper Morgan alpha"
            ],
            "team": {
                "engineers": 5,
                "designers": 2,
                "role": "Head of Product"
            },
            "context": {
                "company": "Kind Systems",
                "projects": ["VA Portal", "DRAGONS"],
                "methodology": "Systematic, evidence-based, cathedral building"
            }
        }

        # Merge with existing preferences
        current_prefs = user.preferences or {}
        updated_prefs = {**current_prefs, **personal_context}

        # Update user record
        user.preferences = updated_prefs
        await db.commit()

        print(f"✅ Personal data migrated for user 'xian'")
        print(f"   Preferences now include: {list(personal_context.keys())}")

        return user.id

if __name__ == "__main__":
    asyncio.run(migrate_personal_data())
```

**Run Migration**:
```bash
python scripts/migrate_personal_data_to_xian.py
```

#### Phase 3: Update Configuration Loading (45 minutes)

**Modify `services/config/config_service.py`**:
```python
from typing import Optional, Dict, Any
import yaml

class ConfigService:
    def __init__(self, db_session):
        self.db = db_session
        self._piper_md_cache = None

    def load_config(self, user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Load configuration with user-specific overlay.

        Returns generic PIPER.md config, optionally merged with
        user's personal preferences from database.
        """
        # 1. Load generic PIPER.md (cached)
        base_config = self._load_piper_md()

        # 2. If no user, return generic only
        if not user_id:
            return base_config

        # 3. Load user-specific context from database
        user_context = await self._load_user_context(user_id)

        # 4. Merge configs (user overrides base)
        config = self._merge_configs(base_config, user_context)

        return config

    def _load_piper_md(self) -> Dict[str, Any]:
        """Load and cache generic PIPER.md configuration"""
        if self._piper_md_cache:
            return self._piper_md_cache

        with open('config/PIPER.md', 'r') as f:
            content = f.read()

        # Parse markdown sections into dict
        config = self._parse_piper_md(content)
        self._piper_md_cache = config
        return config

    async def _load_user_context(self, user_id: str) -> Dict[str, Any]:
        """Load user-specific preferences from database"""
        from sqlalchemy import select
        from models.user import AlphaUser

        result = await self.db.execute(
            select(AlphaUser).where(AlphaUser.id == user_id)
        )
        user = result.scalar_one_or_none()

        if not user or not user.preferences:
            return {}

        return user.preferences

    def _merge_configs(
        self,
        base: Dict[str, Any],
        user: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Merge user preferences over base configuration"""
        merged = base.copy()

        # User preferences override base
        for key, value in user.items():
            if isinstance(value, dict) and key in merged:
                # Recursive merge for nested dicts
                merged[key] = {**merged.get(key, {}), **value}
            else:
                merged[key] = value

        return merged
```

### Verification Steps

1. **Test with multiple users**:
```bash
# As test user (should see only generic)
export PIPER_USER=test-user-1
python main.py chat "What are my current projects?"
# Expected: "I don't have information about your specific projects yet"

# As Christian (should see personal context)
export PIPER_USER=xian
python main.py chat "What are my current projects?"
# Expected: "Your current projects include VA Portal, DRAGONS, and Kind Systems"
```

2. **Verify no data leakage**:
```bash
# Check PIPER.md has no personal data
grep -i "christian\|xian\|VA\|DRAGONS\|Q4\|Kind Systems" config/PIPER.md
# Expected: No matches found
```

3. **Confirm generic capabilities work**:
```bash
python main.py chat "What can you help me with?"
# Expected: Generic capabilities list, no personal examples
```

### Acceptance Criteria
- [ ] PIPER.md contains zero personal/company data
- [ ] Generic capabilities clearly documented
- [ ] Christian's personal data in alpha_users.preferences
- [ ] ConfigService loads user-specific data correctly
- [ ] Multiple users tested with isolated configs
- [ ] No data leakage between users
- [ ] All tests pass

### Common Pitfalls to Avoid

1. **Don't delete everything** - Keep generic capabilities and personality
2. **Don't hardcode user IDs** - Use dynamic user lookup
3. **Don't forget backup** - Always backup before modifying
4. **Test multi-user** - Actually test with 2+ different users

---

## ISSUE #2: CORE-ALPHA-FILE-UPLOAD (#282)
**Effort**: Small-Medium (2-4 hours)
**Severity**: CRITICAL - Core feature broken
**Priority**: P0 BLOCKER

### The Problem

File upload functionality is completely broken, preventing users from uploading documents for analysis, summarization, or processing. This blocks a core PM workflow.

### Implementation Plan

#### Phase -1: Investigation (30 minutes)

**Use Serena MCP to investigate**:
```python
# Find upload-related code
serena.find_symbol("upload")
serena.find_symbol("UploadFile")
serena.find_symbol("file_upload")

# Check web routes
serena.view_file("web/app.py")

# Check frontend
serena.list_dir("web/static")
serena.view_file("web/static/index.html")
```

**Questions to Answer**:
1. Does `/upload` endpoint exist?
2. Is frontend upload component wired up?
3. Is file storage configured?
4. Is document processor connected?

#### Phase 0: Identify Root Cause (30 minutes)

**Potential Failure Points**:
- Frontend upload button not wired
- API endpoint missing or not registered
- File storage path misconfigured
- Document processor not integrated
- Permission issues on upload directory

**Investigation Steps**:
1. Check if endpoint exists in web/app.py
2. Test endpoint directly with curl
3. Check upload directory exists and is writable
4. Verify file metadata storage in database

#### Phase 1: Fix Broken Component (1-2 hours)

**If endpoint missing**, create:

```python
# web/app.py
from fastapi import UploadFile, File, HTTPException, Depends
import aiofiles
import uuid
from pathlib import Path

# Ensure upload directory exists
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: dict = Depends(require_auth)  # From Issue #281
):
    """Handle file upload with user isolation"""

    # 1. Validate file
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    file_content = await file.read()

    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File too large (max 10MB)"
        )

    ALLOWED_TYPES = {
        'text/plain',
        'application/pdf',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'text/markdown',
        'application/json'
    }

    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type: {file.content_type}"
        )

    # 2. Save file with user isolation
    file_id = str(uuid.uuid4())
    user_dir = UPLOAD_DIR / current_user['user_id']
    user_dir.mkdir(exist_ok=True)

    file_path = user_dir / f"{file_id}_{file.filename}"

    async with aiofiles.open(file_path, 'wb') as f:
        await f.write(file_content)

    # 3. Store metadata in database
    from services.document_service import DocumentService
    doc_service = DocumentService(db)

    doc_id = await doc_service.store_document_metadata(
        user_id=current_user['user_id'],
        file_id=file_id,
        filename=file.filename,
        path=str(file_path),
        content_type=file.content_type,
        size=len(file_content)
    )

    # 4. Process document (extract text, index)
    if file.content_type == 'text/plain':
        text_content = file_content.decode('utf-8')
        await doc_service.index_document(
            document_id=doc_id,
            content=text_content
        )

    return {
        "file_id": file_id,
        "document_id": doc_id,
        "filename": file.filename,
        "size": len(file_content),
        "status": "uploaded",
        "indexed": file.content_type == 'text/plain'
    }
```

**If frontend broken**, fix:

```html
<!-- web/static/index.html -->
<div id="uploadSection" class="upload-section">
    <h3>Upload Document</h3>
    <input type="file" id="fileInput" accept=".txt,.pdf,.docx,.md,.json">
    <button onclick="uploadFile()" class="btn-primary">Upload</button>
    <div id="uploadStatus" class="status-message"></div>
    <div id="uploadProgress" class="progress-bar" style="display: none;">
        <div id="progressFill" class="progress-fill"></div>
    </div>
</div>

<script>
async function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];

    if (!file) {
        showError('Please select a file');
        return;
    }

    const statusDiv = document.getElementById('uploadStatus');
    const progressDiv = document.getElementById('uploadProgress');
    const progressFill = document.getElementById('progressFill');

    statusDiv.textContent = 'Uploading...';
    progressDiv.style.display = 'block';

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData,
            credentials: 'include'  // Include auth cookies
        });

        if (response.ok) {
            const result = await response.json();
            statusDiv.textContent = `✅ Uploaded: ${result.filename} (${formatBytes(result.size)})`;
            statusDiv.className = 'status-success';
            progressFill.style.width = '100%';

            // Clear input
            fileInput.value = '';

            // Hide progress after delay
            setTimeout(() => {
                progressDiv.style.display = 'none';
                progressFill.style.width = '0%';
            }, 2000);
        } else {
            const error = await response.json();
            showError(error.detail || 'Upload failed');
        }
    } catch (error) {
        console.error('Upload error:', error);
        showError('Upload failed - please try again');
    }
}

function formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

function showError(message) {
    const statusDiv = document.getElementById('uploadStatus');
    statusDiv.textContent = '❌ ' + message;
    statusDiv.className = 'status-error';
    document.getElementById('uploadProgress').style.display = 'none';
}
</script>

<style>
.upload-section {
    margin: 20px 0;
    padding: 20px;
    border: 2px dashed #ccc;
    border-radius: 8px;
}

.progress-bar {
    width: 100%;
    height: 20px;
    background-color: #f0f0f0;
    border-radius: 10px;
    overflow: hidden;
    margin-top: 10px;
}

.progress-fill {
    height: 100%;
    background-color: #4CAF50;
    width: 0%;
    transition: width 0.3s ease;
}

.status-message {
    margin-top: 10px;
    padding: 10px;
    border-radius: 4px;
}

.status-success {
    background-color: #d4edda;
    color: #155724;
}

.status-error {
    background-color: #f8d7da;
    color: #721c24;
}
</style>
```

#### Phase 2: Test File Upload (1 hour)

**Test with various file types**:
```bash
# Test text file
echo "Test content" > test.txt
curl -X POST http://localhost:8001/upload \
  -H "Authorization: Bearer TOKEN" \
  -F "file=@test.txt"

# Test PDF
curl -X POST http://localhost:8001/upload \
  -H "Authorization: Bearer TOKEN" \
  -F "file=@document.pdf"

# Test large file (should reject)
dd if=/dev/zero of=large.txt bs=1M count=20
curl -X POST http://localhost:8001/upload \
  -H "Authorization: Bearer TOKEN" \
  -F "file=@large.txt"
# Expected: 413 File too large
```

### Acceptance Criteria
- [ ] Users can upload files via web UI
- [ ] Multiple file types supported (txt, pdf, docx, md, json)
- [ ] Upload progress indication
- [ ] Files properly stored and indexed
- [ ] User-isolated file storage
- [ ] Documents can be referenced in chat
- [ ] Error messages are helpful
- [ ] File size limits enforced (10MB)
- [ ] File type validation works

---

## ISSUE #3: CORE-ALPHA-WEB-AUTH (#281)
**Effort**: Medium (6-8 hours) - **Option B: Alpha-Ready**
**Severity**: CRITICAL - No multi-user support
**Priority**: P0 BLOCKER

### The Problem in Detail

The web UI has zero authentication or session management. Any user can access any session, and there's no user identity verification. This blocks any multi-user deployment.

**Current Code** (NO AUTH):
```python
@app.post("/chat")
async def chat_endpoint(request: Request):
    # NO authentication check
    # NO user verification
    # Anyone can send messages
    # Predictable session IDs
    message = data.get("message", "")
    session_id = data.get("session_id", "default_session")
    result = await intent_service.process_intent(message, session_id)
    return {"response": result.message}
```

### Option B: Alpha-Ready Auth (Recommended)

**What's Included**:
- ✅ Bcrypt password hashing
- ✅ JWT token generation/validation
- ✅ Login/logout endpoints
- ✅ Auth middleware
- ✅ Session management
- ✅ User context passing
- ✅ Admin script to set passwords

**What's Deferred to MVP**:
- ⏭️ Password reset flow
- ⏭️ Email service integration
- ⏭️ "Forgot password" UI

**Rationale**:
- Alpha testers are trusted (5-10 known people)
- Manual password assistance acceptable for alpha
- Email system can wait until MVP
- Faster path to external alpha testing

### Implementation Plan

#### Phase -1: Verify Existing Infrastructure (20 minutes)

**Use Serena MCP**:
```python
# Check alpha_users table structure
serena.find_symbol("AlphaUser")
serena.find_symbol("password_hash")

# Look for any existing auth code
serena.find_symbol("JWT")
serena.find_symbol("authenticate")
serena.find_symbol("login")

# Check if bcrypt is installed
# pip list | grep bcrypt
```

**Verification Questions**:
- Does alpha_users.password_hash field exist?
- Is bcrypt in requirements.txt?
- Are there any auth stubs to build on?

#### Phase 0: Install Dependencies (15 minutes)

**Add to `requirements.txt`**:
```
bcrypt==4.1.1
pyjwt==2.8.0
python-multipart==0.0.6  # For form data
```

**Install**:
```bash
pip install bcrypt pyjwt python-multipart --break-system-packages
```

**Verify**:
```python
python -c "import bcrypt; print(bcrypt.gensalt())"
python -c "import jwt; print(jwt.__version__)"
```

#### Phase 1: Password Hashing Service (1 hour)

**Create `services/auth/password_service.py`**:
```python
"""
Password hashing and verification service using bcrypt.
"""
import bcrypt
from typing import Optional

class PasswordService:
    """Handles password hashing and verification"""

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using bcrypt.

        Args:
            password: Plain text password

        Returns:
            Hashed password as string
        """
        # Generate salt and hash password
        salt = bcrypt.gensalt(rounds=12)  # 12 rounds is good balance
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """
        Verify a password against its hash.

        Args:
            password: Plain text password to verify
            hashed: Stored password hash

        Returns:
            True if password matches, False otherwise
        """
        try:
            return bcrypt.checkpw(
                password.encode('utf-8'),
                hashed.encode('utf-8')
            )
        except Exception:
            return False

    @staticmethod
    def generate_temp_password(length: int = 16) -> str:
        """
        Generate a temporary secure password.

        Args:
            length: Password length (default 16)

        Returns:
            Random secure password
        """
        import secrets
        import string

        alphabet = string.ascii_letters + string.digits + "!@#$%^&*()"
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        return password

# Example usage
if __name__ == "__main__":
    ps = PasswordService()

    # Hash a password
    password = "secure_alpha_password_123"
    hashed = ps.hash_password(password)
    print(f"Hashed: {hashed}")

    # Verify correct password
    is_valid = ps.verify_password(password, hashed)
    print(f"Valid: {is_valid}")  # True

    # Verify wrong password
    is_valid = ps.verify_password("wrong_password", hashed)
    print(f"Wrong: {is_valid}")  # False
```

**Test**:
```bash
python services/auth/password_service.py
```

#### Phase 2: JWT Token Service (1 hour)

**Create `services/auth/jwt_service.py`**:
```python
"""
JWT token generation and validation service.
"""
import jwt
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

class JWTService:
    """Handles JWT token generation and validation"""

    def __init__(self):
        self.secret_key = os.getenv(
            'JWT_SECRET_KEY',
            'alpha-jwt-secret-change-in-production'  # Default for alpha only
        )
        self.algorithm = 'HS256'
        self.access_token_expire_hours = 24  # 24 hours for alpha

    def generate_token(
        self,
        user_id: str,
        username: str,
        additional_claims: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate JWT access token.

        Args:
            user_id: User's UUID
            username: User's username
            additional_claims: Optional additional claims

        Returns:
            JWT token as string
        """
        expire = datetime.utcnow() + timedelta(
            hours=self.access_token_expire_hours
        )

        payload = {
            'user_id': user_id,
            'username': username,
            'exp': expire,
            'iat': datetime.utcnow(),
            'type': 'access'
        }

        if additional_claims:
            payload.update(additional_claims)

        token = jwt.encode(
            payload,
            self.secret_key,
            algorithm=self.algorithm
        )

        return token

    def validate_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Validate JWT token and return payload.

        Args:
            token: JWT token string

        Returns:
            Decoded payload if valid, None if invalid
        """
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            return payload
        except jwt.ExpiredSignatureError:
            # Token expired
            return None
        except jwt.InvalidTokenError:
            # Invalid token
            return None

    def decode_token_unsafe(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Decode token without validation (for debugging).

        Args:
            token: JWT token string

        Returns:
            Decoded payload (unverified)
        """
        try:
            return jwt.decode(
                token,
                options={"verify_signature": False}
            )
        except Exception:
            return None

# Example usage
if __name__ == "__main__":
    jwt_service = JWTService()

    # Generate token
    token = jwt_service.generate_token(
        user_id="user-123",
        username="xian"
    )
    print(f"Token: {token}")

    # Validate token
    payload = jwt_service.validate_token(token)
    print(f"Payload: {payload}")
```

**Test**:
```bash
python services/auth/jwt_service.py
```

#### Phase 3: Auth Endpoints (1.5 hours)

**Create `web/routes/auth.py`**:
```python
"""
Authentication endpoints for login/logout.
"""
from fastapi import APIRouter, HTTPException, Response, Cookie, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db_session
from models.user import AlphaUser
from services.auth.password_service import PasswordService
from services.auth.jwt_service import JWTService

router = APIRouter(prefix="/auth", tags=["authentication"])

# Initialize services
password_service = PasswordService()
jwt_service = JWTService()

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    token: str
    user_id: str
    username: str
    message: str

@router.post("/login", response_model=LoginResponse)
async def login(
    request: LoginRequest,
    response: Response,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Authenticate user and return JWT token.

    Sets token in HTTP-only cookie for web UI.
    Also returns token in response for API clients.
    """
    # 1. Find user in alpha_users
    result = await db.execute(
        select(AlphaUser).where(AlphaUser.username == request.username)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    # 2. Verify password
    if not user.password_hash:
        raise HTTPException(
            status_code=401,
            detail="Password not set. Contact administrator."
        )

    is_valid = password_service.verify_password(
        request.password,
        user.password_hash
    )

    if not is_valid:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    # 3. Generate JWT token
    token = jwt_service.generate_token(
        user_id=str(user.id),
        username=user.username
    )

    # 4. Set HTTP-only cookie for web UI
    response.set_cookie(
        key="auth_token",
        value=token,
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite="lax",
        max_age=24 * 60 * 60  # 24 hours
    )

    return LoginResponse(
        token=token,
        user_id=str(user.id),
        username=user.username,
        message="Login successful"
    )

@router.post("/logout")
async def logout(response: Response):
    """
    Logout user by clearing auth cookie.
    """
    response.delete_cookie(key="auth_token")
    return {"message": "Logout successful"}

@router.get("/me")
async def get_current_user(
    auth_token: str = Cookie(None),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get current authenticated user info.
    """
    if not auth_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # Validate token
    payload = jwt_service.validate_token(auth_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    # Get user from database
    result = await db.execute(
        select(AlphaUser).where(AlphaUser.id == payload['user_id'])
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return {
        "user_id": str(user.id),
        "username": user.username,
        "email": user.email
    }
```

**Register router in `web/app.py`**:
```python
from web.routes.auth import router as auth_router

app.include_router(auth_router)
```

#### Phase 4: Auth Middleware (1 hour)

**Create `web/middleware/auth.py`**:
```python
"""
Authentication middleware for protected endpoints.
"""
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Dict, Any

from services.auth.jwt_service import JWTService

jwt_service = JWTService()
security = HTTPBearer(auto_error=False)

async def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Dict[str, Any]:
    """
    Dependency to get current authenticated user.

    Checks for token in:
    1. Authorization header (Bearer token)
    2. Cookie (auth_token)

    Returns user payload if valid, raises 401 if not.
    """
    token = None

    # Try Authorization header first
    if credentials:
        token = credentials.credentials

    # Try cookie if no header
    if not token:
        token = request.cookies.get("auth_token")

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    # Validate token
    payload = jwt_service.validate_token(token)
    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    return payload

async def require_auth(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Dependency that requires authentication.

    Use this on endpoints that need authentication.
    """
    return current_user

# Optional: Check for specific permissions
async def require_admin(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Dependency that requires admin privileges.

    (Not needed for alpha, but shows pattern)
    """
    if not current_user.get('is_admin', False):
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )
    return current_user
```

**Protect existing endpoints in `web/app.py`**:
```python
from web.middleware.auth import require_auth

@app.post("/chat")
async def chat_endpoint(
    request: Request,
    current_user: Dict = Depends(require_auth)  # ← ADD THIS
):
    """Chat endpoint - now requires authentication"""
    data = await request.json()
    message = data.get("message", "")

    # Use authenticated user's ID for session
    user_id = current_user['user_id']
    session_id = f"{user_id}:{data.get('session_id', 'default')}"

    # Process with user context
    result = await intent_service.process_intent(
        message,
        session_id,
        user_id=user_id  # ← PASS USER CONTEXT
    )
    return {"response": result.message}

# Protect all other endpoints similarly
@app.get("/status")
async def status(current_user: Dict = Depends(require_auth)):
    ...

@app.post("/upload")
async def upload(
    file: UploadFile,
    current_user: Dict = Depends(require_auth)
):
    ...
```

#### Phase 5: Admin Password Setup Script (45 minutes)

**Create `scripts/setup_alpha_passwords.py`**:
```python
"""
Admin script to set passwords for alpha users.

Usage:
    python scripts/setup_alpha_passwords.py xian
    python scripts/setup_alpha_passwords.py --all
"""
import asyncio
import argparse
from sqlalchemy import select

from database import get_db_session
from models.user import AlphaUser
from services.auth.password_service import PasswordService

password_service = PasswordService()

async def set_user_password(username: str, password: Optional[str] = None):
    """Set password for a specific user"""
    async with get_db_session() as db:
        result = await db.execute(
            select(AlphaUser).where(AlphaUser.username == username)
        )
        user = result.scalar_one_or_none()

        if not user:
            print(f"❌ User '{username}' not found")
            return False

        # Generate password if not provided
        if not password:
            password = password_service.generate_temp_password()
            print(f"Generated password: {password}")

        # Hash and store
        hashed = password_service.hash_password(password)
        user.password_hash = hashed
        await db.commit()

        print(f"✅ Password set for user '{username}'")
        print(f"   User ID: {user.id}")
        print(f"   Username: {user.username}")
        print(f"   Email: {user.email or 'Not set'}")

        return True

async def set_all_passwords():
    """Set passwords for all users without passwords"""
    async with get_db_session() as db:
        result = await db.execute(
            select(AlphaUser).where(
                (AlphaUser.password_hash == None) |
                (AlphaUser.password_hash == '')
            )
        )
        users = result.scalars().all()

        if not users:
            print("✅ All users already have passwords")
            return

        print(f"Found {len(users)} users without passwords:")
        print()

        credentials = []
        for user in users:
            password = password_service.generate_temp_password()
            hashed = password_service.hash_password(password)
            user.password_hash = hashed

            credentials.append({
                'username': user.username,
                'password': password,
                'email': user.email
            })

            print(f"  {user.username}: {password}")

        await db.commit()

        print()
        print("✅ Passwords set for all users")
        print()
        print("IMPORTANT: Save these credentials securely and share with users!")

        return credentials

async def main():
    parser = argparse.ArgumentParser(
        description="Set passwords for alpha users"
    )
    parser.add_argument(
        'username',
        nargs='?',
        help='Username to set password for'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Set passwords for all users without passwords'
    )
    parser.add_argument(
        '--password',
        help='Specific password to set (if not provided, generates random)'
    )

    args = parser.parse_args()

    if args.all:
        await set_all_passwords()
    elif args.username:
        await set_user_password(args.username, args.password)
    else:
        parser.print_help()

if __name__ == "__main__":
    asyncio.run(main())
```

**Usage**:
```bash
# Set password for xian (generates random)
python scripts/setup_alpha_passwords.py xian

# Set specific password for xian
python scripts/setup_alpha_passwords.py xian --password "my_secure_password"

# Set passwords for all users without passwords
python scripts/setup_alpha_passwords.py --all
```

#### Phase 6: Login UI (1 hour)

**Create `web/static/login.html`**:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Piper Morgan - Login</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .login-container {
            background: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            width: 100%;
            max-width: 400px;
        }

        .logo {
            text-align: center;
            margin-bottom: 30px;
        }

        .logo h1 {
            color: #667eea;
            font-size: 28px;
            font-weight: 600;
        }

        .logo p {
            color: #666;
            font-size: 14px;
            margin-top: 5px;
        }

        .form-group {
            margin-bottom: 20px;
        }

        .form-group label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 500;
        }

        .form-group input {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 6px;
            font-size: 16px;
            transition: border-color 0.3s;
        }

        .form-group input:focus {
            outline: none;
            border-color: #667eea;
        }

        .btn-login {
            width: 100%;
            padding: 14px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.3s;
        }

        .btn-login:hover {
            background: #5568d3;
        }

        .btn-login:disabled {
            background: #ccc;
            cursor: not-allowed;
        }

        .error-message {
            background: #fee;
            color: #c33;
            padding: 12px;
            border-radius: 6px;
            margin-bottom: 20px;
            display: none;
        }

        .error-message.show {
            display: block;
        }

        .help-text {
            text-align: center;
            margin-top: 20px;
            color: #666;
            font-size: 14px;
        }

        .help-text a {
            color: #667eea;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="logo">
            <h1>🏰 Piper Morgan</h1>
            <p>Alpha Testing Portal</p>
        </div>

        <div id="errorMessage" class="error-message"></div>

        <form id="loginForm" onsubmit="handleLogin(event)">
            <div class="form-group">
                <label for="username">Username</label>
                <input
                    type="text"
                    id="username"
                    name="username"
                    required
                    autocomplete="username"
                    placeholder="Enter your username"
                >
            </div>

            <div class="form-group">
                <label for="password">Password</label>
                <input
                    type="password"
                    id="password"
                    name="password"
                    required
                    autocomplete="current-password"
                    placeholder="Enter your password"
                >
            </div>

            <button type="submit" id="loginBtn" class="btn-login">
                Sign In
            </button>
        </form>

        <div class="help-text">
            <p>Need help? Contact the admin for password assistance.</p>
        </div>
    </div>

    <script>
        async function handleLogin(event) {
            event.preventDefault();

            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const loginBtn = document.getElementById('loginBtn');
            const errorMsg = document.getElementById('errorMessage');

            // Clear previous error
            errorMsg.classList.remove('show');
            errorMsg.textContent = '';

            // Disable button
            loginBtn.disabled = true;
            loginBtn.textContent = 'Signing in...';

            try {
                const response = await fetch('/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ username, password })
                });

                if (response.ok) {
                    const data = await response.json();

                    // Store token in localStorage for API calls
                    localStorage.setItem('auth_token', data.token);
                    localStorage.setItem('user_id', data.user_id);
                    localStorage.setItem('username', data.username);

                    // Redirect to main app
                    window.location.href = '/';
                } else {
                    const error = await response.json();
                    showError(error.detail || 'Login failed. Please try again.');
                }
            } catch (error) {
                console.error('Login error:', error);
                showError('Connection error. Please try again.');
            } finally {
                loginBtn.disabled = false;
                loginBtn.textContent = 'Sign In';
            }
        }

        function showError(message) {
            const errorMsg = document.getElementById('errorMessage');
            errorMsg.textContent = message;
            errorMsg.classList.add('show');
        }

        // Check if already logged in
        window.addEventListener('DOMContentLoaded', async () => {
            const token = localStorage.getItem('auth_token');
            if (token) {
                try {
                    const response = await fetch('/auth/me', {
                        headers: {
                            'Authorization': `Bearer ${token}`
                        }
                    });

                    if (response.ok) {
                        // Already logged in, redirect
                        window.location.href = '/';
                    }
                } catch (error) {
                    // Token invalid, stay on login page
                    localStorage.clear();
                }
            }
        });
    </script>
</body>
</html>
```

**Update `web/app.py` to serve login page**:
```python
from fastapi.responses import FileResponse

@app.get("/login")
async def login_page():
    """Serve login page"""
    return FileResponse("web/static/login.html")

# Redirect root to login if not authenticated
@app.get("/")
async def root(auth_token: str = Cookie(None)):
    """Serve main app or redirect to login"""
    if not auth_token:
        return RedirectResponse(url="/login")

    # Validate token
    payload = jwt_service.validate_token(auth_token)
    if not payload:
        return RedirectResponse(url="/login")

    return FileResponse("web/static/index.html")
```

#### Phase 7: Testing (1 hour)

**Test Checklist**:
```bash
# 1. Set up test user password
python scripts/setup_alpha_passwords.py xian --password "test_password_123"

# 2. Test login endpoint
curl -X POST http://localhost:8001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "xian", "password": "test_password_123"}'
# Expected: Returns token

# 3. Test with wrong password
curl -X POST http://localhost:8001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "xian", "password": "wrong_password"}'
# Expected: 401 error

# 4. Test protected endpoint without auth
curl http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "hello"}'
# Expected: 401 error

# 5. Test protected endpoint with auth
curl http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{"message": "hello"}'
# Expected: Success

# 6. Test web UI login
# Open browser to http://localhost:8001/login
# Enter username and password
# Should redirect to main app
```

**Multi-User Testing**:
```bash
# Create second test user
python scripts/create_alpha_user.py --username test-user-2 --email test2@example.com
python scripts/setup_alpha_passwords.py test-user-2

# Test in different browsers:
# - Chrome: Login as xian
# - Chrome Incognito: Login as test-user-2
# - Verify sessions are isolated
# - Verify no data leakage between users
```

### Acceptance Criteria
- [ ] Login page implemented and functional
- [ ] JWT tokens properly generated and validated
- [ ] Bcrypt password hashing working
- [ ] All API endpoints require authentication
- [ ] Sessions isolated by user
- [ ] Logout clears session properly
- [ ] User context available in all handlers
- [ ] Multi-user testing confirms isolation
- [ ] Admin script can set passwords
- [ ] Security best practices followed
- [ ] No passwords in logs or errors

### Common Pitfalls

1. **Token in logs**: Never log JWT tokens or passwords
2. **Hardcoded secrets**: Use environment variables
3. **Weak passwords**: Enforce minimum password strength for production
4. **Session fixation**: Generate new session ID after login
5. **CORS issues**: Configure CORS properly for frontend

---

## Execution Order & Dependencies

### Recommended Order:

1. **First: Data Leak** (2-3 hours)
   - No dependencies
   - Quick win
   - Immediately improves security
   - Can work in parallel with other issues

2. **Second: File Upload** (2-4 hours)
   - Easier than auth
   - Can test while doing auth
   - Unblocks document workflows
   - Needs auth from Issue #3 (but can stub it temporarily)

3. **Third: Web Auth** (6-8 hours)
   - Most complex
   - Do when fresh
   - Completes the foundation for alpha testing

### Parallel Approach (if using multiple agents):

**Agent 1 (Code)**: Data Leak + File Upload (4-7 hours total)
**Agent 2 (Cursor)**: Web Auth (6-8 hours)
**Integration**: Test together after both complete

---

## Success Criteria

### Sprint Complete When:

1. **Data Leak Fixed**:
   - [ ] PIPER.md contains zero personal data
   - [ ] Christian's data in database
   - [ ] Other users see only generic info
   - [ ] Tested with 2+ users

2. **Auth Working**:
   - [ ] Login/logout functional
   - [ ] Sessions isolated by user
   - [ ] All endpoints protected
   - [ ] Multi-user test passes
   - [ ] Passwords properly hashed

3. **Upload Functional**:
   - [ ] Files upload successfully
   - [ ] Multiple formats supported
   - [ ] Security validations work
   - [ ] Documents referenceable in chat

### Ready for External Alpha When:
- ✅ All P0 issues resolved
- ✅ PM can create second test user
- ✅ Second user sees no personal data
- ✅ Basic flows work end-to-end
- ✅ No security vulnerabilities
- ✅ Multi-user testing successful

---

## Common Blockers & Solutions

### "I can't find the code"
Use Serena MCP to search:
```python
serena.find_symbol("upload")
serena.find_symbol("auth")
serena.find_symbol("ConfigService")
serena.view_file("path/to/file.py")
```

### "Tests are failing"
These changes will break existing tests that assume no auth:
```python
# Update test fixtures to include auth
@pytest.fixture
async def authenticated_client():
    client = TestClient(app)
    # Login first
    response = client.post("/auth/login", json={
        "username": "test_user",
        "password": "test_password"
    })
    token = response.json()["token"]
    client.headers["Authorization"] = f"Bearer {token}"
    return client

# Use in tests
async def test_chat_requires_auth(authenticated_client):
    response = authenticated_client.post("/chat", json={
        "message": "hello"
    })
    assert response.status_code == 200
```

### "Database migrations failing"
The alpha_users table already exists:
```sql
-- Check what exists
\dt alpha_users
\d alpha_users

-- Verify password_hash column exists
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'alpha_users';
```

### "Can't test multi-user locally"
Use different browsers or incognito windows:
- Chrome normal: User 1
- Chrome incognito: User 2
- Firefox: User 3

---

## Deferred to MVP (Not in This Sprint)

The following are **intentionally deferred** to MVP milestone:

1. **Password Reset Flow** ⏭️
   - "Forgot password" UI
   - Reset token generation
   - Reset token validation
   - Reset link email

2. **Email System** ⏭️
   - SendGrid integration
   - Email templates
   - Domain verification
   - SMTP configuration

3. **Advanced Auth Features** ⏭️
   - OAuth integration (Google, GitHub)
   - Two-factor authentication
   - Password strength requirements
   - Account lockout after failed attempts

**Rationale**: Alpha testing with 5-10 trusted users doesn't need these features. Manual password assistance is acceptable. We can add these features before opening to wider MVP audience.

---

## Go/No-Go Checklist

### Before Starting:
- [ ] All 3 P0 issues in GitHub (#280, #281, #282)
- [ ] Test environment ready
- [ ] Database backup taken
- [ ] Can rollback if needed
- [ ] 10-15 hours allocated
- [ ] Coding agents ready (Code and/or Cursor)

### After Completion:
- [ ] All 3 issues resolved
- [ ] Multi-user test passes (2+ users)
- [ ] No personal data exposed
- [ ] Auth properly securing endpoints
- [ ] File upload working end-to-end
- [ ] Ready to invite external alpha tester

---

## Timeline Estimate

**Optimistic** (everything works): 10 hours
**Realistic** (some debugging needed): 12-13 hours
**Pessimistic** (significant issues found): 15 hours

**Most Likely**: 12-13 hours over 2 days

---

## Final Notes

**Remember**: These are BLOCKERS. Nothing else matters until these are fixed. Don't get distracted by other issues, improvements, or refactoring. Fix these three things, verify they work, then celebrate being ready to invite your first external alpha tester!

**You're Close**: The system is 95% complete. These final blockers are well-understood with clear solutions. The foundation is solid. This is the home stretch before external alpha testing!

Good luck! You're about to unlock external alpha testing! 🚀🏰

---

**Version**: 2.0
**Last Updated**: November 1, 2025, 6:57 AM PT
**Changes from v1.0**:
- Auth reduced to Option B (6-8h vs 8-12h)
- Email system deferred to MVP
- Password reset deferred to MVP
- Total estimate: 10-15h (down from 12-18h)
- Added detailed bcrypt implementation
- Added admin password setup script
- Clarified what's included vs deferred

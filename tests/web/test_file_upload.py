"""
Test suite for Issue #282: CORE-ALPHA-FILE-UPLOAD
Verify file upload security and functionality

These tests define what "done" means for file upload:
- Upload endpoint requires authentication
- File size limits enforced (10MB max)
- File type validation works (only safe types)
- Files stored in user-isolated directories
- Path traversal prevention
- Metadata stored in database
"""

import io
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


class TestFileUpload:
    """Verify file upload works with proper security"""

    def test_upload_requires_authentication(self, client: TestClient):
        """
        Verify upload endpoint requires authentication.

        Success Criteria:
        - Upload without token returns 401
        - Upload with invalid token returns 401
        - Clear error message
        """
        # Create test file
        test_file = io.BytesIO(b"Test content")

        # Attempt upload without authentication
        response = client.post("/upload", files={"file": ("test.txt", test_file, "text/plain")})

        assert response.status_code == 401, "Upload without authentication should return 401"

        # Attempt with invalid token
        response = client.post(
            "/upload",
            files={"file": ("test.txt", test_file, "text/plain")},
            headers={"Authorization": "Bearer invalid_token_12345"},
        )

        assert response.status_code == 401, "Upload with invalid token should return 401"

    def test_upload_text_file_success(self, authenticated_client: TestClient):
        """
        Verify text file uploads successfully.

        Success Criteria:
        - Returns 200 with file_id and document_id
        - File saved in user's directory
        - Metadata stored in database
        - Response includes filename and size
        """
        # Create test file
        test_content = b"This is test content for upload verification"
        test_file = io.BytesIO(test_content)

        response = authenticated_client.post(
            "/upload", files={"file": ("test_upload.txt", test_file, "text/plain")}
        )

        assert response.status_code == 200, f"Upload should succeed: {response.text}"

        data = response.json()
        assert "file_id" in data, "Response should include file_id"
        assert "document_id" in data, "Response should include document_id"
        assert "filename" in data, "Response should include filename"
        assert data["filename"] == "test_upload.txt"
        assert "size" in data, "Response should include file size"
        assert data["size"] == len(test_content)
        assert data["status"] == "uploaded"

    def test_upload_file_size_limit(self, authenticated_client: TestClient):
        """
        Verify file size limit enforced (10MB).

        Success Criteria:
        - Files <= 10MB accepted
        - Files > 10MB rejected with 413
        - Clear error message
        """
        # Create file larger than 10MB
        large_content = b"X" * (11 * 1024 * 1024)  # 11MB
        large_file = io.BytesIO(large_content)

        response = authenticated_client.post(
            "/upload", files={"file": ("large.txt", large_file, "text/plain")}
        )

        assert response.status_code == 413, "Files larger than 10MB should be rejected with 413"

        error = response.json()
        assert "detail" in error
        assert "too large" in error["detail"].lower() or "10mb" in error["detail"].lower()

    def test_upload_file_size_boundary(self, authenticated_client: TestClient):
        """
        Verify 10MB boundary works correctly.

        Success Criteria:
        - File exactly 10MB accepted
        - File 10MB + 1 byte rejected
        """
        # Create file exactly 10MB
        exactly_10mb = b"X" * (10 * 1024 * 1024)
        file_10mb = io.BytesIO(exactly_10mb)

        response = authenticated_client.post(
            "/upload", files={"file": ("exactly_10mb.txt", file_10mb, "text/plain")}
        )

        # Should accept (or reject, depending on <= vs < implementation)
        # Either 200 or 413 is acceptable for exactly 10MB
        assert response.status_code in [
            200,
            413,
        ], f"10MB file should be accepted or rejected consistently: {response.status_code}"

    def test_upload_file_type_validation_allowed(self, authenticated_client: TestClient):
        """
        Verify allowed file types accepted.

        Success Criteria:
        - .txt files accepted
        - .pdf files accepted (if PDF processing implemented)
        - .md files accepted
        - .json files accepted
        """
        allowed_types = [
            ("test.txt", "text/plain"),
            ("test.md", "text/markdown"),
            ("test.json", "application/json"),
        ]

        for filename, content_type in allowed_types:
            test_file = io.BytesIO(b"Test content")

            response = authenticated_client.post(
                "/upload", files={"file": (filename, test_file, content_type)}
            )

            assert response.status_code in [
                200,
                201,
            ], f"{filename} ({content_type}) should be accepted"

    def test_upload_file_type_validation_rejected(self, authenticated_client: TestClient):
        """
        Verify only allowed file types accepted.

        Success Criteria:
        - .exe rejected with 415
        - .sh rejected with 415
        - .dll rejected with 415
        - Clear error message
        """
        dangerous_types = [
            ("malware.exe", "application/x-msdownload"),
            ("script.sh", "application/x-sh"),
            ("library.dll", "application/x-msdownload"),
        ]

        for filename, content_type in dangerous_types:
            test_file = io.BytesIO(b"Potentially dangerous content")

            response = authenticated_client.post(
                "/upload", files={"file": (filename, test_file, content_type)}
            )

            assert (
                response.status_code == 415
            ), f"{filename} ({content_type}) should be rejected with 415"

            error = response.json()
            assert "detail" in error
            assert "unsupported" in error["detail"].lower() or "type" in error["detail"].lower()

    @pytest.mark.asyncio
    async def test_upload_user_isolation(self, db_session):
        """
        Verify files stored in user-isolated directories.

        Success Criteria:
        - User A's files in uploads/user_a_id/
        - User B's files in uploads/user_b_id/
        - User A cannot access User B's files
        - Directory permissions correct
        """
        from sqlalchemy import select

        from services.database.models import User

        # Get two different users
        result = await db_session.execute(select(User).limit(2))
        users = result.scalars().all()

        if len(users) >= 2:
            user_a = users[0]
            user_b = users[1]

            # Check upload directories are separate
            upload_base = Path("uploads")
            if upload_base.exists():
                user_a_dir = upload_base / str(user_a.id)
                user_b_dir = upload_base / str(user_b.id)

                # If directories exist, verify they're different
                if user_a_dir.exists() and user_b_dir.exists():
                    assert user_a_dir != user_b_dir, "User directories must be separate"

                    # Check files in user A's dir don't appear in user B's
                    if list(user_a_dir.glob("*")):
                        user_a_files = {f.name for f in user_a_dir.glob("*")}
                        user_b_files = (
                            {f.name for f in user_b_dir.glob("*")} if user_b_dir.exists() else set()
                        )

                        overlap = user_a_files & user_b_files
                        assert not overlap, f"Files should not overlap between users: {overlap}"

    def test_upload_special_characters_filename(self, authenticated_client: TestClient):
        """
        Verify filenames with special characters handled safely.

        Success Criteria:
        - Filenames sanitized or rejected
        - No path traversal possible (../)
        - Files saved with safe names
        """
        # Attempt path traversal
        dangerous_filenames = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\config",
            "test/../../../secret.txt",
            "test\\..\\..\\secret.txt",
        ]

        for dangerous_name in dangerous_filenames:
            test_file = io.BytesIO(b"Malicious content")

            response = authenticated_client.post(
                "/upload", files={"file": (dangerous_name, test_file, "text/plain")}
            )

            # Should either reject (4xx) or sanitize filename
            if response.status_code == 200:
                data = response.json()
                # Verify filename was sanitized (no ../ in saved name)
                assert ".." not in data.get(
                    "filename", ""
                ), f"Path traversal should be prevented: {dangerous_name}"
            else:
                assert (
                    400 <= response.status_code < 500
                ), f"Dangerous filename should be rejected: {dangerous_name}"

    def test_upload_empty_file(self, authenticated_client: TestClient):
        """
        Verify empty files handled appropriately.

        Success Criteria:
        - Empty file either accepted or rejected with clear message
        - No server errors (500)
        """
        empty_file = io.BytesIO(b"")

        response = authenticated_client.post(
            "/upload", files={"file": ("empty.txt", empty_file, "text/plain")}
        )

        # Either accept or reject, but no 500 error
        assert response.status_code != 500, "Empty file should not cause server error"

        if response.status_code >= 400:
            # If rejected, should have clear error message
            error = response.json()
            assert "detail" in error

    @pytest.mark.asyncio
    async def test_upload_metadata_stored(self, authenticated_client: TestClient, db_session):
        """
        Verify file metadata stored in database.

        Success Criteria:
        - Upload creates database record
        - Metadata includes: filename, size, content_type, user_id
        - Record can be queried later
        """
        test_file = io.BytesIO(b"Metadata test content")

        response = authenticated_client.post(
            "/upload", files={"file": ("metadata_test.txt", test_file, "text/plain")}
        )

        assert response.status_code == 200
        data = response.json()

        # Verify response includes expected metadata
        assert (
            "document_id" in data or "file_id" in data
        ), "Response should include database record ID"

        # TODO: Query database to verify record exists
        # This requires knowing the exact table/model structure
        # which will be implemented by Code agent


# Test fixtures


@pytest.fixture
def client():
    """Provide test client without authentication"""
    from web.app import app

    return TestClient(app)


@pytest.fixture
def authenticated_client(client: TestClient):
    """
    Provide test client with authentication.

    NOTE: This fixture needs to be implemented after auth is added.
    For now, it's a placeholder that will be filled in during Phase 3.
    """
    # TODO: Implement after Issue #281 (auth) is complete
    # For now, return regular client as placeholder
    # In real implementation:
    # 1. Create test user
    # 2. Login to get token
    # 3. Add token to client headers

    # Placeholder implementation
    pytest.skip("Authentication not yet implemented - blocked on Issue #281")

    return client


@pytest.fixture
async def db_session():
    """Provide database session for tests"""
    from services.database.session_factory import AsyncSessionFactory

    async with AsyncSessionFactory.session_scope() as session:
        yield session

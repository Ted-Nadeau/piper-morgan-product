import pytest
from datetime import datetime
from services.session.session_manager import SessionManager

class TestSessionFileTracking:
    """Test file tracking functionality in sessions"""
    
    @pytest.fixture
    def session_manager(self):
        """Create a fresh session manager for each test"""
        return SessionManager(ttl_minutes=30)
    
    def test_add_uploaded_file(self, session_manager):
        """Test adding a file to session tracking"""
        session_id = "test_file_tracking"
        session = session_manager.get_or_create_session(session_id)
        
        # Add a file
        file_id = "test_file_123"
        filename = "test.csv"
        file_type = "text/csv"
        upload_time = datetime.utcnow()
        
        session.add_uploaded_file(file_id, filename, file_type, upload_time)
        
        # Verify file was added
        assert len(session.uploaded_files) == 1
        assert session.active_file_id == file_id
        
        file_info = session.uploaded_files[0]
        assert file_info["file_id"] == file_id
        assert file_info["filename"] == filename
        assert file_info["file_type"] == file_type
        assert file_info["upload_time"] == upload_time
        assert file_info["referenced"] == False
    
    def test_get_recent_files(self, session_manager):
        """Test retrieving recent files in correct order"""
        session_id = "test_recent_files"
        session = session_manager.get_or_create_session(session_id)
        
        # Add multiple files with different timestamps
        files = [
            ("file1.pdf", "application/pdf", datetime(2025, 1, 1, 10, 0, 0)),
            ("file2.csv", "text/csv", datetime(2025, 1, 1, 11, 0, 0)),
            ("file3.txt", "text/plain", datetime(2025, 1, 1, 12, 0, 0))
        ]
        
        for i, (filename, file_type, upload_time) in enumerate(files):
            file_id = f"file_{i+1}"
            session.add_uploaded_file(file_id, filename, file_type, upload_time)
        
        # Get recent files (should be in reverse chronological order)
        recent_files = session.get_recent_files()
        
        assert len(recent_files) == 3
        assert recent_files[0]["filename"] == "file3.txt"  # Most recent
        assert recent_files[1]["filename"] == "file2.csv"
        assert recent_files[2]["filename"] == "file1.pdf"  # Oldest
        
        # Test limit parameter
        recent_2 = session.get_recent_files(limit=2)
        assert len(recent_2) == 2
        assert recent_2[0]["filename"] == "file3.txt"
        assert recent_2[1]["filename"] == "file2.csv"
    
    def test_active_file_id_tracking(self, session_manager):
        """Test that active_file_id is updated with most recent upload"""
        session_id = "test_active_file"
        session = session_manager.get_or_create_session(session_id)
        
        # Add first file
        session.add_uploaded_file("file1", "first.pdf", "application/pdf", datetime.utcnow())
        assert session.active_file_id == "file1"
        
        # Add second file
        session.add_uploaded_file("file2", "second.csv", "text/csv", datetime.utcnow())
        assert session.active_file_id == "file2"  # Should be updated to most recent
    
    def test_file_reference_tracking(self, session_manager):
        """Test that files can be marked as referenced"""
        session_id = "test_reference"
        session = session_manager.get_or_create_session(session_id)
        
        # Add a file
        session.add_uploaded_file("test_file", "test.pdf", "application/pdf", datetime.utcnow())
        
        # Initially not referenced
        assert session.uploaded_files[0]["referenced"] == False
        
        # Mark as referenced
        session.uploaded_files[0]["referenced"] = True
        assert session.uploaded_files[0]["referenced"] == True
    
    def test_session_persistence(self, session_manager):
        """Test that file tracking persists across session retrievals"""
        session_id = "test_persistence"
        
        # Create session and add file
        session1 = session_manager.get_or_create_session(session_id)
        session1.add_uploaded_file("test_file", "test.pdf", "application/pdf", datetime.utcnow())
        
        # Retrieve same session
        session2 = session_manager.get_or_create_session(session_id)
        
        # Should have the same file tracking
        assert len(session2.uploaded_files) == 1
        assert session2.uploaded_files[0]["file_id"] == "test_file"
        assert session2.active_file_id == "test_file" 
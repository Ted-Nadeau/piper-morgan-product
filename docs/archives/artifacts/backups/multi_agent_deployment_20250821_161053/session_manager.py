import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from services.domain.models import Intent
from services.utils.serialization import serialize_dataclass


class ConversationSession:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.created_at = datetime.utcnow()
        self.last_activity = datetime.utcnow()
        self.history: List[Dict] = []
        self.pending_clarification: Optional[Dict] = None
        self.context: Dict = {}
        self.uploaded_files: List[Dict] = []  # Track file metadata
        self.active_file_id: Optional[str] = None  # Most recent file
        # NEW: File disambiguation fields
        self.awaiting_clarification: Optional[str] = None
        self.clarification_context: Dict[str, Any] = {}

    def add_interaction(self, intent: Intent, response: str):
        """Record an interaction in session history"""
        self.history.append(
            {
                "timestamp": datetime.utcnow().isoformat(),
                "intent": serialize_dataclass(intent),
                "response": response,
            }
        )
        self.last_activity = datetime.utcnow()

    def set_pending_clarification(
        self, original_intent: Intent, missing_info: Dict, clarification_prompt: str
    ):
        """Store state for ongoing clarification"""
        self.pending_clarification = {
            "original_intent": original_intent,
            "missing_info": missing_info,
            "clarification_prompt": clarification_prompt,
        }
        self.last_activity = datetime.utcnow()

    def get_pending_clarification(self) -> Optional[Dict]:
        """Retrieve pending clarification if exists"""
        return self.pending_clarification

    def clear_pending_clarification(self):
        """Clear after clarification is resolved"""
        self.pending_clarification = None
        self.last_activity = datetime.utcnow()

    # NEW: File disambiguation methods
    def set_clarification(self, clarification_type: str, context: Dict):
        """Set disambiguation state"""
        self.awaiting_clarification = clarification_type
        self.clarification_context = context
        self.last_activity = datetime.utcnow()

    def get_clarification_context(self, key: str, default=None):
        """Get disambiguation context"""
        return self.clarification_context.get(key, default)

    def clear_clarification(self):
        """Clear disambiguation state"""
        self.awaiting_clarification = None
        self.clarification_context = {}
        self.last_activity = datetime.utcnow()

    def add_uploaded_file(self, file_id: str, filename: str, file_type: str, upload_time: datetime):
        """Track a file upload in session"""
        file_info = {
            "file_id": file_id,
            "filename": filename,
            "file_type": file_type,
            "upload_time": upload_time,
            "referenced": False,
        }
        self.uploaded_files.append(file_info)
        self.active_file_id = file_id

    def get_recent_files(self, limit: int = 5) -> List[Dict]:
        """Get recently uploaded files"""
        return sorted(self.uploaded_files, key=lambda x: x["upload_time"], reverse=True)[:limit]


class SessionManager:
    def __init__(self, ttl_minutes: int = 30):
        self._sessions: Dict[str, ConversationSession] = {}
        self.ttl = timedelta(minutes=ttl_minutes)

    def get_or_create_session(self, session_id: Optional[str] = None) -> ConversationSession:
        """Get existing session or create new one"""
        now = datetime.utcnow()
        if session_id and session_id in self._sessions:
            session = self._sessions[session_id]
            session.last_activity = now
            return session
        # Create new session
        new_id = session_id or str(uuid.uuid4())
        session = ConversationSession(new_id)
        self._sessions[new_id] = session
        return session

    def cleanup_expired_sessions(self):
        """Remove sessions older than TTL"""
        now = datetime.utcnow()
        expired = [
            sid for sid, sess in self._sessions.items() if now - sess.last_activity > self.ttl
        ]
        for sid in expired:
            del self._sessions[sid]

import time

import pytest

from services.domain.models import Intent
from services.session.session_manager import ConversationSession, SessionManager
from services.shared_types import IntentCategory


class DummyIntent:
    def __init__(self, action="test", category=IntentCategory.CONVERSATION, confidence=1.0):
        self.action = action
        self.category = category
        self.confidence = confidence
        self.context = {}

    def to_dict(self):
        return {
            "action": self.action,
            "category": self.category.value,
            "confidence": self.confidence,
        }


def test_conversation_session_interaction():
    session = ConversationSession("test-session")
    intent = DummyIntent(action="greeting")
    session.add_interaction(intent, "Hello!")
    assert len(session.history) == 1
    assert session.history[0]["intent"]["action"] == "greeting"
    assert session.history[0]["response"] == "Hello!"

    # Test clarification
    session.set_pending_clarification(intent, {"missing": "project"}, "Which project?")
    pending = session.get_pending_clarification()
    assert pending is not None
    assert pending["clarification_prompt"] == "Which project?"
    session.clear_pending_clarification()
    assert session.get_pending_clarification() is None


def test_session_manager_get_or_create():
    manager = SessionManager(ttl_minutes=0.001)  # Short TTL for test
    session1 = manager.get_or_create_session()
    session2 = manager.get_or_create_session(session1.session_id)
    assert session1 is session2
    session3 = manager.get_or_create_session()
    assert session3.session_id != session1.session_id
    # Test cleanup
    session1.last_activity = session1.last_activity.replace(year=2000)  # Simulate old session
    manager.cleanup_expired_sessions()
    assert session1.session_id not in manager._sessions

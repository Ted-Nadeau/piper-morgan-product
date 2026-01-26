"""
Tests for ProcessRegistry (ADR-049: Two-Tier Intent Architecture).

Issue #427: MUX-IMPLEMENT-CONVERSE-MODEL
Issue #687: ADR-049 Implementation
"""

from typing import Optional

import pytest

from services.process.registry import (
    GuidedProcess,
    ProcessCheckResult,
    ProcessRegistry,
    ProcessType,
    get_process_registry,
)


class MockGuidedProcess:
    """Mock guided process for testing."""

    def __init__(
        self,
        process_type: ProcessType,
        is_active: bool = False,
        response_message: str = "Mock response",
    ):
        self._process_type = process_type
        self._is_active = is_active
        self._response_message = response_message
        self._check_active_called = False
        self._handle_message_called = False

    @property
    def process_type(self) -> ProcessType:
        return self._process_type

    async def check_active(
        self,
        user_id: Optional[str],
        session_id: Optional[str],
    ) -> bool:
        self._check_active_called = True
        return self._is_active

    async def handle_message(
        self,
        user_id: Optional[str],
        session_id: Optional[str],
        message: str,
    ) -> ProcessCheckResult:
        self._handle_message_called = True
        return ProcessCheckResult.handled_by(
            process_type=self._process_type,
            response_message=self._response_message,
            intent_data={"action": "test", "bypassed_classification": True},
        )


class TestProcessCheckResult:
    """Tests for ProcessCheckResult dataclass."""

    def test_not_handled(self):
        """not_handled() creates unhandled result."""
        result = ProcessCheckResult.not_handled()
        assert result.handled is False
        assert result.process_type is None
        assert result.response_message is None
        assert result.intent_data is None

    def test_handled_by(self):
        """handled_by() creates handled result with data."""
        result = ProcessCheckResult.handled_by(
            process_type=ProcessType.ONBOARDING,
            response_message="Welcome!",
            intent_data={"action": "onboard"},
        )
        assert result.handled is True
        assert result.process_type == ProcessType.ONBOARDING
        assert result.response_message == "Welcome!"
        assert result.intent_data == {"action": "onboard"}


class TestProcessRegistry:
    """Tests for ProcessRegistry."""

    @pytest.fixture(autouse=True)
    def reset_singleton(self):
        """Reset singleton before each test."""
        ProcessRegistry.reset_instance()
        yield
        ProcessRegistry.reset_instance()

    def test_singleton(self):
        """Registry is a singleton."""
        r1 = get_process_registry()
        r2 = get_process_registry()
        assert r1 is r2

    def test_register_handler(self):
        """Can register a guided process handler."""
        registry = get_process_registry()
        handler = MockGuidedProcess(ProcessType.ONBOARDING)

        registry.register(handler)

        assert ProcessType.ONBOARDING in registry.registered_types

    def test_register_multiple_handlers(self):
        """Can register multiple handlers with different types."""
        registry = get_process_registry()

        registry.register(MockGuidedProcess(ProcessType.ONBOARDING))
        registry.register(MockGuidedProcess(ProcessType.STANDUP))

        assert ProcessType.ONBOARDING in registry.registered_types
        assert ProcessType.STANDUP in registry.registered_types

    def test_register_replaces_same_type(self):
        """Registering same type replaces existing handler."""
        registry = get_process_registry()
        handler1 = MockGuidedProcess(ProcessType.ONBOARDING, response_message="First")
        handler2 = MockGuidedProcess(ProcessType.ONBOARDING, response_message="Second")

        registry.register(handler1)
        registry.register(handler2)

        # Only one handler of this type
        assert registry.registered_types.count(ProcessType.ONBOARDING) == 1

    def test_unregister_handler(self):
        """Can unregister a handler by type."""
        registry = get_process_registry()
        registry.register(MockGuidedProcess(ProcessType.ONBOARDING))

        result = registry.unregister(ProcessType.ONBOARDING)

        assert result is True
        assert ProcessType.ONBOARDING not in registry.registered_types

    def test_unregister_nonexistent(self):
        """Unregistering nonexistent type returns False."""
        registry = get_process_registry()

        result = registry.unregister(ProcessType.PLANNING)

        assert result is False

    @pytest.mark.asyncio
    async def test_check_no_handlers(self):
        """No handlers returns not_handled."""
        registry = get_process_registry()

        result = await registry.check_active_processes("user1", "session1", "hello")

        assert result.handled is False

    @pytest.mark.asyncio
    async def test_check_no_active_process(self):
        """Handler with no active session returns not_handled."""
        registry = get_process_registry()
        handler = MockGuidedProcess(ProcessType.ONBOARDING, is_active=False)
        registry.register(handler)

        result = await registry.check_active_processes("user1", "session1", "hello")

        assert result.handled is False
        assert handler._check_active_called is True
        assert handler._handle_message_called is False

    @pytest.mark.asyncio
    async def test_check_active_process_handles(self):
        """Active process handles the message."""
        registry = get_process_registry()
        handler = MockGuidedProcess(
            ProcessType.ONBOARDING,
            is_active=True,
            response_message="Welcome to onboarding!",
        )
        registry.register(handler)

        result = await registry.check_active_processes("user1", "session1", "hello")

        assert result.handled is True
        assert result.process_type == ProcessType.ONBOARDING
        assert result.response_message == "Welcome to onboarding!"
        assert handler._check_active_called is True
        assert handler._handle_message_called is True

    @pytest.mark.asyncio
    async def test_priority_order(self):
        """Higher priority process is checked first."""
        registry = get_process_registry()

        # Register standup first (lower priority)
        standup = MockGuidedProcess(ProcessType.STANDUP, is_active=True)
        registry.register(standup)

        # Register onboarding second (higher priority)
        onboarding = MockGuidedProcess(ProcessType.ONBOARDING, is_active=True)
        registry.register(onboarding)

        result = await registry.check_active_processes("user1", "session1", "hello")

        # Onboarding should handle (higher priority)
        assert result.process_type == ProcessType.ONBOARDING
        assert onboarding._check_active_called is True
        # Standup should not even be checked
        assert standup._check_active_called is False

    @pytest.mark.asyncio
    async def test_fallthrough_to_lower_priority(self):
        """Falls through to lower priority if higher is not active."""
        registry = get_process_registry()

        # Onboarding not active
        onboarding = MockGuidedProcess(ProcessType.ONBOARDING, is_active=False)
        registry.register(onboarding)

        # Standup is active
        standup = MockGuidedProcess(ProcessType.STANDUP, is_active=True)
        registry.register(standup)

        result = await registry.check_active_processes("user1", "session1", "hello")

        # Standup should handle
        assert result.process_type == ProcessType.STANDUP
        assert onboarding._check_active_called is True
        assert standup._check_active_called is True

    @pytest.mark.asyncio
    async def test_handler_exception_continues(self):
        """Exception in handler doesn't stop checking other handlers."""

        class FailingProcess:
            @property
            def process_type(self) -> ProcessType:
                return ProcessType.ONBOARDING

            async def check_active(self, user_id, session_id) -> bool:
                raise RuntimeError("Test failure")

            async def handle_message(self, user_id, session_id, message):
                return ProcessCheckResult.not_handled()

        registry = get_process_registry()
        registry.register(FailingProcess())

        standup = MockGuidedProcess(ProcessType.STANDUP, is_active=True)
        registry.register(standup)

        # Should not raise, should fall through to standup
        result = await registry.check_active_processes("user1", "session1", "hello")

        assert result.handled is True
        assert result.process_type == ProcessType.STANDUP


class TestGuidedProcessProtocol:
    """Tests for GuidedProcess protocol compliance."""

    def test_mock_implements_protocol(self):
        """MockGuidedProcess implements GuidedProcess protocol."""
        handler = MockGuidedProcess(ProcessType.ONBOARDING)
        assert isinstance(handler, GuidedProcess)

    def test_protocol_requires_process_type(self):
        """Protocol requires process_type property."""

        class MissingProcessType:
            async def check_active(self, user_id, session_id):
                return False

            async def handle_message(self, user_id, session_id, message):
                return ProcessCheckResult.not_handled()

        assert not isinstance(MissingProcessType(), GuidedProcess)

    def test_protocol_requires_check_active(self):
        """Protocol requires check_active method."""

        class MissingCheckActive:
            @property
            def process_type(self):
                return ProcessType.ONBOARDING

            async def handle_message(self, user_id, session_id, message):
                return ProcessCheckResult.not_handled()

        assert not isinstance(MissingCheckActive(), GuidedProcess)

    def test_protocol_requires_handle_message(self):
        """Protocol requires handle_message method."""

        class MissingHandleMessage:
            @property
            def process_type(self):
                return ProcessType.ONBOARDING

            async def check_active(self, user_id, session_id):
                return False

        assert not isinstance(MissingHandleMessage(), GuidedProcess)

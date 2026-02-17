"""
Tests for SlotFillingProcessAdapter (ProcessRegistry integration).

Issue #765: GLUE-SLOTFILL — Natural Slot Filling Without Interrogation
Phase 3: SlotFillingManager + ProcessRegistry Integration

Tests cover:
- Adapter delegates correctly to manager
- check_active returns true/false correctly
- ProcessCheckResult formatting
- ProcessRegistry integration (real objects, not mocks per #490)
"""

from unittest.mock import AsyncMock

import pytest

from services.process.registry import ProcessCheckResult, ProcessRegistry, ProcessType
from services.shared_types import SlotFillingState
from services.slot_filling.slot_filling_adapter import SlotFillingProcessAdapter
from services.slot_filling.slot_filling_manager import SlotFillingManager
from services.slot_filling.slot_template import MEETING_TEMPLATE


@pytest.fixture
def mock_llm():
    llm = AsyncMock()
    llm.complete = AsyncMock(return_value="{}")
    return llm


@pytest.fixture
def manager(mock_llm):
    return SlotFillingManager(llm_service=mock_llm)


@pytest.fixture
def adapter(manager):
    return SlotFillingProcessAdapter(manager=manager)


class TestAdapterProperties:
    def test_process_type(self, adapter):
        assert adapter.process_type == ProcessType.SLOT_FILLING

    def test_manager_accessible(self, adapter, manager):
        assert adapter.manager is manager


class TestCheckActive:
    @pytest.mark.asyncio
    async def test_no_session_returns_false(self, adapter):
        result = await adapter.check_active("user1", "sess1")
        assert result is False

    @pytest.mark.asyncio
    async def test_active_session_returns_true(self, adapter, manager, mock_llm):
        mock_llm.complete.return_value = "{}"
        await manager.start_filling(
            user_id="user1",
            session_id="sess1",
            template=MEETING_TEMPLATE,
            initial_message="Meeting",
        )
        result = await adapter.check_active("user1", "sess1")
        assert result is True


class TestHandleMessage:
    @pytest.mark.asyncio
    async def test_delegates_to_manager(self, adapter, manager, mock_llm):
        """handle_message delegates to manager.handle_turn."""
        mock_llm.complete.return_value = "{}"
        await manager.start_filling(
            user_id="user1",
            session_id="sess1",
            template=MEETING_TEMPLATE,
            initial_message="Meeting",
        )

        mock_llm.complete.return_value = '{"attendee": "Sarah"}'
        result = await adapter.handle_message("user1", "sess1", "With Sarah")
        assert isinstance(result, ProcessCheckResult)
        assert result.handled is True
        assert result.process_type == ProcessType.SLOT_FILLING

    @pytest.mark.asyncio
    async def test_intent_data_structure(self, adapter, manager, mock_llm):
        """Intent data has expected fields."""
        mock_llm.complete.return_value = "{}"
        await manager.start_filling(
            user_id="user1",
            session_id="sess1",
            template=MEETING_TEMPLATE,
            initial_message="Meeting",
        )

        result = await adapter.handle_message("user1", "sess1", "With Sarah")
        assert result.intent_data is not None
        assert result.intent_data["action"] == "slot_filling"
        assert result.intent_data["context"]["guided_process"] == "slot_filling"
        assert result.intent_data["context"]["bypassed_classification"] is True

    @pytest.mark.asyncio
    async def test_cancel_intent_data(self, adapter, manager, mock_llm):
        """Cancelled session has cancel action."""
        mock_llm.complete.return_value = "{}"
        await manager.start_filling(
            user_id="user1",
            session_id="sess1",
            template=MEETING_TEMPLATE,
            initial_message="Meeting",
        )

        result = await adapter.handle_message("user1", "sess1", "Never mind")
        assert result.intent_data["action"] == "slot_filling_cancelled"
        assert result.intent_data["context"]["is_cancelled"] is True


class TestProcessRegistryIntegration:
    """Wiring tests with real objects (not mocks) per #490 learning."""

    @pytest.fixture(autouse=True)
    def reset_registry(self):
        """Reset ProcessRegistry singleton between tests."""
        ProcessRegistry.reset_instance()
        yield
        ProcessRegistry.reset_instance()

    @pytest.mark.asyncio
    async def test_register_slot_filling_adapter(self, adapter):
        """SlotFillingProcessAdapter can be registered."""
        registry = ProcessRegistry.get_instance()
        registry.register(adapter)
        assert ProcessType.SLOT_FILLING in registry.registered_types

    @pytest.mark.asyncio
    async def test_priority_order(self, adapter):
        """Slot filling has correct priority (after standup, before clarification)."""
        registry = ProcessRegistry.get_instance()
        registry.register(adapter)
        # Priority should be 25 (between standup=20 and clarification=30)
        assert registry._priority_order[ProcessType.SLOT_FILLING] == 25

    @pytest.mark.asyncio
    async def test_check_active_processes_finds_slot_filling(self, adapter, manager, mock_llm):
        """ProcessRegistry finds active slot-filling session."""
        registry = ProcessRegistry.get_instance()
        registry.register(adapter)

        # No active session → not handled
        result = await registry.check_active_processes("user1", "sess1", "Hello")
        assert result.handled is False

        # Start a session
        mock_llm.complete.return_value = "{}"
        await manager.start_filling(
            user_id="user1",
            session_id="sess1",
            template=MEETING_TEMPLATE,
            initial_message="Meeting",
        )

        # Now should be handled
        mock_llm.complete.return_value = '{"attendee": "Sarah"}'
        result = await registry.check_active_processes("user1", "sess1", "With Sarah")
        assert result.handled is True
        assert result.process_type == ProcessType.SLOT_FILLING

    @pytest.mark.asyncio
    async def test_slot_filling_type_exists(self):
        """ProcessType.SLOT_FILLING exists and has correct value."""
        assert ProcessType.SLOT_FILLING == "slot_filling"
        assert ProcessType.SLOT_FILLING.value == "slot_filling"

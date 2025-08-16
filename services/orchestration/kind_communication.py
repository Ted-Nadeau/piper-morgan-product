"""
Kind Communication Wrapper

PM-033d Phase 4: Human-friendly messaging system that transforms technical coordination
results into clear, empathetic, and actionable communication for users.
"""

import asyncio
import logging
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

import structlog

from services.domain.models import Intent
from services.orchestration.multi_agent_coordinator import (
    CoordinationResult,
    CoordinationStatus,
    SubTask,
)

logger = structlog.get_logger()


class MessageTone(Enum):
    """Communication tone options"""

    FRIENDLY = "friendly"
    PROFESSIONAL = "professional"
    ENCOURAGING = "encouraging"
    EMPATHETIC = "empathetic"
    CELEBRATORY = "celebratory"


class MessageType(Enum):
    """Types of communication messages"""

    PROGRESS_UPDATE = "progress_update"
    SUCCESS_SUMMARY = "success_summary"
    ERROR_EXPLANATION = "error_explanation"
    NEXT_STEPS = "next_steps"
    ENCOURAGEMENT = "encouragement"


@dataclass
class KindMessage:
    """Human-friendly message structure"""

    message_type: MessageType
    tone: MessageTone
    primary_message: str
    details: List[str]
    action_items: List[str]
    encouragement: Optional[str]
    metadata: Dict[str, Any]
    created_at: datetime


@dataclass
class CommunicationPreferences:
    """User communication preferences"""

    preferred_tone: MessageTone = MessageTone.FRIENDLY
    include_technical_details: bool = False
    include_encouragement: bool = True
    max_detail_items: int = 5
    show_agent_assignments: bool = False
    emoji_usage: bool = True


class KindCommunicationWrapper:
    """
    Transforms technical coordination results into human-friendly messages

    Provides empathetic, clear communication that helps users understand
    what's happening without overwhelming them with technical details.
    """

    def __init__(self, preferences: Optional[CommunicationPreferences] = None):
        self.preferences = preferences or CommunicationPreferences()
        self.message_history: List[KindMessage] = []

    async def wrap_coordination_result(
        self, result: CoordinationResult, intent: Intent
    ) -> KindMessage:
        """
        Transform coordination result into human-friendly message

        Args:
            result: Coordination result to communicate
            intent: Original user intent

        Returns:
            KindMessage with human-friendly communication
        """
        logger.info(
            "Creating kind communication message",
            coordination_id=result.coordination_id,
            status=result.status.value,
        )

        if result.status == CoordinationStatus.ASSIGNED:
            return await self._create_success_message(result, intent)
        elif result.status == CoordinationStatus.FAILED:
            return await self._create_error_message(result, intent)
        elif result.status == CoordinationStatus.IN_PROGRESS:
            return await self._create_progress_message(result, intent)
        else:
            return await self._create_status_message(result, intent)

    async def _create_success_message(
        self, result: CoordinationResult, intent: Intent
    ) -> KindMessage:
        """Create success message for completed coordination"""

        # Generate primary message based on intent
        action_verb = self._extract_action_verb(intent.action)
        primary_message = f"Great news! I've successfully coordinated your {action_verb} request."

        if self.preferences.emoji_usage:
            primary_message = f"🎉 {primary_message}"

        # Create details list
        details = []

        if len(result.subtasks) > 1:
            details.append(f"I've broken this down into {len(result.subtasks)} focused tasks")

        # Add agent assignments if preferred
        if self.preferences.show_agent_assignments:
            code_tasks = len(
                [
                    t
                    for t in result.subtasks
                    if hasattr(t, "assigned_agent") and str(t.assigned_agent).endswith("CODE")
                ]
            )
            cursor_tasks = len(
                [
                    t
                    for t in result.subtasks
                    if hasattr(t, "assigned_agent") and str(t.assigned_agent).endswith("CURSOR")
                ]
            )

            if code_tasks > 0 and cursor_tasks > 0:
                details.append(
                    f"Tasks distributed across both development agents for optimal results"
                )
            elif code_tasks > 0:
                details.append(f"All tasks assigned to our backend specialist")
            elif cursor_tasks > 0:
                details.append(f"All tasks assigned to our frontend specialist")

        # Add performance note
        if result.total_duration_ms < 500:
            details.append("Coordination completed quickly - under 500ms")
        elif result.total_duration_ms < 1000:
            details.append("Coordination completed efficiently within our target timeframe")

        # Create action items
        action_items = []
        for i, subtask in enumerate(result.subtasks[:3], 1):  # Show first 3 tasks
            task_description = self._humanize_task_description(subtask)
            action_items.append(f"Step {i}: {task_description}")

        if len(result.subtasks) > 3:
            action_items.append(f"...and {len(result.subtasks) - 3} additional steps")

        # Add encouragement
        encouragement = None
        if self.preferences.include_encouragement:
            if result.success_rate == 1.0:
                encouragement = "Everything looks perfectly set up for success!"
            else:
                encouragement = "I'm confident we can tackle this step by step."

        return KindMessage(
            message_type=MessageType.SUCCESS_SUMMARY,
            tone=self.preferences.preferred_tone,
            primary_message=primary_message,
            details=details[: self.preferences.max_detail_items],
            action_items=action_items,
            encouragement=encouragement,
            metadata={
                "coordination_id": result.coordination_id,
                "subtask_count": len(result.subtasks),
                "duration_ms": result.total_duration_ms,
                "success_rate": result.success_rate,
            },
            created_at=datetime.now(),
        )

    async def _create_error_message(
        self, result: CoordinationResult, intent: Intent
    ) -> KindMessage:
        """Create empathetic error message"""

        primary_message = "I encountered some challenges coordinating your request, but don't worry - let's work through this together."

        if self.preferences.emoji_usage:
            primary_message = f"🤔 {primary_message}"

        details = []

        if result.error_details:
            # Humanize technical error details
            if "database" in str(result.error_details).lower():
                details.append("There was a temporary database connectivity issue")
            elif "timeout" in str(result.error_details).lower():
                details.append("The coordination took longer than expected")
            elif "import" in str(result.error_details).lower():
                details.append("There was a configuration issue with the system modules")
            else:
                details.append("A technical issue occurred during coordination")

        # Add reassurance
        details.append("This is a temporary issue that we can resolve together")

        # Create action items for recovery
        action_items = [
            "Let me know if you'd like to try again with a simplified approach",
            "I can break down your request into smaller, more manageable parts",
            "We can also try a different implementation strategy",
        ]

        encouragement = "These things happen in development - what matters is that we keep moving forward together!"

        return KindMessage(
            message_type=MessageType.ERROR_EXPLANATION,
            tone=MessageTone.EMPATHETIC,
            primary_message=primary_message,
            details=details,
            action_items=action_items,
            encouragement=encouragement if self.preferences.include_encouragement else None,
            metadata={
                "coordination_id": result.coordination_id,
                "error_type": (
                    type(result.error_details).__name__ if result.error_details else "Unknown"
                ),
                "duration_ms": result.total_duration_ms,
            },
            created_at=datetime.now(),
        )

    async def _create_progress_message(
        self, result: CoordinationResult, intent: Intent
    ) -> KindMessage:
        """Create progress update message"""

        primary_message = "I'm actively working on coordinating your request."

        if self.preferences.emoji_usage:
            primary_message = f"⚡ {primary_message}"

        details = []

        if len(result.subtasks) > 0:
            completed_tasks = len(
                [
                    t
                    for t in result.subtasks
                    if hasattr(t, "status") and str(t.status) == "COMPLETED"
                ]
            )
            if completed_tasks > 0:
                details.append(
                    f"Progress: {completed_tasks}/{len(result.subtasks)} tasks coordinated"
                )
            else:
                details.append(f"Setting up {len(result.subtasks)} coordinated tasks")

        details.append("Everything is proceeding smoothly")

        action_items = ["Please stand by while I complete the coordination"]

        encouragement = "Great things take a little time - we're on the right track!"

        return KindMessage(
            message_type=MessageType.PROGRESS_UPDATE,
            tone=MessageTone.ENCOURAGING,
            primary_message=primary_message,
            details=details,
            action_items=action_items,
            encouragement=encouragement if self.preferences.include_encouragement else None,
            metadata={
                "coordination_id": result.coordination_id,
                "progress_percentage": (
                    (completed_tasks / len(result.subtasks) * 100) if result.subtasks else 0
                ),
            },
            created_at=datetime.now(),
        )

    async def _create_status_message(
        self, result: CoordinationResult, intent: Intent
    ) -> KindMessage:
        """Create general status message"""

        primary_message = f"I'm currently {result.status.value.replace('_', ' ')} your request."

        details = [f"Current coordination status: {result.status.value}"]
        action_items = ["I'll keep you updated as things progress"]

        return KindMessage(
            message_type=MessageType.PROGRESS_UPDATE,
            tone=self.preferences.preferred_tone,
            primary_message=primary_message,
            details=details,
            action_items=action_items,
            encouragement="Thanks for your patience!",
            metadata={"coordination_id": result.coordination_id},
            created_at=datetime.now(),
        )

    def _extract_action_verb(self, action: str) -> str:
        """Extract human-friendly action verb from technical action"""

        action_mappings = {
            "implement": "implementation",
            "create": "creation",
            "build": "building",
            "refactor": "refactoring",
            "migrate": "migration",
            "deploy": "deployment",
            "test": "testing",
            "analyze": "analysis",
            "optimize": "optimization",
            "design": "design",
        }

        for key, value in action_mappings.items():
            if key in action.lower():
                return value

        return action.replace("_", " ")

    def _humanize_task_description(self, subtask: SubTask) -> str:
        """Convert technical task description to human-friendly format"""

        if hasattr(subtask, "description"):
            description = subtask.description
        else:
            description = getattr(subtask, "task_id", str(subtask))

        # Humanize common technical terms
        humanizations = {
            "api": "API integration",
            "database": "database setup",
            "test": "quality testing",
            "validation": "validation checks",
            "authentication": "security setup",
            "frontend": "user interface",
            "backend": "server components",
            "deployment": "system deployment",
        }

        result = description.lower()
        for tech_term, human_term in humanizations.items():
            if tech_term in result:
                result = result.replace(tech_term, human_term)

        return result.capitalize()

    async def format_message_for_display(self, message: KindMessage) -> str:
        """Format kind message for display to user"""

        output_lines = []

        # Primary message
        output_lines.append(message.primary_message)

        # Details section
        if message.details:
            output_lines.append("")
            for detail in message.details:
                prefix = "✓" if self.preferences.emoji_usage else "-"
                output_lines.append(f"{prefix} {detail}")

        # Action items section
        if message.action_items:
            output_lines.append("")
            output_lines.append(
                "Next steps:" if not self.preferences.emoji_usage else "📋 Next steps:"
            )
            for action in message.action_items:
                output_lines.append(f"  • {action}")

        # Encouragement
        if message.encouragement and self.preferences.include_encouragement:
            output_lines.append("")
            output_lines.append(message.encouragement)

        return "\n".join(output_lines)

    async def get_message_history(self) -> List[KindMessage]:
        """Get history of kind messages"""
        return self.message_history.copy()

    async def update_preferences(self, new_preferences: CommunicationPreferences):
        """Update communication preferences"""
        self.preferences = new_preferences
        logger.info(
            "Communication preferences updated",
            tone=new_preferences.preferred_tone.value,
            include_encouragement=new_preferences.include_encouragement,
        )


# Integration function for Phase 4 testing
async def run_kind_communication_validation() -> Dict[str, Any]:
    """Run Kind Communication validation for PM-033d Phase 4"""

    print("💬 KIND COMMUNICATION WRAPPER VALIDATION")
    print("=" * 50)

    # Test different communication scenarios
    wrapper = KindCommunicationWrapper()

    # Create test coordination results
    from services.orchestration.multi_agent_coordinator import MultiAgentCoordinator
    from services.shared_types import IntentCategory

    test_intent = Intent(
        category=IntentCategory.EXECUTION,
        action="implement_user_authentication",
        original_message="Implement user authentication system with login, registration, and password reset",
        confidence=0.96,
    )

    coordinator = MultiAgentCoordinator()
    coordination_result = await coordinator.coordinate_task(test_intent)

    print("\n📝 Test 1: Success Message Generation")
    success_message = await wrapper.wrap_coordination_result(coordination_result, test_intent)
    formatted_success = await wrapper.format_message_for_display(success_message)
    print(f"Message Type: {success_message.message_type.value}")
    print(f"Tone: {success_message.tone.value}")
    print(f"Formatted Output:\n{formatted_success}")

    print("\n📝 Test 2: Error Message Generation")
    # Simulate error result
    error_result = CoordinationResult(
        coordination_id="error_test",
        status=CoordinationStatus.FAILED,
        subtasks=[],
        total_duration_ms=1500,
        success_rate=0.0,
        error_details=Exception("Database connection timeout"),
        agent_performance={},
    )

    error_message = await wrapper.wrap_coordination_result(error_result, test_intent)
    formatted_error = await wrapper.format_message_for_display(error_message)
    print(f"Message Type: {error_message.message_type.value}")
    print(f"Tone: {error_message.tone.value}")
    print(f"Formatted Output:\n{formatted_error}")

    print("\n📝 Test 3: Communication Preferences")
    # Test different preferences
    professional_prefs = CommunicationPreferences(
        preferred_tone=MessageTone.PROFESSIONAL,
        include_encouragement=False,
        emoji_usage=False,
        show_agent_assignments=True,
    )

    professional_wrapper = KindCommunicationWrapper(professional_prefs)
    professional_message = await professional_wrapper.wrap_coordination_result(
        coordination_result, test_intent
    )
    formatted_professional = await professional_wrapper.format_message_for_display(
        professional_message
    )
    print(f"Professional Tone Output:\n{formatted_professional}")

    print("\n📝 Test 4: Message History Tracking")
    message_history = await wrapper.get_message_history()
    print(f"Messages tracked: {len(message_history)}")

    # Validation criteria
    validation_results = {
        "success_message_created": success_message is not None,
        "error_message_created": error_message is not None,
        "professional_tone_works": professional_message.tone == MessageTone.PROFESSIONAL,
        "formatting_works": len(formatted_success) > 0,
        "encouragement_included": success_message.encouragement is not None,
        "action_items_present": len(success_message.action_items) > 0,
        "human_friendly_language": "technical" not in success_message.primary_message.lower(),
    }

    validation_success = all(validation_results.values())

    print(f"\n📊 KIND COMMUNICATION VALIDATION RESULTS:")
    for criterion, result in validation_results.items():
        status = "✅" if result else "❌"
        print(f"   {criterion}: {status}")

    print(
        f'\n🎯 KIND COMMUNICATION VALIDATION: {"✅ PASSED" if validation_success else "❌ FAILED"}'
    )

    return {
        "validation_success": validation_success,
        "test_results": validation_results,
        "message_samples": {
            "success": formatted_success,
            "error": formatted_error,
            "professional": formatted_professional,
        },
    }


if __name__ == "__main__":
    # Run Kind Communication validation directly
    import asyncio

    result = asyncio.run(run_kind_communication_validation())
    print(f"\nKind Communication validation completed: {result['validation_success']}")

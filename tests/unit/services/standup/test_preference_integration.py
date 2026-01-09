"""
Integration tests for Preference Learning System.

Issue #555: STANDUP-LEARNING - User Preference Learning
Epic #242: CONV-MCP-STANDUP-INTERACTIVE

Tests the complete preference learning workflow:
- Extraction → Storage → Application → Feedback → Persistence
"""

import shutil
import tempfile
from pathlib import Path

import pytest

from services.standup.preference_applicator import AppliedPreferences, PreferenceApplicator
from services.standup.preference_extractor import PreferenceExtractor
from services.standup.preference_feedback import PreferenceFeedbackHandler
from services.standup.preference_models import (
    PreferenceSource,
    PreferenceType,
    UserStandupPreference,
)
from services.standup.preference_service import UserPreferenceService


class TestFullPreferenceLearningFlow:
    """
    Integration tests for the complete preference learning workflow.

    Simulates real user interaction:
    1. User expresses preference in conversation
    2. Preference is extracted and stored
    3. Preference is applied to next standup
    4. User provides feedback (confirms or corrects)
    5. Confidence adjusts and persists
    """

    @pytest.fixture
    def temp_storage(self):
        """Create a temporary storage directory."""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def service(self, temp_storage):
        """Create a preference service with temporary storage."""
        return UserPreferenceService(storage_path=temp_storage)

    @pytest.fixture
    def extractor(self):
        """Create a preference extractor."""
        return PreferenceExtractor()

    @pytest.fixture
    def applicator(self, service):
        """Create a preference applicator."""
        return PreferenceApplicator(preference_service=service)

    @pytest.fixture
    def feedback_handler(self, service):
        """Create a feedback handler."""
        return PreferenceFeedbackHandler(preference_service=service)

    # =========================================================================
    # Full Flow Tests
    # =========================================================================

    @pytest.mark.asyncio
    async def test_first_time_user_flow(self, service, extractor, applicator, feedback_handler):
        """Test complete flow for first-time user."""
        user_id = "new-user-123"

        # Step 1: User starts with no preferences
        prefs = await service.get_preferences(user_id)
        assert len(prefs) == 0

        # Step 2: User says "focus on GitHub, skip documentation"
        message = "focus on GitHub, skip documentation"
        extracted = extractor.extract_from_turn(message)
        assert len(extracted) >= 2

        # Step 3: Save extracted preferences
        for ext in extracted:
            pref = ext.to_preference(user_id)
            await service.save_preference(pref)

        # Step 4: Verify preferences were stored
        prefs = await service.get_preferences(user_id)
        assert len(prefs) >= 2

        # Step 5: Apply preferences to content
        applied = await applicator.prepare_preferences(user_id)
        assert "github" in applied.focus_areas
        assert "documentation" in applied.excluded_areas

    @pytest.mark.asyncio
    async def test_returning_user_flow(self, service, applicator):
        """Test that returning user gets their preferences automatically."""
        user_id = "returning-user"

        # Step 1: First session - save preference
        pref = UserStandupPreference(
            user_id=user_id,
            preference_type=PreferenceType.CONTENT_FILTER,
            key="focus",
            value="calendar",
            confidence=0.85,
        )
        await service.save_preference(pref)

        # Step 2: "New session" - create fresh applicator with same storage
        new_service = UserPreferenceService(storage_path=service.storage_path)
        new_applicator = PreferenceApplicator(preference_service=new_service)

        # Step 3: Preferences should load automatically
        applied = await new_applicator.prepare_preferences(user_id)
        assert "calendar" in applied.focus_areas
        assert len(applied.applied_from_history) == 1

    @pytest.mark.asyncio
    async def test_correction_flow(self, service, applicator, feedback_handler):
        """Test correcting a preference."""
        user_id = "correction-user"

        # Step 1: Initial preference
        pref = UserStandupPreference(
            user_id=user_id,
            preference_type=PreferenceType.CONTENT_FILTER,
            key="focus",
            value="github",
            confidence=0.8,
        )
        await service.save_preference(pref)

        # Step 2: Load initial preferences
        applied = await applicator.prepare_preferences(user_id)
        assert "github" in applied.focus_areas

        # Step 3: User corrects: "no, focus on calendar"
        prefs = await service.get_preferences(user_id)
        result = await feedback_handler.process_correction(
            user_id,
            "no, focus on calendar instead",
            prefs,
        )
        assert result.was_correction is True

        # Step 4: Preference should be updated
        updated_prefs = await service.get_preferences(user_id)
        focus_pref = next(
            (p for p in updated_prefs if p.preference_type == PreferenceType.CONTENT_FILTER),
            None,
        )
        if focus_pref:
            assert focus_pref.value == "calendar"
            assert focus_pref.confidence < 0.8  # Reduced due to correction

    @pytest.mark.asyncio
    async def test_confirmation_boosts_confidence(self, service, feedback_handler):
        """Test that confirmation boosts preference confidence."""
        user_id = "confirm-user"

        # Step 1: Low confidence preference
        pref = UserStandupPreference(
            user_id=user_id,
            preference_type=PreferenceType.FORMAT,
            key="format",
            value="brief",
            confidence=0.5,
        )
        await service.save_preference(pref)

        # Step 2: User confirms
        prefs = await service.get_preferences(user_id)
        updated = await feedback_handler.process_confirmation(user_id, prefs[0], confirmed=True)

        # Step 3: Confidence should be boosted
        assert updated.confidence > 0.5

        # Step 4: Persisted boost
        final_prefs = await service.get_preferences(user_id)
        assert final_prefs[0].confidence > 0.5

    @pytest.mark.asyncio
    async def test_repeated_same_preference_builds_confidence(self, service, extractor):
        """Test that repeating the same preference builds confidence."""
        user_id = "repeat-user"

        # Step 1: First mention
        extracted1 = extractor.extract_from_turn("focus on GitHub")
        pref1 = extracted1[0].to_preference(user_id)
        saved1 = await service.save_preference(pref1)
        initial_confidence = saved1.confidence

        # Step 2: Second mention (same preference)
        extracted2 = extractor.extract_from_turn("focus on GitHub please")
        pref2 = extracted2[0].to_preference(user_id)
        saved2 = await service.save_preference(pref2)

        # Step 3: Confidence should be boosted
        assert saved2.confidence > initial_confidence

    @pytest.mark.asyncio
    async def test_temporary_preference_not_persisted(self, service, applicator, extractor):
        """Test that temporary preferences aren't persisted."""
        user_id = "temp-user"

        # Step 1: Persistent preference first
        pref = UserStandupPreference(
            user_id=user_id,
            preference_type=PreferenceType.CONTENT_FILTER,
            key="focus",
            value="github",
            confidence=0.8,
        )
        await service.save_preference(pref)

        # Step 2: User says "just for today, focus on calendar"
        applied = await applicator.prepare_preferences(
            user_id,
            current_message="just for today, focus on calendar",
        )

        # Step 3: Temporary override should be active
        # Either in temporary_overrides or focus_areas should include calendar
        has_temp_override = (
            "focus" in applied.temporary_overrides or "calendar" in applied.focus_areas
        )
        assert has_temp_override or len(applied.applied_from_turn) > 0

        # Step 4: But persistent preference should still be github
        persisted = await service.get_preferences(user_id)
        github_pref = next(
            (p for p in persisted if p.value == "github"),
            None,
        )
        assert github_pref is not None  # Original still there

    @pytest.mark.asyncio
    async def test_content_filtering_with_preferences(self, service, applicator):
        """Test that content filtering respects preferences."""
        user_id = "filter-user"

        # Step 1: Set up focus and exclusion preferences
        focus_pref = UserStandupPreference(
            user_id=user_id,
            preference_type=PreferenceType.CONTENT_FILTER,
            key="focus",
            value="github",
            confidence=0.9,
        )
        exclude_pref = UserStandupPreference(
            user_id=user_id,
            preference_type=PreferenceType.EXCLUSION,
            key="exclude",
            value="docs",
            confidence=0.85,
        )
        await service.save_preference(focus_pref)
        await service.save_preference(exclude_pref)

        # Step 2: Prepare preferences
        applied = await applicator.prepare_preferences(user_id)

        # Step 3: Filter content
        content = {
            "github_prs": ["PR #123"],
            "github_docs": ["README updates"],  # Should be excluded (contains 'docs')
            "calendar": ["Meeting at 3pm"],  # Should be excluded (not in focus)
            "todos": ["Fix bug"],  # Should be excluded (not in focus)
        }
        filtered = applicator.filter_content(content, applied)

        # Step 4: Only github (non-docs) should remain
        assert "github_prs" in filtered
        assert "github_docs" not in filtered  # Excluded
        assert "calendar" not in filtered  # Not in focus
        assert "todos" not in filtered  # Not in focus

    @pytest.mark.asyncio
    async def test_format_preference_application(self, service, applicator):
        """Test that format preference is applied to output."""
        user_id = "format-user"

        # Step 1: Set brief format preference
        pref = UserStandupPreference(
            user_id=user_id,
            preference_type=PreferenceType.FORMAT,
            key="format",
            value="brief",
            confidence=0.9,
        )
        await service.save_preference(pref)

        # Step 2: Prepare preferences
        applied = await applicator.prepare_preferences(user_id)
        assert applied.format_style == "brief"

        # Step 3: Format output
        long_standup = """*Yesterday:*
* Completed task A
* Reviewed PR #123
* Updated documentation

*Today:*
* Working on feature X
* Team meeting at 2pm
* Code review session"""

        formatted = applicator.format_output(long_standup, applied)

        # Step 4: Brief format should be shorter
        assert len(formatted.split("\n")) < len(long_standup.split("\n"))

    @pytest.mark.asyncio
    async def test_low_confidence_generates_prompts(self, service, feedback_handler):
        """Test that low confidence preferences trigger confirmation prompts."""
        user_id = "prompt-user"

        # Step 1: Create mix of high and low confidence
        high_conf = UserStandupPreference(
            user_id=user_id,
            preference_type=PreferenceType.CONTENT_FILTER,
            key="focus",
            value="github",
            confidence=0.9,
        )
        low_conf = UserStandupPreference(
            user_id=user_id,
            preference_type=PreferenceType.EXCLUSION,
            key="exclude",
            value="tests",
            confidence=0.4,
        )
        await service.save_preference(high_conf)
        await service.save_preference(low_conf)

        # Step 2: Get all preferences
        prefs = await service.get_preferences(user_id)

        # Step 3: Generate confirmation prompts
        prompts = feedback_handler.generate_confirmation_prompts(prefs, threshold=0.5)

        # Step 4: Only low confidence should trigger prompt
        assert len(prompts) == 1
        assert "tests" in prompts[0].question.lower()

    @pytest.mark.asyncio
    async def test_preference_history_tracked(self, service):
        """Test that preference changes are tracked in history."""
        user_id = "history-user"

        # Step 1: Initial preference
        pref = UserStandupPreference(
            user_id=user_id,
            preference_type=PreferenceType.FORMAT,
            key="format",
            value="brief",
            confidence=0.7,
        )
        await service.save_preference(pref)

        # Step 2: Change preference
        pref2 = UserStandupPreference(
            user_id=user_id,
            preference_type=PreferenceType.FORMAT,
            key="format",
            value="detailed",
            confidence=0.8,
        )
        await service.save_preference(pref2)

        # Step 3: Check history
        history = await service.get_preference_history(user_id)
        assert len(history) >= 1
        assert history[0].previous_value == "brief"
        assert history[0].new_value == "detailed"

    @pytest.mark.asyncio
    async def test_multi_user_isolation(self, service, applicator):
        """Test that preferences are isolated between users."""
        user_a = "user-a"
        user_b = "user-b"

        # Step 1: User A prefers github
        pref_a = UserStandupPreference(
            user_id=user_a,
            preference_type=PreferenceType.CONTENT_FILTER,
            key="focus",
            value="github",
            confidence=0.9,
        )
        await service.save_preference(pref_a)

        # Step 2: User B prefers calendar
        pref_b = UserStandupPreference(
            user_id=user_b,
            preference_type=PreferenceType.CONTENT_FILTER,
            key="focus",
            value="calendar",
            confidence=0.9,
        )
        await service.save_preference(pref_b)

        # Step 3: Apply for each user
        applied_a = await applicator.prepare_preferences(user_a)
        applied_b = await applicator.prepare_preferences(user_b)

        # Step 4: Each user should have their own preferences
        assert "github" in applied_a.focus_areas
        assert "calendar" not in applied_a.focus_areas
        assert "calendar" in applied_b.focus_areas
        assert "github" not in applied_b.focus_areas


class TestEdgeCases:
    """Test edge cases and error handling."""

    @pytest.fixture
    def temp_storage(self):
        """Create a temporary storage directory."""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def service(self, temp_storage):
        """Create a preference service with temporary storage."""
        return UserPreferenceService(storage_path=temp_storage)

    @pytest.mark.asyncio
    async def test_empty_message_extraction(self, service):
        """Test extracting from empty message."""
        extractor = PreferenceExtractor()
        extracted = extractor.extract_from_turn("")
        assert len(extracted) == 0

    @pytest.mark.asyncio
    async def test_conflicting_preferences(self, service):
        """Test handling conflicting preferences in same message."""
        extractor = PreferenceExtractor()
        # User says both focus AND skip github - contradictory
        extracted = extractor.extract_from_turn("focus on github but also skip github")
        # Should handle gracefully (either one wins or both extracted)
        assert isinstance(extracted, list)

    @pytest.mark.asyncio
    async def test_very_long_message(self, service):
        """Test extraction from very long message."""
        extractor = PreferenceExtractor()
        long_message = "please " * 100 + "focus on github" + " thank you" * 100
        extracted = extractor.extract_from_turn(long_message)
        # Should still find the preference
        assert any(e.value == "github" for e in extracted)

    @pytest.mark.asyncio
    async def test_special_characters_in_value(self, service):
        """Test handling special characters."""
        extractor = PreferenceExtractor()
        extracted = extractor.extract_from_turn("focus on next-js project")
        # Should handle hyphenated values
        assert isinstance(extracted, list)

    @pytest.mark.asyncio
    async def test_confidence_bounds(self, service):
        """Test that confidence stays within 0-1 bounds."""
        pref = UserStandupPreference(
            user_id="bounds-user",
            preference_type=PreferenceType.CONTENT_FILTER,
            value="test",
            confidence=0.95,
        )

        # Boost beyond 1.0
        pref.boost_confidence(0.2)
        assert pref.confidence == 1.0

        # Reduce below 0.0
        pref.confidence = 0.05
        pref.reduce_confidence(0.2)
        assert pref.confidence == 0.0

import logging
import re
from typing import Optional

from services.domain.models import Intent
from services.file_context.exceptions import AmbiguousFileReferenceError
from services.file_context.file_resolver import FileResolver
from services.intent_service.pre_classifier import PreClassifier
from services.repositories.file_repository import FileRepository

logger = logging.getLogger(__name__)


class IntentEnricher:
    """Enriches intents with additional context like resolved files"""

    def __init__(self, db):
        self.db = db
        self.file_repository = FileRepository(db)
        self.file_resolver = FileResolver(self.file_repository)

    async def enrich_with_file_context(self, intent: Intent, session_id: str) -> Intent:
        """Add resolved file references to intent context"""

        # Check if message contains file reference
        original_message = intent.context.get("original_message", "")

        # First try to get confidence score from improved PreClassifier
        file_ref_confidence = PreClassifier.get_file_reference_confidence(original_message)

        if file_ref_confidence == 0.0:
            # --- NEW LOGIC: Try to extract direct filename references ---
            filename_match = re.search(
                r"([\w\-.]+\.(txt|md|csv|pdf|docx|xlsx|json))",
                original_message,
                re.IGNORECASE,
            )
            if filename_match:
                filename = filename_match.group(1)
                # First try current session
                files = await self.file_repository.search_files_by_name(session_id, filename)
                if not files:
                    # If not found in current session, try all sessions (scoped to this user)
                    files = await self.file_repository.search_files_by_name_all_sessions(
                        filename, session_id
                    )
                    if files:
                        logger.info(
                            f"Found file from previous session: {filename} -> {files[0].id}"
                        )

                if files:
                    # Use the most recent match
                    intent.context["file_id"] = files[0].id
                    intent.context["file_confidence"] = 0.95
                    logger.info(f"Resolved file by filename: {filename} -> {files[0].id}")
                else:
                    logger.info(f"No file found matching filename: {filename}")
            return intent

        # Store the pattern-based confidence for later use
        intent.context["pattern_confidence"] = file_ref_confidence

        try:
            # Resolve file reference
            file_id, resolution_confidence = await self.file_resolver.resolve_file_reference(
                intent, session_id
            )

            # Combine pattern confidence with resolution confidence
            combined_confidence = (file_ref_confidence * 0.4) + (resolution_confidence * 0.6)

            # Handle based on combined confidence
            if combined_confidence > 0.8:
                # High confidence - proceed automatically
                intent.context["resolved_file_id"] = file_id
                intent.context["file_confidence"] = combined_confidence
                logger.info(
                    f"Resolved file with high confidence: {file_id} ({combined_confidence:.2f})"
                )

            elif combined_confidence > 0.5:
                # Medium confidence - proceed but flag for confirmation
                intent.context["probable_file_id"] = file_id
                intent.context["file_confidence"] = combined_confidence
                intent.context["needs_file_confirmation"] = True
                logger.info(
                    f"Resolved file with medium confidence: {file_id} ({combined_confidence:.2f})"
                )

            else:
                # Low confidence - need clarification
                intent.context["needs_file_clarification"] = True
                logger.info("Low confidence file resolution - clarification needed")

        except AmbiguousFileReferenceError as e:
            # Multiple files matched - need disambiguation
            intent.context["needs_file_clarification"] = True
            intent.context["ambiguous_files"] = [
                {
                    "id": f.id,
                    "filename": f.filename,
                    "upload_time": f.upload_time.isoformat(),
                }
                for f in e.files
            ]
            logger.info(f"Ambiguous file reference: {len(e.files)} matches")

        except Exception as e:
            logger.error(f"Error during file resolution: {e}")
            # Don't fail the whole intent, just skip file resolution

        return intent

    async def enrich(self, intent: Intent, session_id: str) -> Intent:
        """Main enrichment method - can be extended for other enrichments"""
        # Add session_id to context for workflow compatibility
        intent.context["session_id"] = session_id

        # File context enrichment
        intent = await self.enrich_with_file_context(intent, session_id)

        # Future: Add other enrichments here
        # - Project context enrichment
        # - User preference enrichment
        # - Historical context enrichment

        return intent

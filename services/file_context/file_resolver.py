"""Intelligent file reference resolution"""

import re
from datetime import datetime, timedelta
from typing import List, Optional, Tuple

from services.domain.models import Intent, UploadedFile
from services.repositories.file_repository import FileRepository

from .exceptions import AmbiguousFileReferenceError, NoFilesFoundError


class FileResolver:
    """Intelligent file reference resolution"""

    def __init__(self, file_repository: FileRepository):
        self.repo = file_repository

        # File type preferences for different intent actions
        self.file_type_preferences = {
            "analyze_report": [
                "application/pdf",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ],
            "analyze_data": [
                "text/csv",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "application/json",
            ],
            "review_document": [
                "application/pdf",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                "text/plain",
            ],
            "process_spreadsheet": [
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "text/csv",
            ],
            "ingest_generic": [],  # No preference, accept any
        }

    async def resolve_file_reference(
        self, intent: Intent, session_id: str
    ) -> Tuple[Optional[str], float]:
        """
        Resolve file reference with confidence score
        Returns: (file_id, confidence) or (None, 0.0)
        """
        original_message = intent.context.get("original_message", "").lower()

        # Check for temporal references that might span sessions
        temporal_patterns = [
            r"\b(few days ago|days ago|yesterday|last week|earlier|previously|before|recently)\b",
            r"\b(uploaded.*ago|uploaded.*earlier|uploaded.*before|uploaded.*recently)\b",
            r"\b(just uploaded|I uploaded|I just uploaded|the file I uploaded)\b",
            r"\b(that file|the file|my file)\b",
        ]

        is_temporal_reference = any(
            re.search(pattern, original_message) for pattern in temporal_patterns
        )

        if is_temporal_reference:
            # For temporal references, search across sessions
            files = await self.repo.get_recent_files_all_sessions(days=7)
            if not files:
                return None, 0.0
        else:
            # Get all files for the current session
            files = await self.repo.get_files_for_session(session_id, limit=20)

            if not files:
                return None, 0.0

        # SPECIAL CASE: If only one file in session and explicit reference
        # ("the file", "that file", "file I uploaded"), use it with high confidence
        explicit_references = [
            "the file",
            "that file",
            "file i",
            "document i",
            "what i uploaded",
            "just uploaded",
        ]

        if len(files) == 1 and any(ref in original_message for ref in explicit_references):
            # Single file with explicit reference = no ambiguity
            return files[0].id, 0.95  # Very high confidence

        # Score each file
        scored_files = []
        for file in files:
            score = self._calculate_score(file, intent)
            scored_files.append((file, score))

        # Sort by score (highest first)
        scored_files.sort(key=lambda x: x[1], reverse=True)

        # Get the best match
        if not scored_files:
            return None, 0.0

        best_file, best_score = scored_files[0]

        # Check for ambiguity (multiple files with similar scores)
        if len(scored_files) > 1:
            second_best_score = scored_files[1][1]
            if best_score - second_best_score < 0.2:  # Close scores indicate ambiguity
                raise AmbiguousFileReferenceError(
                    [f for f, _ in scored_files[:3]],  # Top 3 candidates
                    [s for _, s in scored_files[:3]],
                )

        # Return result with confidence
        return best_file.id, best_score

    def _calculate_score(self, file: UploadedFile, intent: Intent) -> float:
        """Multi-factor scoring algorithm"""
        total_score = 0.0
        components = {}

        # Factor 1: Recency (max 0.3)
        recency_score = self._calculate_recency_score(file.upload_time)
        components["recency"] = recency_score
        total_score += recency_score * 0.3

        # Factor 2: File type relevance (max 0.3)
        type_score = self._calculate_type_score(file.file_type, intent.action)
        components["type"] = type_score
        total_score += type_score * 0.3

        # Factor 3: Filename matching (max 0.2)
        name_score = self._calculate_name_score(file.filename, intent)
        components["name"] = name_score
        total_score += name_score * 0.2

        # Factor 4: Usage history (max 0.2)
        usage_score = self._calculate_usage_score(file)
        components["usage"] = usage_score
        total_score += usage_score * 0.2

        final_score = min(total_score, 1.0)  # Cap at 1.0

        # Debug logging
        print(f"DEBUG Scoring {file.filename}: total={final_score:.3f}, components={components}")

        return final_score

    def _calculate_recency_score(self, upload_time: datetime) -> float:
        """Calculate recency score (0.0 to 1.0)"""
        if not upload_time:
            return 0.0

        now = datetime.now()
        age = now - upload_time

        # Last 5 minutes: full score
        if age <= timedelta(minutes=5):
            return 1.0

        # Decay over 1 hour
        if age <= timedelta(hours=1):
            minutes_old = age.total_seconds() / 60
            return max(0.0, 1.0 - (minutes_old / 60))

        # Very old files get minimal score
        return 0.1

    def _calculate_type_score(self, file_type: str, intent_action: str) -> float:
        """Calculate file type relevance score"""
        if not file_type or not intent_action:
            return 0.5  # Neutral score

        preferred_types = self.file_type_preferences.get(intent_action, [])

        if not preferred_types:
            return 0.5  # No preference, neutral score

        if file_type in preferred_types:
            return 1.0  # Perfect match

        # Check for partial matches (e.g., "pdf" in "application/pdf")
        file_extension = file_type.split("/")[-1] if "/" in file_type else file_type
        for preferred in preferred_types:
            if file_extension in preferred or preferred in file_type:
                return 0.7  # Partial match

        return 0.2  # Poor match

    def _calculate_name_score(self, filename: str, intent: Intent) -> float:
        """Calculate filename relevance score"""
        if not filename:
            return 0.0

        # Extract keywords from intent context and action
        keywords = []

        # Add action keywords
        action_keywords = intent.action.split("_")
        keywords.extend(action_keywords)

        # Add context keywords
        if intent.context:
            context_text = str(intent.context).lower()
            # Extract meaningful words (improved regex)
            words = re.findall(r"\b[a-z0-9_-]{3,}\b", context_text)
            keywords.extend(words)

        if not keywords:
            return 0.5  # No keywords, neutral score

        # Check filename against keywords
        filename_lower = filename.lower()
        matches = 0
        for keyword in keywords:
            if keyword.lower() in filename_lower:
                matches += 1

        if matches == 0:
            return 0.1  # No matches

        # Score based on match ratio
        match_ratio = matches / len(keywords)
        return min(match_ratio, 1.0)

    def _calculate_usage_score(self, file: UploadedFile) -> float:
        """Calculate usage history score"""
        if not file.reference_count:
            return 0.5  # No usage history, neutral score

        # Recent references worth more
        recency_bonus = 0.0
        if file.last_referenced:
            age = datetime.now() - file.last_referenced
            if age <= timedelta(hours=1):
                recency_bonus = 0.3
            elif age <= timedelta(hours=24):
                recency_bonus = 0.1

        # Base score from reference count (capped)
        base_score = min(file.reference_count / 10.0, 0.7)

        return min(base_score + recency_bonus, 1.0)

    async def get_resolution_suggestions(
        self, session_id: str, reference: str
    ) -> List[Tuple[UploadedFile, float]]:
        """Get file suggestions for ambiguous references"""
        files = await self.repo.get_files_for_session(session_id, limit=10)

        if not files:
            return []

        # Simple scoring based on filename similarity
        scored_files = []
        for file in files:
            # Simple fuzzy matching
            filename_lower = file.filename.lower()
            reference_lower = reference.lower()

            score = 0.0
            if reference_lower in filename_lower:
                score = 0.8
            elif any(word in filename_lower for word in reference_lower.split()):
                score = 0.5

            scored_files.append((file, score))

        # Sort by score and return top matches
        scored_files.sort(key=lambda x: x[1], reverse=True)
        return scored_files[:5]  # Top 5 suggestions

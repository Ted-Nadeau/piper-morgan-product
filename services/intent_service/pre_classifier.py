import re
import string
from typing import Optional

from services.domain.models import Intent
from services.shared_types import IntentCategory


class PreClassifier:
    """Rule-based pre-classification for common patterns"""

    # Greeting patterns - using regex with word boundaries for precision
    GREETING_PATTERNS = [
        r"\bhello\b",
        r"\bhi\b",
        r"\bhey\b",
        r"\bgood morning\b",
        r"\bgood afternoon\b",
        r"\bgood evening\b",
        r"\bgreetings\b",
        r"\bhowdy\b",
        r"\bhi there\b",
    ]

    # Farewell patterns - using regex with word boundaries for precision
    FAREWELL_PATTERNS = [
        r"\bbye\b",
        r"\bgoodbye\b",
        r"\bsee you\b",
        r"\blater\b",
        r"\bfarewell\b",
    ]

    # Thanks patterns - using regex with word boundaries for precision
    THANKS_PATTERNS = [
        r"\bthanks\b",
        r"\bthank you\b",
        r"\bthx\b",
        r"\bty\b",
        r"\bmuch appreciated\b",
    ]

    # Canonical query patterns for enhanced standup experience
    IDENTITY_PATTERNS = [
        r"\bwhat'?s your name\b",
        r"\bwho are you\b",
        r"\byour role\b",
        r"\bwhat do you do\b",
        r"\btell me about yourself\b",
        r"\bintroduce yourself\b",
        r"\bwhat are your capabilities\b",
    ]

    TEMPORAL_PATTERNS = [
        r"\bwhat day is it\b",
        r"\bwhat'?s the date\b",
        r"\bwhat time is it\b",
        r"\bcurrent date\b",
        r"\btoday'?s date\b",
        r"\bwhat'?s today\b",
        r"\bdate and time\b",
    ]

    STATUS_PATTERNS = [
        r"\bwhat am i working on\b",
        r"\bwhat'?s my current project\b",
        r"\bmy projects\b",
        r"\bcurrent work\b",
        r"\bwhat'?s on my plate\b",
        r"\bmy portfolio\b",
        r"\bwhat'?s my status\b",
        r"\bproject status\b",
    ]

    PRIORITY_PATTERNS = [
        r"\bwhat'?s my top priority\b",
        r"\bhighest priority\b",
        r"\bmost important task\b",
        r"\bwhat should i do first\b",
        r"\bmy priorities\b",
        r"\btop priority\b",
        r"\bpriority one\b",
    ]

    GUIDANCE_PATTERNS = [
        r"\bwhat should i focus on\b",
        r"\bwhere should i focus\b",
        r"\bwhat'?s next\b",
        r"\bguidance\b",
        r"\brecommendation\b",
        r"\badvice\b",
        r"\bwhat now\b",
        r"\bnext steps\b",
        r"\bshould i focus\b",
    ]

    # File reference patterns (with variations and typo tolerance)
    FILE_REFERENCE_PATTERNS = [
        # Direct references
        r"\b(the file|that file|my file|this file)\b",
        r"\b(the document|that document|my document|this document)\b",
        r"\b(the doc|that doc|my doc|this doc)\b",
        r"\b(what i uploaded|the upload|that upload|this upload)\b",
        # File types
        r"\b(the csv|that csv|my csv|this csv)\b",
        r"\b(the pdf|that pdf|my pdf|this pdf)\b",
        r"\b(the spreadsheet|that spreadsheet|my spreadsheet|this spreadsheet)\b",
        r"\b(the excel file|that excel file|my excel file|this excel file)\b",
        r"\b(the report|that report|my report|this report)\b",
        r"\b(the data file|that data file|my data file|this data file)\b",
        r"\b(the text file|that text file|my text file|this text file)\b",
        r"\b(the markdown file|that markdown file|my markdown file|this markdown file)\b",
        r"\b(the json file|that json file|my json file|this json file)\b",
        # Abbreviated forms
        r"\b(the txt|that txt|my txt|this txt)\b",
        r"\b(the md|that md|my md|this md)\b",
        r"\b(the xlsx|that xlsx|my xlsx|this xlsx)\b",
        r"\b(the docx|that docx|my docx|this docx)\b",
        # Generic patterns with adjectives
        r"\b(that \w+(?:\s+\w+)* file|the \w+(?:\s+\w+)* file|my \w+(?:\s+\w+)* file|this \w+(?:\s+\w+)* file)\b",
        r"\b(that \w+(?:\s+\w+)* document|the \w+(?:\s+\w+)* document|my \w+(?:\s+\w+)* document|this \w+(?:\s+\w+)* document)\b",
        r"\b(that \w+(?:\s+\w+)* doc|the \w+(?:\s+\w+)* doc|my \w+(?:\s+\w+)* doc|this \w+(?:\s+\w+)* doc)\b",
        # Common typos and variations
        r"\b(teh file|taht file|th file)\b",
        r"\b(documnet|docuemnt|docment)\b",
        r"\b(fiel|fils|fille)\b",
        r"\b(uploded|uplaoded|uploadd)\b",
        r"\b(reprot|reoprt|raport)\b",
        r"\b(excell|exel|excel)\b",
        r"\b(spreedsheet|spredsheet|spreadsheat)\b",
        # Integration-related typos (from handoff doc)
        r"\b(intregration|integartion|intergration)\b",
        r"\b(analys[ei]s|analisys|anlyze)\b",
        r"\b(summar[iy]ze|summerize|summarise)\b",
    ]

    @staticmethod
    def pre_classify(message: str) -> Optional[Intent]:
        """Pre-classify message using rule-based patterns"""
        clean_msg = message.strip().lower()
        clean_for_matching = clean_msg.rstrip(string.punctuation + "!?.,;:😊🙂👋")

        # DEBUG: Log the processing
        import structlog

        logger = structlog.get_logger()
        logger.info(f"PRE_CLASSIFIER DEBUG - Original: '{message}'")
        logger.info(f"PRE_CLASSIFIER DEBUG - Clean: '{clean_msg}'")
        logger.info(f"PRE_CLASSIFIER DEBUG - Clean for matching: '{clean_for_matching}'")

        # Check for greetings
        greeting_match = PreClassifier._matches_patterns(
            clean_for_matching, PreClassifier.GREETING_PATTERNS
        )
        logger.info(f"PRE_CLASSIFIER DEBUG - Greeting match: {greeting_match}")
        if greeting_match:
            # Find which pattern matched for debugging
            for pattern in PreClassifier.GREETING_PATTERNS:
                if re.search(pattern, clean_for_matching):
                    logger.info(f"PRE_CLASSIFIER DEBUG - Matched greeting pattern: '{pattern}'")
                    break
            return Intent(
                category=IntentCategory.CONVERSATION,
                action="greeting",
                confidence=1.0,
                context={"original_message": message},
            )

        # Check for farewells
        if PreClassifier._matches_patterns(clean_for_matching, PreClassifier.FAREWELL_PATTERNS):
            return Intent(
                category=IntentCategory.CONVERSATION,
                action="farewell",
                confidence=1.0,
                context={"original_message": message},
            )

        # Check for thanks
        if PreClassifier._matches_patterns(clean_for_matching, PreClassifier.THANKS_PATTERNS):
            return Intent(
                category=IntentCategory.CONVERSATION,
                action="thanks",
                confidence=1.0,
                context={"original_message": message},
            )

        # Check for canonical queries
        if PreClassifier._matches_patterns(clean_for_matching, PreClassifier.IDENTITY_PATTERNS):
            return Intent(
                category=IntentCategory.IDENTITY,
                action="get_identity",
                confidence=1.0,
                context={"original_message": message},
            )

        if PreClassifier._matches_patterns(clean_for_matching, PreClassifier.TEMPORAL_PATTERNS):
            return Intent(
                category=IntentCategory.TEMPORAL,
                action="get_current_time",
                confidence=1.0,
                context={"original_message": message},
            )

        if PreClassifier._matches_patterns(clean_for_matching, PreClassifier.STATUS_PATTERNS):
            return Intent(
                category=IntentCategory.STATUS,
                action="get_project_status",
                confidence=1.0,
                context={"original_message": message},
            )

        if PreClassifier._matches_patterns(clean_for_matching, PreClassifier.PRIORITY_PATTERNS):
            return Intent(
                category=IntentCategory.PRIORITY,
                action="get_top_priority",
                confidence=1.0,
                context={"original_message": message},
            )

        if PreClassifier._matches_patterns(clean_for_matching, PreClassifier.GUIDANCE_PATTERNS):
            return Intent(
                category=IntentCategory.GUIDANCE,
                action="get_contextual_guidance",
                confidence=1.0,
                context={"original_message": message},
            )

        return None

    @staticmethod
    def detect_file_reference(message: str) -> bool:
        """Check if message references an uploaded file"""
        clean_msg = message.strip().lower()

        # Exclude verb usage of "file" (e.g., "file the report", "file a complaint")
        verb_file_patterns = [
            r"\bfile\s+(?:the|a|an|this|that)\s+\w+",  # "file the report", "file a complaint"
            r"\bfile\s+\w+\s+(?:for|against|with)",  # "file complaint for", "file report against"
        ]

        # If message matches verb usage patterns, it's not a file reference
        if PreClassifier._matches_patterns(clean_msg, verb_file_patterns):
            return False

        return PreClassifier._matches_patterns(clean_msg, PreClassifier.FILE_REFERENCE_PATTERNS)

    @staticmethod
    def get_file_reference_confidence(message: str) -> float:
        """Calculate confidence score for file reference detection"""
        clean_msg = message.strip().lower()

        # Different patterns have different confidence weights
        high_confidence_patterns = [
            r"\b(the file|that file|my file|this file)\b",
            r"\b(the document|that document|my document|this document)\b",
            r"\b(what i uploaded|the upload|that upload|this upload|my upload)\b",
        ]

        medium_confidence_patterns = [
            r"\b(the csv|that csv|my csv|this csv)\b",
            r"\b(the pdf|that pdf|my pdf|this pdf)\b",
            r"\b(the doc|that doc|my doc|this doc)\b",
            r"\b(the report|that report|my report|this report)\b",
        ]

        low_confidence_patterns = [
            r"\b(teh file|taht file|th file)\b",
            r"\b(documnet|docuemnt|docment)\b",
            r"\b(fiel|fils|fille)\b",
            r"\b(uploded|uplaoded|uploadd)\b",
        ]

        # Check for matches and return highest confidence
        if PreClassifier._matches_patterns(clean_msg, high_confidence_patterns):
            return 0.9
        elif PreClassifier._matches_patterns(clean_msg, medium_confidence_patterns):
            return 0.7
        elif PreClassifier._matches_patterns(clean_msg, low_confidence_patterns):
            return 0.5
        elif PreClassifier._matches_patterns(clean_msg, PreClassifier.FILE_REFERENCE_PATTERNS):
            return 0.6  # Generic patterns
        else:
            return 0.0

    @staticmethod
    def _matches_patterns(message: str, patterns: list) -> bool:
        """Check if message matches any of the given patterns using regex"""
        for pattern in patterns:
            if re.search(pattern, message):
                return True
        return False

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
        # Issue #487: Added capability discovery patterns for alpha onboarding
        r"\bwhat services\b",
        r"\bwhat do you offer\b",
        r"\bwhat features\b",
        r"\bwhat can you help\b",
        r"\bshow me your capabilities\b",
        r"\bwhat can you do\b",
        r"\bmenu of services\b",
        r"\blist.*capabilities\b",
        r"\byour capabilities\b",
        # Issue #487 follow-up: Additional patterns from manual testing
        r"\bcapability menu\b",
        r"\bcapabilities menu\b",
        r"\bshow.*menu\b",
    ]

    TEMPORAL_PATTERNS = [
        # Time queries
        r"\bwhat time is it\b",
        r"\bwhat'?s the time\b",
        r"\bcurrent time\b",
        r"\btime now\b",
        r"\btell me the time\b",
        # Date queries
        r"\bwhat day is it\b",
        r"\bwhat'?s the date\b",
        r"\bcurrent date\b",
        r"\btoday'?s date\b",
        r"\bwhat'?s today\b",
        r"\bdate and time\b",
        r"\bday of the week\b",
        r"\btell me the date\b",
        r"\bwhat date is it\b",
        r"\btoday'?s day\b",
        # Calendar/schedule queries
        r"\bmy calendar\b",
        r"\bshow.{0,10}calendar\b",
        r"\bmy schedule\b",
        r"\bshow.{0,10}schedule\b",
        r"\bcalendar.*today\b",
        r"\bschedule.*today\b",
        r"\bwhat'?s on my calendar\b",
        r"\bwhat'?s on my schedule\b",
        r"\bmy appointments\b",
        r"\bshow.{0,10}appointments\b",
        # Meeting queries
        r"\bmy meetings\b",
        r"\bnext meeting\b",
        r"\bupcoming meetings\b",
        r"\bwhen is my.{0,10}meeting\b",
        r"\bwhen am i.{0,10}meeting\b",
        r"\bmeeting.*today\b",
        r"\bmeeting.*tomorrow\b",
        r"\bmeetings this week\b",
        # Event queries
        r"\bmy events\b",
        r"\bshow.{0,10}events\b",
        r"\bupcoming events\b",
        r"\bevents.*today\b",
        r"\bevents.*tomorrow\b",
        r"\bnext event\b",
        # Relative time
        r"\bagenda.*today\b",
        r"\bwork on today\b",
        r"\bwhat.*yesterday\b",
        r"\bdid.*yesterday\b",
        r"\bhappened yesterday\b",
        r"\blast time.*worked\b",
        r"\bhow long.*working\b",
        r"\bhow long.*been working\b",
        r"\bwhat'?s.{0,10}tomorrow\b",
        r"\btomorrow'?s schedule\b",
        r"\bthis week'?s\b",
        r"\bnext week'?s\b",
        r"\bthis month'?s\b",
        # Availability queries
        r"\bwhen am i free\b",
        r"\bwhen'?s my next.{0,10}free\b",
        r"\bavailable time\b",
        r"\bfree time\b",
        r"\bopen slots\b",
    ]

    STATUS_PATTERNS = [
        # Work status queries
        r"\bwhat am i working on\b",
        r"\bwhat'?s my current project\b",
        r"\bmy projects\b",
        r"\bcurrent work\b",
        # Removed: r"\bwhat'?s on my plate\b" - false positive with temporal ("what's on my plate today")
        r"\bmy portfolio\b",
        r"\bshow.*projects\b",
        r"\bcurrent projects\b",
        r"\bproject overview\b",
        r"\bproject landscape\b",
        r"\blist.*projects\b",
        r"\bprojects.*working on\b",
        r"\bwhat.*working on\b",
        r"\bworking on now\b",
        r"\bmy current work\b",
        r"\bactive projects\b",
        r"\bactive work\b",
        # Status update queries
        r"\bwhat'?s my status\b",
        r"\bproject status\b",
        r"\bstatus update\b",
        r"\bmy status\b",
        r"\bwork status\b",
        r"\bshow.*status\b",
        r"\bcurrent status\b",
        r"\bstatus report\b",
        # Standup queries (with context to avoid false positives)
        # Removed: r"\bstandup\b" - false positive with temporal ("what time is standup")
        r"\bstand-up\b",
        r"\bstand up\b",
        r"\bmy standup\b",
        r"\bstandup update\b",
        r"\bstandup report\b",
        r"\bdaily standup\b",
        r"\bshow.*standup\b",
        # Progress queries
        r"\bmy progress\b",
        r"\bprogress update\b",
        r"\bprogress report\b",
        r"\bprogress on\b",
        r"\bshow.*progress\b",
        r"\bcurrent progress\b",
        r"\bhow'?s.*progress\b",
        r"\bwhat'?s.*progress\b",
        # Task queries
        r"\bmy tasks\b",
        r"\bcurrent tasks\b",
        r"\bactive tasks\b",
        r"\bshow.*tasks\b",
        r"\blist.*tasks\b",
        r"\btasks.*working\b",
        r"\bwhat tasks\b",
        r"\btask status\b",
        # Assignment queries
        r"\bmy assignments\b",
        r"\bcurrent assignments\b",
        r"\bwhat'?s assigned\b",
        r"\bshow.*assignments\b",
    ]

    # Issue #521: Contextual Intelligence query patterns
    # MUST be checked BEFORE PRIORITY to avoid pattern collision
    CONTEXTUAL_QUERY_PATTERNS = [
        # Changes query - Query #29
        r"\bwhat changed since\b",
        r"\bwhat'?s changed since\b",
        r"\bshow.*changes since\b",
        r"\bshow me.*changed\b",
        r"\bchanges since\b",
        r"\bactivity since\b",
        r"\bupdates since\b",
        # Attention query - Query #30
        r"\bwhat needs my attention\b",
        r"\bwhat needs attention\b",
        r"\bneeds my attention\b",
        r"\bshow.*needs.*attention\b",
        r"\bitems.*need.*attention\b",
        r"\battention items\b",
    ]

    # Issue #523: Phase A Canonical Query patterns
    # Calendar queries - Queries #34, #35, #61
    CALENDAR_QUERY_PATTERNS = [
        # Meeting time query - Query #34
        r"\bhow much time in meetings\b",
        r"\bhow much time.*meetings\b",
        r"\btime spent in meetings\b",
        r"\bmeeting time\b",
        # Recurring meetings query - Query #35
        r"\breview.*recurring meetings\b",
        r"\bshow.*recurring meetings\b",
        r"\baudit.*standing meetings\b",
        r"\brecurring meetings\b",
        # Week calendar query - Query #61
        r"\bwhat'?s my week look like\b",
        r"\bshow.*my week\b",
        r"\bweek ahead\b",
        r"\bweek calendar\b",
    ]

    # GitHub queries - Queries #41, #42, #45, #59, #60
    GITHUB_QUERY_PATTERNS = [
        # Shipped query - Query #41
        r"\bwhat did we ship\b",
        r"\bwhat shipped\b",
        r"\bshow.*what.*shipped\b",
        r"\bwhat.*shipped.*week\b",
        # Stale PRs query - Query #42
        r"\bshow.*stale prs\b",
        r"\bstale pull requests\b",
        r"\bold prs\b",
        r"\bprs.*needing review\b",
        # Close issue query - Query #45
        r"\bclose issue\s*#?\d+\b",
        r"\bclose.*completed.*issue\b",
        r"\bclose.*issue\b",
        # Comment issue query - Query #59
        r"\bcomment on issue\s*#?\d+\b",
        r"\badd comment to issue\s*#?\d+\b",
        r"\breply to issue\s*#?\d+\b",
        r"\bcomment\s+on\s+#?\d+\b",
        # Review issue query - Query #60
        r"\breview issue\s*#?\d+\b",
        r"\bshow.*issue\s*#?\d+\b",
        r"\bissue\s*#?\d+\s*details\b",
        r"\bget issue\s*#?\d+\b",
    ]

    # Productivity query - Query #51
    PRODUCTIVITY_QUERY_PATTERNS = [
        r"\bwhat'?s my productivity\b",
        r"\bshow.*productivity\b",
        r"\bproductivity metrics\b",
        r"\bmy productivity\b",
    ]

    # Todo queries - Queries #56, #57
    TODO_QUERY_PATTERNS = [
        # List todos query - Query #56
        r"\bshow my todos\b",
        r"\blist my todos\b",
        r"\bwhat are my todos\b",
        r"\bmy todos\b",
        # Next todo query - Query #57
        r"\bwhat'?s my next todo\b",
        r"\bnext todo\b",
        r"\bwhat should i do next\b",
        r"\bwhat.*next.*do\b",
    ]

    # Issue #522: Document update query patterns - Query #40
    DOCUMENT_QUERY_PATTERNS = [
        # Update document patterns
        r"\bupdate\s+(?:the\s+)?[\w\s]+\s+doc(?:ument)?\b",
        r"\bedit\s+(?:the\s+)?[\w\s]+\s+doc(?:ument)?\b",
        r"\bmodify\s+(?:the\s+)?[\w\s]+\s+doc(?:ument)?\b",
        r"\bchange\s+(?:the\s+)?[\w\s]+\s+doc(?:ument)?\b",
        # Add to document patterns
        r"\badd\s+(?:to\s+)?(?:the\s+)?[\w\s]+\s+doc(?:ument)?\b",
        r"\bappend\s+(?:to\s+)?(?:the\s+)?[\w\s]+\s+doc(?:ument)?\b",
        # Update with content patterns (e.g., "update X with Y", "edit X with Y")
        r"\bupdate\s+(?:the\s+)?[\w\s]+\s+with\b",
        r"\bedit\s+(?:the\s+)?[\w\s]+\s+with\b",
        r"\bmodify\s+(?:the\s+)?[\w\s]+\s+with\b",
        r"\bchange\s+(?:the\s+)?[\w\s]+\s+to\b",
    ]

    PRIORITY_PATTERNS = [
        # Priority queries
        r"\bmy priorities\b",
        r"\bwhat'?s my top priority\b",
        r"\btop priority\b",
        r"\bhighest priority\b",
        r"\bpriority one\b",
        r"\bshow.*priorities\b",
        r"\blist.*priorities\b",
        r"\bwhat are my priorities\b",
        r"\bcurrent priorities\b",
        r"\btop priorities\b",
        r"\bkey priorities\b",
        # Importance queries
        r"\bmost important\b",
        r"\bmost important task\b",
        r"\bmost important work\b",
        r"\bwhat'?s most important\b",
        r"\bwhat matters most\b",
        r"\bkey tasks\b",
        r"\bkey items\b",
        # Focus queries
        r"\bwhat should i focus on\b",
        r"\bshould i focus\b",
        r"\bwhat.*focus on\b",
        r"\bwhere.*focus\b",
        r"\bfocus areas\b",
        r"\bfocus on today\b",
        r"\bfocus this week\b",
        r"\bwhat to focus\b",
        # Urgency queries
        r"\bwhat'?s urgent\b",
        r"\burgent tasks\b",
        r"\burgent items\b",
        r"\burgent work\b",
        r"\bmost urgent\b",
        r"\bneeds.*focus\b",
        r"\brequires attention\b",
        # Critical queries
        r"\bwhat'?s critical\b",
        r"\bcritical tasks\b",
        r"\bcritical items\b",
        r"\bcritical work\b",
        r"\bmost critical\b",
        # Next action queries
        r"\bwhat should i do first\b",
        r"\bwhat.*next\b",
        r"\bwhat.*first\b",
        r"\bwhich project.*focus\b",
        r"\bwhich task.*focus\b",
        r"\bwhat.*work on next\b",
        r"\bwhat to do\b",
    ]

    GUIDANCE_PATTERNS = [
        # GREAT-4A: Removed focus patterns (moved to PRIORITY)
        r"\bwhere should i focus\b",
        r"\bwhat'?s next\b",
        r"\bguidance\b",
        r"\brecommendation\b",
        r"\badvice\b",
        r"\bwhat now\b",
        r"\bnext steps\b",
        # GAP-3 Phase 2: Added October 13, 2025 - Edge case patterns for GUIDANCE disambiguation
        r"\bwhat should (i|we) do (about|with)\b",  # Advice-seeking questions
        r"\badvise (me|us) on\b",  # Direct advice requests
        r"\bwhat('?s| is) the process for\b",  # Process/how-to questions
        # Issue #487: Added setup/configuration patterns for alpha onboarding
        r"\bhelp.*setup\b",
        r"\bhelp.*configure\b",
        r"\bsetup.*projects?\b",  # matches "setup project" or "setup projects"
        r"\bconfigure.*projects?\b",  # matches "configure project" or "configure projects"
        r"\bhow do i.*setup\b",
        r"\bhow do i.*configure\b",
        r"\bget started\b",
        r"\bgetting started\b",
        # Issue #487 follow-up: "set up" with space (common user spelling)
        r"\bhelp.*set up\b",
        r"\bset up.*projects?\b",
        r"\bhow do i.*set up\b",
        r"\bset up.*portfolio\b",
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

        # Issue #521: Check CONTEXTUAL_QUERY before TEMPORAL to prevent pattern collision
        # "what changed since yesterday" would match r"\bwhat.*yesterday\b" in TEMPORAL
        # but should route to changes_query instead
        if PreClassifier._matches_patterns(
            clean_for_matching, PreClassifier.CONTEXTUAL_QUERY_PATTERNS
        ):
            # Determine specific action based on which pattern matched
            if any(
                re.search(pattern, clean_for_matching)
                for pattern in [
                    r"\bwhat changed since\b",
                    r"\bwhat'?s changed since\b",
                    r"\bshow.*changes since\b",
                    r"\bshow me.*changed\b",
                    r"\bchanges since\b",
                    r"\bactivity since\b",
                    r"\bupdates since\b",
                ]
            ):
                action = "changes_query"
            else:
                action = "attention_query"

            return Intent(
                category=IntentCategory.QUERY,
                action=action,
                confidence=1.0,
                context={"original_message": message},
            )

        # Issue #523: Phase A Canonical Query patterns
        # Check Calendar queries (Queries #34, #35, #61)
        if PreClassifier._matches_patterns(
            clean_for_matching, PreClassifier.CALENDAR_QUERY_PATTERNS
        ):
            # Determine specific action based on which pattern matched
            if any(
                re.search(pattern, clean_for_matching)
                for pattern in [
                    r"\bhow much time in meetings\b",
                    r"\bhow much time.*meetings\b",
                    r"\btime spent in meetings\b",
                    r"\bmeeting time\b",
                ]
            ):
                action = "meeting_time_query"
            elif any(
                re.search(pattern, clean_for_matching)
                for pattern in [
                    r"\breview.*recurring meetings\b",
                    r"\bshow.*recurring meetings\b",
                    r"\baudit.*standing meetings\b",
                    r"\brecurring meetings\b",
                ]
            ):
                action = "recurring_meetings_query"
            else:
                action = "week_calendar_query"

            return Intent(
                category=IntentCategory.QUERY,
                action=action,
                confidence=1.0,
                context={"original_message": message},
            )

        # Check GitHub queries (Queries #41, #42, #45, #59, #60)
        if PreClassifier._matches_patterns(clean_for_matching, PreClassifier.GITHUB_QUERY_PATTERNS):
            # Determine specific action based on which pattern matched
            if any(
                re.search(pattern, clean_for_matching)
                for pattern in [
                    r"\bwhat did we ship\b",
                    r"\bwhat shipped\b",
                    r"\bshow.*what.*shipped\b",
                    r"\bwhat.*shipped.*week\b",
                ]
            ):
                action = "shipped_query"
            elif any(
                re.search(pattern, clean_for_matching)
                for pattern in [
                    r"\bshow.*stale prs\b",
                    r"\bstale pull requests\b",
                    r"\bold prs\b",
                    r"\bprs.*needing review\b",
                ]
            ):
                action = "stale_prs_query"
            elif any(
                re.search(pattern, clean_for_matching)
                for pattern in [
                    r"\bclose issue\s*#?\d+\b",
                    r"\bclose.*completed.*issue\b",
                    r"\bclose.*issue\b",
                ]
            ):
                action = "close_issue_query"
            elif any(
                re.search(pattern, clean_for_matching)
                for pattern in [
                    r"\bcomment on issue\s*#?\d+\b",
                    r"\badd comment to issue\s*#?\d+\b",
                    r"\breply to issue\s*#?\d+\b",
                    r"\bcomment\s+on\s+#?\d+\b",
                ]
            ):
                action = "comment_issue_query"
            else:
                # Review issue query - Query #60
                action = "review_issue_query"

            return Intent(
                category=IntentCategory.QUERY,
                action=action,
                confidence=1.0,
                context={"original_message": message},
            )

        # Check Productivity query (Query #51)
        if PreClassifier._matches_patterns(
            clean_for_matching, PreClassifier.PRODUCTIVITY_QUERY_PATTERNS
        ):
            return Intent(
                category=IntentCategory.QUERY,
                action="productivity_query",
                confidence=1.0,
                context={"original_message": message},
            )

        # Check Todo queries (Queries #56, #57)
        if PreClassifier._matches_patterns(clean_for_matching, PreClassifier.TODO_QUERY_PATTERNS):
            # Determine specific action based on which pattern matched
            if any(
                re.search(pattern, clean_for_matching)
                for pattern in [
                    r"\bshow my todos\b",
                    r"\blist my todos\b",
                    r"\bwhat are my todos\b",
                    r"\bmy todos\b",
                ]
            ):
                action = "list_todos_query"
            else:
                action = "next_todo_query"

            return Intent(
                category=IntentCategory.QUERY,
                action=action,
                confidence=1.0,
                context={"original_message": message},
            )

        # Issue #522: Check Document query patterns - Query #40
        if PreClassifier._matches_patterns(
            clean_for_matching, PreClassifier.DOCUMENT_QUERY_PATTERNS
        ):
            return Intent(
                category=IntentCategory.QUERY,
                action="update_document_query",
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

        # Issue #487: Check GUIDANCE before STATUS to catch "help setup my projects"
        # before "my projects" triggers STATUS. More specific patterns should match first.
        if PreClassifier._matches_patterns(clean_for_matching, PreClassifier.GUIDANCE_PATTERNS):
            return Intent(
                category=IntentCategory.GUIDANCE,
                action="get_contextual_guidance",
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

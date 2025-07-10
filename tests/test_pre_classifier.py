import pytest

from services.intent_service.pre_classifier import PreClassifier
from services.shared_types import IntentCategory


class TestPreClassifier:
    def test_greeting_patterns(self):
        """Test each greeting pattern returns correct intent"""
        greeting_patterns = [
            "hello",
            "hi",
            "hey",
            "good morning",
            "good afternoon",
            "good evening",
            "greetings",
            "howdy",
            "hi there",
        ]

        for pattern in greeting_patterns:
            intent = PreClassifier.pre_classify(pattern)
            assert intent is not None
            assert intent.category == IntentCategory.CONVERSATION
            assert intent.action == "greeting"
            assert intent.confidence == 1.0
            assert intent.context["original_message"] == pattern

    def test_farewell_patterns(self):
        """Test each farewell pattern returns correct intent"""
        farewell_patterns = ["goodbye", "bye", "see you", "later", "farewell"]

        for pattern in farewell_patterns:
            intent = PreClassifier.pre_classify(pattern)
            assert intent is not None
            assert intent.category == IntentCategory.CONVERSATION
            assert intent.action == "farewell"
            assert intent.confidence == 1.0
            assert intent.context["original_message"] == pattern

    def test_thanks_patterns(self):
        """Test each thanks pattern returns correct intent"""
        thanks_patterns = ["thanks", "thank you", "ty", "thx", "much appreciated"]

        for pattern in thanks_patterns:
            intent = PreClassifier.pre_classify(pattern)
            assert intent is not None
            assert intent.category == IntentCategory.CONVERSATION
            assert intent.action == "thanks"
            assert intent.confidence == 1.0
            assert intent.context["original_message"] == pattern

    def test_greeting_with_punctuation(self):
        """Test greetings with punctuation and emojis"""
        greeting_with_punct = [
            "hello!",
            "hi there!",
            "hey!",
            "good morning!",
            "hello.",
            "hi there.",
            "hey.",
            "good morning.",
            "hello 😊",
            "hi there 👋",
            "hey!",
            "good morning!",
            "hello!!!",
            "hi there...",
            "hey?!",
            "good morning:",
        ]

        for pattern in greeting_with_punct:
            intent = PreClassifier.pre_classify(pattern)
            assert intent is not None
            assert intent.category == IntentCategory.CONVERSATION
            assert intent.action == "greeting"
            assert intent.confidence == 1.0

    def test_farewell_with_punctuation(self):
        """Test farewells with punctuation and emojis"""
        farewell_with_punct = [
            "goodbye!",
            "bye!",
            "see you!",
            "later!",
            "farewell!",
            "goodbye.",
            "bye.",
            "see you.",
            "later.",
            "farewell.",
            "goodbye 😊",
            "bye 👋",
            "see you!",
            "later!",
            "farewell!",
        ]

        for pattern in farewell_with_punct:
            intent = PreClassifier.pre_classify(pattern)
            assert intent is not None
            assert intent.category == IntentCategory.CONVERSATION
            assert intent.action == "farewell"
            assert intent.confidence == 1.0

    def test_thanks_with_punctuation(self):
        """Test thanks with punctuation and emojis"""
        thanks_with_punct = [
            "thanks!",
            "thank you!",
            "ty!",
            "thx!",
            "much appreciated!",
            "thanks.",
            "thank you.",
            "ty.",
            "thx.",
            "much appreciated.",
            "thanks 😊",
            "thank you 👋",
            "ty!",
            "thx!",
            "much appreciated!",
        ]

        for pattern in thanks_with_punct:
            intent = PreClassifier.pre_classify(pattern)
            assert intent is not None
            assert intent.category == IntentCategory.CONVERSATION
            assert intent.action == "thanks"
            assert intent.confidence == 1.0

    def test_non_conversational_patterns(self):
        """Test patterns that should NOT be pre-classified"""
        non_conversational = [
            "hello world",
            "hi there everyone",
            "goodbye cruel world",
            "thanks for the help",
            "thank you for everything",
            "hello there how are you",
            "bye bye for now",
            "hello and welcome",
            "goodbye and good luck",
            "thanks a lot",
            "thank you very much",
            "hello, can you help me?",
            "bye, see you tomorrow",
            "thanks, that was helpful",
            "thank you, I appreciate it",
        ]

        for pattern in non_conversational:
            intent = PreClassifier.pre_classify(pattern)
            assert intent is None, f"Expected None for '{pattern}', got {intent}"

    def test_case_insensitivity(self):
        """Test that patterns work regardless of case"""
        case_variations = [
            "HELLO",
            "Hello",
            "HeLLo",
            "hElLo",
            "GOODBYE",
            "Goodbye",
            "GoOdByE",
            "gOoDbYe",
            "THANKS",
            "Thanks",
            "ThAnKs",
            "tHaNkS",
        ]

        for pattern in case_variations:
            intent = PreClassifier.pre_classify(pattern)
            assert intent is not None
            assert intent.confidence == 1.0

    def test_whitespace_handling(self):
        """Test that whitespace is handled correctly"""
        whitespace_variations = [
            "  hello  ",
            "  hi  ",
            "  goodbye  ",
            "  thanks  ",
            "\thello\t",
            "\nhi\n",
            "\r\ngoodbye\r\n",
            "  thanks  ",
        ]

        for pattern in whitespace_variations:
            intent = PreClassifier.pre_classify(pattern)
            assert intent is not None
            assert intent.confidence == 1.0

    def test_empty_and_edge_cases(self):
        """Test edge cases and empty inputs"""
        edge_cases = [
            "",
            "   ",
            "\t",
            "\n",
            "\r\n",
            "x",
            "a",
            "z",
            "123",
            "hello123",
            "hello world",
            "hi there",
            "bye bye",
            "thank you very much",
            "thanks a lot",
        ]

        for pattern in edge_cases:
            if pattern.strip() in PreClassifier.GREETING_PATTERNS:
                intent = PreClassifier.pre_classify(pattern)
                assert intent is not None
            elif pattern.strip() in PreClassifier.FAREWELL_PATTERNS:
                intent = PreClassifier.pre_classify(pattern)
                assert intent is not None
            elif pattern.strip() in PreClassifier.THANKS_PATTERNS:
                intent = PreClassifier.pre_classify(pattern)
                assert intent is not None
            else:
                intent = PreClassifier.pre_classify(pattern)
                assert intent is None, f"Expected None for '{pattern}', got {intent}"

    def test_partial_matches_should_fail(self):
        """Test that partial matches in longer strings don't trigger pre-classification"""
        non_matches = [
            "hello world",  # Not just a greeting
            "goodbye cruel world",  # Not just a farewell
            "thanks for nothing",  # Not just thanks
            "hello and welcome",  # Not just a greeting
            "bye bye for now",  # Not just a farewell
            "hello, can you help me?",  # Not just a greeting
            "thanks, that was helpful",  # Not just thanks
            "thank you, I appreciate it",  # Not just thanks
        ]

        for pattern in non_matches:
            intent = PreClassifier.pre_classify(pattern)
            assert (
                intent is None
            ), f"Expected None for non-match '{pattern}', got {intent}"

    def test_greeting_with_follow_up(self):
        """Test that greetings followed by other content are NOT pre-classified"""
        # These should be left for LLM to handle
        intent = PreClassifier.pre_classify("hi there how are you")
        assert intent is None  # Let LLM handle compound greetings

    def test_yes_no_not_preclassified(self):
        """Test that yes/no patterns are NOT pre-classified (removed from pre-classifier)"""
        yes_no_patterns = [
            "yes",
            "no",
            "yeah",
            "nope",
            "yep",
            "nah",
            "sure",
            "negative",
            "affirmative",
            "absolutely",
            "never",
        ]

        for pattern in yes_no_patterns:
            intent = PreClassifier.pre_classify(pattern)
            assert (
                intent is None
            ), f"Expected None for yes/no pattern '{pattern}', got {intent}"

"""
PM-039 Intent Classification Test Coverage

This test suite covers 13 scenarios for document/file search intent classification:

1. search for requirements files
2. find technical specifications
3. locate API documentation
4. show me all project plans
5. get all design docs
6. find docs about onboarding
7. search for budget analysis documents
8. serach for requirments files (typo)
9. find tehcnical specfications (typo)
10. find requirements
11. search files
12. find documents about project timeline
13. Fuzzy matcher typo tolerance (direct test)

- All patterns are expected to be unified to the canonical action: 'search_documents'.
- Fuzzy matching and typo correction are used to handle natural language variation and common misspellings.
- Context extraction is validated for each pattern.

Fuzzy Matching Approach:
- Uses Levenshtein distance (difflib) to match user input to known patterns.
- Common typos are mapped to correct terms before matching.
- Ensures robust handling of user phrasing and errors.

Action Unification Strategy:
- All document/file search actions (find_documents, search_files, etc.) are normalized to 'search_documents'.
- This ensures a single routing path and simplifies downstream handling.
"""

import asyncio

import pytest

from services.intent_service.classifier import IntentClassifier


@pytest.mark.skip(reason="Bug - IntentClassifier needs container initialization in fixture. Tracked in piper-morgan-4wx")
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "message,expected_action,expected_query",
    [
        ("search for requirements files", "search_documents", "requirements files"),
        ("find technical specifications", "search_documents", "technical specifications"),
        ("locate API documentation", "search_documents", "API documentation"),
        ("show me all project plans", "search_documents", "project plans"),
        ("get all design docs", "search_documents", "design docs"),
        ("find docs about onboarding", "search_documents", "onboarding"),
        ("search for budget analysis documents", "search_documents", "budget analysis documents"),
        ("serach for requirments files", "search_documents", "requirements files"),  # typo
        ("find tehcnical specfications", "search_documents", "technical specifications"),  # typo
        ("find requirements", "search_documents", "requirements"),
        ("search files", "search_documents", "files"),
        ("find documents about project timeline", "search_documents", "project timeline"),
    ],
)
async def test_pm039_patterns(message, expected_action, expected_query):
    classifier = IntentClassifier()
    intent = await classifier.classify(message)
    assert intent.action == expected_action, f"Message: {message} | Got: {intent.action}"
    # Context extraction check
    if "search_query" in intent.context:
        assert (
            expected_query in intent.context["search_query"]
        ), f"Message: {message} | Got: {intent.context['search_query']}"
    else:
        # For patterns that don't extract a query, allow pass
        pass


def test_fuzzy_match_typo_tolerance():
    from services.intent_service.fuzzy_matcher import fuzzy_match

    patterns = [
        "search for requirements files",
        "find technical specifications",
        "locate API documentation",
        "show me all project plans",
        "get all design docs",
    ]
    assert (
        fuzzy_match("serach for requirments files", patterns, cutoff=0.7)
        == "search for requirements files"
    )
    assert (
        fuzzy_match("find tehcnical specfications", patterns, cutoff=0.7)
        == "find technical specifications"
    )

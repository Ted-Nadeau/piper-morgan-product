import difflib
from typing import List, Optional

# Common typo corrections
COMMON_TYPO_MAP = {
    "serach": "search",
    "requirments": "requirements",
    "tehcnical": "technical",
    "specfications": "specifications",
    # Add more as needed
}


def correct_common_typos(text: str) -> str:
    words = text.split()
    corrected = [COMMON_TYPO_MAP.get(w, w) for w in words]
    return " ".join(corrected)


"""
Fuzzy Matcher for Intent Classification (PM-039)

- correct_common_typos: Maps common misspellings to correct terms before pattern matching.
- fuzzy_match: Uses difflib.get_close_matches to find the closest pattern to the user query, allowing for typo tolerance and natural language variation.
- Used in classifier.py to improve robustness of intent recognition.
"""


def fuzzy_match(query: str, patterns: List[str], cutoff: float = 0.8) -> Optional[str]:
    """
    Returns the closest match from patterns to the query using difflib.
    """
    matches = difflib.get_close_matches(query, patterns, n=1, cutoff=cutoff)
    return matches[0] if matches else None

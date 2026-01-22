"""
Consciousness Wrapper for Search Results

Transforms search output into conscious narrative expression.
Issue: #634 CONSCIOUSNESS-TRANSFORM: Search Results

This module transforms data-driven search results into conscious narrative
that feels like interaction with an embodied AI. It follows the MVC
(Mindful, Voice-consistent, Connected) pattern.

Key transformations:
- Identity voice: "I searched..." instead of "Found..."
- Source attribution: Where the results came from
- Dialogue invitation: Questions that continue conversation
"""

from typing import Any, Dict, List


def format_search_results_conscious(
    query: str, results: List[Dict[str, Any]], source: str = "your documents"
) -> str:
    """
    Format search results with consciousness.

    Transforms from:
        "Found 3 documents matching 'auth':
         1. Auth Guide
         2. JWT Docs
         3. Security Overview"

    To:
        "I searched through your Notion workspace for 'auth' and found 3 results.
         The top match is **Auth Guide**.
         ...
         Want me to summarize any of these, or search for something more specific?"

    Args:
        query: The search query that was performed
        results: List of result dicts with at least 'title' key, optionally 'url'
        source: Description of where the search was performed

    Returns:
        Conscious narrative string with identity, attribution, and invitation
    """
    count = len(results)

    if count == 0:
        return format_no_results_conscious(query)

    # Build conscious narrative
    sections = []

    # Opening with identity and source attribution
    sections.append(
        f'I searched through {source} for "{query}" and found {count} '
        f"{'result' if count == 1 else 'results'}."
    )

    # Highlight top result(s)
    if count >= 1:
        top = results[0]
        top_title = top.get("title", "Untitled")
        sections.append(f"\nThe top match is **{top_title}**.")

        if count >= 2:
            second = results[1]
            second_title = second.get("title", "Untitled")
            sections.append(f"I also found **{second_title}** which might be relevant.")

    # List all results (capped at 10 for readability)
    if count > 0:
        sections.append("\nHere's what I found:")
        display_count = min(count, 10)
        for i, result in enumerate(results[:display_count], 1):
            title = result.get("title", "Untitled")
            url = result.get("url", "")
            if url:
                sections.append(f"{i}. **{title}**\n   {url}")
            else:
                sections.append(f"{i}. **{title}**")

        # Note if there are more results
        if count > 10:
            sections.append(f"\n...and {count - 10} more results.")

    # Dialogue invitation
    sections.append("\nWant me to summarize any of these, or search for something more specific?")

    return "\n".join(sections)


def format_no_results_conscious(query: str) -> str:
    """
    Format no-results message with consciousness.

    Transforms from:
        "No documents found matching 'obscure query'."

    To:
        "I searched but didn't find any documents matching 'obscure query'.
         Want me to try a different search term, or maybe check a specific location?"

    Args:
        query: The search query that returned no results

    Returns:
        Conscious narrative with identity and invitation
    """
    return (
        f'I searched but didn\'t find any documents matching "{query}". '
        f"Want me to try a different search term, or maybe check a specific location?"
    )


def format_search_error_conscious(error: str) -> str:
    """
    Format search error with consciousness and invitation.

    Transforms from:
        "Unable to search documents: Connection timeout"

    To:
        "I ran into a problem while searching: Connection timeout.
         Want me to try again, or is there something else I can help with?"

    Args:
        error: The error message or description

    Returns:
        Conscious error message with identity and invitation
    """
    return (
        f"I ran into a problem while searching: {error}. "
        f"Want me to try again, or is there something else I can help with?"
    )

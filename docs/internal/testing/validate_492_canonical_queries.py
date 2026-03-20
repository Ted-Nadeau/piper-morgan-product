#!/usr/bin/env python3
"""
Issue #492 Validation Script - Canonical Query Test Matrix Refresh

Tests all 25 canonical queries against the current codebase to verify
the test matrix accuracy before alpha testing.
"""

import asyncio
import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# The 25 canonical queries organized by category
CANONICAL_QUERIES = {
    "Identity": [
        ("1", "What's your name?", "IDENTITY"),
        ("2", "What can you help me with?", "IDENTITY"),
        ("3", "Are you working properly?", "IDENTITY"),
        ("4", "How do I get help?", "IDENTITY"),
        ("5", "What makes you different?", "IDENTITY"),
    ],
    "Temporal": [
        ("6", "What day is it?", "TEMPORAL"),
        ("7", "What did we accomplish yesterday?", "TEMPORAL"),
        ("8", "What's on the agenda for today?", "TEMPORAL"),
        ("9", "When was the last time we worked on this?", "TEMPORAL"),
        ("10", "How long have we been working on this project?", "TEMPORAL"),
    ],
    "Spatial": [
        ("11", "What projects are we working on?", "STATUS"),
        ("12", "Show me the project landscape", "STATUS"),
        ("13", "Which project should I focus on?", "PRIORITY"),
        ("14", "What's the status of project X?", "STATUS"),
        ("15", "Where are we in the project lifecycle?", "STATUS"),
    ],
    "Capability": [
        ("16", "Create a GitHub issue about testing", "EXECUTION"),
        ("17", "Analyze this document", "EXECUTION"),
        ("18", "List all my projects", "QUERY"),
        ("19", "Generate a status report", "QUERY"),
        ("20", "Search for authentication in our documents", "QUERY"),
    ],
    "Predictive": [
        ("21", "What should I focus on today?", "PRIORITY"),
        ("22", "What patterns do you see?", "LEARNING"),
        ("23", "What risks should I be aware of?", "ANALYSIS"),
        ("24", "What opportunities should I pursue?", "SYNTHESIS"),
        ("25", "What's the next milestone?", "PLANNING"),
    ],
}


async def test_single_query(query_num: str, query_text: str, expected_category: str) -> dict:
    """Test a single canonical query and return results."""
    from services.intent_service.classifier import IntentClassifier

    result = {
        "query_num": query_num,
        "query": query_text,
        "expected_category": expected_category,
        "actual_category": None,
        "confidence": None,
        "status": "UNKNOWN",
        "error": None,
        "response_preview": None,
    }

    try:
        classifier = IntentClassifier()
        intent = await classifier.classify(query_text)

        result["actual_category"] = intent.category.value if intent.category else "NONE"
        result["confidence"] = intent.confidence

        # Check if category matches expectation
        if result["actual_category"] == expected_category:
            result["status"] = "PASS"
        elif result["actual_category"] in ["QUERY", "STATUS", "PRIORITY", "GUIDANCE"]:
            # Some flexibility for related categories
            result["status"] = "PARTIAL"
        else:
            result["status"] = "MISMATCH"

    except Exception as e:
        result["status"] = "ERROR"
        result["error"] = str(e)

    return result


async def test_query_with_handler(query_num: str, query_text: str) -> dict:
    """Test query through the full intent service to see actual response."""
    from unittest.mock import MagicMock

    from services.intent.intent_service import IntentService

    result = {
        "query_num": query_num,
        "query": query_text,
        "has_response": False,
        "response_type": None,
        "is_placeholder": False,
        "status": "UNKNOWN",
        "error": None,
    }

    try:
        # Create mock dependencies
        intent_service = IntentService()

        # Create a minimal mock for process_message
        mock_user_context = MagicMock()
        mock_user_context.user_id = "test-user"
        mock_user_context.preferences = {}

        response = await intent_service.process_message(
            message=query_text,
            user_context=mock_user_context,
            session_id="test-session",
        )

        result["has_response"] = response is not None
        if response:
            response_str = str(response)
            result["response_type"] = type(response).__name__

            # Check for placeholder indicators
            placeholder_indicators = [
                "not yet implemented",
                "capability pending",
                "coming soon",
                "placeholder",
                "your key priorities",  # Generic placeholder text
            ]
            result["is_placeholder"] = any(
                ind.lower() in response_str.lower() for ind in placeholder_indicators
            )

            if result["is_placeholder"]:
                result["status"] = "NOT_IMPL"
            else:
                result["status"] = "PASS"

    except Exception as e:
        result["status"] = "ERROR"
        result["error"] = str(e)[:200]

    return result


async def run_classification_tests():
    """Run classification tests for all 25 queries."""
    print("\n" + "=" * 70)
    print("PHASE 1: Intent Classification Tests")
    print("=" * 70)

    all_results = []

    for category, queries in CANONICAL_QUERIES.items():
        print(f"\n### {category} Queries ###")

        for query_num, query_text, expected_cat in queries:
            result = await test_single_query(query_num, query_text, expected_cat)
            all_results.append(result)

            status_icon = {
                "PASS": "✅",
                "PARTIAL": "⚠️",
                "MISMATCH": "❌",
                "ERROR": "💥",
                "UNKNOWN": "❓",
            }.get(result["status"], "?")

            conf_str = f"{result['confidence']:.2f}" if result["confidence"] else "N/A"
            print(
                f"  {status_icon} Q{query_num}: {result['status']} "
                f"(expected={expected_cat}, got={result['actual_category']}, "
                f"conf={conf_str})"
            )

    return all_results


def summarize_results(results: list) -> dict:
    """Summarize test results by category and status."""
    summary = {
        "total": len(results),
        "pass": 0,
        "partial": 0,
        "mismatch": 0,
        "error": 0,
        "not_impl": 0,
        "by_category": {},
    }

    for r in results:
        status = r.get("status", "UNKNOWN")
        if status == "PASS":
            summary["pass"] += 1
        elif status == "PARTIAL":
            summary["partial"] += 1
        elif status == "MISMATCH":
            summary["mismatch"] += 1
        elif status == "ERROR":
            summary["error"] += 1
        elif status == "NOT_IMPL":
            summary["not_impl"] += 1

    return summary


async def main():
    """Run the full validation suite."""
    print("=" * 70)
    print("Issue #492: Canonical Query Test Matrix Validation")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 70)

    # Phase 1: Classification tests
    classification_results = await run_classification_tests()

    # Summary
    summary = summarize_results(classification_results)

    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    print(f"  Total queries tested: {summary['total']}")
    print(f"  ✅ PASS:     {summary['pass']}")
    print(f"  ⚠️  PARTIAL:  {summary['partial']}")
    print(f"  ❌ MISMATCH: {summary['mismatch']}")
    print(f"  💥 ERROR:    {summary['error']}")

    # Return results for further processing
    return {
        "classification": classification_results,
        "summary": summary,
        "timestamp": datetime.now().isoformat(),
    }


if __name__ == "__main__":
    results = asyncio.run(main())

    # Save results to JSON for analysis
    output_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "canonical_query_results.json"
    )
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nResults saved to: {output_path}")

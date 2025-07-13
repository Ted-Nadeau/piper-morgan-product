#!/usr/bin/env python3
"""
Test script to analyze the fallback classification behavior
"""

from services.intent_service.classifier import IntentClassifier
from services.intent_service.pre_classifier import PreClassifier
from services.shared_types import IntentCategory


def test_fallback_classification():
    """Test the fallback classification behavior"""

    classifier = IntentClassifier()

    bug_report_messages = [
        "Users are complaining that the mobile app crashes",
        "Users are complaining about the login page being slow",
        "Users are reporting that the checkout process is broken",
        "Users are saying the search feature doesn't work",
        "Users are experiencing issues with the payment system",
        "Users are complaining the website is down",
        "Users are complaining about slow page load times",
        "Users are reporting errors when uploading files",
    ]

    print("Testing Fallback Classification...")
    print("=" * 50)

    for message in bug_report_messages:
        # Test pre-classifier first
        pre_result = PreClassifier.pre_classify(message)
        print(f"Message: '{message}'")
        print(f"  Pre-classifier result: {pre_result}")

        # Test fallback classification
        fallback_result = classifier._fallback_classify(message)
        print(
            f"  Fallback result: {fallback_result.category.value}/{fallback_result.action} (confidence: {fallback_result.confidence})"
        )

        # Test vague detection
        is_vague = classifier._seems_vague(fallback_result)
        print(f"  Is vague: {is_vague}")
        print()


if __name__ == "__main__":
    test_fallback_classification()

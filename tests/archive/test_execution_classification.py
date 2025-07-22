#!/usr/bin/env python3
"""
Test script to check if bug reports with execution intent are classified correctly
"""

import asyncio

from services.intent_service.classifier import IntentClassifier
from services.intent_service.pre_classifier import PreClassifier
from services.shared_types import IntentCategory


async def test_execution_classification():
    """Test that bug reports with execution intent are classified as EXECUTION"""

    execution_messages = [
        "Create a ticket for the mobile app crashes",
        "Create an issue for the login page being slow",
        "File a bug report for the checkout process being broken",
        "Create a GitHub issue for the search feature not working",
        "Submit a ticket for the payment system issues",
        "Log an issue for the website being down",
        "Create a bug report for slow page load times",
        "File a ticket for file upload errors",
        "I need to create a ticket for users complaining about app crashes",
        "Can you create an issue for the performance problems users are reporting?",
    ]

    print("Testing Execution Classification...")
    print("=" * 50)

    classifier = IntentClassifier()

    for message in execution_messages:
        try:
            result = await classifier.classify(message)
            print(f"Message: '{message}'")
            print(
                f"  Classified as: {result.category.value}/{result.action} (confidence: {result.confidence})"
            )

            # Check if it's correctly classified as EXECUTION
            if result.category == IntentCategory.EXECUTION:
                print(f"  ✅ Correctly classified as EXECUTION")
            else:
                print(
                    f"  ❌ Incorrectly classified as {result.category.value} - should be EXECUTION"
                )
            print()

        except Exception as e:
            print(f"Message: '{message}'")
            print(f"  Error: {e}")
            print()


if __name__ == "__main__":
    asyncio.run(test_execution_classification())

#!/usr/bin/env python3
"""
Test script to trace the complete classification flow
"""

import asyncio

from services.domain.models import Intent
from services.intent_service.classifier import IntentClassifier
from services.intent_service.pre_classifier import PreClassifier
from services.shared_types import IntentCategory


def simulate_classification_without_llm():
    """Simulate what happens when LLM fails"""

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

    print("Simulating Classification Flow (without LLM)...")
    print("=" * 60)

    for message in bug_report_messages:
        print(f"Message: '{message}'")

        # Step 1: Pre-classifier
        pre_result = PreClassifier.pre_classify(message)
        print(f"  1. Pre-classifier: {pre_result}")

        if pre_result:
            print(
                f"     -> Pre-classified as: {pre_result.category.value}/{pre_result.action}"
            )
            continue

        # Step 2: LLM would fail (no API keys)
        print(f"  2. LLM: Would fail (no API keys)")

        # Step 3: Fallback classification
        fallback_result = classifier._fallback_classify(message)
        print(
            f"  3. Fallback: {fallback_result.category.value}/{fallback_result.action} (confidence: {fallback_result.confidence})"
        )

        # Step 4: Check if it's vague
        is_vague = classifier._seems_vague(fallback_result)
        print(f"  4. Is vague: {is_vague}")

        # Step 5: What happens if vague or low confidence?
        if fallback_result.confidence < 0.7 or is_vague:
            print(f"  5. Would return CONVERSATION/clarification_needed")
        else:
            print(f"  5. Would return the fallback result")

        print()


if __name__ == "__main__":
    simulate_classification_without_llm()

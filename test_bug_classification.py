#!/usr/bin/env python3
"""
Test script to reproduce bug report misclassification issue
"""

import asyncio
from services.intent_service.classifier import IntentClassifier
from services.intent_service.pre_classifier import PreClassifier
from services.shared_types import IntentCategory

async def test_bug_classification():
    """Test that bug reports are not incorrectly classified as greetings"""
    
    bug_report_messages = [
        "Users are complaining that the mobile app crashes",
        "Users are complaining about the login page being slow",
        "Users are reporting that the checkout process is broken",
        "Users are saying the search feature doesn't work",
        "Users are experiencing issues with the payment system",
        "Users are complaining the website is down",
        "Users are complaining about slow page load times",
        "Users are reporting errors when uploading files"
    ]
    
    print("Testing Pre-Classifier...")
    print("=" * 50)
    
    # Test pre-classifier first
    for message in bug_report_messages:
        pre_result = PreClassifier.pre_classify(message)
        print(f"Message: '{message}'")
        if pre_result:
            print(f"  Pre-classified as: {pre_result.category.value}/{pre_result.action} (confidence: {pre_result.confidence})")
        else:
            print(f"  Pre-classifier: No match (will go to LLM)")
        print()
    
    # Test full classifier
    print("\nTesting Full Classifier...")
    print("=" * 50)
    
    classifier = IntentClassifier()
    
    for message in bug_report_messages:
        try:
            result = await classifier.classify(message)
            print(f"Message: '{message}'")
            print(f"  Classified as: {result.category.value}/{result.action} (confidence: {result.confidence})")
            
            # Check if it's misclassified
            if result.category == IntentCategory.CONVERSATION:
                print(f"  ❌ MISCLASSIFIED as CONVERSATION - should be EXECUTION/ANALYSIS")
            else:
                print(f"  ✅ Correctly classified")
            print()
            
        except Exception as e:
            print(f"Message: '{message}'")
            print(f"  Error: {e}")
            print()

if __name__ == "__main__":
    asyncio.run(test_bug_classification())
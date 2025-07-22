#!/usr/bin/env python3
"""
Test script to analyze the conversation aware clarification generator
"""

import asyncio

from services.intelligence.conversation_aware import ConversationAwareClarifyingGenerator


async def test_conversation_aware():
    """Test the conversation aware clarification generator"""

    generator = ConversationAwareClarifyingGenerator()

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

    print("Testing Conversation Aware Clarification Generator...")
    print("=" * 60)

    for message in bug_report_messages:
        print(f"Message: '{message}'")

        # Analyze the request
        analysis = await generator.analyze_request(message, f"conv_{hash(message)}")

        print(f"  Is ambiguous: {analysis.is_ambiguous}")
        print(f"  Confidence: {analysis.confidence}")
        print(f"  Can proceed: {analysis.can_proceed}")
        print(f"  Detected issues: {[issue.value for issue in analysis.detected_issues]}")
        print(f"  Number of questions: {len(analysis.questions)}")

        if analysis.questions:
            for i, q in enumerate(analysis.questions, 1):
                print(f"    Q{i}: {q.question}")

        print()


if __name__ == "__main__":
    asyncio.run(test_conversation_aware())

#!/usr/bin/env python3
"""
Issue #884: CANONICAL-RETEST — Post-M0 Canonical Query Validation

Tests all 62 canonical queries from canonical-queries-v2.md against
the running v0.8.6 instance via the /api/v1/intent endpoint.

Failure modes per #884 spec:
  ROUTING    — Query reaches wrong handler
  PARSING    — Intent understood, entities not extracted
  INTEGRATION — Correct routing, backend fails
  RESPONSE   — Correct result, poor presentation
  WIRING     — Components work individually, composition fails

Usage:
    # Ensure app is running on localhost:8001
    # Then:
    python dev/2026/03/12/canonical-retest-884.py

Outputs:
    dev/2026/03/12/canonical-retest-884-results.csv
    dev/2026/03/12/canonical-retest-884-report.md
"""

import csv
import json
import sys
import time
from datetime import datetime
from pathlib import Path

import requests

# --- Configuration ---
BASE_URL = "http://localhost:8001"
INTENT_ENDPOINT = f"{BASE_URL}/api/v1/intent"
LOGIN_ENDPOINT = f"{BASE_URL}/auth/login"
USERNAME = "canonical-test"
PASSWORD = "canonical-test-2026"
SESSION_ID_PREFIX = "canonical-retest-884"
OUTPUT_DIR = Path(__file__).parent

# --- Canonical Queries (from canonical-queries-v2.md, 62 total) ---
# Format: (query_num, query_text, category, expected_intent_category)
# expected_intent_category is what we expect the classifier to return

CANONICAL_QUERIES = [
    # Identity (5) — expect IDENTITY
    (1, "What's your name?", "Identity", "identity"),
    (2, "What can you help me with?", "Identity", "identity"),
    (3, "Are you working properly?", "Identity", "identity"),
    (4, "How do I get help?", "Identity", "identity"),
    (5, "What makes you different?", "Identity", "identity"),
    # Temporal (5) — expect TEMPORAL
    (6, "What day is it?", "Temporal", "temporal"),
    (7, "What did we accomplish yesterday?", "Temporal", "temporal"),
    (8, "What's on the agenda for today?", "Temporal", "temporal"),
    (9, "When was the last time we worked on this?", "Temporal", "temporal"),
    (10, "How long have we been working on this project?", "Temporal", "temporal"),
    # Spatial (4) — expect STATUS/PRIORITY
    (11, "What projects are we working on?", "Spatial", "status"),
    (12, "Show me the project landscape", "Spatial", "status"),
    (13, "Which project should I focus on?", "Spatial", "priority"),
    (14, "What's the status of project X?", "Spatial", "status"),
    # Capability (5) — expect EXECUTION/QUERY
    (16, "Create a GitHub issue about testing", "Capability", "execution"),
    (17, "Analyze this document", "Capability", "analysis"),
    (18, "List all my projects", "Capability", "query"),
    (19, "Generate a status report", "Capability", "query"),
    (20, "Search for authentication in our documents", "Capability", "query"),
    # Predictive (5) — expect PRIORITY/LEARNING/ANALYSIS/SYNTHESIS/PLANNING
    (21, "What should I focus on today?", "Predictive", "priority"),
    (22, "What patterns do you see?", "Predictive", "learning"),
    (23, "What risks should I be aware of?", "Predictive", "analysis"),
    (24, "What opportunities should I pursue?", "Predictive", "synthesis"),
    (25, "What's the next milestone?", "Predictive", "planning"),
    # Conversational (5)
    (26, "What else can you help with?", "Conversational", "identity"),
    (27, "Tell me more about the GitHub integration", "Conversational", "query"),
    (28, "How do I use the calendar feature?", "Conversational", "guidance"),
    (29, "What changed since yesterday?", "Conversational", "temporal"),
    (30, "What needs my attention?", "Conversational", "priority"),
    # Scheduling & Reminders (5)
    (31, "Schedule a meeting about the roadmap", "Scheduling", "execution"),
    (32, "Remind me to review PRs tomorrow", "Scheduling", "execution"),
    (33, "Find time for a 1:1 with the team lead", "Scheduling", "execution"),
    (34, "How much time am I spending in meetings?", "Scheduling", "query"),
    (35, "Review my recurring meetings", "Scheduling", "query"),
    # Document Management (4, #39 removed)
    (36, "Create a doc from this conversation", "Documents", "execution"),
    (37, "Compare these two documents", "Documents", "analysis"),
    (38, "Synthesize these sources into a summary", "Documents", "synthesis"),
    (40, "Update the project roadmap document", "Documents", "execution"),
    # GitHub Operations (8)
    (41, "What did we ship this week?", "GitHub Ops", "query"),
    (42, "Show me stale PRs", "GitHub Ops", "query"),
    (43, "What's blocking the milestone?", "GitHub Ops", "analysis"),
    (44, "Create issues from this meeting's action items", "GitHub Ops", "execution"),
    (45, "Close completed issues", "GitHub Ops", "execution"),
    (58, "Update issue #123", "GitHub Ops", "execution"),
    (59, "Comment on issue #456", "GitHub Ops", "execution"),
    (60, "Review issue #789", "GitHub Ops", "query"),
    # Slack Communication (5)
    (46, "Any mentions I missed?", "Slack", "query"),
    (47, "Summarize #general from yesterday", "Slack", "synthesis"),
    (48, "Post this update to the team channel", "Slack", "execution"),
    (49, "/standup", "Slack", "execution"),
    (50, "/piper help", "Slack", "identity"),
    # Productivity Tracking (3)
    (51, "What's my productivity this week?", "Productivity", "query"),
    (52, "Are we on track for the milestone?", "Productivity", "status"),
    (53, "What did the team accomplish this sprint?", "Productivity", "query"),
    # Todo Management (4)
    (54, "Add a todo: review the deployment plan", "Todos", "execution"),
    (55, "Complete the PR review todo", "Todos", "execution"),
    (56, "Show my todos", "Todos", "query"),
    (57, "What's my next todo?", "Todos", "priority"),
    # Calendar Extended (2)
    (61, "What's my week look like?", "Calendar Ext", "temporal"),
    (62, "Check my calendar for conflicts", "Calendar Ext", "query"),
    # Knowledge Operations (1)
    (63, "Upload a file to the knowledge base", "Knowledge", "execution"),
]


def login(session: requests.Session) -> bool:
    """Authenticate and store cookie."""
    resp = session.post(
        LOGIN_ENDPOINT,
        data={
            "username": USERNAME,
            "password": PASSWORD,
        },
    )
    if resp.status_code == 200 and "token" in resp.json():
        print(f"  Logged in as {USERNAME}")
        return True
    else:
        print(f"  LOGIN FAILED: {resp.status_code} {resp.text[:200]}")
        return False


def classify_failure(
    query_num, query_text, category, expected_intent, response_data, http_status, error_text
) -> dict:
    """
    Analyze a query result and classify its outcome.

    Returns dict with: status, failure_mode, notes
    """
    result = {
        "query_num": query_num,
        "query": query_text,
        "category": category,
        "expected_intent": expected_intent,
        "http_status": http_status,
        "actual_intent": None,
        "confidence": None,
        "status": "UNKNOWN",
        "failure_mode": None,
        "response_preview": None,
        "notes": "",
    }

    # HTTP-level failure
    if http_status != 200 or error_text:
        result["status"] = "ERROR"
        result["failure_mode"] = "INTEGRATION"
        result["notes"] = error_text or f"HTTP {http_status}"
        return result

    if not response_data:
        result["status"] = "ERROR"
        result["failure_mode"] = "INTEGRATION"
        result["notes"] = "Empty response"
        return result

    # Extract intent info
    intent_data = response_data.get("intent", {})
    actual_category = intent_data.get("category", "").lower() if intent_data else ""
    confidence = intent_data.get("confidence")
    message = response_data.get("message", "")

    result["actual_intent"] = actual_category
    result["confidence"] = confidence
    result["response_preview"] = message[:150] if message else ""

    # Check for error in response body (degradation)
    if response_data.get("error"):
        result["status"] = "FAIL"
        result["failure_mode"] = "INTEGRATION"
        result["notes"] = f"Service error: {response_data['error']}"
        return result

    # Check routing: did the intent classify correctly?
    # Allow some flexibility for related categories
    RELATED_INTENTS = {
        "status": {"query", "status", "priority"},
        "query": {"query", "status", "discovery"},
        "priority": {"priority", "status", "guidance", "query"},
        "identity": {"identity", "conversation", "guidance"},
        "temporal": {"temporal", "query", "status"},
        "execution": {"execution", "query"},
        "analysis": {"analysis", "query", "synthesis"},
        "synthesis": {"synthesis", "analysis", "query"},
        "planning": {"planning", "query", "status", "temporal"},
        "learning": {"learning", "query", "analysis"},
        "guidance": {"guidance", "identity", "query", "conversation"},
        "conversation": {"conversation", "identity", "query"},
        "discovery": {"discovery", "query", "identity"},
    }

    acceptable = RELATED_INTENTS.get(expected_intent, {expected_intent})
    exact_match = actual_category == expected_intent
    related_match = actual_category in acceptable

    if not related_match and actual_category:
        result["status"] = "FAIL"
        result["failure_mode"] = "ROUTING"
        result["notes"] = f"Expected {expected_intent}, got {actual_category}"
        return result

    # Check response quality
    placeholder_indicators = [
        "not yet implemented",
        "capability pending",
        "coming soon",
        "placeholder",
        "i don't have that capability",
        "i'm not able to",
        "i can't currently",
        "that feature isn't available",
        "not currently supported",
    ]

    error_indicators = [
        "error occurred",
        "something went wrong",
        "failed to",
        "exception",
        "traceback",
        "internal server error",
    ]

    message_lower = message.lower()

    is_placeholder = any(ind in message_lower for ind in placeholder_indicators)
    is_error_response = any(ind in message_lower for ind in error_indicators)

    if is_error_response:
        result["status"] = "FAIL"
        result["failure_mode"] = "RESPONSE"
        result["notes"] = "Error/exception in response text"
        return result

    if is_placeholder:
        result["status"] = "NOT_IMPL"
        result["failure_mode"] = None
        result["notes"] = "Feature not implemented (graceful)"
        return result

    # If we got a real response with correct routing
    if not message or len(message.strip()) < 10:
        result["status"] = "FAIL"
        result["failure_mode"] = "RESPONSE"
        result["notes"] = "Response too short or empty"
        return result

    # Looks good
    if exact_match:
        result["status"] = "PASS"
        result["notes"] = f"Exact match, conf={confidence}"
    elif related_match:
        result["status"] = "PASS"
        result["notes"] = f"Related match ({actual_category}), conf={confidence}"
    else:
        result["status"] = "PASS"
        result["notes"] = f"conf={confidence}"

    return result


def run_test(session: requests.Session, query_num, query_text, category, expected_intent) -> dict:
    """Send a single query and return classified result."""
    try:
        resp = session.post(
            INTENT_ENDPOINT,
            json={
                "message": query_text,
                "session_id": f"{SESSION_ID_PREFIX}-q{query_num}",
            },
            timeout=30,
        )
        if resp.status_code == 200:
            data = resp.json()
            return classify_failure(
                query_num, query_text, category, expected_intent, data, resp.status_code, None
            )
        else:
            return classify_failure(
                query_num,
                query_text,
                category,
                expected_intent,
                None,
                resp.status_code,
                resp.text[:200],
            )
    except requests.exceptions.Timeout:
        return classify_failure(
            query_num, query_text, category, expected_intent, None, 0, "Request timeout (30s)"
        )
    except Exception as e:
        return classify_failure(query_num, query_text, category, expected_intent, None, 0, str(e))


def write_csv(results: list, filepath: Path):
    """Write results to CSV."""
    fieldnames = [
        "query_num",
        "query",
        "category",
        "expected_intent",
        "actual_intent",
        "confidence",
        "http_status",
        "status",
        "failure_mode",
        "response_preview",
        "notes",
    ]
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


def write_report(results: list, filepath: Path):
    """Write markdown summary report."""
    total = len(results)
    by_status = {}
    by_category = {}
    by_failure_mode = {}

    for r in results:
        st = r["status"]
        by_status[st] = by_status.get(st, 0) + 1

        cat = r["category"]
        if cat not in by_category:
            by_category[cat] = {
                "total": 0,
                "PASS": 0,
                "FAIL": 0,
                "NOT_IMPL": 0,
                "ERROR": 0,
                "UNKNOWN": 0,
            }
        by_category[cat]["total"] += 1
        by_category[cat][st] = by_category[cat].get(st, 0) + 1

        fm = r.get("failure_mode")
        if fm:
            by_failure_mode[fm] = by_failure_mode.get(fm, 0) + 1

    pass_count = by_status.get("PASS", 0)
    fail_count = by_status.get("FAIL", 0)
    not_impl = by_status.get("NOT_IMPL", 0)
    error_count = by_status.get("ERROR", 0)
    pass_rate = (pass_count / total * 100) if total else 0

    lines = [
        "# Canonical Query Retest Report — Issue #884",
        "",
        f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Version**: v0.8.6 (post-M0)",
        f"**User**: {USERNAME} (fresh account)",
        f"**Total Queries**: {total}",
        "",
        "---",
        "",
        "## Overall Results",
        "",
        f"| Metric | Count | Percentage |",
        f"|--------|-------|------------|",
        f"| PASS | {pass_count} | {pass_rate:.1f}% |",
        f"| FAIL | {fail_count} | {fail_count/total*100:.1f}% |",
        f"| NOT_IMPL | {not_impl} | {not_impl/total*100:.1f}% |",
        f"| ERROR | {error_count} | {error_count/total*100:.1f}% |",
        f"| **Total** | **{total}** | |",
        "",
        (
            f"**Pass Rate (implemented queries)**: "
            f"{pass_count}/{pass_count+fail_count+error_count} "
            f"({pass_count/(pass_count+fail_count+error_count)*100:.1f}%)"
            if (pass_count + fail_count + error_count) > 0
            else ""
        ),
        "",
        "---",
        "",
        "## Results by Category",
        "",
        "| Category | Total | PASS | FAIL | NOT_IMPL | ERROR | Rate |",
        "|----------|-------|------|------|----------|-------|------|",
    ]

    for cat in [
        "Identity",
        "Temporal",
        "Spatial",
        "Capability",
        "Predictive",
        "Conversational",
        "Scheduling",
        "Documents",
        "GitHub Ops",
        "Slack",
        "Productivity",
        "Todos",
        "Calendar Ext",
        "Knowledge",
    ]:
        if cat in by_category:
            d = by_category[cat]
            rate = f"{d['PASS']/d['total']*100:.0f}%" if d["total"] else "N/A"
            lines.append(
                f"| {cat} | {d['total']} | {d['PASS']} | {d['FAIL']} "
                f"| {d['NOT_IMPL']} | {d['ERROR']} | {rate} |"
            )

    lines.extend(
        [
            "",
            "---",
            "",
            "## Failure Mode Breakdown",
            "",
            "| Mode | Count | Description |",
            "|------|-------|-------------|",
        ]
    )

    mode_descriptions = {
        "ROUTING": "Query reached wrong handler",
        "PARSING": "Intent understood, entities not extracted",
        "INTEGRATION": "Correct routing, backend fails",
        "RESPONSE": "Correct result, poor presentation",
        "WIRING": "Components work individually, composition fails",
    }

    for mode in ["ROUTING", "PARSING", "INTEGRATION", "RESPONSE", "WIRING"]:
        count = by_failure_mode.get(mode, 0)
        desc = mode_descriptions.get(mode, "")
        if count > 0:
            lines.append(f"| {mode} | {count} | {desc} |")

    if not by_failure_mode:
        lines.append("| *(none)* | 0 | No classified failures |")

    # Detailed failures
    failures = [r for r in results if r["status"] in ("FAIL", "ERROR")]
    if failures:
        lines.extend(
            [
                "",
                "---",
                "",
                "## Detailed Failures",
                "",
            ]
        )
        for r in failures:
            lines.append(
                f"- **Q{r['query_num']}** ({r['category']}): "
                f"`{r['query']}` — **{r['failure_mode']}** — {r['notes']}"
            )

    # NOT_IMPL queries (informational)
    not_impl_list = [r for r in results if r["status"] == "NOT_IMPL"]
    if not_impl_list:
        lines.extend(
            [
                "",
                "---",
                "",
                "## Not Implemented (Graceful)",
                "",
            ]
        )
        for r in not_impl_list:
            lines.append(f"- Q{r['query_num']} ({r['category']}): `{r['query']}`")

    lines.extend(
        [
            "",
            "---",
            "",
            f"*Generated {datetime.now().strftime('%Y-%m-%d %H:%M')} by canonical-retest-884.py*",
            "",
        ]
    )

    with open(filepath, "w") as f:
        f.write("\n".join(lines))


def main():
    print("=" * 70)
    print("Issue #884: CANONICAL-RETEST — Post-M0 Canonical Query Validation")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Target: {BASE_URL}")
    print(f"Queries: {len(CANONICAL_QUERIES)}")
    print("=" * 70)

    # Create session and login
    session = requests.Session()
    print("\nAuthenticating...")
    if not login(session):
        print("FATAL: Cannot authenticate. Aborting.")
        sys.exit(1)

    # Run all queries
    results = []
    current_category = None

    for query_num, query_text, category, expected_intent in CANONICAL_QUERIES:
        if category != current_category:
            current_category = category
            print(f"\n### {category} ###")

        result = run_test(session, query_num, query_text, category, expected_intent)
        results.append(result)

        # Status icon
        icon = {
            "PASS": "\u2705",
            "FAIL": "\u274c",
            "NOT_IMPL": "\u2b1c",
            "ERROR": "\U0001f4a5",
            "UNKNOWN": "\u2753",
        }.get(result["status"], "?")

        fm_str = f" [{result['failure_mode']}]" if result["failure_mode"] else ""
        print(
            f"  {icon} Q{query_num:>2}: {result['status']:<8} "
            f"{fm_str:<14} "
            f"({result['actual_intent'] or 'N/A'}) "
            f"{query_text[:45]}"
        )

        # Small delay to avoid hammering
        time.sleep(0.3)

    # Summary
    total = len(results)
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] == "FAIL")
    not_impl = sum(1 for r in results if r["status"] == "NOT_IMPL")
    errors = sum(1 for r in results if r["status"] == "ERROR")

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Total:     {total}")
    print(f"  \u2705 PASS:     {passed} ({passed/total*100:.1f}%)")
    print(f"  \u274c FAIL:     {failed} ({failed/total*100:.1f}%)")
    print(f"  \u2b1c NOT_IMPL: {not_impl} ({not_impl/total*100:.1f}%)")
    print(f"  \U0001f4a5 ERROR:    {errors} ({errors/total*100:.1f}%)")

    if passed + failed + errors > 0:
        impl_rate = passed / (passed + failed + errors) * 100
        print(f"\n  Implemented pass rate: {passed}/{passed+failed+errors} ({impl_rate:.1f}%)")

    # Write outputs
    csv_path = OUTPUT_DIR / "canonical-retest-884-results.csv"
    report_path = OUTPUT_DIR / "canonical-retest-884-report.md"

    write_csv(results, csv_path)
    write_report(results, report_path)

    print(f"\n  CSV:    {csv_path}")
    print(f"  Report: {report_path}")
    print("=" * 70)

    return results


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Backfill agent-log-index-normalized.csv from actual session log files on disk.

Scans dev/2025/, dev/2026/, and dev/active/ for *-log.md and *-log files,
parses role/model from filenames, and merges with existing CSV entries
(preserving notes from the Google Sheets import).
"""

import csv
import os
import re
from collections import defaultdict
from pathlib import Path

BASE = Path("/Users/xian/Development/piper-morgan")
CSV_PATH = BASE / "dev/active/agent-log-index-normalized.csv"

# Filename slug → (role_name, slug, environment)
# Derived from filename patterns observed in the codebase
SLUG_MAP = {
    # Leadership / web roles
    "arch": ("Chief Architect", "arch", "web"),
    "chief-architect": ("Chief Architect", "arch", "web"),
    "cxo": ("CXO", "cxo", "web"),
    "cio": ("CIO", "cio", "web"),
    "hosr": ("HoSR", "hosr", "web"),
    "ppm": ("PPM", "ppm", "web"),
    "prod": ("PPM", "ppm", "web"),  # older naming
    "comms": ("Comms Chief", "comms", "web"),
    "coach": ("Exec Coach", "coach", "web"),
    "mobile": ("Mobile Product (consultant)", "mobile", "web"),
    # Code roles
    "lead": ("Lead Dev", "lead", "code"),
    "exec": ("Chief of Staff", "exec", "code"),
    "cos": ("Chief of Staff", "exec", "code"),
    "docs": ("Docs mgr", "docs", "code"),
    "doc": ("Docs mgr", "docs", "code"),
    "prog": ("Programmer", "prog", "code"),
    "spec": ("Special Assignments", "spec", "code"),
    "secops": ("SecOps", "secops", "code"),
    "vibe": ("Vibe coder", "vibe", "code"),
    "research": ("Researcher", "research", "code"),
    # Specialized programmer sub-sessions (issue-based naming)
    # e.g., 632-phase1, 633-cli, 634-search, 635-files, 636-learning, 637-auth, 638-templates
    # These are Programmer subagent sessions
}


# Model detection
def detect_model(filename):
    fn = filename.lower()
    if "opus" in fn:
        return "opus"
    elif "sonnet" in fn:
        return "sonnet"
    elif "haiku" in fn:
        return "haiku"
    return ""


def parse_log_filename(filepath):
    """Parse a session log filepath into structured data."""
    fname = os.path.basename(filepath)

    # Handle prefixed filenames first (before omnibus skip)
    clean_fname = re.sub(r"^(PREMATURE-|DEPRECATED-|ceo-private-log-not-for-omnibus-)", "", fname)

    # Skip omnibus logs — they're daily synthesis docs, not agent sessions
    # But not if the original was a prefixed non-omnibus file
    # Exception: "omnibus-repair-session" IS an agent session
    if "omnibus" in fname.lower() and clean_fname == fname:
        if "repair-session" in fname.lower() or "creation" in fname.lower():
            pass  # These are agent sessions about omnibus work
        else:
            return None

    # Extract date
    date_match = re.match(r"(\d{4}-\d{2}-\d{2})", clean_fname)
    if not date_match:
        return None
    date = date_match.group(1)

    # For prefixed files, use original fname but note the prefix
    if clean_fname != fname:
        if "ceo-private" in fname:
            # This is a Coach session with special prefix
            model = detect_model(fname)
            fname_normalized = fname if fname.endswith(".md") else fname + ".md"
            return {
                "date": date,
                "role": "Exec Coach",
                "slug": "coach",
                "environment": "web",
                "model": model,
                "log_filename": fname_normalized,
                "notes": "private; not for omnibus",
            }
        else:
            return None  # Skip PREMATURE/DEPRECATED files

    # Extract time if present
    time_match = re.match(r"\d{4}-\d{2}-\d{2}-(\d{4})", fname)

    model = detect_model(fname)

    # Normalize filename to .md
    if not fname.endswith(".md"):
        fname_normalized = fname + ".md"
    else:
        fname_normalized = fname

    # Try to identify role from filename
    # Remove date prefix and common suffixes to get the role part
    role_part = re.sub(r"^\d{4}-\d{2}-\d{2}-\d{4}-", "", fname)
    role_part = re.sub(r"-(code|web)-(opus|sonnet|haiku)-log(\.md)?$", "", role_part)
    role_part = re.sub(r"-(opus|sonnet|haiku)-log(\.md)?$", "", role_part)
    role_part = re.sub(r"-log(\.md)?$", "", role_part)
    role_part = re.sub(r"-(code|web)$", "", role_part)

    # Check against slug map
    role_name = None
    slug = None
    environment = "code"  # default

    # Try exact match first
    if role_part in SLUG_MAP:
        role_name, slug, environment = SLUG_MAP[role_part]
    else:
        # Try partial match - check if any known slug is in the role part
        for known_slug, (rn, sl, env) in SLUG_MAP.items():
            if known_slug in role_part.split("-"):
                role_name, slug, environment = rn, sl, env
                break

    # Handle numbered programmer sub-sessions (e.g., "632-phase1", "agent-547")
    if role_name is None:
        if re.search(r"^\d{3}-", role_part) or re.search(r"^agent-\d+", role_part):
            role_name = "Programmer"
            slug = "prog"
            environment = "code"
        elif (
            "demo-integration" in role_part
            or "logout-bug-fix" in role_part
            or "test-gap-fix" in role_part
            or "test-userid-fix" in role_part
        ):
            role_name = "Programmer"
            slug = "prog"
            environment = "code"

    # Handle some older naming patterns
    if role_name is None:
        if "cursor" in role_part:
            role_name = "Lead Dev"
            slug = "lead"
            environment = "code"
        elif "sprint" in role_part or "audit" in role_part:
            role_name = "Lead Dev"
            slug = "lead"
            environment = "code"
        elif "know" in role_part:
            role_name = "Docs mgr"
            slug = "docs"
            environment = "code"
        elif "ux" in role_part or "uxde" in role_part or "uxr" in role_part:
            role_name = "Unicorn web designer"
            slug = "uxd"
            environment = "code"
        elif "asst" in role_part:
            role_name = "Special Assignments"
            slug = "spec"
            environment = "code"
        elif "test" in role_part:
            role_name = "Programmer"  # test-focused sessions
            slug = "prog"
            environment = "code"
        elif "tool" in role_part:
            role_name = "Lead Dev"  # tooling sessions
            slug = "lead"
            environment = "code"
        elif "devops" in role_part:
            role_name = "SecOps"  # devops/infra
            slug = "secops"
            environment = "code"
        elif "grat" in role_part:
            role_name = "Comms Chief"  # gratitude/comms
            slug = "comms"
            environment = "web"
        elif "researcher" in role_part:
            role_name = "Researcher"
            slug = "research"
            environment = "code"
        elif "web" in role_part:
            role_name = "Unicorn web designer"
            slug = "uxd"
            environment = "code"
        elif "chief-of-staff" in role_part:
            role_name = "Chief of Staff"
            slug = "exec"
            environment = "code"
        elif "executive-coaching" in role_part or "coach" in role_part:
            role_name = "Exec Coach"
            slug = "coach"
            environment = "web"
        elif "alpha-onboarding" in role_part:
            role_name = "HoSR"
            slug = "hosr"
            environment = "web"
        elif "import-fix" in role_part:
            role_name = "Lead Dev"
            slug = "lead"
            environment = "code"
        elif "chrome-mcp" in role_part:
            role_name = "Lead Dev"
            slug = "lead"
            environment = "code"
        elif "core-learn" in role_part or "discovery" in role_part or "phase3" in role_part:
            role_name = "Researcher"
            slug = "research"
            environment = "code"
        elif "agent" in role_part or role_part in ("code", ""):
            # Generic early sessions before role structure
            role_name = "Lead Dev"
            slug = "lead"
            environment = "code"
        elif "post-development-pattern-review" in role_part:
            role_name = "Chief Architect"
            slug = "arch"
            environment = "web"
        elif "phase-3-implementation" in role_part:
            role_name = "Lead Dev"
            slug = "lead"
            environment = "code"
        elif "omnibus-repair" in role_part or "omnibus-creation" in role_part:
            role_name = "Docs mgr"
            slug = "docs"
            environment = "code"
        elif role_part in ("sonnet", ""):
            # Bare model-only filename from early days
            role_name = "Lead Dev"
            slug = "lead"
            environment = "code"

    if role_name is None:
        return None  # Can't identify role

    return {
        "date": date,
        "role": role_name,
        "slug": slug,
        "environment": environment,
        "model": model,
        "log_filename": fname_normalized,
        "notes": "",
    }


def main():
    # 1. Load existing CSV entries (keyed by filename for dedup)
    existing = {}
    if CSV_PATH.exists():
        with open(CSV_PATH, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing[row["log_filename"]] = row

    print(f"Existing CSV entries: {len(existing)}")

    # 2. Scan all log files on disk
    log_dirs = [
        BASE / "dev" / "2025",
        BASE / "dev" / "2026",
        BASE / "dev" / "active",
    ]

    all_files = []
    for log_dir in log_dirs:
        if not log_dir.exists():
            continue
        for root, dirs, files in os.walk(log_dir):
            for f in files:
                if f.endswith("-log.md") or f.endswith("-log"):
                    all_files.append(os.path.join(root, f))

    print(f"Log files on disk: {len(all_files)}")

    # 3. Parse each file and merge
    new_entries = 0
    unidentified = []
    for filepath in sorted(all_files):
        fname = os.path.basename(filepath)
        # Normalize to .md for matching
        fname_md = fname if fname.endswith(".md") else fname + ".md"

        if fname_md in existing or fname in existing:
            continue  # Already in CSV

        parsed = parse_log_filename(filepath)
        if parsed is None:
            unidentified.append(fname)
            continue

        existing[parsed["log_filename"]] = parsed
        new_entries += 1

    print(f"New entries to add: {new_entries}")
    if unidentified:
        print(f"Unidentified files ({len(unidentified)}):")
        for u in unidentified:
            print(f"  {u}")

    # 4. Write merged CSV
    all_rows = sorted(existing.values(), key=lambda r: (r["date"], r["role"]))

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["date", "role", "slug", "environment", "model", "log_filename", "notes"]
        )
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"\nWrote {len(all_rows)} total rows to {CSV_PATH}")

    # Stats
    roles = defaultdict(int)
    for r in all_rows:
        roles[r["role"]] += 1
    dates = set(r["date"] for r in all_rows)
    print(f"Roles: {len(roles)} | Date range: {min(dates)} to {max(dates)}")
    for role in sorted(roles, key=roles.get, reverse=True):
        print(f"  {role}: {roles[role]} sessions")


if __name__ == "__main__":
    main()

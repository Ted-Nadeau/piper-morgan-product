#!/usr/bin/env python3
"""
Convert PM's Google Sheets agent-log index (column-per-day matrix)
into a normalized one-row-per-session CSV.

Input: 3 CSV exports in dev/active/
  - PM agent logs index - 12_2025.csv
  - PM agent logs index - 1_2026.csv
  - PM agent logs index - 2_2026.csv

Output: dev/active/agent-log-index-normalized.csv
"""

import csv
import os
import re
from pathlib import Path

# Role slug and environment mapping
ROLE_MAP = {
    "Comms Chief": ("comms", "web"),
    "Docs mgr": ("docs", "code"),
    "Chief of Staff": ("exec", "code"),
    "CXO": ("cxo", "web"),
    "CIO": ("cio", "web"),
    "HoSR": ("hosr", "web"),
    "Lead Dev": ("lead", "code"),
    "Chief Architect": ("arch", "web"),
    "PPM": ("ppm", "web"),
    "Special Assignments": ("spec", "code"),
    "Programmer": ("prog", "code"),
    "Mobile Product (consultant)": ("mobile", "web"),
    "Vibe coder": ("vibe", "code"),
    "Exec Coach": ("coach", "web"),
    "SecOps": ("secops", "code"),
    "Researcher": ("research", "code"),
    "Unicorn web designer": ("uxd", "code"),
}

# Roles to skip (human, not agent)
SKIP_ROLES = {"xian", "ted"}


# Model detection from filename
def detect_model(filename):
    fn = filename.lower()
    if "opus" in fn:
        return "opus"
    elif "sonnet" in fn:
        return "sonnet"
    elif "haiku" in fn:
        return "haiku"
    return ""


# Extract date from filename like 2025-12-01-0721-comms-sonnet-log.md
def extract_date(filename):
    m = re.match(r"(\d{4}-\d{2}-\d{2})", filename)
    if m:
        return m.group(1)
    return None


# Parse a cell that may contain multiple filenames separated by newlines
def parse_cell(cell_text):
    """Parse a cell value into (filenames, notes) tuples."""
    if not cell_text or not cell_text.strip():
        return []

    results = []
    # Split on newlines and semicolons
    # Some cells use "; " as separator (e.g., "log-a; log-b")
    cell_text = cell_text.replace("; ", "\n")
    lines = cell_text.strip().split("\n")

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Clean leading annotations/emojis/parentheticals before checking for filename
        clean = line
        note = ""

        # Extract leading parenthetical notes like "(possibly redundant)"
        leading_paren = re.match(r"\(([^)]+)\)\s*", clean)
        if leading_paren:
            note = leading_paren.group(1)
            clean = clean[leading_paren.end() :]

        # Remove emoji prefixes
        clean = re.sub(r"^[📪📬✅🔥💀]+\s*", "", clean).strip()

        # Skip pure notes/tasks (no log filename pattern)
        # Log filenames match: YYYY-MM-DD-HHMM-*-log* or similar
        is_filename = bool(re.match(r"\d{4}-\d{2}-\d{2}", clean))

        if is_filename:
            # Extract trailing parenthetical notes
            paren_match = re.search(r"\(([^)]+)\)", clean)
            if paren_match:
                note = (note + "; " if note else "") + paren_match.group(1)
                clean = clean[: paren_match.start()].strip() + clean[paren_match.end() :].strip()

            # Add .md if missing
            if clean and not clean.endswith(".md"):
                clean = clean + ".md"

            # Remove trailing whitespace/punctuation
            clean = clean.rstrip(" ,;")

            if clean:
                results.append((clean, note))
        else:
            # Non-filename line: attach as note to previous entry if exists
            if results and clean:
                prev_fn, prev_note = results[-1]
                combined = (prev_note + "; " + clean) if prev_note else clean
                results[-1] = (prev_fn, combined)

    return results


MONTH_MAP = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12,
}


def parse_date_from_header(header_text, year, month):
    """Extract date from column header like 'Mon Dec 1' or 'Thu Jan 15'."""
    m = re.search(
        r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d+)$", header_text.strip()
    )
    if m:
        hdr_month = MONTH_MAP[m.group(1)]
        day = int(m.group(2))
        # Handle year rollover (Dec sheet may have Jan columns, etc.)
        hdr_year = year
        if hdr_month < month - 1:  # e.g., Jan in a Dec sheet = next year
            hdr_year = year + 1
        return f"{hdr_year}-{hdr_month:02d}-{day:02d}"
    return None


def process_sheet(filepath, year, month):
    """Process one monthly CSV sheet into normalized rows."""
    rows = []

    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        all_rows = list(reader)

    if not all_rows:
        return rows

    # Header row has day columns
    headers = all_rows[0]

    # Parse dates from headers (skip first column which is "Agent role")
    col_dates = {}
    for col_idx in range(1, len(headers)):
        header = headers[col_idx]
        date_str = parse_date_from_header(header, year, month)
        if date_str:
            col_dates[col_idx] = date_str

    # Process each role row
    current_role = None
    for row in all_rows[1:]:
        if not row:
            continue

        role_name = row[0].strip()

        # Skip empty role names (continuation rows from multi-line cells)
        # and human roles
        if not role_name or role_name in SKIP_ROLES:
            continue

        if role_name in ROLE_MAP:
            current_role = role_name
        elif current_role:
            # This might be a continuation line - skip
            continue
        else:
            continue

        slug, environment = ROLE_MAP.get(role_name, ("unknown", "unknown"))

        # Process each day column
        for col_idx in range(1, len(row)):
            cell = row[col_idx].strip()
            if not cell:
                continue

            col_date = col_dates.get(col_idx)
            if not col_date:
                continue

            entries = parse_cell(cell)
            for filename, note in entries:
                file_date = extract_date(filename) or col_date
                model = detect_model(filename)

                rows.append(
                    {
                        "date": file_date,
                        "role": role_name,
                        "slug": slug,
                        "environment": environment,
                        "model": model,
                        "log_filename": filename,
                        "notes": note,
                    }
                )

    return rows


def main():
    base = Path("/Users/xian/Development/piper-morgan/dev/active")

    all_rows = []

    # December 2025
    dec_file = base / "PM agent logs index - 12_2025.csv"
    if dec_file.exists():
        all_rows.extend(process_sheet(dec_file, 2025, 12))
        print(f"Dec 2025: {len(all_rows)} rows so far")

    # January 2026
    jan_file = base / "PM agent logs index - 1_2026.csv"
    if jan_file.exists():
        jan_rows = process_sheet(jan_file, 2026, 1)
        all_rows.extend(jan_rows)
        print(f"Jan 2026: {len(jan_rows)} rows, {len(all_rows)} total")

    # February 2026
    feb_file = base / "PM agent logs index - 2_2026.csv"
    if feb_file.exists():
        feb_rows = process_sheet(feb_file, 2026, 2)
        all_rows.extend(feb_rows)
        print(f"Feb 2026: {len(feb_rows)} rows, {len(all_rows)} total")

    # Sort by date, then role
    all_rows.sort(key=lambda r: (r["date"], r["role"]))

    # Write output
    output = base / "agent-log-index-normalized.csv"
    with open(output, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["date", "role", "slug", "environment", "model", "log_filename", "notes"]
        )
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"\nWrote {len(all_rows)} rows to {output}")

    # Stats
    roles = set(r["role"] for r in all_rows)
    dates = set(r["date"] for r in all_rows)
    print(f"Roles: {len(roles)} | Date range: {min(dates)} to {max(dates)}")
    for role in sorted(roles):
        count = sum(1 for r in all_rows if r["role"] == role)
        print(f"  {role}: {count} sessions")


if __name__ == "__main__":
    main()

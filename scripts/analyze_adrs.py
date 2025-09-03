#!/usr/bin/env python3
"""
ADR Metadata Analysis Script
Scans all ADRs for metadata structure and patterns
"""

import os
import re
from pathlib import Path


def extract_adr_metadata(file_path):
    """Extract metadata from an ADR file"""
    metadata = {
        "file": os.path.basename(file_path),
        "title": "",
        "number": "",
        "status": "",
        "date": "",
        "author": "",
        "decision_maker": "",
        "stakeholders": "",
        "context": "",
        "has_summary": False,
        "has_context": False,
        "has_decision": False,
        "has_consequences": False,
        "has_references": False,
        "structure_notes": [],
    }

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            lines = content.split("\n")
    except Exception as e:
        metadata["structure_notes"].append(f"Error reading file: {e}")
        return metadata

    # Extract title and number
    for line in lines[:10]:  # Check first 10 lines for title
        if line.startswith("# ADR-"):
            metadata["title"] = line[2:].strip()  # Remove '# '
            match = re.search(r"ADR-(\d+)", line)
            if match:
                metadata["number"] = match.group(1)
            break

    # Extract metadata fields from the header
    header_section = "\n".join(lines[:30])  # Check first 30 lines

    # Status patterns
    status_patterns = [r"\*\*Status\*\*:?\s*(.+)", r"## Status\s*\n(.+)", r"Status:\s*(.+)"]
    for pattern in status_patterns:
        match = re.search(pattern, header_section, re.IGNORECASE | re.MULTILINE)
        if match:
            metadata["status"] = match.group(1).strip()
            break

    # Date patterns
    date_patterns = [r"\*\*Date\*\*:?\s*(.+)", r"Date:\s*(.+)", r"## Date\s*\n(.+)"]
    for pattern in date_patterns:
        match = re.search(pattern, header_section, re.IGNORECASE)
        if match:
            metadata["date"] = match.group(1).strip()
            break

    # Author/Decision Maker patterns
    author_patterns = [
        r"\*\*Decision Maker\*\*:?\s*(.+)",
        r"\*\*Decision Makers\*\*:?\s*(.+)",
        r"\*\*Author\*\*:?\s*(.+)",
        r"Decision Maker:\s*(.+)",
        r"Author:\s*(.+)",
    ]
    for pattern in author_patterns:
        match = re.search(pattern, header_section, re.IGNORECASE)
        if match:
            if "Decision Maker" in match.group(0):
                metadata["decision_maker"] = match.group(1).strip()
            else:
                metadata["author"] = match.group(1).strip()

    # Stakeholders
    stakeholder_match = re.search(r"\*\*Stakeholders\*\*:?\s*(.+)", header_section, re.IGNORECASE)
    if stakeholder_match:
        metadata["stakeholders"] = stakeholder_match.group(1).strip()

    # Context field
    context_match = re.search(r"\*\*Context\*\*:?\s*(.+)", header_section, re.IGNORECASE)
    if context_match:
        metadata["context"] = context_match.group(1).strip()

    # Check for standard sections
    content_lower = content.lower()
    metadata["has_summary"] = "## summary" in content_lower
    metadata["has_context"] = "## context" in content_lower
    metadata["has_decision"] = "## decision" in content_lower
    metadata["has_consequences"] = (
        "## consequences" in content_lower or "## implications" in content_lower
    )
    metadata["has_references"] = "## references" in content_lower or "adr-" in content_lower

    # Structure notes
    if not metadata["status"]:
        metadata["structure_notes"].append("Missing status field")
    if not metadata["date"]:
        metadata["structure_notes"].append("Missing date field")
    if not metadata["decision_maker"] and not metadata["author"]:
        metadata["structure_notes"].append("Missing author/decision maker")

    return metadata


def analyze_all_adrs():
    """Analyze all ADRs in the directory"""
    adr_dir = Path("/Users/xian/Development/piper-morgan/docs/architecture/adr")
    results = []

    for adr_file in sorted(adr_dir.glob("adr-*.md")):
        if adr_file.name != "adr-index.md":  # Skip index file
            metadata = extract_adr_metadata(adr_file)
            results.append(metadata)

    return results


def generate_report(results):
    """Generate analysis report"""
    print("# ADR Metadata Field Analysis Report")
    print(f"**Generated:** August 29, 2025 4:51 PM")
    print(f"**Total ADRs Analyzed:** {len(results)}")
    print()

    # Summary table
    print("## Summary Table")
    print()
    print("| ADR | Title | Status | Date | Author/Decision Maker | Notes |")
    print("|-----|-------|--------|------|----------------------|-------|")

    for adr in results:
        number = adr["number"]
        title = adr["title"].replace(f"ADR-{number}: ", "")[:40] + (
            "..." if len(adr["title"]) > 40 else ""
        )
        status = adr["status"][:15] + ("..." if len(adr["status"]) > 15 else "")
        date = adr["date"][:15] + ("..." if len(adr["date"]) > 15 else "")
        author = adr["decision_maker"] or adr["author"]
        author = author[:20] + ("..." if len(author) > 20 else "") if author else "Missing"
        notes = "; ".join(adr["structure_notes"][:2])  # First 2 notes

        print(f"| {number:>3} | {title:<40} | {status:<15} | {date:<15} | {author:<20} | {notes} |")

    print()

    # Field presence analysis
    print("## Field Presence Analysis")
    print()

    status_count = sum(1 for adr in results if adr["status"])
    date_count = sum(1 for adr in results if adr["date"])
    author_count = sum(1 for adr in results if adr["decision_maker"] or adr["author"])
    context_count = sum(1 for adr in results if adr["has_context"])
    decision_count = sum(1 for adr in results if adr["has_decision"])
    summary_count = sum(1 for adr in results if adr["has_summary"])

    total = len(results)

    print(f"- **Status Field**: {status_count}/{total} ({status_count/total*100:.1f}%)")
    print(f"- **Date Field**: {date_count}/{total} ({date_count/total*100:.1f}%)")
    print(f"- **Author/Decision Maker**: {author_count}/{total} ({author_count/total*100:.1f}%)")
    print(f"- **Context Section**: {context_count}/{total} ({context_count/total*100:.1f}%)")
    print(f"- **Decision Section**: {decision_count}/{total} ({decision_count/total*100:.1f}%)")
    print(f"- **Summary Section**: {summary_count}/{total} ({summary_count/total*100:.1f}%)")
    print()

    # Status values analysis
    status_values = {}
    for adr in results:
        if adr["status"]:
            status = adr["status"].lower().strip()
            status_values[status] = status_values.get(status, 0) + 1

    print("## Status Values Found")
    print()
    for status, count in sorted(status_values.items()):
        print(f"- **{status.title()}**: {count} ADRs")
    print()

    # Author patterns
    authors = {}
    for adr in results:
        author = adr["decision_maker"] or adr["author"]
        if author:
            authors[author] = authors.get(author, 0) + 1

    print("## Author/Decision Maker Patterns")
    print()
    for author, count in sorted(authors.items(), key=lambda x: x[1], reverse=True):
        print(f"- **{author}**: {count} ADRs")
    print()

    # Recommendations
    print("## Recommendations")
    print()
    print("### Required Fields (High Priority)")
    print(
        "1. **Status** - Present in most ADRs, standardize values: Proposed, Accepted, Superseded, Deprecated"
    )
    print("2. **Date** - Critical for historical tracking, use YYYY-MM-DD format")
    print("3. **Title** - Already consistent across all ADRs")
    print()
    print("### Optional Fields (Medium Priority)")
    print("1. **Decision Maker/Author** - Important for accountability, standardize terminology")
    print("2. **Context Section** - Already present in most, make consistent")
    print("3. **Summary Section** - Add to ADRs lacking overview")
    print()
    print("### Backfill Strategy")
    print("1. **Missing Dates**: Extract from git history or session logs")
    print("2. **Missing Authors**: Use git blame or session log attribution")
    print("3. **Status Standardization**: Review and normalize to standard values")
    print("4. **Missing Summaries**: Add brief overview sections to complex ADRs")
    print()


if __name__ == "__main__":
    results = analyze_all_adrs()
    generate_report(results)

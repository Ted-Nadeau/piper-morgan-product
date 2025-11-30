#!/usr/bin/env python3
"""
Advisor Mailbox Utility

Simple CLI tool for managing the advisor mailbox system.
Designed for Ted Nadeau to use and extend.

Usage:
    python mailbox.py status              # Show mailbox status
    python mailbox.py list [inbox|outbox] # List messages
    python mailbox.py read <id>           # Mark message as read
    python mailbox.py respond <id>        # Create response template
    python mailbox.py archive <id>        # Move conversation to archive
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# Mailbox root directory (relative to this script)
MAILBOX_ROOT = Path(__file__).parent.parent
MANIFEST_PATH = MAILBOX_ROOT / "manifest.json"


def load_manifest() -> dict:
    """Load the manifest.json file."""
    with open(MANIFEST_PATH) as f:
        return json.load(f)


def save_manifest(manifest: dict) -> None:
    """Save the manifest.json file."""
    manifest["last_checked"] = datetime.utcnow().isoformat() + "Z"
    with open(MANIFEST_PATH, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"Manifest updated: {MANIFEST_PATH}")


def cmd_status():
    """Show mailbox status."""
    manifest = load_manifest()
    stats = manifest.get("stats", {})

    print("\n=== Advisor Mailbox Status ===")
    print(f"Advisor: {manifest.get('advisor', 'unknown')}")
    print(f"Last checked: {manifest.get('last_checked', 'never')}")
    print()
    print(f"Total received: {stats.get('total_received', 0)}")
    print(f"Unread:         {stats.get('unread', 0)}")
    print(f"Awaiting response: {stats.get('awaiting_response', 0)}")
    print(f"Total sent:     {stats.get('total_sent', 0)}")
    print()

    # Show unread messages
    inbox = manifest.get("messages", {}).get("inbox", [])
    unread = [m for m in inbox if m.get("status") == "unread"]
    if unread:
        print("--- Unread Messages ---")
        for msg in unread:
            priority = (
                f"[{msg.get('priority', '?').upper()}]" if msg.get("priority") == "high" else ""
            )
            print(f"  {msg['id']}: {msg['subject']} {priority}")
            print(f"      From: {msg.get('from', 'unknown')} | {msg.get('date', '')}")
        print()


def cmd_list(folder: str = "inbox"):
    """List messages in a folder."""
    manifest = load_manifest()
    messages = manifest.get("messages", {}).get(folder, [])

    if not messages:
        print(f"No messages in {folder}")
        return

    print(f"\n=== {folder.upper()} ({len(messages)} messages) ===")
    for msg in messages:
        status_icon = "○" if msg.get("status") == "unread" else "●"
        priority = f"[{msg.get('priority', '').upper()}]" if msg.get("priority") == "high" else ""
        print(f"{status_icon} {msg['id']}: {msg['subject']} {priority}")
        print(f"   From: {msg.get('from', 'unknown')} | {msg.get('date', '')}")
        print(f"   File: {msg.get('file', 'unknown')}")
        print()


def cmd_read(message_id: str):
    """Mark a message as read."""
    manifest = load_manifest()
    inbox = manifest.get("messages", {}).get("inbox", [])

    for msg in inbox:
        if msg["id"] == message_id:
            if msg["status"] == "read":
                print(f"Message {message_id} already marked as read")
                return

            msg["status"] = "read"
            msg["read_at"] = datetime.utcnow().isoformat() + "Z"

            # Update stats
            stats = manifest.get("stats", {})
            stats["unread"] = max(0, stats.get("unread", 1) - 1)
            manifest["stats"] = stats

            save_manifest(manifest)
            print(f"Marked message {message_id} as read")
            return

    print(f"Message {message_id} not found in inbox")


def cmd_respond(message_id: str):
    """Create a response template for a message."""
    manifest = load_manifest()
    inbox = manifest.get("messages", {}).get("inbox", [])

    original = None
    for msg in inbox:
        if msg["id"] == message_id:
            original = msg
            break

    if not original:
        print(f"Message {message_id} not found in inbox")
        return

    # Create response file
    response_path = MAILBOX_ROOT / "outbox" / f"{message_id}-response.md"

    if response_path.exists():
        print(f"Response file already exists: {response_path}")
        return

    template = f"""# Re: {original.get('subject', 'Unknown')}

**From**: Ted Nadeau
**To**: {original.get('from', 'Team')}
**Date**: {datetime.utcnow().strftime('%Y-%m-%d')}
**In-Reply-To**: {message_id}

---

## Response

[Your response here]

## Follow-up Questions

[Any questions for the team]

## Next Steps

[Suggested actions or decisions]

---

*Response to inbox/{message_id}*
"""

    response_path.write_text(template)
    print(f"Created response template: {response_path}")
    print("\nNext steps:")
    print(f"  1. Edit {response_path}")
    print(f"  2. Run: python mailbox.py read {message_id}")
    print(f"  3. Add your response to manifest.json outbox array")


def cmd_archive(message_id: str):
    """Move a completed conversation to archive."""
    manifest = load_manifest()
    inbox = manifest.get("messages", {}).get("inbox", [])
    outbox = manifest.get("messages", {}).get("outbox", [])
    archive = manifest.get("messages", {}).get("archive", [])

    # Find inbox message
    inbox_msg = None
    for i, msg in enumerate(inbox):
        if msg["id"] == message_id:
            inbox_msg = inbox.pop(i)
            break

    if not inbox_msg:
        print(f"Message {message_id} not found in inbox")
        return

    # Find matching outbox response
    outbox_msg = None
    for i, msg in enumerate(outbox):
        if msg.get("in_reply_to") == message_id or msg["id"] == message_id:
            outbox_msg = outbox.pop(i)
            break

    # Create archive entry
    archive_entry = {
        "id": message_id,
        "subject": inbox_msg.get("subject"),
        "archived_at": datetime.utcnow().isoformat() + "Z",
        "inbox_file": inbox_msg.get("file"),
        "outbox_file": outbox_msg.get("file") if outbox_msg else None,
    }
    archive.append(archive_entry)

    # Update stats
    stats = manifest.get("stats", {})
    stats["awaiting_response"] = max(0, stats.get("awaiting_response", 1) - 1)
    manifest["stats"] = stats

    save_manifest(manifest)
    print(f"Archived conversation {message_id}")

    # Move files
    inbox_file = MAILBOX_ROOT / inbox_msg.get("file", "")
    if inbox_file.exists():
        archive_file = MAILBOX_ROOT / "archive" / inbox_file.name
        inbox_file.rename(archive_file)
        print(f"Moved {inbox_file} to archive/")


def cmd_help():
    """Show help."""
    print(__doc__)


def main():
    if len(sys.argv) < 2:
        cmd_status()
        return

    command = sys.argv[1].lower()

    if command == "status":
        cmd_status()
    elif command == "list":
        folder = sys.argv[2] if len(sys.argv) > 2 else "inbox"
        cmd_list(folder)
    elif command == "read":
        if len(sys.argv) < 3:
            print("Usage: mailbox.py read <message_id>")
            return
        cmd_read(sys.argv[2])
    elif command == "respond":
        if len(sys.argv) < 3:
            print("Usage: mailbox.py respond <message_id>")
            return
        cmd_respond(sys.argv[2])
    elif command == "archive":
        if len(sys.argv) < 3:
            print("Usage: mailbox.py archive <message_id>")
            return
        cmd_archive(sys.argv[2])
    elif command in ("help", "-h", "--help"):
        cmd_help()
    else:
        print(f"Unknown command: {command}")
        cmd_help()


if __name__ == "__main__":
    main()

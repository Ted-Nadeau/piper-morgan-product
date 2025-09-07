#!/usr/bin/env python3
"""
Google Calendar OAuth Setup Script

This script completes the OAuth flow for Google Calendar integration.
It will open a browser for authorization and create token.json for future use.
"""

import os
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow


def setup_google_calendar_oauth():
    """Complete Google Calendar OAuth setup"""

    # Check if credentials file exists
    if not Path("credentials.json").exists():
        print("❌ credentials.json not found!")
        print("Please ensure credentials.json is in the current directory")
        return False

    # Check if token already exists
    if Path("token.json").exists():
        print("✅ token.json already exists - OAuth may already be set up")
        return True

    # Define required scopes
    SCOPES = [
        "https://www.googleapis.com/auth/calendar.readonly",
        "https://www.googleapis.com/auth/calendar.events.readonly",
        "https://www.googleapis.com/auth/calendar.calendarlist.readonly",
        "https://www.googleapis.com/auth/calendar.calendars.readonly",
    ]

    try:
        print("🚀 Starting Google Calendar OAuth setup...")
        print("📋 Required permissions:")
        for scope in SCOPES:
            print(f"   - {scope}")

        # Create OAuth flow
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)

        print("\n🌐 Opening browser for authorization...")
        print("   Please grant the requested permissions in your browser")

        # Run OAuth flow (this will open browser)
        credentials = flow.run_local_server(port=8084)

        # Save credentials to token.json
        with open("token.json", "w") as token_file:
            token_file.write(credentials.to_json())

        print("✅ OAuth setup complete!")
        print("📁 token.json created successfully")
        print("🎉 Google Calendar integration is now ready!")

        return True

    except Exception as e:
        print(f"❌ OAuth setup failed: {e}")
        return False


if __name__ == "__main__":
    success = setup_google_calendar_oauth()
    if success:
        print("\n🎯 Next steps:")
        print("   1. Test calendar integration: ./py cli/commands/standup.py --with-calendar")
        print("   2. Calendar events should now appear in standup output")
    else:
        print("\n🔧 Troubleshooting:")
        print("   1. Ensure credentials.json is valid")
        print("   2. Check internet connection")
        print("   3. Try running the script again")

"""
One-time migration: Move Christian's personal data from PIPER.md to alpha_users.preferences

This script migrates personal context from the old PIPER.md file (which was shared
across all users) to the xian user's alpha_users.preferences JSONB field, enabling
proper user data isolation.

Issue: #280 CORE-ALPHA-DATA-LEAK
Date: November 1, 2025
"""

import asyncio
import json
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select

from services.database.connection import db
from services.database.models import AlphaUser


async def migrate_personal_data():
    """
    Move xian's personal data to alpha_users.preferences JSONB field.

    Returns:
        str: User ID if successful, None if failed
    """
    print("=" * 70)
    print("Personal Data Migration: PIPER.md → alpha_users.preferences")
    print("=" * 70)
    print()

    # Initialize database connection
    await db.initialize()

    # Get a session
    async with await db.get_session() as session:
        try:
            # 1. Find xian's user record
            print("1. Looking up user 'xian' in alpha_users table...")
            result = await session.execute(select(AlphaUser).where(AlphaUser.username == "xian"))
            user = result.scalar_one_or_none()

            if not user:
                print("❌ ERROR: User 'xian' not found in alpha_users table")
                print()
                print("Available users:")
                all_users_result = await session.execute(select(AlphaUser))
                for u in all_users_result.scalars():
                    print(f"  - {u.username} (ID: {u.id})")
                return None

            print(f"✅ Found user: {user.username}")
            print(f"   User ID: {user.id}")
            print(f"   Email: {user.email or 'Not set'}")
            print()

            # 2. Prepare personal context data
            print("2. Preparing personal context data...")
            personal_context = {
                "user_context": {
                    "name": "Christian",
                    "role": "Product Manager / Developer",
                    "timezone": "Pacific Time (PT)",
                    "working_hours": "6:00 AM - 6:00 PM PT",
                    "location": "San Francisco Bay Area",
                    "communication_style": "Direct, efficiency-focused, pattern-oriented",
                },
                "key_characteristics": [
                    "Values systematic approaches and evidence-based development",
                    "Prefers quick wins and iterative improvement",
                    "Maintains high standards for code quality and documentation",
                    "Uses GitHub-first tracking for project management",
                    "Emphasizes the Excellence Flywheel methodology",
                ],
                "current_focus": {
                    "quarter": "Q4 2025",
                    "primary_objective": "VA/Decision Reviews Q4 Onramp implementation and delivery",
                    "strategic_goal": "Successfully launch VA decision review system for Q4 2025",
                    "week_priority": "VA deliverables and onramp system implementation",
                },
                "key_initiatives": [
                    {
                        "name": "VA Q4 Onramp",
                        "status": "ACTIVE",
                        "description": "VA decision review system implementation",
                    },
                    {
                        "name": "Kind Systems Integration",
                        "status": "ACTIVE",
                        "description": "Company and DRAGONS team collaboration",
                    },
                    {
                        "name": "Director of PM Role",
                        "status": "ACTIVE",
                        "description": "Product management leadership responsibilities",
                    },
                    {
                        "name": "Piper Morgan AI",
                        "status": "COMPLETE",
                        "description": "Production-ready MCP Consumer delivered",
                    },
                ],
                "success_metrics": [
                    "VA Q4 Onramp delivery: On-time completion and system validation",
                    "Kind Systems collaboration: Successful DRAGONS team integration",
                    "Director of PM effectiveness: Leadership and strategic delivery",
                    "Piper Morgan AI performance: <150ms target (achieving 36.43ms)",
                ],
                "projects": [
                    {
                        "name": "VA/Decision Reviews Q4 Onramp",
                        "allocation": 70,
                        "status": "Active development and implementation",
                        "focus": "VA decision review system onramp for Q4 2025",
                        "company": "Kind Systems",
                        "team": "DRAGONS",
                        "role": "Director of Product Management",
                        "next_milestone": "Q4 onramp completion and system validation",
                    },
                    {
                        "name": "Piper Morgan AI Assistant",
                        "allocation": 25,
                        "status": "Production-ready MCP Consumer with real GitHub integration",
                        "phase": "UX enhancement and conversational AI improvement",
                        "next_milestone": "Enhanced standup experience with PIPER.md context",
                        "achievements": [
                            "2,480 lines of production code",
                            "84 real GitHub issues retrieved",
                        ],
                    },
                    {
                        "name": "OneJob/Content/Other",
                        "allocation": 5,
                        "status": "Ongoing maintenance and development",
                        "focus": "Core functionality, technical writing, pattern documentation",
                    },
                ],
                "calendar": {
                    "daily_routines": {
                        "06:00": "Daily standup with Piper Morgan",
                        "09:00": "Development focus time",
                        "14:00": "UX and improvement work",
                        "17:00": "Documentation and handoff preparation",
                    },
                    "recurring_meetings": {
                        "Monday": "MCP development sprints",
                        "Wednesday": "UX enhancement sessions",
                        "Friday": "Pattern review and methodology validation",
                    },
                    "key_dates": {
                        "2025-08-11": "MCP Monday Sprint completed",
                        "2025-08-12": "Enhanced standup experience target",
                        "2025-08-15": "UX improvement validation",
                        "2025-08-18": "Next development sprint planning",
                    },
                },
                "priorities": [
                    {
                        "rank": 1,
                        "name": "VA Q4 Onramp system implementation and delivery",
                        "goal": "Complete VA decision review system for Q4 2025",
                        "success": "System operational and validated for production use",
                        "timeline": "Q4 2025 completion",
                    },
                    {
                        "rank": 2,
                        "name": "Kind Systems and DRAGONS team collaboration",
                        "goal": "Successful integration and collaboration with company team",
                        "success": "Effective team coordination and project delivery",
                        "timeline": "Ongoing throughout Q4",
                    },
                    {
                        "rank": 3,
                        "name": "Pattern application and validation",
                        "goal": "Apply consolidated patterns to new development",
                        "success": "Consistent architecture and implementation quality",
                        "timeline": "Ongoing",
                    },
                    {
                        "rank": 4,
                        "name": "UX enhancement and user experience",
                        "goal": "Improve overall conversational AI experience",
                        "success": "Natural language workflows and context awareness",
                        "timeline": "Q4 2025",
                    },
                    {
                        "rank": 5,
                        "name": "Documentation and knowledge management",
                        "goal": "Maintain comprehensive and accurate documentation",
                        "success": "All links working, up-to-date guides",
                        "timeline": "Ongoing",
                    },
                ],
                "knowledge_sources": {
                    "core_documentation": [
                        "docs/patterns/PATTERN-INDEX.md - Master index of 25+ patterns",
                        "docs/architecture/ - System design and implementation patterns",
                        "docs/user-guides/ - Conversational AI and usage patterns",
                        "docs/development/session-logs/ - Development history",
                    ],
                    "key_resources": [
                        "MCP Foundation: 15,457+ lines of MCP infrastructure code",
                        "Excellence Flywheel: Verify First, Evidence Required, Complete Bookending",
                        "Dual-Agent Coordination: Validated patterns for complex tasks",
                        "GitHub Integration: Real-time issue tracking and management",
                    ],
                    "recent_achievements": [
                        "MCP Consumer: 2,480 lines of production-ready code",
                        "Performance: 36.43ms response time (target: <150ms)",
                        "Integration: 84 real GitHub issues retrieved",
                        "Documentation: Complete deployment and implementation guides",
                    ],
                },
                "migration_metadata": {
                    "source": "config/PIPER.md.backup-20251101",
                    "migration_date": "2025-11-01",
                    "issue": "#280 CORE-ALPHA-DATA-LEAK",
                    "migrated_by": "scripts/migrate_personal_data_to_xian.py",
                },
            }

            print(f"   Prepared {len(personal_context)} top-level context keys")
            print(f"   Projects: {len(personal_context['projects'])}")
            print(f"   Priorities: {len(personal_context['priorities'])}")
            print(f"   Initiatives: {len(personal_context['key_initiatives'])}")
            print()

            # 3. Merge with existing preferences (if any)
            print("3. Merging with existing preferences...")
            current_prefs = user.preferences or {}
            print(
                f"   Current preferences keys: {list(current_prefs.keys()) if current_prefs else '(empty)'}"
            )

            # Merge - personal_context takes precedence
            updated_prefs = {**current_prefs, **personal_context}
            print(f"   Updated preferences keys: {list(updated_prefs.keys())}")
            print()

            # 4. Update user record
            print("4. Updating alpha_users.preferences...")
            user.preferences = updated_prefs
            await session.commit()
            print("✅ Database commit successful")
            print()

            # 5. Verify update
            print("5. Verifying migration...")
            await session.refresh(user)

            if user.preferences and "migration_metadata" in user.preferences:
                print("✅ Migration metadata found in preferences")
                print(
                    f"   Migration date: {user.preferences['migration_metadata']['migration_date']}"
                )
                print(f"   Source: {user.preferences['migration_metadata']['source']}")
            else:
                print("⚠️  Warning: Could not verify migration metadata")

            print()
            print("=" * 70)
            print("✅ MIGRATION COMPLETE")
            print("=" * 70)
            print()
            print(f"User ID: {user.id}")
            print(f"Username: {user.username}")
            print(f"Preferences keys: {list(user.preferences.keys())}")
            print()
            print("Next steps:")
            print("1. Update UserContextService to load from alpha_users.preferences")
            print("2. Test multi-user isolation")
            print("3. Verify no personal data in generic PIPER.md")
            print()

            return str(user.id)

        except Exception as e:
            print(f"❌ ERROR during migration: {str(e)}")
            print(f"   Type: {type(e).__name__}")
            import traceback

            traceback.print_exc()
            return None


async def main():
    """Main entry point"""
    result = await migrate_personal_data()

    if result:
        print(f"✅ Migration successful. User ID: {result}")
        sys.exit(0)
    else:
        print("❌ Migration failed. See errors above.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

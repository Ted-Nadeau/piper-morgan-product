#!/bin/bash

# Pre-Push Hook: Release Notes Enforcement
# Version: 2.0.0 (Issue #610)
# Purpose: Ensure release notes exist when version is bumped
# Trigger: PM increments version number in pyproject.toml
# Policy: Release notes mandatory for production deployments
#
# Changes in 2.0.0:
# - Fixed release notes path: now checks docs/releases/ (canonical location)
# - Removed date-based path (dev/YYYY/MM/DD/) which was gitignored
# - Simplified validation

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the branch being pushed
while read local_ref local_sha remote_ref remote_sha; do
    # Only check pushes to production branch
    if [[ "$remote_ref" != "refs/heads/production" ]]; then
        exit 0  # Not pushing to production, skip check
    fi

    echo "🔍 Checking for release notes (production push detected)..."

    # Get current version from pyproject.toml
    CURRENT_VERSION=$(grep '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/')

    if [ -z "$CURRENT_VERSION" ]; then
        echo -e "${RED}❌ ERROR: Could not read version from pyproject.toml${NC}"
        exit 1
    fi

    # Get the version from the remote production branch
    REMOTE_VERSION=$(git show origin/production:pyproject.toml 2>/dev/null | grep '^version = ' | sed 's/version = "\(.*\)"/\1/' || echo "")

    # If remote doesn't exist yet (first push), skip version check
    if [ -z "$REMOTE_VERSION" ]; then
        echo -e "${YELLOW}⚠️  First push to production - skipping version check${NC}"
        exit 0
    fi

    # Check if version changed
    if [ "$CURRENT_VERSION" == "$REMOTE_VERSION" ]; then
        echo -e "${GREEN}✓ Version unchanged ($CURRENT_VERSION) - release notes not required${NC}"
        exit 0
    fi

    echo -e "${YELLOW}📋 Version change detected: $REMOTE_VERSION → $CURRENT_VERSION${NC}"
    echo "   Release notes are MANDATORY for version changes"

    # Expected release notes file location (canonical location per release runbook)
    RELEASE_NOTES_FILE="docs/releases/RELEASE-NOTES-v${CURRENT_VERSION}.md"

    # Check if release notes exist
    if [ ! -f "$RELEASE_NOTES_FILE" ]; then
        echo -e "${RED}❌ PUSH BLOCKED: Release notes missing${NC}"
        echo ""
        echo "Required file: $RELEASE_NOTES_FILE"
        echo ""
        echo "Policy: When PM increments version in pyproject.toml,"
        echo "        release notes documenting changes are mandatory."
        echo ""
        echo "To fix:"
        echo "  1. Create release notes file:"
        echo "     docs/releases/RELEASE-NOTES-v${CURRENT_VERSION}.md"
        echo ""
        echo "  2. Follow template from previous release notes in docs/releases/"
        echo "  3. Update docs/releases/README.md with new version"
        echo "  4. Commit and push again"
        echo ""
        echo "See: docs/internal/operations/release-runbook.md"
        echo ""
        echo "To bypass (NOT RECOMMENDED):"
        echo "  git push --no-verify"
        echo ""
        exit 1
    fi

    # Verify file is not empty
    if [ ! -s "$RELEASE_NOTES_FILE" ]; then
        echo -e "${RED}❌ PUSH BLOCKED: Release notes file is empty${NC}"
        echo ""
        echo "File exists but has no content: $RELEASE_NOTES_FILE"
        echo ""
        echo "Please add release notes content and commit before pushing."
        echo ""
        exit 1
    fi

    # Verify file contains version number
    if ! grep -q "$CURRENT_VERSION" "$RELEASE_NOTES_FILE"; then
        echo -e "${RED}❌ PUSH BLOCKED: Release notes don't mention version $CURRENT_VERSION${NC}"
        echo ""
        echo "File: $RELEASE_NOTES_FILE"
        echo "Expected to find: $CURRENT_VERSION"
        echo ""
        echo "Please verify release notes are for the correct version."
        echo ""
        exit 1
    fi

    echo -e "${GREEN}✓ Release notes found and validated${NC}"
    echo "  File: $RELEASE_NOTES_FILE"
    echo "  Version: $CURRENT_VERSION"
    echo ""
    echo "Proceeding with push..."

done

exit 0

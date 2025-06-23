#!/bin/bash
#
# This script updates GitHub issue #27 with refined architectural recommendations.
#
# Requirements:
# 1. GitHub CLI ('gh') must be installed: https://cli.github.com/
# 2. You must be authenticated: `gh auth login`
# 3. The script must be run from within the git repository.

set -e # Exit immediately if a command exits with a non-zero status.

ISSUE_NUMBER=27
NEW_TITLE="TOOL: Create domain/database schema validator"

# --- Cleanup function ---
# Ensures temporary file is removed on exit
cleanup() {
    rm -f issue_body.tmp
}
trap cleanup EXIT

echo "🔎 Checking for GitHub CLI..."
if ! command -v gh &> /dev/null
then
    echo "❌ GitHub CLI ('gh') could not be found. Please install it to continue."
    exit 1
fi

echo "🔐 Checking GitHub authentication status..."
if ! gh auth status &> /dev/null
then
    echo "❌ You are not logged into GitHub. Please run 'gh auth login'."
    exit 1
fi

# Attempt to get the repository from the git remote URL
REPO=$(gh repo view --json nameWithOwner --jq .nameWithOwner 2>/dev/null || echo "")

if [ -z "$REPO" ]; then
    echo "❌ Could not determine GitHub repository from git remote. Please run this script from the repository's root directory."
    exit 1
fi

echo "✅ Ready to update issue #$ISSUE_NUMBER in repository: $REPO"
echo ""

# Create the new issue body in a temporary file
cat > issue_body.tmp <<'EOF'
**Description:**
We've had multiple bugs from domain/database drift. This ticket is to create a tool that programmatically compares SQLAlchemy models with our domain dataclasses to enforce the "Domain-First" architectural pattern.

**Acceptance Criteria:**
- [ ] A new script is created (e.g., `tools/check_domain_db_consistency.py`).
- [ ] The script compares field names between domain models (e.g., `Workflow`) and their corresponding database models (e.g., `WorkflowDB`).
- [ ] The script is integrated into the CI/CD pipeline.
- [ ] The build fails if a mismatch is detected.
- [ ] The script's output provides hints for creating a new migration if a mismatch is found.

**Implementation Hint:**
```python
# tools/check_domain_db_consistency.py
import dataclasses
from services.domain.models import Workflow
from services.database.models import WorkflowDB

def check_consistency():
    domain_fields = {f.name for f in dataclasses.fields(Workflow)}
    db_fields = {c.name for c in WorkflowDB.__table__.columns}
    
    missing_in_domain = db_fields - domain_fields
    missing_in_db = domain_fields - db_fields
    
    if missing_in_domain or missing_in_db:
        # Custom error class would be ideal
        raise Exception(
            f"Domain/DB mismatch found!\n"
            f"Fields in DB but not Domain: {missing_in_domain}\n"
            f"Fields in Domain but not DB: {missing_in_db}"
        )
```

**Architectural Insight:**
These bugs reveal that our Domain-First Database Pattern needs stronger enforcement. The pattern is correct, but we lack tooling to ensure the database actually follows the domain. This tool will close that gap.
EOF

# Update the issue using the temporary file
gh issue edit "$ISSUE_NUMBER" --repo "$REPO" \
  --title "$NEW_TITLE" \
  --body-file issue_body.tmp

echo "🎉 Issue #$ISSUE_NUMBER has been successfully updated." 
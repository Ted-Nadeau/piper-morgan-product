#!/bin/bash
#
# This script creates the architectural follow-up tickets in GitHub.
#
# Requirements:
# 1. GitHub CLI ('gh') must be installed: https://cli.github.com/
# 2. You must be authenticated: `gh auth login`
# 3. The script must be run from within the git repository.

set -e # Exit immediately if a command exits with a non-zero status.

# --- Cleanup function ---
# Ensures temporary files are removed on exit
cleanup() {
    rm -f ticket_*.tmp
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

echo "✅ Ready to create issues in repository: $REPO"
echo ""

# --- Ticket 1: Python Version Consistency ---
echo "📄 Creating Ticket 1: Enforce Python Version Consistency..."

cat > ticket_1.tmp <<'EOF'
**Description:**
The recent `asyncio.timeout` bug in production was caused by a mismatch between the Python version used in development and the one implicitly used in deployment. To prevent this entire class of errors, we need to enforce version consistency.

**Acceptance Criteria:**
- [ ] A `.python-version` file is added to the repository root, specifying Python `3.11`.
- [ ] A `Dockerfile` is created for the main Python application service that uses the official Python `3.11` base image.
- [ ] The `docker-compose.yml` file is updated to include a build context for the Python application service.

**Labels:** `eng-quality`, `bug`, `dev-ops`
EOF

gh issue create --repo "$REPO" \
  --title "ENG: Enforce Python Version Consistency Across Environments" \
  --body-file ticket_1.tmp

echo "✅ Ticket 1 created."
echo ""

# --- Ticket 2: Workflow Context Validation ---
echo "📄 Creating Ticket 2: Implement Workflow Context Validation..."

cat > ticket_2.tmp <<'EOF'
**Description:**
The `TASK_FAILED` error occurred because a workflow was started with incorrect context (e.g., the `analyze_github_issue` workflow was triggered without a GitHub URL). Workflows should fail fast if they don't have the required data to execute.

**Acceptance Criteria:**
- [ ] A centralized validation registry (e.g., a dictionary) is created in the `WorkflowFactory` to define the required context keys for each `WorkflowType`.
- [ ] The `create_from_intent` method in the `WorkflowFactory` is updated to validate the incoming context against the registry.
- [ ] If validation fails, an `InvalidWorkflowContextError` (or similar) is raised.
- [ ] Unit tests are added for the validation logic.

**Labels:** `eng-quality`, `bug`, `architecture`, `refactor`
EOF

gh issue create --repo "$REPO" \
  --title "ENG: Implement Pre-execution Context Validation for Workflows" \
  --body-file ticket_2.tmp

echo "✅ Ticket 2 created."
echo ""

# --- Ticket 3: CI Check for Database Schema Integrity ---
echo "📄 Creating Ticket 3: Add CI Check for Database Schema Integrity..."

cat > ticket_3.tmp <<'EOF'
**Description:**
The `input_data` field mismatch between our domain models and the database schema went undetected until it caused a runtime error. We need to add an automated check to our CI pipeline to catch this type of drift early.

**Acceptance Criteria:**
- [ ] A new step is added to the CI pipeline (e.g., in GitHub Actions).
- [ ] This step runs `alembic check` to compare the current state of the database models with the latest migration.
- [ ] The CI job fails if `alembic check` reports a mismatch.

**Labels:** `eng-quality`, `bug`, `CI/CD`, `dev-ops`
EOF

gh issue create --repo "$REPO" \
  --title "CI: Add Automated Check for Domain/Database Schema Drift" \
  --body-file ticket_3.tmp

echo "✅ Ticket 3 created."
echo ""

echo "🎉 All architectural follow-up tickets have been successfully created."

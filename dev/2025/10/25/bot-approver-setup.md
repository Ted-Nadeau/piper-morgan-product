# GitHub Bot Auto-Approver Setup

## Quick Implementation (15 minutes)

### Step 1: Create the GitHub Action

Create file: `.github/workflows/auto-approve.yml`

```yaml
name: Auto Approve Safe PRs
on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  auto-approve:
    runs-on: ubuntu-latest
    if: github.actor == 'mediajunkie'  # Only auto-approve your own PRs
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run safety checks
        id: safety
        run: |
          # Check for secrets/keys
          if git diff origin/main..HEAD | grep -E "(api_key|secret|token|password)" -i; then
            echo "::set-output name=safe::false"
            echo "Found potential secrets in diff"
            exit 1
          fi

          # Check for direct DB modifications
          if git diff origin/main..HEAD --name-only | grep -E "migrations/|schema\.sql"; then
            echo "::set-output name=safe::false"
            echo "Found database schema changes"
            exit 1
          fi

          echo "::set-output name=safe::true"

      - name: Auto approve if safe
        if: steps.safety.outputs.safe == 'true'
        uses: hmarr/auto-approve-action@v3
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}

      - name: Add label
        if: steps.safety.outputs.safe == 'true'
        uses: actions-ecosystem/action-add-labels@v1
        with:
          labels: auto-approved
```

### Step 2: Create a GitHub App (Better Approach)

Since you can't approve your own PRs even with automation, create a GitHub App:

1. Go to GitHub Settings → Developer settings → GitHub Apps → New GitHub App
2. Name: "Piper Auto-Approver"
3. Permissions needed:
   - Pull requests: Write
   - Contents: Read
   - Checks: Read
4. Install on your repository

### Step 3: Update the workflow to use the App

```yaml
name: Auto Approve Safe PRs
on:
  pull_request:
    types: [opened, synchronize, reopened]
  workflow_dispatch:  # Allow manual trigger

jobs:
  auto-approve:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Generate token
        id: generate_token
        uses: tibdex/github-app-token@v2
        with:
          app_id: ${{ secrets.APP_ID }}
          private_key: ${{ secrets.APP_PRIVATE_KEY }}

      - name: Check PR safety
        id: check
        run: |
          # Add your safety checks here
          echo "Checking for common issues..."

          # No secrets
          ! git diff origin/main..HEAD | grep -qiE "(api_key|secret|token|password)"

      - name: Approve PR
        if: success()
        uses: hmarr/auto-approve-action@v3
        with:
          github-token: ${{ steps.generate_token.outputs.token }}

      - name: Comment
        if: success()
        uses: actions/github-script@v6
        with:
          github-token: ${{ steps.generate_token.outputs.token }}
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '✅ Auto-approved: All safety checks passed'
            })
```

## Alternative: Quick Hack (5 minutes)

If the above seems like too much for alpha:

1. Create a second GitHub account: "piper-reviewer"
2. Add it as a collaborator with write access
3. Use GitHub CLI to approve from that account:

```bash
# One-time setup
gh auth login  # Login as piper-reviewer

# To approve a PR
gh pr review --approve PR_NUMBER
```

## Recommendation

For Alpha (next 4 days): Use the quick hack (second account)
Post-Alpha: Set up the proper GitHub App

The GitHub App is the "right" solution but the second account works fine for alpha testing purposes.

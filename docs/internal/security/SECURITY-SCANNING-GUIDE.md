# Security Scanning Guide

**Last Updated**: November 28, 2025
**Author**: Claude Code (Opus 4.1), Security DevOps Agent

---

## Overview

This guide documents the comprehensive security scanning setup for Piper Morgan, including dependency auditing, code analysis, secret detection, and continuous monitoring.

---

## Quick Start

### Local Security Commands

```bash
# NPM Security (JavaScript dependencies)
npm run security:audit          # Run basic audit
npm run security:check          # Check for moderate+ issues
npm run security:audit-fix      # Auto-fix vulnerabilities
npm run security:report         # Generate JSON report

# Python Security (requires 'pip install safety')
safety check                    # Check Python dependencies
safety check --json            # JSON output

# Pre-commit Security Hook
.pre-commit-hooks/security-check.sh  # Run all pre-commit checks
```

---

## CI/CD Security Pipeline

### GitHub Actions Workflow

**File**: `.github/workflows/security-scan.yml`

**Triggers**:
- Every push to `main` or `develop`
- Every pull request
- Daily at 2 AM UTC (scheduled scan)
- Manual trigger via GitHub Actions UI

### Security Jobs

#### 1. NPM Audit
- **Purpose**: Check JavaScript/Node.js dependencies
- **Tool**: Native `npm audit`
- **Failure Condition**: Critical vulnerabilities
- **Report**: npm-audit-report.txt artifact

#### 2. Python Safety Check
- **Purpose**: Check Python dependencies
- **Tool**: `safety` package
- **Failure Condition**: Currently warning only
- **Report**: safety-report.json artifact

#### 3. CodeQL Analysis
- **Purpose**: Static Application Security Testing (SAST)
- **Languages**: JavaScript, Python
- **Queries**: security-extended, security-and-quality
- **Results**: GitHub Security tab

#### 4. Trivy Scan
- **Purpose**: Container and filesystem vulnerability scanning
- **Coverage**: All files, focusing on HIGH/CRITICAL
- **Results**: SARIF format to GitHub Security tab

#### 5. TruffleHog Secret Scan
- **Purpose**: Detect leaked secrets in code history
- **Coverage**: Full git history
- **Mode**: Only verified secrets (reduces false positives)

#### 6. License Compliance
- **Purpose**: Ensure license compatibility
- **Tool**: license-checker
- **Output**: Summary in workflow run

#### 7. OWASP Dependency Check
- **Purpose**: Known vulnerability database check
- **Coverage**: All dependencies
- **Reports**: HTML and JSON formats

#### 8. Security Summary
- **Purpose**: Consolidated report
- **Location**: GitHub Actions summary page

---

## Pre-Commit Hooks

### Setup

```bash
# Add to your .git/hooks/pre-commit
#!/bin/bash
.pre-commit-hooks/security-check.sh
```

### Checks Performed

1. **Secret Detection**
   - API keys, tokens, passwords
   - AWS credentials
   - GitHub tokens
   - OpenAI keys

2. **Dependency Audit** (if package files changed)
   - NPM vulnerabilities
   - Python vulnerabilities

3. **Debug Code Detection** (informational)
   - console.log statements
   - print() statements
   - debugger/pdb traces

---

## Security Levels

### NPM Audit Levels

| Level | Description | Action |
|-------|-------------|--------|
| Critical | Remote code execution, etc. | Block deployment |
| High | Significant security risk | Fix immediately |
| Moderate | Potential security issue | Fix within sprint |
| Low | Minor issues | Fix when convenient |

### Python Safety Levels

| Level | Description | Action |
|-------|-------------|--------|
| Critical | Known exploits | Block deployment |
| High | Serious vulnerabilities | Fix immediately |
| Medium | Potential issues | Review and plan fix |
| Low | Informational | Monitor |

---

## Remediation Procedures

### When Vulnerabilities Are Found

#### NPM Dependencies

```bash
# View detailed vulnerability information
npm audit

# Automatic fix (safe updates)
npm audit fix

# Force major version updates (test thoroughly!)
npm audit fix --force

# Manual fix for specific package
npm install package-name@latest
```

#### Python Dependencies

```bash
# Check current vulnerabilities
safety check

# Update specific package
pip install --upgrade package-name

# Update all packages (careful!)
pip list --outdated
pip install --upgrade -r requirements.txt
```

### When Secrets Are Detected

1. **DO NOT COMMIT** the secret
2. Remove from staged files: `git reset HEAD <file>`
3. Clean the secret from the file
4. Use environment variables or secret management
5. If already committed:
   - Rotate the secret immediately
   - Use `git filter-branch` or BFG Repo-Cleaner to remove from history
   - Force push cleaned branch (coordinate with team)

---

## Configuration Files

### package.json Scripts

```json
{
  "scripts": {
    "security:audit": "npm audit",
    "security:audit-fix": "npm audit fix",
    "security:audit-fix-force": "npm audit fix --force",
    "security:check": "npm audit --audit-level=moderate",
    "security:report": "npm audit --json > security-audit-report.json"
  }
}
```

### GitHub Actions Schedule

```yaml
on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM UTC
```

---

## Monitoring & Alerts

### GitHub Security Tab
- CodeQL alerts
- Dependabot alerts
- Secret scanning alerts
- Trivy vulnerability reports

### Workflow Notifications
- Failed security scans trigger GitHub notifications
- Check email for critical security alerts

### Manual Review Schedule
- Daily: Check GitHub Actions security summary
- Weekly: Review Dependabot pull requests
- Monthly: Full security audit and report

---

## Tools Reference

| Tool | Purpose | Documentation |
|------|---------|---------------|
| npm audit | Node.js dependencies | https://docs.npmjs.com/cli/v9/commands/npm-audit |
| safety | Python dependencies | https://pyup.io/safety/ |
| CodeQL | SAST | https://codeql.github.com/ |
| Trivy | Container scanning | https://aquasecurity.github.io/trivy/ |
| TruffleHog | Secret detection | https://github.com/trufflesecurity/trufflehog |
| OWASP Dependency Check | Vulnerability DB | https://owasp.org/www-project-dependency-check/ |

---

## Best Practices

1. **Never commit secrets** - Use environment variables
2. **Keep dependencies updated** - Review Dependabot PRs weekly
3. **Fix critical issues immediately** - Don't accumulate security debt
4. **Test after security updates** - Ensure nothing breaks
5. **Monitor security alerts** - Set up GitHub notifications
6. **Regular audits** - Run manual scans monthly
7. **Document exceptions** - If you must accept a risk, document why

---

## Troubleshooting

### NPM Audit Issues

```bash
# Clear cache if audit is stuck
npm cache clean --force

# Regenerate package-lock.json
rm package-lock.json
npm install
```

### Python Safety Issues

```bash
# Update safety database
safety check --update

# Check specific requirements file
safety check -r requirements.txt
```

### GitHub Actions Failures

1. Check the workflow run logs
2. Download artifacts for detailed reports
3. Run the same commands locally to debug
4. Check GitHub Security tab for details

---

## Contact & Support

- **Security Issues**: Create private security advisory in GitHub
- **Questions**: File issue with `security` label
- **Urgent**: Contact PM directly

---

## Changelog

- **2025-11-28**: Initial setup with comprehensive scanning pipeline
- Added npm audit, Python safety, CodeQL, Trivy, TruffleHog
- Created pre-commit hooks and documentation

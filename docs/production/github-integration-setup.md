# GitHub Integration Production Setup Guide

**Date:** 2025-07-23
**PM-012 Implementation:** GitHub API Design + High-Impact Implementation
**Status:** Production Ready

This guide provides comprehensive setup instructions for deploying Piper Morgan's GitHub integration in production environments.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Configuration Requirements](#configuration-requirements)
3. [Authentication Setup](#authentication-setup)
4. [Repository Configuration](#repository-configuration)
5. [Feature Flags](#feature-flags)
6. [Production Deployment](#production-deployment)
7. [Monitoring and Troubleshooting](#monitoring-and-troubleshooting)

---

## Quick Start

### Minimum Required Configuration

```bash
# Required environment variables
export GITHUB_TOKEN="ghp_your_github_personal_access_token"
export GITHUB_DEFAULT_REPO="your-org/your-repo"

# Optional but recommended
export PIPER_ENVIRONMENT="production"
export GITHUB_ALLOWED_REPOS="your-org/repo1,your-org/repo2"
```

### Test the Setup

```bash
# Verify configuration
PYTHONPATH=. python -c "
from services.integrations.github.config_service import GitHubConfigService
config = GitHubConfigService()
summary = config.get_configuration_summary()
print('GitHub Integration Status:', 'READY' if summary['has_authentication_token'] else 'NOT CONFIGURED')
print('Environment:', summary['environment'])
print('Default Repository:', summary['default_repository'])
"
```

---

## Configuration Requirements

### Environment Variables

**Required:**
```bash
GITHUB_TOKEN                    # GitHub Personal Access Token or App Token
```

**Recommended:**
```bash
GITHUB_DEFAULT_REPO            # Default repository for issue creation (format: owner/repo)
PIPER_ENVIRONMENT              # production, staging, development, testing
GITHUB_ALLOWED_REPOS           # Comma-separated list of allowed repositories
```

**Optional:**
```bash
GITHUB_API_TIMEOUT             # API timeout in seconds (default: 30)
GITHUB_API_PER_PAGE           # Pagination size (default: 30, max: 100)
GITHUB_ENABLE_METRICS         # Enable performance metrics (default: true)
GITHUB_USE_PRODUCTION_CLIENT  # Use ProductionGitHubClient (default: true)
GITHUB_ENABLE_CONTENT_GENERATION # Enable LLM content generation (default: true)
```

### Environment-Specific Defaults

The system automatically adjusts configuration based on the `PIPER_ENVIRONMENT` setting:

**Production Environment:**
- Maximum retry attempts: 5
- Maximum retry delay: 120 seconds
- Rate limit monitoring: Enabled
- Issue template validation: Enabled
- Enhanced error handling: Enabled

**Development Environment:**
- Maximum retry attempts: 3
- Maximum retry delay: 60 seconds
- Rate limit monitoring: Disabled
- All features enabled for testing

**Testing Environment:**
- Maximum retry attempts: 1
- Retry delays: Minimal (0.1 seconds)
- Rate limit retries: Disabled
- Metrics collection: Disabled

---

## Authentication Setup

### GitHub Personal Access Token (Recommended)

1. **Create Personal Access Token:**
   - Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Click "Generate new token (classic)"
   - Select appropriate scopes:
     ```
     repo              # Full repository access
     read:org          # Read organization membership (if needed)
     read:user         # Read user profile information
     ```

2. **Configure Token:**
   ```bash
   export GITHUB_TOKEN="ghp_your_generated_token_here"
   ```

3. **Verify Token:**
   ```bash
   curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user
   ```

### GitHub App Authentication (Advanced)

For organization-wide deployments, consider using a GitHub App:

1. **Create GitHub App** in organization settings
2. **Generate private key** and install app
3. **Configure environment:**
   ```bash
   export GITHUB_APP_ID="your_app_id"
   export GITHUB_APP_PRIVATE_KEY_PATH="/path/to/private-key.pem"
   export GITHUB_APP_INSTALLATION_ID="installation_id"
   ```

**Note:** GitHub App authentication requires additional implementation - currently uses Personal Access Token flow.

---

## Repository Configuration

### Single Repository Setup

For teams working with one primary repository:

```bash
export GITHUB_DEFAULT_REPO="your-org/your-main-repo"
```

### Multi-Repository Setup

For organizations with multiple repositories:

```bash
export GITHUB_ALLOWED_REPOS="your-org/frontend,your-org/backend,your-org/docs"
export GITHUB_DEFAULT_REPO="your-org/backend"  # Primary repository for default operations
```

### Repository Security

**Important:** The system validates repository access to prevent unauthorized issue creation:

- If `GITHUB_ALLOWED_REPOS` is set, only listed repositories can be accessed
- If not set, the system allows access to all repositories the token can reach
- Invalid repository names result in clear error messages with recovery suggestions

---

## Feature Flags

### Production Client Features

```bash
# Enable/disable production GitHub client (default: true)
export GITHUB_USE_PRODUCTION_CLIENT="true"

# Enable/disable LLM-powered content generation (default: true)
export GITHUB_ENABLE_CONTENT_GENERATION="true"

# Enable/disable performance metrics collection (default: true)
export GITHUB_ENABLE_METRICS="true"
```

### Content Generation Settings

The system uses advanced LLM integration to transform natural language requests into professional GitHub issues:

**Input:** `"Fix critical login bug affecting social media authentication"`

**Output:**
- **Title:** "Fix authentication failure in social media login flow"
- **Body:** Structured markdown with problem description, impact, and suggested approach
- **Labels:** `["bug", "critical", "authentication", "social-media"]`
- **Priority:** "high"

**Configuration:**
```bash
# Enable/disable this feature
export GITHUB_ENABLE_CONTENT_GENERATION="true"

# The system automatically uses Claude Opus for content generation
# Fallback behavior: Creates basic issue structure if LLM unavailable
```

---

## Production Deployment

### Deployment Checklist

**Pre-Deployment:**
- [ ] GitHub token configured with appropriate scopes
- [ ] Repository access validated
- [ ] Environment variables set correctly
- [ ] Feature flags configured for production use
- [ ] Database schema includes `GENERATE_GITHUB_ISSUE_CONTENT` enum value

**Deployment:**
- [ ] Environment configuration deployed
- [ ] Application containers restarted
- [ ] GitHub API connectivity verified
- [ ] Sample issue creation tested
- [ ] Error handling and fallback behavior tested

**Post-Deployment:**
- [ ] Monitoring alerts configured
- [ ] Performance metrics collection verified
- [ ] User documentation distributed
- [ ] Support team notified of new capabilities

### Database Requirements

Ensure the database includes the new task type enum:

```sql
-- Check if enum value exists
SELECT unnest(enum_range(NULL::tasktype)) WHERE unnest = 'GENERATE_GITHUB_ISSUE_CONTENT';

-- Add if missing (safe to run multiple times)
ALTER TYPE tasktype ADD VALUE IF NOT EXISTS 'GENERATE_GITHUB_ISSUE_CONTENT';
```

### Container Configuration

**Docker Environment:**
```dockerfile
ENV GITHUB_TOKEN=${GITHUB_TOKEN}
ENV GITHUB_DEFAULT_REPO=${GITHUB_DEFAULT_REPO}
ENV PIPER_ENVIRONMENT=production
ENV GITHUB_ALLOWED_REPOS=${GITHUB_ALLOWED_REPOS}
```

**Kubernetes ConfigMap:**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: piper-github-config
data:
  PIPER_ENVIRONMENT: "production"
  GITHUB_DEFAULT_REPO: "your-org/your-repo"
  GITHUB_ALLOWED_REPOS: "your-org/repo1,your-org/repo2"
  GITHUB_USE_PRODUCTION_CLIENT: "true"
  GITHUB_ENABLE_CONTENT_GENERATION: "true"
```

---

## Monitoring and Troubleshooting

### Health Checks

**Configuration Validation:**
```python
from services.integrations.github.config_service import GitHubConfigService

config_service = GitHubConfigService()
summary = config_service.get_configuration_summary()

# Check critical settings
assert summary['has_authentication_token'], "GitHub token not configured"
assert summary['default_repository'], "Default repository not set"
print(f"Environment: {summary['environment']}")
print(f"Feature flags: {summary['feature_flags']}")
```

**API Connectivity:**
```python
from services.integrations.github.production_client import ProductionGitHubClient

client = ProductionGitHubClient()
health = await client.health_check()

print(f"GitHub API Status: {health['status']}")
if health['status'] == 'healthy':
    print(f"Response time: {health['response_time_ms']}ms")
    print(f"Authenticated as: {health['authenticated_user']}")
```

### Common Issues and Solutions

**1. Authentication Failures**
```
Error: "GitHubAuthFailedError: Invalid GitHub token"

Solutions:
- Verify token hasn't expired
- Check token has required scopes (repo, read:user)
- Ensure token is properly set in environment
- Test token with: curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user
```

**2. Repository Access Denied**
```
Error: "Repository 'org/repo' not in allowed list"

Solutions:
- Add repository to GITHUB_ALLOWED_REPOS
- Verify repository name format (owner/repo)
- Check token has access to repository
- Clear allowed repos list to allow all accessible repositories
```

**3. Rate Limit Issues**
```
Error: "GitHubRateLimitError: Rate limit exceeded"

Solutions:
- Check rate limit status: client.get_rate_limit_info()
- Wait for rate limit reset (automatic in production client)
- Consider GitHub App authentication for higher limits
- Review API usage patterns for optimization opportunities
```

**4. Content Generation Failures**
```
Warning: "Failed to generate GitHub issue content, using fallback"

Impact: Issues created with basic formatting instead of enhanced content
Solutions:
- Check LLM service connectivity
- Verify ANTHROPIC_API_KEY or OPENAI_API_KEY configured
- Review LLM client logs for specific errors
- System continues to work with fallback content generation
```

### Performance Monitoring

**Metrics Collection:**
```python
# Get client performance metrics
client = ProductionGitHubClient()
metrics = client.get_client_metrics()

print(f"Requests made: {metrics['request_count']}")
print(f"Error rate: {metrics['error_rate']:.2%}")
print(f"Last request: {metrics['last_request_time']}")

# Rate limit monitoring
rate_limit = client.get_rate_limit_info()
if rate_limit:
    print(f"Rate limit usage: {rate_limit.usage_percentage:.1f}%")
    print(f"Remaining requests: {rate_limit.remaining}")
```

**Log Monitoring:**
- Monitor for `GitHubAuthFailedError` patterns
- Track `GitHubRateLimitError` frequency
- Watch for `ProductionGitHubClient unavailable` fallback messages
- Monitor LLM content generation success rates

---

## User Guide: Creating GitHub Issues

### Natural Language Interface

Users can create GitHub issues using simple natural language:

**Examples:**

1. **Bug Reports:**
   ```
   "Create a bug report for the login system crashing when users try to authenticate with Google"
   ```

   **Result:** Professional issue with title "Fix authentication crash in Google login integration", structured markdown body, and appropriate labels.

2. **Feature Requests:**
   ```
   "We need a dark mode toggle in the user settings page"
   ```

   **Result:** Feature request with implementation suggestions, acceptance criteria, and design considerations.

3. **Critical Issues:**
   ```
   "URGENT: Payment processing is down affecting all users"
   ```

   **Result:** High-priority issue with critical labels, impact assessment, and escalation information.

### API Integration

**REST API Endpoint:**
```bash
curl -X POST http://your-piper-instance/api/v1/intent \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Create a ticket for fixing the authentication bug",
    "project_id": "optional-project-id"
  }'
```

**Web Interface:**
- Navigate to Piper Morgan web UI
- Type natural language request in chat interface
- System automatically detects GitHub issue creation intent
- Review generated content before creation
- Issue created in configured repository

---

## Support and Maintenance

### Regular Maintenance Tasks

**Weekly:**
- Review rate limit usage patterns
- Check for authentication token expiration warnings
- Monitor error rates and failed requests
- Validate repository access permissions

**Monthly:**
- Review and update allowed repositories list
- Check for GitHub API changes or deprecations
- Assess content generation quality and user feedback
- Update documentation based on usage patterns

**Quarterly:**
- Evaluate GitHub App migration benefits
- Review security and access patterns
- Assess performance optimization opportunities
- Plan feature enhancements based on user needs

### Getting Help

**Internal Documentation:**
- Architecture patterns: `docs/architecture/`
- Configuration standards: `docs/architecture/adr/adr-010-configuration-patterns.md`
- Development workflow: `docs/development/claude-code-workflow.md`

**External Resources:**
- GitHub API documentation: https://docs.github.com/en/rest
- GitHub App authentication: https://docs.github.com/en/developers/apps
- Rate limiting guidelines: https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting

---

*This setup guide ensures reliable, secure, and efficient GitHub integration for daily product management workflows.*
